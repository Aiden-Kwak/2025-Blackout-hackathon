# llmapp/views/slack_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import render
from .serializers import PostSerializer, CategorySerializer
from .models import PostHistory, Categories
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
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
            print(response) # 됐어
            print("WE FUCKED\n"*10)
            print(request.user) # AnonymousUser
            print("="*50)
            category, created = Categories.objects.get_or_create(user=1, category_name="미정")
            post, created2 = PostHistory.objects.get_or_create(user=1,title=text,
                                                               content=response,category=category)
            print("YOU HAVE TO SEE ME: ", post)
            print(created)
            print("="*50)
            print(created2)
            return Response({
                "question": text,
                "response": response,
                "similar_messages": similar_messages
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error occurred: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FetchPostsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        posts = PostHistory.objects.filter(user=1)
        result = PostSerializer(posts, many=True)  # many=True 추가
        return Response(result.data)


class PostSearchAPIView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get(self, request, post_id, *args, **kwargs):
        try:
            # post_id로 필터링
            post = PostHistory.objects.get(id=post_id, user=1)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except PostHistory.DoesNotExist:
            return Response({"error": "Post not found"}, status=404)
    def put(self, request, post_id, *args, **kwargs):
        try:
            # post_id와 사용자로 게시물 필터링
            post = PostHistory.objects.get(id=post_id, user=1)
        except PostHistory.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        # 요청 데이터에서 category_name 추출
        category_name = request.data.get("category_name")
        if not category_name:
            return Response({"error": "category_name is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # category_name으로 Categories 모델에서 카테고리 찾기
            new_category = Categories.objects.get(category_name=category_name, user=1)
        except Categories.DoesNotExist:
            return Response({"error": f"Category '{category_name}' not found"}, status=status.HTTP_404_NOT_FOUND)

        # category_id를 request.data에 추가
        data = request.data.copy()  # request.data는 불변 객체이므로 복사본을 생성
        data["category"] = new_category.id  # category 필드에 ID 추가

        # serializer를 통해 title, content, category 업데이트
        serializer = PostSerializer(post, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()  # 데이터 저장
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostSearchCategoryAPIView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능
    def get(self, request, category, *args, **kwargs):
        try:
            # category로 filtering
            post = PostHistory.objects.get(category=category, user=1)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except PostHistory.DoesNotExist:
            return Response({"error": "Post not found"}, status=404)

class CreatePostAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user = 1
        content = request.data.get("content")
        title = request.data.get("title")
        category_name = request.data.get("category_name")  # 카테고리 이름

        if not all([title, content, category_name]):
            return Response({"error": "All fields (title, content, category) are required"}, status=400)

        try:
            # 카테고리 검색 또는 생성
            category, created = Categories.objects.get_or_create(user=user, category_name=category_name)

            # 포스트 생성
            post = PostHistory.objects.create(
                user=user, content=content, title=title, category=category
            )
            result = PostSerializer(post)
            return Response(result.data, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class CreateCategoryAPIView(APIView):
    def post(self, request, *args, **kwargs):
        category_name = request.data.get("category_name")  # JSON body에서 카테고리 이름 가져오기
        if not category_name:
            return Response({"error": "Category name is required"}, status=400)

        try:
            user = 1
            category = Categories.objects.create(
                user=user, category_name=category_name
            )
            result = CategorySerializer(category)
            return Response(result.data, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

class FetchCategoryAPIView(APIView):
    def get(self,request,*args,**kwargs):
        user = 1
        categories = Categories.objects.filter(user=1)
        result = CategorySerializer(categories, many=True)  # many=True 추가
        return Response(result.data)


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