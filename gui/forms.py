from django import forms
from django.conf import settings


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

    pos = forms.CharField(required=False, label='Part-of-speech tag')
    lemmata = forms.CharField(required=False)
    alignment = forms.MultipleChoiceField(choices=[
        ('en', 'en'),
        ('nl', 'nl'),
        ('fr', 'fr')])

    file_limit = forms.IntegerField(required=False, label='Limit search to X files', initial=25)
