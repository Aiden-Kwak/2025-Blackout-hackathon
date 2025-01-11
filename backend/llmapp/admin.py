from django.contrib import admin
from .models import SlackMessage, MessageEmbedding

@admin.register(SlackMessage)
class SlackMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "channel_id", "user_id", "text", "timestamp", "embedding_created", "created_at")
    list_filter = ("channel_id", "embedding_created", "created_at")  # 필터 추가
    search_fields = ("text", "user_id", "channel_id")  # 검색 가능 필드
    ordering = ("-created_at",)  # 최신 메시지가 먼저 보이도록 정렬
    readonly_fields = ("timestamp", "created_at")  # 읽기 전용 필드

@admin.register(MessageEmbedding)
class MessageEmbeddingAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "created_at")
    list_filter = ("created_at",)  # 날짜별 필터 추가
    search_fields = ("message__text",)  # 관련 메시지 내용 검색 가능
    ordering = ("-created_at",)  # 최신 임베딩이 먼저 보이도록 정렬
    readonly_fields = ("created_at",)  # 읽기 전용 필드
