# llmapp/views/slack_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .utils.slack_utils import save_slack_messages, create_message_embeddings


class FetchSlackMessagesAPIView(APIView):
    def post(self, request, *args, **kwargs):
        text = request.data.get("text")  # 질문 내용
        channel_id = request.data.get("channel_id")
        user_id = request.data.get("user_id")
        print("FUCK="*50)
        print(text)
        print(channel_id)
        print(user_id)
        print("="*50) # 너 잘했어

        if not channel_id or not text:
            return Response({"error": "Invalid request data."}, status=status.HTTP_400_BAD_REQUEST)

        #저장 트리거
        try:
            print("I AM HERE: 1") # 굿
            save_slack_messages(channel_id)
            print("I AM OUT: 1")
            #return Response({"message": f"Messages fetched for channel {channel_id}."}, status=status.HTTP_200_OK)
            try:
                print("EMBEDDING START")
                create_message_embeddings()
                print("EMBEDDING FIN.")
                return Response({"message": "Embeddings created successfully."}, status=status.HTTP_200_OK)
            except Exception as e:
                print("EMBEDDING ERR")
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print("YOU FUCKED")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        


"""
class CreateEmbeddingsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            create_message_embeddings()
            return Response({"message": "Embeddings created successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
"""