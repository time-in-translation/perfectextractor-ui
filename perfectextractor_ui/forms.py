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


class PossiblyMultipleCharField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = PossiblyMultipleTextInput
        super().__init__(*args, **kwargs)

    def to_python(self, value):
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

    file_limit = forms.IntegerField(required=False, label='Limit search to X files', initial=25)

    def __init__(self, *args, **kwargs):
        corpus = kwargs.pop('corpus') if 'corpus' in kwargs else None
        super().__init__(*args, **kwargs)
        if corpus:
            self.fields['corpus'].initial = corpus
            self.fields['alignment'] = forms.MultipleChoiceField(choices=zip(corpus.sources, corpus.sources))
            self.fields['source'] = forms.ChoiceField(choices=zip(corpus.sources, corpus.sources))
        elif self.is_bound:
            corpus = self.clean_field('corpus')
            self.fields['alignment'] = forms.MultipleChoiceField(choices=zip(corpus.sources, corpus.sources))
            self.fields['source'] = forms.ChoiceField(choices=zip(corpus.sources, corpus.sources))

    def clean_field(self, field):
        value = self.fields[field].widget.value_from_datadict(self.data, self.files, self.add_prefix(field))
        return self.fields[field].clean(value)
