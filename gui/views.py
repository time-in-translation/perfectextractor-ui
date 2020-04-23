import csv
import tempfile
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from .forms import MainForm
from .models import Task
from .tasks import tasks
from perfectextractor.corpora.europarl.extractor import EuroparlPerfectExtractor, EuroparlPoSExtractor


def home(request):
    form = MainForm()
    return render(request, 'home.html', dict(form=form))


def run_task(result_cb, extractor, path):
    def progress_cb(progress, total):
        result_cb(dict(progress=progress, total=total))

    extractor.process_folder(path, progress_cb=progress_cb)


def resolve_extractor(extractor):
    return {
        'pos': EuroparlPoSExtractor,
        'perfect': EuroparlPerfectExtractor}[extractor]


def run(request):
    form = MainForm(request.POST, request.FILES)
    if form.is_valid():
        kwargs = dict()
        for key in ['pos', 'lemmata']:
            if form.cleaned_data[key]:
                kwargs[key] = form.cleaned_data[key].split()

        outfile = tempfile.mktemp()
        kwargs['outfile'] = outfile
        kwargs['file_limit'] = form.cleaned_data.get('file_limit', 0)
        extractor = resolve_extractor(form.cleaned_data['extractor'])('en', ['nl'], **kwargs)

        path = form.cleaned_data['path']
        task_id = tasks.add(run_task, (extractor, path))
        Task.objects.filter(pk=task_id).update(outfile=outfile)
        return render(request, 'progress.html', dict(task_id=task_id))
    else:
        return render(request, 'home.html', dict(form=form))


def status(request, task_id):
    return JsonResponse(dict(status=tasks.monitor(task_id)))


def csv_to_records(path, limit=10, delimiter=';'):
    with open(path, 'r', encoding='utf-8-sig') as f:
        reader = iter(csv.reader(f, delimiter=delimiter))
        headers = next(reader)
        data = [next(reader) for i in range(limit)]
        return [dict((headers[i], line[i]) for i in range(len(line))) for line in data]


def peek(request, task_id):
    outfile = Task.objects.get(pk=task_id).outfile
    head = csv_to_records(outfile)
    return JsonResponse(dict(head=head))


def download(request, task_id):
    outfile = Task.objects.get(pk=task_id).outfile
    contents = open(outfile, 'rb').read()
    response = HttpResponse(contents, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=results.csv'
    return response


def cancel(request, task_id):
    tasks.cancel(task_id)
    return JsonResponse(dict(success=True))
