# llmapp/utils/slack_utils.py
import os
import openai
from openai import OpenAI, AuthenticationError, APIConnectionError, RateLimitError, OpenAIError
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

"""
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
"""

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

        user_id = msg.get("user", "Unknown")
        text = msg.get("text", "").strip()  # 빈 문자열 처리
        timestamp = msg.get("ts")
        thread_ts = msg.get("thread_ts")

        if not timestamp:
            print(f"Skipping message due to missing timestamp: {msg}")
            continue

        if not text:  # 텍스트가 비어 있으면 스킵
            print(f"Skipping message due to empty text: {msg}")
            continue

        # 스레드가 있으면 스레드 메시지를 가져와 본문과 결합
        full_text = text
        if thread_ts:
            print(f"Fetching thread for message with thread_ts: {thread_ts}")
            thread_text = fetch_thread_messages(channel_id, thread_ts, headers)
            if thread_text:
                full_text += f"\n\n--- Thread ---\n{thread_text}"

        try:
            # 메시지 저장
            _, created = SlackMessage.objects.get_or_create(
                channel_id=channel_id,
                user_id=user_id,
                text=full_text,  # 스레드 메시지와 본문 결합
                timestamp=timestamp,
                defaults={"thread_ts": thread_ts}  # 스레드 ID 저장
            )
            print("YOU HAVE TO GET SOME CREATED: ", created)
            if not created:
                print(f"Message already exists: {msg}")

        except Exception as e:
            print(f"Failed to save message: {msg}. Error: {e}")


def fetch_thread_messages(channel_id, thread_ts, headers):
    print(f"Fetching thread messages for thread_ts: {thread_ts}")

    url = "https://slack.com/api/conversations.replies"
    params = {"channel": channel_id, "ts": thread_ts, "limit": 100}

    response = requests.get(url, headers=headers, params=params)
    print("Thread response: ", response)
    if response.status_code != 200:
        print(f"Failed to fetch thread messages: {response.text}")
        return ""

    data = response.json()
    print("Thread data: ", data)
    if not data.get("ok"):
        print(f"Slack API error in thread replies: {data.get('error')}")
        return ""

    thread_messages = data.get("messages", [])
    thread_text = []

    for msg in thread_messages:
        user_id = msg.get("user", "Unknown")
        text = msg.get("text", "").strip()
        timestamp = msg.get("ts")

        if not timestamp or not text:
            continue

        # 스레드 메시지 포맷팅
        thread_text.append(f"[{user_id} at {timestamp}]: {text}")

    # 스레드 메시지를 하나의 문자열로 반환
    return "\n".join(thread_text)




def generate_embedding(text):
    print("I AM HERE: generate_embedding entered")
    try:
        print("I AM HERE: generate_embedding try") # 여기까지 ㅇㅋ
        if not openai_api_key:
            print("no openai_api_key")
            raise ValueError("OpenAI API 키가 설정되지 않았습니다. 환경 변수 OPENAI_API_KEY를 확인하세요.")
        
        if not isinstance(text, str):
            print("no text")
            raise ValueError(f"Input text must be a string. Got: {type(text)}")

        try:
            client = OpenAI(api_key=openai_api_key)
            response = client.embeddings.create(model="text-embedding-3-small", input=text)
            
            embedding_data = response.data
            if not isinstance(embedding_data, list) or not embedding_data:
                raise RuntimeError(f"Invalid API response: response.data is not a non-empty list. Actual data: {embedding_data}")

            first_item = embedding_data[0]
            if not isinstance(first_item, openai.types.embedding.Embedding):
                raise RuntimeError(f"Unexpected type for response.data[0]: {type(first_item)}. Expected openai.types.embedding.Embedding.")
            if not hasattr(first_item, "embedding"):
                raise RuntimeError(f"'embedding' attribute is missing in response.data[0]: {first_item}")

            embedding = np.array(first_item.embedding, dtype=np.float32)
            return embedding

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
