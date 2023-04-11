from django import forms
from sttapp.models import SpeechToText


class SpeechToTextForm(forms.Form):
    fileName = forms.CharField(max_length=128)
    filePath = forms.FileField()
