import csv
import itertools
import json
import tempfile
import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, QueryDict
from django.shortcuts import render

from perfectextractor.corpora.opus.extractor import OPUSPerfectExtractor, OPUSPoSExtractor

from .forms import MainForm, ImportQueryForm
from .models import Corpus, Task
from .tasks import tasks

@login_required
def home(request):
    corpus = None
    form = MainForm()
    if request.GET.get('corpus') is not None:
        try:
            if request.GET['corpus'].isdigit():
                corpus = Corpus.objects.get(pk=request.GET['corpus'])
                if len(corpus.sources) < 1:
                    messages.error(request, f'Corpus files for {corpus.title} not accessible, please check configuration')
                else:
                    form = partially_filled_form(request.GET, corpus)
        except Corpus.DoesNotExist:
            pass

    return render(request, 'home.html', dict(corpus=corpus, form=form))


def partially_filled_form(params, corpus):
    initial = params.dict()
    # unfortunately we need to manually specify parameters which are lists
    for param in ['pos', 'lemmata', 'regex']:
        initial[param] = params.getlist(param)

    # we send a parial form when the user changes corpus or source
    # in either case, they will have to choose new documents
    if 'documents' in initial:
        del initial['documents']

    return MainForm(initial=initial, corpus=corpus, source=params.get('source'))


def run_task(result_cb, extractor, path):
    def progress_cb(progress, total):
        result_cb(dict(progress=progress, total=total))

    extractor.process_folder(path, progress_cb=progress_cb)


def resolve_extractor(extractor):
    return {
        'pos': (EuroparlPoSExtractor, {'pos', 'lemmata', 'regex'}),
        'perfect': (EuroparlPerfectExtractor, {'lemmata'})}[extractor]


def prepare_query(form, arguments):
    known_arguments = ['pos', 'lemmata', 'regex']

    kwargs = dict()
    any_error = False
    for key in known_arguments:
        if form.cleaned_data[key] and key not in arguments:
            form.add_error(key, 'field is not supported by the chosen extractor')
            any_error = True
        elif key in arguments:
            entries = form.cleaned_data[key]
            if not isinstance(entries, list):
                entries = [entries]
            kwargs[key] = [entry for entry in entries if entry]

    if form.cleaned_data['position']:
        kwargs['position'] = form.cleaned_data['position']

    if any_error:
        return dict(), False
    return kwargs, True


@login_required
def run(request):
    form = MainForm(request.POST)
    if form.is_valid():
        extractor, query_arguments = resolve_extractor(form.cleaned_data['extractor'])

        kwargs, ok = prepare_query(form, query_arguments)
        if not ok:
            return render(request, 'home.html', dict(corpus=form.cleaned_data['corpus'], form=form))

        outfile = tempfile.mktemp()
        kwargs['outfile'] = outfile
        kwargs['file_limit'] = form.cleaned_data.get('file_limit', 0)
        kwargs['output'] = form.cleaned_data.get('output_format')
        kwargs['file_names'] = form.cleaned_data['documents']

        corpus = form.cleaned_data['corpus']
        source = form.cleaned_data['source']
        alignment = [os.path.basename(path) for path in form.cleaned_data['alignment']]
        extractor = extractor(source, alignment, **kwargs)

        path = os.path.join(corpus.path, source)
        task_id = tasks.add(run_task, (extractor, path))
        Task.objects.filter(pk=task_id).update(outfile=outfile)

        # prepare POST query string for json export
        query = request.POST.copy()
        query.pop('csrfmiddlewaretoken')
        query_json = json.dumps(dict(query=query.urlencode()))

        return render(request, 'progress.html', dict(task_id=task_id,
                                                     source=source,
                                                     output_format=kwargs['output'],
                                                     alignment=alignment,
                                                     query_json=query_json))
    else:
        return render(request, 'home.html', dict(form=form))


@login_required
def status(request, task_id):
    return JsonResponse(dict(status=tasks.monitor(task_id)))


def csv_to_records(path, limit=10, delimiter=';'):
    with open(path, 'r', encoding='utf-8-sig') as f:
        reader = iter(csv.reader(f, delimiter=delimiter))
        try:
            headers = next(reader)
        except StopIteration:
            return []

        data = itertools.islice(reader, limit)
        return [dict((headers[i], line[i]) for i in range(len(line))) for line in data]


def count_results(path):
    return len(csv_to_records(path, limit=None))


@login_required
def peek(request, task_id):
    outfile = Task.objects.get(pk=task_id).outfile
    head = csv_to_records(outfile)
    results = count_results(outfile)
    return JsonResponse(dict(head=head, results=results))


@login_required
def download(request, task_id):
    outfile = Task.objects.get(pk=task_id).outfile
    contents = open(outfile, 'rb').read()
    response = HttpResponse(contents, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=results.csv'
    return response


@login_required
def cancel(request, task_id):
    tasks.cancel(task_id)
    return JsonResponse(dict(success=True))


@login_required
def import_query(request):
    if 'query_file' in request.FILES:
        query = QueryDict(json.load(request.FILES['query_file'])['query'])
        corpus = Corpus.objects.get(pk=query['corpus'])
        form = MainForm(query, corpus=corpus)
        return render(request, 'home.html', dict(corpus=corpus, form=form))
    else:
        form = ImportQueryForm()
        return render(request, 'import.html', dict(form=form))


def help(request):
    return render(request, 'help.html')
