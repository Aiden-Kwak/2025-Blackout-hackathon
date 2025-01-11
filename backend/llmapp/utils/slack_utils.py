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
    print("=======SAVE_MSG_FUNC======")
    print("=============> params:", params)
    
    response = requests.get(url, headers=headers, params=params)
    print("YOU HAVE TO GET SOME RESPONSE: ", response)
    if response.status_code != 200:
        print("FUCKED CASE: 1")
        raise RuntimeError(f"Failed to fetch messages: {response.text}")

    data = response.json()
    print("YOU HAVE TO GET SOME DATA: ", data)
    if not data.get("ok"):
        print("FUCKED CASE: 2")
        raise RuntimeError(f"Slack API error: {data.get('error')}")

    messages = data.get("messages", [])
    print("YOU HAVE TO GET SOME MESSAGES: ", messages)

    for msg in messages:
        print("YOU HAVE TO GET SOME MSG LIST: ", msg)

        # 데이터 검증
        user_id = msg.get("user", "Unknown")
        text = msg.get("text", "").strip()  # 빈 문자열 처리
        timestamp = msg.get("ts")

        if not timestamp:  # 필수 필드 확인
            print(f"Skipping message due to missing timestamp: {msg}")
            continue

        if not text:  # 텍스트가 비어 있으면 스킵
            print(f"Skipping message due to empty text: {msg}")
            continue

        try:
            _, created = SlackMessage.objects.get_or_create(
                channel_id=channel_id,
                user_id=user_id,
                text=text,
                timestamp=timestamp
            )
            if not created:
                print(f"Message already exists: {msg}")
        except Exception as e:
            print(f"Failed to save message: {msg}. Error: {e}")


def generate_embedding(text):
    print("I AM HERE: generate_embedding entered")
    try:
        print("I AM HERE: generate_embedding try")
        if not openai_api_key:
            print("no openai_api_key")
            raise ValueError("OpenAI API 키가 설정되지 않았습니다. 환경 변수 OPENAI_API_KEY를 확인하세요.")
        
        if not isinstance(text, str):
            print("no text")
            raise ValueError(f"Input text must be a string. Got: {type(text)}")

        response = openai.Embedding.create(
            input=text,
            model="text-embedding-3-small",
            api_key=openai_api_key
        )
        print("I AM HERE: generate_embedding response")
        embedding = response["data"][0]["embedding"]
        return np.array(embedding, dtype=np.float32)

    except openai.error.OpenAIError as e:
        raise RuntimeError(f"OpenAI API 호출 중 오류가 발생했습니다: {e}")
    except Exception as e:
        raise RuntimeError(f"임베딩 생성 실패: {e}")

def create_message_embeddings():
    print("I AM HERE: embedding")
    messages = SlackMessage.objects.filter(embedding_created=False)
    print("YOU HAVE TO GET SOME MESSAGES: ", messages)
    for message in messages:
        print("YOU HAVE TO GET SOME MESSAGE(single): ", message)
        embedding = generate_embedding(message.text)
        print("YOU HAVE TO SEE ME: generate_embedding safe")
        MessageEmbedding.objects.create(message=message, embedding_data=embedding.tobytes())
        print("YOU HAVE TO SEE ME 2: object create safe")
        message.embedding_created = True
        message.save()
