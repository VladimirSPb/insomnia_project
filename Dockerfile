# 📁 Файл: Dockerfile
# Docker-контейнер для FastAPI сервиса с OPUS-MT

# ✅ Базовый образ с поддержкой PyTorch и CUDA (или CPU-совместимый)
FROM python:3.10-slim

# ✅ Установка системных зависимостей
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean

# ✅ Установка Git LFS (если модель будет загружаться с huggingface)
RUN apt-get update && \
    apt-get install -y curl && \
    curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash && \
    apt-get install -y git-lfs && \
    git lfs install

# ✅ Установка зависимостей Python
COPY requirements.txt ./
RUN pip install --no-cache-dir --timeout=180 -r requirements.txt

# ✅ Копируем приложение внутрь контейнера
WORKDIR /app
COPY . .

# ✅ Команда запуска FastAPI-сервера
CMD ["uvicorn", "fastapi_opus_server:app", "--host", "0.0.0.0", "--port", "8000"]
