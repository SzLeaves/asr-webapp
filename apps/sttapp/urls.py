from django.urls import path

from sttapp.views import SpeechToTextView, DeleteHistoriesView

app_name = "apps.sttapp"
urlpatterns = [
    path("app/", SpeechToTextView.as_view(), name="app"),
    path("delete/", DeleteHistoriesView.as_view(), name="delete"),
]
