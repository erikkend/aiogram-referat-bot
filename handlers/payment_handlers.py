import re

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery

import db
from keyboards import back_to_main_kb


router = Router()


@router.callback_query(F.data.regexp(r'\d+days_tariff'))
async def tariff_pay(callback: CallbackQuery, bot: Bot):
    await callback.answer()
    match = re.match(r'(\d+)days_tariff', callback.data)
    days = match.group(1)

    if days == "7":
        price = LabeledPrice(label='Подписка на 7 дней', amount=50000)
    elif days == "14":
        price = LabeledPrice(label='Подписка на 14 дней', amount=100000)
    elif days == "30":
        price = LabeledPrice(label='Подписка на 30 дней', amount=200000)

    await bot.send_invoice(
        chat_id=callback.message.chat.id,
        title=f"Подписка на {days} дней",
        description=f"Подписка в боте",
        payload=days,
        provider_token="2051251535:TEST:OTk5MDA4ODgxLTAwNQ",
        currency='RUB',
        prices=[price]
    )

@router.pre_checkout_query()
async def pre_checkout_query(checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(checkout_query.id, ok=True)

@router.message(F.successful_payment)
async def successful_payment(message: Message):
    days = message.successful_payment.invoice_payload
    await db.set_subscription(message.from_user.id, int(days))
    await message.answer(f"Вы купили подписку на {days} дней", reply_markup=back_to_main_kb)
