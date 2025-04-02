# Slack RAG 기반 정보 검색 및 블로그 생성 서비스  
# Slack RAG-based Information Retrieval and Blog Generation Service

## 목차 / Table of Contents
- [한국어](#%ED%95%9C%EA%B5%AD%EC%96%B4)
- [English](#english)

---

## 한국어

### blackout-hackathon  
본 서비스는 2025년 1월 11일부터 2025년 1월 12일까지 진행된 서, 연, 고, 카, 포, 지 연합해커톤 기간 동안 개발되었습니다.

<p align="center">
  <img src="img/해커톤표지.png" width="300" alt="해커톤 표지"/>
</p>

### 기술스택
- Django REST Framework
- Next.js
- OPENAI API (gpt-3.5-turbo, text-embedding-3-small)
- Slack
- EC2, Nginx

### 소개
이 서비스는 Slack 채널의 대화 데이터를 활용하여 질문에 대한 과거 대화를 검색하고, 이를 기반으로 적합한 답변을 생성합니다.  
또한 생성된 답변은 블로그 형태로 자동 문서화하여 손쉽게 관리할 수 있도록 돕습니다.  
반복되는 질문에 대한 부담을 줄이고, Slack의 정보를 체계적으로 정리할 수 있는 새로운 도구를 제공합니다.

### 주요 기능
1. **Slack 채널 데이터 검색**  
   - Slack 채널 내의 과거 대화를 RAG (Retrieval-Augmented Generation) 방식으로 검색합니다.  
   - 질문에 대한 원래 메시지, 관련 스레드, 그리고 이를 바탕으로 생성된 답변을 제공합니다.  
   - 임베딩은 매번 진행하지 않습니다. 슬랙 커맨드로 트리거되어 임베딩을 진행할 때, 이미 임베딩 된 글과 스레드는 재처리하지 않고, 새로운 글만 추가되어 자원 낭비를 방지합니다.

2. **임베딩 검색**  
   - Slack 대화 데이터를 효율적으로 검색하기 위해 CDIST 기반의 코사인 거리 검색을 수행합니다.  
   - 모든 임베딩을 Numpy 형식으로 변환하고, 쿼리 임베딩과 저장된 임베딩 간의 거리 계산을 통해 상위 k개의 과거 유사 스레드를 추출합니다.

3. **자동 블로그 생성**  
   - 질문과 추출된 과거 유사 답변들을 기반으로 블로그 형태의 문서를 생성합니다.  
   - 생성된 문서는 개인 블로그에 업로드되어 링크가 제공되며, 카테고리는 기본값 '미정'으로 설정됩니다.  
   - 블로그 제목은 질문 내용을 사용하며, Slack 대화를 체계적으로 문서화합니다.  
   - 스레드에 참고 링크가 포함되어 있다면 해당 링크도 함께 제공됩니다.

### 환경변수 설정
1. 아래 변수들을 `backend/.env` 파일에 작성해야 합니다.
   ```bash
   DJANGO_SECRET_KEY=key
   DJANGO_GOOGLE_OAUTH2_CLIENT_ID=key
   DJANGO_GOOGLE_OAUTH2_CLIENT_SECRET=key
   DJANGO_GOOGLE_OAUTH2_PROJECT_ID=key
   DEEPSEEK_API_KEY=key # not used in this project
   DEEPSEEK_BASE_URL=https://api.deepseek.com
   OPENAI_API_KEY=key
   SLACK_SECRET_KEY=key
   SLACK_BOT_TOKEN=key
   SLACK_VERIFICATION_TOKEN=key # not used in this project
   ```

2. Slack 권한 요약:
   ```bash
   channels:read, groups:read, im:read, mpim:read  # 채널 목록 및 메시지 접근
   channels:history, groups:history, im:history, mpim:history  # 메시지 기록 읽기
   chat:write  # 메시지 전송
   # 슬랙 커맨드 설정 (슬래시 명령어 사용)
   ```

### 시연
<p align="center">
  <img src="img/demo.png" width="700" alt="데모 이미지"/>
</p>

### 팀원 및 역할

| 성명              | 담당                                                       | 깃허브                                                                 |
| ----------------- | ---------------------------------------------------------- | ---------------------------------------------------------------------- |
| 곽병혁 (leader)   | LLM RAG 구현 및 슬랙봇 개발<br/>서비스 기획 및 디자인 (frontend) | [![Aiden-Kwak](http://img.shields.io/badge/Aiden--Kwak-655ced?style=social&logo=github)](https://github.com/Aiden-Kwak) |
| 김재윤            | 블로그 기능 서버 및 프론트엔드 개발<br/>발표자료 디자인          | [![1MTW](http://img.shields.io/badge/1MTW-655ced?style=social&logo=github)](https://github.com/1MTW)            |
| 고대희            | 인프라 (EC2, Nginx)<br/>슬랙봇 개발<br/>최종 발표               | [![DaehuiG](http://img.shields.io/badge/DaehuiG-655ced?style=social&logo=github)](https://github.com/DaehuiG)      |

---

## English

### blackout-hackathon  
This service was developed during the blackout-hackathon held from January 11, 2025 to January 12, 2025 by the collaboration of teams Seoul National University, Yonsei University, Korea University, KAIST, POSTECH, GIST.

<p align="center">
  <img src="img/해커톤표지.png" width="300" alt="Hackathon Cover"/>
</p>

### Technology Stack
- Django REST Framework
- Next.js
- OPENAI API (gpt-3.5-turbo, text-embedding-3-small)
- Slack
- EC2, Nginx

### Overview
This service leverages conversation data from Slack channels to search past dialogues relevant to a query and generates an appropriate response.  
The generated answer is automatically documented as a blog post for easy management.  
It reduces the burden of repetitive queries and offers a new tool for systematically organizing Slack information.

### Key Features
1. **Slack Channel Data Retrieval**  
   - Searches past conversations in Slack channels using the RAG (Retrieval-Augmented Generation) approach.  
   - Provides the original message, related threads, and a generated answer based on the query.  
   - Embeddings are not performed repeatedly. When triggered by a Slack command, only new messages are embedded and added to existing embeddings to avoid unnecessary resource usage.

2. **Embedding-based Search**  
   - Uses cosine distance search based on CDIST to efficiently query Slack conversation data.  
   - Converts all embeddings to Numpy format and computes distances between the query embedding and stored embeddings to extract the top k similar past threads.

3. **Automatic Blog Generation**  
   - Creates a blog post based on the query and extracted similar past responses.  
   - The generated document is uploaded to a personal blog and a link is provided. The category is set to "미정" (undecided) by default.  
   - The blog title is derived from the query, systematically documenting the Slack conversation.  
   - If the thread contains reference links, those links are always included.

### Environment Variable Configuration
1. Add the following variables to your `backend/.env` file:
   ```bash
   DJANGO_SECRET_KEY=key
   DJANGO_GOOGLE_OAUTH2_CLIENT_ID=key
   DJANGO_GOOGLE_OAUTH2_CLIENT_SECRET=key
   DJANGO_GOOGLE_OAUTH2_PROJECT_ID=key
   DEEPSEEK_API_KEY=key # not used in this project
   DEEPSEEK_BASE_URL=https://api.deepseek.com
   OPENAI_API_KEY=key
   SLACK_SECRET_KEY=key
   SLACK_BOT_TOKEN=key
   SLACK_VERIFICATION_TOKEN=key # not used in this project
   ```

2. Slack Permissions Summary:
   ```bash
   channels:read, groups:read, im:read, mpim:read  # Access to channel lists and messages
   channels:history, groups:history, im:history, mpim:history  # Read message history
   chat:write  # Send messages
   # Slack commands configuration (for using slash commands)
   ```

### Demo
<p align="center">
  <img src="img/demo.png" width="700" alt="Demo Image"/>
</p>

### Team Members and Roles

| Name              | Role                                                       | GitHub                                                                 |
| ----------------- | ---------------------------------------------------------- | ---------------------------------------------------------------------- |
| Aiden-Kwak (leader)   | LLM RAG implementation and Slack bot development<br/>Service planning and design (frontend) | [![Aiden-Kwak](http://img.shields.io/badge/Aiden--Kwak-655ced?style=social&logo=github)](https://github.com/Aiden-Kwak) |
| 김재윤            | Blog functionality server and frontend development<br/>Presentation design          | [![1MTW](http://img.shields.io/badge/1MTW-655ced?style=social&logo=github)](https://github.com/1MTW)            |
| 고대희            | Infrastructure (EC2, Nginx)<br/>Slack bot development<br/>Final presentation               | [![DaehuiG](http://img.shields.io/badge/DaehuiG-655ced?style=social&logo=github)](https://github.com/DaehuiG)      |

---
