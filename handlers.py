from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from texts import start_text
from keyboards import start_kb, gen_kb

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(text=start_text, reply_markup=start_kb)

@router.callback_query(F.data == 'main_menu')
async def start(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text=start_text, reply_markup=start_kb)

@router.callback_query(F.data == 'documents')
async def gen_doc(callback: CallbackQuery):
    await callback.answer('Генерация документа')
    await callback.message.edit_text(text="Выберите функцию", reply_markup=gen_kb)