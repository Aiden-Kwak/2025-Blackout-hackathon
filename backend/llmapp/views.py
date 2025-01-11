# llmapp/views/slack_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .utils.slack_utils import save_slack_messages, create_message_embeddings

class FetchSlackMessagesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        channel_id = request.data.get("channel_id")
        if not channel_id:
            print("You are fucked")
            return Response({"error": "Channel ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            save_slack_messages(channel_id)
            return Response({"message": "Messages fetched and saved successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateEmbeddingsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            create_message_embeddings()
            return Response({"message": "Embeddings created successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
