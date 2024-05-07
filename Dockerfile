FROM python:3.11-slim

WORKDIR /app

ARG AWS_ACCESS_KEY_ID=""
ARG AWS_SECRET_ACCESS_KEY=""

ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    alsa-utils \
    ffmpeg \
    && python -m ensurepip && pip install --upgrade pip \
    && rm -rf /var/lib/apt/lists/*

# RUN git clone https://github.com/nesaboz/whisper.git .
COPY . .

RUN pip3 install --verbose -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

CMD streamlit run app.py --server.port=8501 --server.address=0.0.0.0