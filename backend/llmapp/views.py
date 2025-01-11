from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import SlackChannel, SlackMessage, BlogPost
from .utils import (
    fetch_slack_channels,
    fetch_slack_messages,
    create_faiss_index,
    update_faiss_index,
    search_faiss_index,
    generate_blog_post
)

class FetchSlackChannelsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        token = request.data.get("token")
        if not token:
            return Response({"error": "Slack API token is required."}, status=400)

        try:
            fetch_slack_channels(token)
            return Response({"message": "Slack channels fetched successfully."}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class FetchSlackMessagesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        token = request.data.get("token")
        channel_id = request.data.get("channel_id")

        if not token or not channel_id:
            return Response({"error": "Token and channel ID are required."}, status=400)

        try:
            fetch_slack_messages(token, channel_id)
            create_faiss_index(channel_id)  # Create index for the channel
            return Response({"message": "Slack messages fetched and indexed successfully."}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class SlackBotQueryAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        channel_id = request.data.get("channel_id")
        query = request.data.get("query")

        if not channel_id or not query:
            return Response({"error": "Channel ID and query are required."}, status=400)

        try:
            answer = generate_blog_post(channel_id, query)
            return Response({"answer": answer}, status=200)
        except Exception as e:
            return Response({"error": f"Failed to process query: {str(e)}"}, status=500)


class BlogListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        blogs = BlogPost.objects.all().order_by('-created_at')
        blog_list = [{"title": blog.title, "content": blog.content} for blog in blogs]
        return Response(blog_list, status=200)
