import aiosqlite
from datetime import datetime, timedelta

DB_PATH = "database.db"  # Путь к файлу базы данных

async def init_db():
    """Создает таблицу пользователей, если она не существует"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                balance INTEGER DEFAULT 0,
                subscription_expiry TEXT DEFAULT NULL
            )
        """)
        await db.commit()

async def add_user(user_id: int):
    """Добавляет пользователя в базу, если его нет"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO users (user_id) 
            VALUES (?) 
            ON CONFLICT(user_id) DO NOTHING
        """, (user_id,))
        await db.commit()

async def update_balance(user_id: int, amount: int):
    """Обновляет баланс пользователя"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            UPDATE users 
            SET balance = balance + ? 
            WHERE user_id = ?
        """, (amount, user_id))
        await db.commit()

async def set_subscription(user_id: int, days: int):
    """Устанавливает подписку на определенное количество дней"""
    expiry_date = datetime.now() + timedelta(days=days)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            UPDATE users 
            SET subscription_expiry = ? 
            WHERE user_id = ?
        """, (expiry_date.strftime("%Y-%m-%d %H:%M:%S"), user_id))
        await db.commit()

async def get_user_info(user_id: int):
    """Получает информацию о пользователе"""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("""
            SELECT balance, subscription_expiry 
            FROM users 
            WHERE user_id = ?
        """, (user_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                balance, expiry = row
                return {"balance": balance, "subscription_expiry": expiry}
            return None

async def check_subscription(user_id: int):
    """Проверяет, активна ли подписка"""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("""
            SELECT subscription_expiry 
            FROM users 
            WHERE user_id = ?
        """, (user_id,)) as cursor:
            row = await cursor.fetchone()
            if row and row[0]:
                expiry_date = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                return expiry_date > datetime.now()
            return False
