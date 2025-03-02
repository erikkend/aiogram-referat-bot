import aiosqlite

from db import DB_PATH

from datetime import datetime
from functools import wraps
from aiogram.types import Message


async def check_subscription(user_id: int) -> bool:
    """Проверяет, активна ли подписка у пользователя."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT subscription_expiry FROM users WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            if row and row[0]:
                expiry_date = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                return expiry_date > datetime.now()  # True, если подписка активна
            return False  # Подписки нет


def require_subscription(func):
    """Декоратор, который ограничивает доступ без подписки"""
    @wraps(func)
    async def wrapper(message: Message, *args, **kwargs):
        if await check_subscription(message.from_user.id):
            return await func(message, *args, **kwargs)
        else:
            await message.answer("⛔ У вас нет подписки. Купите подписку, чтобы использовать эту функцию.")
    return wrapper