from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

import db
from texts import start_text
from utils import require_subscription
from keyboards import main_kb, doc_kb, select_tariff_kb, tariffs_kb

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(text=start_text, reply_markup=main_kb)
    await db.add_user(message.from_user.id)

@router.callback_query(F.data == 'main_menu')
async def start(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text=start_text, reply_markup=main_kb)

@router.callback_query(F.data == 'documents')
async def doc_menu(callback: CallbackQuery):
    await callback.answer('Генерация документа')
    await callback.message.edit_text(text="Выберите функцию", reply_markup=doc_kb)

@router.callback_query(F.data == 'sub_info')
async def sub_menu(callback: CallbackQuery):
    await callback.answer()

    user_info = await db.get_user_info(callback.from_user.id)
    user_balance = user_info["balance"]
    user_sub_expiry = "Подписки нет" if user_info["subscription_expiry"] is None else user_info["subscription_expiry"]

    await callback.message.edit_text(text=f"""Ваш баланс: {user_balance}\nПодписка до: {user_sub_expiry}""", reply_markup=select_tariff_kb)

@router.callback_query(F.data == 'select_tariff')
async def tariffs_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text="Выберите один из тарифов", reply_markup=tariffs_kb)
