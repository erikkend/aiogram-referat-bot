from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from aiogram.filters import CommandStart, Command
from texts import start_text
from keyboards import start_kb, gen_kb

from db import add_user

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(text=start_text, reply_markup=start_kb)
    await add_user(message.from_user.id)

@router.callback_query(F.data == 'main_menu')
async def start(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text=start_text, reply_markup=start_kb)

@router.callback_query(F.data == 'documents')
async def gen_doc(callback: CallbackQuery):
    await callback.answer('Генерация документа')
    await callback.message.edit_text(text="Выберите функцию", reply_markup=gen_kb)


@router.message(Command('pay'))
async def pay(message: Message, bot: Bot):
    await bot.send_invoice(
        chat_id=message.chat.id,
        title="Оплата доступа:",
        description=f"Подписка в боте",
        payload="Subscribe 1 mount",
        provider_token="2051251535:TEST:OTk5MDA4ODgxLTAwNQ",
        currency='RUB',
        prices=[LabeledPrice(label='Подписка на месяц', amount=10000)]
    )

@router.pre_checkout_query()
async def pre_checkout_query(checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(checkout_query.id, ok=True)

@router.message(F.successful_payment)
async def successful_payment(message: Message):
    msg = f"Оплачено {message.successful_payment.total_amount} {message.successful_payment.currency}"
    await message.answer(msg)
