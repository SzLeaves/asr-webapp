from import_export import resources
from sttapp.models import SpeechToText


class SpeechToTextResource(resources.ModelResource):
    class Meta:
        model = SpeechToText
