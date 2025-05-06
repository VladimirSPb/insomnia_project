# 📁 Файл: fastapi_opus_server.py
# FastAPI сервер, обслуживающий локальную модель OPUS-MT для перевода текста

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# ✅ Инициализация FastAPI-приложения
app = FastAPI(title="Local OPUS-MT Translator API")

# ✅ Модель и токенизатор загружаются при старте сервера (однократно)
model_name = "Helsinki-NLP/opus-mt-mul-en"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


# ✅ Структура входящего JSON-запроса
class TranslationRequest(BaseModel):
    text: str
    src_lang: str = "mul"        # Язык-источник (многоязычный)
    tgt_lang: str = "en"         # Язык-перевода (английский по умолчанию)


# ✅ Основная ручка API: POST /translate
@app.post("/translate")
def translate(request: TranslationRequest):
    """
    Принимает JSON:
    {
        "text": "Bonjour le monde",
        "src_lang": "fr",
        "tgt_lang": "en"
    }

    Возвращает JSON:
    {
        "translated_text": "Hello world"
    }
    """
    try:
        # 🔽 Получаем текст для перевода
        input_text = request.text

        # 🔽 Токенизируем текст (оборачиваем в тензоры для подачи в модель)
        inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)
        inputs = {key: value.to(model.device) for key, value in inputs.items()}

        # 🔽 Генерация перевода моделью
        outputs = model.generate(**inputs)

        # 🔽 Декодируем токены обратно в строку
        translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # 🔼 Возвращаем JSON с переводом
        return {"translated_text": translated_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка перевода: {str(e)}")


# ✅ Блок запуска при использовании через Docker (или напрямую как python скрипт)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fastapi_opus_server:app", host="0.0.0.0", port=8000, reload=True)
