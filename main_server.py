# main_server.py
# Общий FastAPI-сервер, который использует MultiAPITranslator

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from translation_module_after_PR import MultiAPITranslator

app = FastAPI(title="MultiAPI Translation Service")
translator = MultiAPITranslator()

class TranslationRequest(BaseModel):
    text: str

class TranslationResponse(BaseModel):
    translated_text: str

@app.post("/translate", response_model=TranslationResponse)
def translate(request: TranslationRequest):
    try:
        result = translator.translate(request.text)
        return {"translated_text": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
