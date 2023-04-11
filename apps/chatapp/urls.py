from django.urls import path

from chatapp.views import *

app_name = "apps.chatapp"

urlpatterns = [
    path("app/", ChatBotView.as_view(), name="app"),
    path("session/", ChatHistoriesView.as_view(), name="session"),
    path("adds/", AddSessionView.as_view(), name="adds"),
    path("edit/", ModifySessionNameView.as_view(), name="edit"),
    path("remove/", RemoveSessionView.as_view(), name="remove"),
]
