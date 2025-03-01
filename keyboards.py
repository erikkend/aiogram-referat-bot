
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton


start_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✏️Генерировать документ", callback_data='documents')],
    [InlineKeyboardButton(text="📊Моя подписка", callback_data='user_sub'), InlineKeyboardButton(text="💬Поддержка", callback_data='supp')],
    [InlineKeyboardButton(text="🤝Пригласить друга", callback_data='invite_friend')]
])

gen_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📝 Написать документ ", callback_data='gen_doc')],
    [InlineKeyboardButton(text="🙌 Увеличить объём текста", callback_data='increase_text'), InlineKeyboardButton(text="✍️ Переписать другими словами", callback_data='rewrite_text')],
    [InlineKeyboardButton(text="🎨 Изменить стиль текста", callback_data='change_text_style'), InlineKeyboardButton(text="📈 Повысить уникальность - платно", callback_data='increase_text_uniq')],
    [InlineKeyboardButton(text="Назад", callback_data='main_menu')]
])