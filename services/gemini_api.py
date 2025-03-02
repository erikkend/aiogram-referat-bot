import os

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

class TextGenerator:
    user_messages = {}  # Храним данные по user_id

    async def generate_text_by_topic(self, user_id: int, topic: str) -> str:
        await self.clear_messages(user_id)
        self.user_messages[user_id].append(
            {'role': 'user', 'parts': [f'Напиши реферат на тему "{topic}"']}
        )
        response = model.generate_content(self.user_messages[user_id])
        await self.save_response(user_id, response.text)
        return response.text

    async def save_response(self, user_id: int, text: str):
        self.user_messages.setdefault(user_id, []).append(
            {'role': 'model', 'parts': [text]}
        )

    async def edit_text(self, user_id: int, edit_type: str):
        if user_id not in self.user_messages:
            self.user_messages[user_id] = []

        if edit_type == "expand_text":
            self.user_messages[user_id].append({'role': 'user', 'parts': ["Добавь больше слов в этот реферат"]})
        elif edit_type == "rewrite_text":
            self.user_messages[user_id].append({'role': 'user', 'parts': ["Напиши этот же реферат другими словами"]})
        elif edit_type == "change_style":
            self.user_messages[user_id].append({'role': 'user', 'parts': ["Измени стиль этого реферата"]})
        elif edit_type == "increase_uniqueness":
            self.user_messages[user_id].append({'role': 'user', 'parts': ["Повысь уникальность этого реферата"]})

        response = model.generate_content(self.user_messages[user_id])
        await self.save_response(user_id, response.text)

        return response.text

    async def clear_messages(self, user_id: int):
        self.user_messages[user_id] = []  # Очищаем историю только для одного юзера
