from django.contrib import admin
from .models import SlackMessage, MessageEmbedding, Categories, PostHistory


@admin.register(SlackMessage)
class SlackMessageAdmin(admin.ModelAdmin):
    list_display = ("channel_id", "user_id", "timestamp", "embedding_created", "created_at")
    search_fields = ("channel_id", "user_id", "text", "timestamp")
    list_filter = ("embedding_created", "created_at")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

@admin.register(MessageEmbedding)
class MessageEmbeddingAdmin(admin.ModelAdmin):
    list_display = ("message", "created_at")
    search_fields = ("message__text", "message__user_id")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("user", "category_name")
    search_fields = ("user__username", "category_name")
    list_filter = ("user",)
    ordering = ("user", "category_name")


@admin.register(PostHistory)
class PostHistoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "category_name", "created_at", "updated_at")
    search_fields = ("title", "content", "user__username", "category__category_name")
    list_filter = ("category", "created_at")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

