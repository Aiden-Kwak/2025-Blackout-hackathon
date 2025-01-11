from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, permissions
from django.shortcuts import render
from .serializers import PostSerializer, CategorySerializer
from .models import PostHistory, Categories
from django.contrib.auth.models import User
from .utils.slack_utils import (
    save_slack_messages, 
    create_message_embeddings, 
    search_similar_messages_in_db, 
    generate_response_from_db
)

class FetchAndGenerateSlackResponseAPIView(APIView):
    def post(self, request, *args, **kwargs):
        test_user = User.objects.first()  # 강제로 첫 번째 사용자 설정
        text = request.data.get("text")  # 질문
        channel_id = request.data.get("channel_id")
        top_k = int(request.data.get("top_k", 5))

        if not channel_id or not text:
            return Response({"error": "'channel_id'와 'text'는 필수입니다."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 메시지 저장
            save_slack_messages(channel_id)
            create_message_embeddings()

            # 유사 메시지 검색
            similar_messages = search_similar_messages_in_db(text, top_k=top_k)
            if not similar_messages:
                return Response({"error": "유사한 메시지가 없습니다."}, status=status.HTTP_404_NOT_FOUND)

            # 답변 생성
            response = generate_response_from_db(text, similar_messages)

            # 카테고리 및 게시물 생성
            category, _ = Categories.objects.get_or_create(user=test_user, category_name="미정")
            post, _ = PostHistory.objects.get_or_create(user=test_user, title=text, content=response, category=category)

            return Response({
                "question": text,
                "response": response,
                "similar_messages": similar_messages
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FetchPostsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        test_user = User.objects.first()
        posts = PostHistory.objects.filter(user=test_user)
        result = PostSerializer(posts, many=True)
        return Response(result.data)

class PostSearchAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id, *args, **kwargs):
        test_user = User.objects.first()
        try:
            post = PostHistory.objects.get(id=post_id, user=test_user)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except PostHistory.DoesNotExist:
            return Response({"error": "Post not found"}, status=404)

    def put(self, request, post_id, *args, **kwargs):
        test_user = User.objects.first()
        try:
            post = PostHistory.objects.get(id=post_id, user=test_user)
        except PostHistory.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        category_name = request.data.get("category_name")
        if not category_name:
            return Response({"error": "'category_name'는 필수입니다."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            new_category = Categories.objects.get(category_name=category_name, user=test_user)
        except Categories.DoesNotExist:
            return Response({"error": f"Category '{category_name}' not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data["category"] = new_category.id

        serializer = PostSerializer(post, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostSearchCategoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, category, *args, **kwargs):
        test_user = User.objects.first()
        try:
            post = PostHistory.objects.get(category=category, user=test_user)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except PostHistory.DoesNotExist:
            return Response({"error": "Post not found"}, status=404)

class CreatePostAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user = User.objects.first()
        content = request.data.get("content")
        title = request.data.get("title")
        category_name = request.data.get("category_name")

        if not all([title, content, category_name]):
            return Response({"error": "모든 필드(title, content, category)가 필수입니다."}, status=400)

        try:
            category, _ = Categories.objects.get_or_create(user=user, category_name=category_name)
            post = PostHistory.objects.create(user=user, content=content, title=title, category=category)
            result = PostSerializer(post)
            return Response(result.data, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

class CreateCategoryAPIView(APIView):
    def post(self, request, *args, **kwargs):
        test_user = User.objects.first()
        category_name = request.data.get("category_name")
        if not category_name:
            return Response({"error": "Category name is required"}, status=400)

        try:
            category = Categories.objects.create(user=test_user, category_name=category_name)
            result = CategorySerializer(category)
            return Response(result.data, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

class FetchCategoryAPIView(APIView):
    def get(self, request, *args, **kwargs):
        test_user = User.objects.first()
        categories = Categories.objects.filter(user=test_user)
        result = CategorySerializer(categories, many=True)
        return Response(result.data)
