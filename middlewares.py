from aiogram import BaseMiddleware
from aiogram.types import Update
from typing import Dict, Any

class TextGeneratorMiddleware(BaseMiddleware):
    def __init__(self, text_generator):
        super().__init__()
        self.text_generator = text_generator

    async def __call__(self, handler, event: Update, data: Dict[str, Any]):
        data["text_generator"] = self.text_generator  # Передаем объект в хэндлер
        return await handler(event, data)
