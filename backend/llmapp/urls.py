# llmapp/urls.py
from django.urls import path
from .views import FetchAndGenerateSlackResponseAPIView

urlpatterns = [
    path("slack/fetch-messages/", FetchAndGenerateSlackResponseAPIView.as_view(), name="fetch_slack_messages"),
    #path("slack/create-embeddings/", CreateEmbeddingsAPIView.as_view(), name="create_embeddings"),
]