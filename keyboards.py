
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton


main_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✏️Генерировать документ", callback_data='documents')],
    [InlineKeyboardButton(text="📊Моя подписка", callback_data='sub_info'), InlineKeyboardButton(text="💬Поддержка", callback_data='supp')],
    [InlineKeyboardButton(text="🤝Пригласить друга", callback_data='invite_friend')]
])

doc_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📝 Написать документ", callback_data='write_doc')],
    [InlineKeyboardButton(text="🙌 Увеличить объём текста", callback_data='increase_text'), InlineKeyboardButton(text="✍️ Переписать другими словами", callback_data='rewrite_text')],
    [InlineKeyboardButton(text="🎨 Изменить стиль текста", callback_data='change_text_style'), InlineKeyboardButton(text="📈 Повысить уникальность - платно", callback_data='increase_text_uniq')],
    [InlineKeyboardButton(text="Назад", callback_data='main_menu')]
])

select_tariff_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💎 Выбрать тариф", callback_data='select_tariff')],
    [InlineKeyboardButton(text="Назад", callback_data='main_menu')]
])

tariffs_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💵 Подписка на 7 дней - 500 рублей", callback_data='7days_tariff')],
    [InlineKeyboardButton(text="💵 Подписка на 14 дней - 1000 рублей", callback_data='14days_tariff')],
    [InlineKeyboardButton(text="💵 Подписка на 30 дней - 2000 рублей", callback_data='30days_tariff')],
])

back_to_main_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Главное меню", callback_data='main_menu')],
])