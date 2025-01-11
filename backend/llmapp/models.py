from django.db import models
from django.contrib.auth.models import User

class SlackMessage(models.Model):
    channel_id = models.CharField(max_length=50)
    user_id = models.CharField(max_length=50)
    text = models.TextField(default="")  # 기본값 추가
    timestamp = models.CharField(max_length=50, unique=True)
    thread_ts = models.CharField(max_length=50, null=True, blank=True) 
    embedding_created = models.BooleanField(default=False)  # 임베딩 생성 여부
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.user_id} in {self.channel_id} at {self.timestamp}"

    class Meta:
        unique_together = ("channel_id", "timestamp")  # 중복 방지


class MessageEmbedding(models.Model):
    message = models.OneToOneField(SlackMessage, on_delete=models.CASCADE, related_name="embedding")
    embedding_data = models.BinaryField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Embedding for message {self.message.id}"

class Categories(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Category")
    category_name = models.CharField(max_length=255) 
    def __str__(self):
        return f"{self.category_name}"

class PostHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="PostHistory")
    title = models.CharField(max_length=255)  # 포스트 제목
    content = models.TextField()  # 포스트 내용
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)  # 카테고리 이름
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간
    updated_at = models.DateTimeField(auto_now=True)  # 업데이트 시간

    def __str__(self):
        return f"{self.title} - {self.category} by {self.user.username}"

    @property
    def category_name(self):
        return self.category.category_name
