from django import forms
from django.conf import settings


class MultipleFilePathField(forms.MultipleChoiceField, forms.FilePathField):
    pass


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
    corpus = forms.ChoiceField(choices=[
        ('europarl', 'europarl'),
        ('bnc', 'bnc'),
        ('dpc', 'dpc')])
    extractor = forms.ChoiceField(choices=[
        ('pos', 'pos'),
        ('perfect', 'perfect')])
    path = forms.FilePathField(label='Source',
                               path=settings.PE_DATA_PATH, allow_files=False, allow_folders=True)

    pos = PossiblyMultipleCharField(required=False, label='Part-of-speech tag')
    lemmata = PossiblyMultipleCharField(required=False)
    alignment = MultipleFilePathField(path=settings.PE_DATA_PATH, allow_files=False, allow_folders=True,
                                      widget=forms.SelectMultiple)

    file_limit = forms.IntegerField(required=False, label='Limit search to X files', initial=25)
