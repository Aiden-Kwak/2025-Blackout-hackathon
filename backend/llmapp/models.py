from django.db import models

class SlackMessage(models.Model):
    channel_id = models.CharField(max_length=50)
    user_id = models.CharField(max_length=50)
    text = models.TextField()
    timestamp = models.CharField(max_length=50, unique=True) 
    embedding_created = models.BooleanField(default=False)  # 임베딩 생성 여부
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.user_id} in {self.channel_id} at {self.timestamp}"


class MessageEmbedding(models.Model):
    message = models.OneToOneField(SlackMessage, on_delete=models.CASCADE, related_name="embedding")
    embedding_data = models.BinaryField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Embedding for message {self.message.id}"
