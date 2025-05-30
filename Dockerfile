# base image
FROM python:3.13-slim

# os 업데이트 & 설치 
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# 코드 복사 
COPY ./common /app/common
COPY ./chatbot.py /app/chatbot.py
COPY ./requirements.txt /app

# 실행 폴더 정의 
WORKDIR /app

# 필요한 라이브러리 설치  
RUN pip3 install -r ./requirements.txt

# 실행 포트 정의 
EXPOSE 8501

# 컨테이너 실행 유무 확인 
HEALTHCHECK CMD [ "$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8501)" = "200" ] && echo "ok"

# 웹서버 실행 
ENTRYPOINT ["chainlit", "run", "chatbot.py", "--port", "8501", "--host", "0.0.0.0"]