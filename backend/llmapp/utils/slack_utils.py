# llmapp/utils/slack_utils.py
import os
import openai
import requests
import numpy as np
from llmapp.models import SlackMessage, MessageEmbedding

SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")
openai_api_key = os.getenv("OPENAI_API_KEY")

def fetch_slack_messages(channel_id, limit=100):
    url = "https://slack.com/api/conversations.history"
    headers = {"Authorization": f"Bearer {SLACK_TOKEN}"}
    params = {"channel": channel_id, "limit": limit}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise RuntimeError(f"Failed to fetch messages: {response.text}")
    
    data = response.json()
    if not data.get("ok"):
        raise RuntimeError(f"Slack API error: {data.get('error')}")
    
    return data.get("messages", [])

def save_slack_messages(channel_id):
    print("잘왔니?: ", channel_id)
    url = "https://slack.com/api/conversations.history"
    headers = {"Authorization": f"Bearer {SLACK_TOKEN}"}
    params = {"channel": channel_id, "limit": 100}
    print("=======SAVE_MSG_FUNC======") # 굿

    response = requests.get(url, headers=headers, params=params)
    print("YOU HAVE TO GET SOME RESPONSE: ", response) # 200 
    if response.status_code != 200:
        print("FUCKED CASE: 1")
        raise RuntimeError(f"Failed to fetch messages: {response.text}")

    data = response.json()
    print("YOU HAVE TO GET SOME DATA: ", data) # {'ok'}
    if not data.get("ok"):
        print("FUCKED CASE: 2") # 여기 들어옴
        raise RuntimeError(f"Slack API error: {data.get('error')}")

    messages = data.get("messages", [])
    print("YOU HAVE TO GET SOME MESSAGES: ", messages)
    for msg in messages:
        print("YOU HAVE TO GET SOME MSG LIST: ", msg)
        SlackMessage.objects.get_or_create(
            channel_id=channel_id,
            user_id=msg.get("user", "Unknown"),
            text=msg.get("text", ""),
            timestamp=msg.get("ts")
        )


def generate_embedding(text):
    try:
        if not openai_api_key:
            raise ValueError("OpenAI API 키가 설정되지 않았습니다. 환경 변수 OPENAI_API_KEY를 확인하세요.")
        
        if not isinstance(text, str):
            raise ValueError(f"Input text must be a string. Got: {type(text)}")

        response = openai.Embedding.create(
            input=text,
            model="text-embedding-3-small",
            api_key=openai_api_key
        )
        
        embedding = response["data"][0]["embedding"]
        return np.array(embedding, dtype=np.float32)

    except openai.error.OpenAIError as e:
        raise RuntimeError(f"OpenAI API 호출 중 오류가 발생했습니다: {e}")
    except Exception as e:
        raise RuntimeError(f"임베딩 생성 실패: {e}")

def create_message_embeddings():
    messages = SlackMessage.objects.filter(embedding_created=False)
    for message in messages:
        embedding = generate_embedding(message.text)
        MessageEmbedding.objects.create(message=message, embedding_data=embedding.tobytes())
        message.embedding_created = True
        message.save()
