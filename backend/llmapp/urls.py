# llmapp/urls.py
from django.urls import path
from .views import (
    FetchAndGenerateSlackResponseAPIView,
    FetchPostsAPIView,
    PostSearchAPIView,
    PostSearchCategoryAPIView,
    CreatePostAPIView,
    CreateCategoryAPIView,
    FetchCategoryAPIView,
)

urlpatterns = [
    path("slack/fetch-messages/", FetchAndGenerateSlackResponseAPIView.as_view(), name="fetch_slack_messages"),
    #path("slack/create-embeddings/", CreateEmbeddingsAPIView.as_view(), name="create_embeddings"),
    path("history/", FetchPostsAPIView.as_view(), name="api_history"),
    path("search/<int:post_id>/", PostSearchAPIView.as_view(), name="api_particular_post"),
    path("search/category/<str:category>/",PostSearchCategoryAPIView.as_view(),name="post_by_category"),
    path("post/",CreatePostAPIView.as_view(),name="post"),
    path("category/create/", CreateCategoryAPIView.as_view(), name="create-category"),
    path("category/",FetchCategoryAPIView.as_view(),name="FetchCategory"),
]