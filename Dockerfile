FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y \
    procps \    
    git \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libx11-6 \
    libegl1 \
    libgles2 \
    mesa-utils \
    v4l-utils

WORKDIR /usr/local/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

