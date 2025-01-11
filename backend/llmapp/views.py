from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import render
from .serializers import PostSerializer, CategorySerializer
from .models import PostHistory, Categories
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from .utils.slack_utils import (
    save_slack_messages, 
    create_message_embeddings, 
    search_similar_messages_in_db, 
    generate_response_from_db
)

import threading
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class FetchAndGenerateSlackResponseAPIView(APIView):
    def post(self, request, *args, **kwargs):
        print("DEBUG: FetchAndGenerateSlackResponseAPIView called")
        test_user = User.objects.first()  # 테스트 사용자
        print(f"DEBUG: Test user: {test_user}")

        text = request.data.get("text")  # 질문
        channel_id = request.data.get("channel_id")
        top_k = int(request.data.get("top_k", 5))

        print(f"DEBUG: Request data - text: {text}, channel_id: {channel_id}, top_k: {top_k}")

        if not channel_id or not text:
            return Response({"error": "'channel_id'와 'text'는 필수입니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 비동기 작업 실행
        threading.Thread(
            target=self._handle_request,
            args=(text, channel_id, top_k, test_user)
        ).start()

        # 즉시 응답 반환
        return Response({"message": "요청이 성공적으로 접수되었습니다."}, status=status.HTTP_200_OK)

    def _handle_request(self, text, channel_id, top_k, test_user):
        try:
            # 메시지 저장
            print("DEBUG: Saving Slack messages...")
            save_slack_messages(channel_id)
            print("DEBUG: Slack messages saved.")

            print("DEBUG: Creating message embeddings...")
            create_message_embeddings()
            print("DEBUG: Message embeddings created.")

            # 유사 메시지 검색
            print("DEBUG: Searching for similar messages...")
            similar_messages = search_similar_messages_in_db(text, top_k=top_k)
            print(f"DEBUG: Similar messages found: {similar_messages}")

            if not similar_messages:
                raise ValueError("유사한 메시지가 없습니다.")

            # 답변 생성
            print("DEBUG: Generating response from similar messages...")
            response = generate_response_from_db(text, similar_messages)
            print(f"DEBUG: Generated response: {response}")

            # 카테고리 및 게시물 생성
            print("DEBUG: Creating or fetching category...")
            category, _ = Categories.objects.get_or_create(user=test_user, category_name="미정")
            print(f"DEBUG: Category: {category}")

            print("DEBUG: Creating or fetching post...")
            post, _ = PostHistory.objects.get_or_create(user=test_user, title=text, content=response, category=category)
            print(f"DEBUG: Post: {post}")

            print("DEBUG: 작업이 성공적으로 완료되었습니다.")
        except Exception as e:
            print(f"DEBUG: Error occurred: {e}")
            self._send_error_to_slack(channel_id, text, str(e))

    def _send_error_to_slack(self, channel_id, text, error_message):
        slack_client = WebClient(token="your-slack-bot-token")  # Slack Bot 토큰
        try:
            message = f"❗ *작업 중 오류 발생*\n*질문*: {text}\n*오류 메시지*: {error_message}"
            slack_client.chat_postMessage(channel=channel_id, text=message)
            print(f"DEBUG: Error message sent to Slack: {channel_id}")
        except SlackApiError as slack_error:
            print(f"DEBUG: Failed to send error to Slack: {slack_error.response['error']}")


class FetchPostsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        print("DEBUG: FetchPostsAPIView called")
        test_user = User.objects.first()
        print(f"DEBUG: Test user: {test_user}")

        posts = PostHistory.objects.filter(user=test_user)
        print(f"DEBUG: Fetched posts: {posts}")

        result = PostSerializer(posts, many=True)
        return Response(result.data)

class PostSearchAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id, *args, **kwargs):
        print("DEBUG: PostSearchAPIView GET called")
        test_user = User.objects.first()
        print(f"DEBUG: Test user: {test_user}")

        try:
            post = PostHistory.objects.get(id=post_id, user=test_user)
            print(f"DEBUG: Found post: {post}")

            serializer = PostSerializer(post)
            return Response(serializer.data)
        except PostHistory.DoesNotExist:
            print("DEBUG: Post not found")
            return Response({"error": "Post not found"}, status=404)

    def put(self, request, post_id, *args, **kwargs):
        print("DEBUG: PostSearchAPIView PUT called")
        test_user = User.objects.first()
        print(f"DEBUG: Test user: {test_user}")

        try:
            post = PostHistory.objects.get(id=post_id, user=test_user)
            print(f"DEBUG: Found post: {post}")
        except PostHistory.DoesNotExist:
            print("DEBUG: Post not found")
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        category_name = request.data.get("category_name")
        print(f"DEBUG: Received category_name: {category_name}")

        if not category_name:
            return Response({"error": "'category_name'는 필수입니다."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            new_category = Categories.objects.get(category_name=category_name, user=test_user)
            print(f"DEBUG: Found category: {new_category}")
        except Categories.DoesNotExist:
            print(f"DEBUG: Category '{category_name}' not found")
            return Response({"error": f"Category '{category_name}' not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data["category"] = new_category.id

        serializer = PostSerializer(post, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            print("DEBUG: Post updated successfully")
            return Response(serializer.data, status=status.HTTP_200_OK)

        print(f"DEBUG: Serializer errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostSearchCategoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, category, *args, **kwargs):
        print("DEBUG: PostSearchCategoryAPIView called")
        test_user = User.objects.first()
        print(f"DEBUG: Test user: {test_user}")

        try:
            post = PostHistory.objects.get(category=category, user=test_user)
            print(f"DEBUG: Found post: {post}")

            serializer = PostSerializer(post)
            return Response(serializer.data)
        except PostHistory.DoesNotExist:
            print("DEBUG: Post not found")
            return Response({"error": "Post not found"}, status=404)

class CreatePostAPIView(APIView):
    def post(self, request, *args, **kwargs):
        print("DEBUG: CreatePostAPIView called")
        user = User.objects.first()
        print(f"DEBUG: Test user: {user}")

        content = request.data.get("content")
        title = request.data.get("title")
        category_name = request.data.get("category_name")

        print(f"DEBUG: Request data - title: {title}, content: {content}, category_name: {category_name}")

        if not all([title, content, category_name]):
            return Response({"error": "모든 필드(title, content, category)가 필수입니다."}, status=400)

        try:
            category, _ = Categories.objects.get_or_create(user=user, category_name=category_name)
            print(f"DEBUG: Category: {category}")

            post = PostHistory.objects.create(user=user, content=content, title=title, category=category)
            print(f"DEBUG: Post created: {post}")

            result = PostSerializer(post)
            return Response(result.data, status=201)
        except Exception as e:
            print(f"DEBUG: Error occurred: {e}")
            return Response({"error": str(e)}, status=400)

class CreateCategoryAPIView(APIView):
    def post(self, request, *args, **kwargs):
        print("DEBUG: CreateCategoryAPIView called")
        test_user = User.objects.first()
        print(f"DEBUG: Test user: {test_user}")

        category_name = request.data.get("category_name")
        print(f"DEBUG: Received category_name: {category_name}")

        if not category_name:
            return Response({"error": "Category name is required"}, status=400)

        try:
            category = Categories.objects.create(user=test_user, category_name=category_name)
            print(f"DEBUG: Category created: {category}")

            result = CategorySerializer(category)
            return Response(result.data, status=201)
        except Exception as e:
            print(f"DEBUG: Error occurred: {e}")
            return Response({"error": str(e)}, status=400)

class FetchCategoryAPIView(APIView):
    def get(self, request, *args, **kwargs):
        print("DEBUG: FetchCategoryAPIView called")
        test_user = User.objects.first()
        print(f"DEBUG: Test user: {test_user}")

        categories = Categories.objects.filter(user=test_user)
        print(f"DEBUG: Fetched categories: {categories}")

        result = CategorySerializer(categories, many=True)
        return Response(result.data)
