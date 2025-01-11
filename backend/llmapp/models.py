from django.db import models
from django.contrib.auth.models import User

class SlackChannel(models.Model):
    channel_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class SlackMessage(models.Model):
    channel = models.ForeignKey(SlackChannel, on_delete=models.CASCADE, related_name="messages")
    message_id = models.CharField(max_length=100, unique=True)
    text = models.TextField()
    timestamp = models.DateTimeField()
    user_name = models.CharField(max_length=200)
    is_question = models.BooleanField(default=True)

    def __str__(self):
        return f"Message {self.message_id} in {self.channel.name}"


class FAISSIndexMetadata(models.Model):
    channel = models.OneToOneField(SlackChannel, on_delete=models.CASCADE, related_name="faiss_index")
    index_file = models.CharField(max_length=255)
    metadata_file = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"FAISS Index for {self.channel.name}"


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
