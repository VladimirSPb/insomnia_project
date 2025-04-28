# 🧠 MultiAPI Translator with OPUS-MT fallback

Проект представляет собой универсальный модуль перевода текста с использованием различных API:
- OpenAI GPT
- DeepL
- Google Translate

В случае ошибки — используется локальная модель OPUS-MT через FastAPI-сервер в Docker.

## 🔧 Запуск

### 🐧 Linux / macOS / Windows (трбуется установка make в gitbash):
для запуска потребуется открыть 2 окна gitbash:
1. запуск сервера со скриптом
```bash
make up          — cобирает и запускает сервис (основной код + Docker с локальной моделью OPUS-MT)
make stop        — останавливает всё
make logs        — показывает логи сервиса
make restart     — полная перезагрузка
```
2. отправляем запросы в кудрявом (curl) формате (см. ниже промты для тестирования)


## 📦 Требования

- Docker
- Python (для основного кода)
- `.env` файл с API-ключами

## 🔍 Примеры curl-запросов

```bash
curl -X POST "http://localhost:8000/translate" -H "Content-Type: application/json" -d "{\"text\": \"Une forêt enchantée baignée dans la lumière dorée du crépuscule.\"}"
curl -X POST "http://localhost:8000/translate" -H "Content-Type: application/json" -d "{\"text\": \"Un dragón de cristal volando sobre montañas nevadas bajo la luna llena.\"}"
curl -X POST "http://localhost:8000/translate" -H "Content-Type: application/json" -d "{\"text\": \"Un castello volante fatto di nuvole e stelle nel cielo notturno.\"}"
curl -X POST "http://localhost:8000/translate" -H "Content-Type: application/json" -d "{\"text\": \"月光の下に浮かぶ巨大な水中都市。\"}"
curl -X POST "http://localhost:8000/translate" -H "Content-Type: application/json" -d "{\"text\": \"在星空下跳舞的光之蝴蝶。\"}"
curl -X POST "http://localhost:8000/translate" -H "Content-Type: application/json" -d "{\"text\": \"Таинственный замок на вершине ледяной горы в полярной ночи.\"}"
curl -X POST "http://localhost:8000/translate" -H "Content-Type: application/json" -d "{\"text\": \"Ein mechanischer Phönix erhebt sich aus einer Steampunk-Stadt.\"}"
curl -X POST "http://localhost:8000/translate" -H "Content-Type: application/json" -d "{\"text\": \"Uma floresta mágica com árvores de cristal sob a aurora boreal.\"}"
curl -X POST "http://localhost:8000/translate" -H "Content-Type: application/json" -d "{\"text\": \"مدينة عائمة مصنوعة من الأضواء الذهبية فوق بحر الغيوم.\"}"
curl -X POST "http://localhost:8000/translate" -H "Content-Type: application/json" -d "{\"text\": \"별빛 아래 펼쳐진 거대한 꽃밭 속의 고양이 왕국.\"}"

```

Хорошего дня!