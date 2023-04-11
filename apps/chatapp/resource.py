from import_export import resources
from chatapp.models import Conversation, Message


class ConversationResource(resources.ModelResource):
    class Meta:
        model = Conversation


class MessageResource(resources.ModelResource):
    class Meta:
        model = Message
