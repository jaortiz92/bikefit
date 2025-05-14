FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y \
    git \
    procps \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libxcb-shm0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/local/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt