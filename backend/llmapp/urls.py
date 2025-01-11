# llmapp/urls.py
from django.urls import path
from .views import FetchSlackMessagesAPIView#, CreateEmbeddingsAPIView

urlpatterns = [
    path("slack/fetch-messages/", FetchSlackMessagesAPIView.as_view(), name="fetch_slack_messages"),
    #path("slack/create-embeddings/", CreateEmbeddingsAPIView.as_view(), name="create_embeddings"),
]