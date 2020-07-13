from django import forms
from django.conf import settings

from .models import Corpus


class PossiblyMultipleTextInput(forms.TextInput):
    def value_from_datadict(self, data, files, name):
        try:
            getter = data.getlist
        except AttributeError:
            getter = data.get
        return getter(name)

    def format_value(self, value):
        if value is not None:
            return ','.join(value)


class PossiblyMultipleCharField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = PossiblyMultipleTextInput
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if value == ['']:
            return None
        if isinstance(value, list):
            out = []
            for part in value:
                out.append(super().to_python(part))
            return out
        return super().to_python(value)


class MainForm(forms.Form):
    corpus = forms.ModelChoiceField(Corpus.objects.all())
    extractor = forms.ChoiceField(choices=[
        ('pos', 'pos'),
        ('perfect', 'perfect')])
    pos = PossiblyMultipleCharField(required=False, label='Part-of-speech tag')
    lemmata = PossiblyMultipleCharField(required=False)
    regex = PossiblyMultipleCharField(required=False, label='Regular Expression')
    position = forms.IntegerField(required=False, label='Word position in sentence',
                                  min_value=1)

    file_limit = forms.IntegerField(required=False, label='Limit search to X files', initial=25)
    output_format = forms.ChoiceField(choices=[
        ('txt', 'Text'),
        ('xml', 'XML')],
        help_text='Choose XML if the output is to be imported in TimeAlign')

    def add_corpus_fields(self, corpus, source):
        if source:
            self.fields['source'].initial = source
        elif self.is_bound:
            source = self.clean_field('source')
        else:
            source = corpus.sources[0]

        documents = corpus.list_documents(source)

        alignments = corpus.sources
        if source in alignments:
            alignments.remove(source)
        self.fields['alignment'] = forms.MultipleChoiceField(choices=zip(alignments, alignments))
        self.fields['documents'] = forms.MultipleChoiceField(choices=zip(documents, documents), required=False)

    def __init__(self, *args, corpus=None, source=None, **kwargs):
        super().__init__(*args, **kwargs)
        if corpus:
            self.fields['corpus'].initial = corpus
            self.fields['source'] = forms.ChoiceField(choices=zip(corpus.sources, corpus.sources))
            self.add_corpus_fields(corpus, source)
        elif self.is_bound:
            corpus = self.clean_field('corpus')
            self.fields['source'] = forms.ChoiceField(choices=zip(corpus.sources, corpus.sources))
            self.add_corpus_fields(corpus, source)

    def clean_field(self, field):
        value = self.fields[field].widget.value_from_datadict(self.data, self.files, self.add_prefix(field))
        return self.fields[field].clean(value)


class ImportQueryForm(forms.Form):
    query_file = forms.FileField(label='Query file', widget=forms.FileInput(attrs=dict(accept='application/json')))
