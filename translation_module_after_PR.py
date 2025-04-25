import requests
import time
import openai
import logging
import os
from dotenv import load_dotenv
from functools import wraps
from typing import Optional, Dict

load_dotenv()  # Загружаем переменные окружения из .env

# Настраиваем логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class TranslatorConfig:
    """Класс для хранения конфигурации API и системных параметров."""
    OPENAI_KEY = os.getenv("OPENAPI_KEY")
    DEEPL_KEY = os.getenv("DEEPL_KEY")
    GOOGLE_KEY = os.getenv("GOOGLE_KEY")
    LOCAL_API_URL = "http://localhost:8000/translate"  # Эндпоинт локального сервиса
    OPENAI_MODEL = "gpt-3.5-turbo"
    SYSTEM_ROLE = "Ты профессиональный переводчик."
    MAX_RETRIES = 1


def retry_request(max_retries=3, fallback_to_opus=False):
    """Декоратор для повторных запросов к API. Если API не отвечает, можно переключиться на OPUS-MT."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.warning(f"Ошибка в {func.__name__}: {e}. Попытка {attempt + 1} из {max_retries}")
                    time.sleep(2)  # Ожидание перед повторной попыткой
            if fallback_to_opus:
                logging.info("Все попытки исчерпаны. Переход на локальную OPUS-MT модель.")
                return _translate_opus_mt_local(kwargs.get("text", ""))
            raise RuntimeError(f"Не удалось выполнить {func.__name__} после {max_retries} попыток.")
        return wrapper
    return decorator


def _make_request(url, method="POST", headers=None, params=None, json_data=None) -> Dict:
    """Универсальная функция запроса к API с обработкой ошибок."""
    try:
        response = requests.request(method, url, headers=headers, params=params, json=json_data, timeout=10)
        response.raise_for_status()
        if not response.text.strip():
            raise ValueError("API вернул пустой ответ")
        return response.json()
    except (requests.RequestException, ValueError) as e:
        logging.error(f"Ошибка запроса {url}: {e}")
        raise


class MultiAPITranslator:
    def __init__(self):
        self.config = TranslatorConfig()

    @retry_request(max_retries=TranslatorConfig.MAX_RETRIES, fallback_to_opus=True)
    def _translate_openai(self, text: str) -> str:
        """Перевод через OpenAI API с повторными попытками."""
        client = openai.OpenAI(api_key=self.config.OPENAI_KEY)
        response = client.chat.completions.create(
            model=self.config.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": self.config.SYSTEM_ROLE},
                {"role": "user", "content": f"Переведи на английский: {text}"}
            ]
        )
        return response.choices[0].message.content

    @retry_request(max_retries=TranslatorConfig.MAX_RETRIES, fallback_to_opus=True)
    def _translate_deepl(self, text: str) -> str:
        url = "https://api-free.deepl.com/v2/translate"
        params = {"auth_key": self.config.DEEPL_KEY, "text": text, "target_lang": "EN"}
        response = _make_request(url, method="POST", params=params)
        return response["translations"][0]["text"]

    @retry_request(max_retries=TranslatorConfig.MAX_RETRIES, fallback_to_opus=True)
    def _translate_google(self, text: str) -> str:
        url = "https://translation.googleapis.com/language/translate/v2"
        params = {"q": text, "target": "en", "format": "text", "key": self.config.GOOGLE_KEY}
        response = _make_request(url, method="POST", params=params)
        return response["data"]["translations"][0]["translatedText"]

    @retry_request(max_retries=TranslatorConfig.MAX_RETRIES, fallback_to_opus=False)
    def _translate_local(self, text: str) -> str:
        """Перевод через локальный FastAPI сервис."""
        url = self.config.LOCAL_API_URL
        json_data = {"text": text, "target_lang": "en"}
        response = _make_request(url, method="POST", json_data=json_data)
        return response.get("translated_text", "Ошибка перевода"), "opus_local"

    def translate(self, text: str) -> str:
        """Основной метод перевода. Использует OpenAI, DeepL, Google или локальную модель."""
        try:
            return self._translate_openai(text)
        except Exception:
            try:
                return self._translate_deepl(text)
            except Exception:
                try:
                    return self._translate_google(text)
                except Exception:
                    return self._translate_local(text)
