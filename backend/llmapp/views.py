# llmapp/views/slack_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .utils.slack_utils import (
    save_slack_messages, 
    create_message_embeddings, 
    search_similar_messages_in_db, 
    generate_response_from_db
)


class FetchAndGenerateSlackResponseAPIView(APIView):
    def post(self, request, *args, **kwargs):
        text = request.data.get("text")  # 질문
        channel_id = request.data.get("channel_id")
        top_k = int(request.data.get("top_k", 5))

        if not channel_id or not text:
            return Response({"error": "Invalid request data. 'channel_id' and 'text' are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 메시지 저장
            save_slack_messages(channel_id)
            print("Slack messages saved successfully.")

            # 임베딩 생성
            create_message_embeddings()
            print("Message embeddings created successfully.")

            # 유사 메시지 검색
            similar_messages = search_similar_messages_in_db(text, top_k=top_k)
            if not similar_messages:
                return Response({"error": "No similar messages found."}, status=status.HTTP_404_NOT_FOUND)

            # 이거답변
            response = generate_response_from_db(text, similar_messages)
            print("="*50)
            print(response)
            return Response({
                "question": text,
                "response": response,
                "similar_messages": similar_messages
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error occurred: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



"""
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
                create_message_embeddings() # 여기 들어감 ㄱ
                print("EMBEDDING FIN.")
                return Response({"message": "Embeddings created successfully."}, status=status.HTTP_200_OK)
            except Exception as e:
                print("EMBEDDING ERR")
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print("YOU FUCKED")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
"""
"""
class GenerateSlackResponseAPIView(APIView):
    def post(self, request, *args, **kwargs):
        question = request.data.get("question")
        top_k = int(request.data.get("top_k", 5))

        if not question:
            return Response({"error": "질문 내용이 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 유사 메시지 검색
            similar_messages = search_similar_messages_in_db(question, top_k=top_k)
            if not similar_messages:
                return Response({"error": "유사한 메시지를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

            # 답변 생성
            response = generate_response_from_db(question, similar_messages)
            print("="*50)
            print("RESPONSE: ", response)
            return Response({"question": question, "response": response}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
"""