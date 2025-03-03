import db

from texts import start_text, supp_text
from utils import require_subscription
from keyboards import main_kb, doc_kb, select_tariff_kb, tariffs_kb, share_friend_kb, back_to_main_kb
from services.gemini_api import TextGenerator
from middlewares import TextGeneratorMiddleware

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State

from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()
txt_generator = TextGenerator()
router.message.middleware(TextGeneratorMiddleware(txt_generator))
router.callback_query.middleware(TextGeneratorMiddleware(txt_generator))


class DocumentState(StatesGroup):
    waiting_for_topic = State()
    editing_text = State()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(text=start_text, reply_markup=main_kb)
    await db.add_user(message.from_user.id)

@router.callback_query(F.data == 'main_menu')
async def start(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text=start_text, reply_markup=main_kb)

@router.callback_query(F.data == "invite_friend")
async def invite_friend(callback: CallbackQuery, bot: Bot):
    await callback.answer()
    await bot.send_message(callback.from_user.id,
                           f'Перешли сообщение другу👇👇👇',
                            reply_markup=share_friend_kb)

@router.callback_query(F.data == "supp")
async def support_contacts(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(supp_text, reply_markup=back_to_main_kb)

@router.callback_query(F.data == 'sub_info')
async def sub_menu(callback: CallbackQuery):
    await callback.answer()
    user_info = await db.get_user_info(callback.from_user.id)
    user_sub_expiry = "⛔ У вас нет подписки" if user_info["subscription_expiry"] is None else user_info["subscription_expiry"]
    await callback.message.edit_text(text=f"""🔑 Ваша подписка действует до: {user_sub_expiry}""", reply_markup=select_tariff_kb)

@router.callback_query(F.data == 'select_tariff')
async def tariffs_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text="Выберите один из тарифов", reply_markup=tariffs_kb)

@router.callback_query(F.data == 'write_doc')
@require_subscription
async def write_doc(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("📝 Введите тему документа:")
    await state.set_state(DocumentState.waiting_for_topic)

@router.message(DocumentState.waiting_for_topic)
async def generate_document(message: Message, state: FSMContext, text_generator: TextGenerator):
    topic = message.text
    await message.answer(f"⏳ Генерирую текст для темы: {topic}...")
    document_text = await text_generator.generate_text_by_topic(message.from_user.id,topic)
    await message.answer(f"📄 Ваш документ по теме *{topic}*:\n\n{document_text}", parse_mode="Markdown", reply_markup=doc_kb)
    await state.set_state(DocumentState.editing_text)
    await state.update_data(topic=topic)

@router.callback_query(F.data.in_({"expand_text", "rewrite_text", "change_style", "increase_uniqueness"}))
async def process_editing(callback: CallbackQuery, state: FSMContext, text_generator: TextGenerator):
    await callback.answer()
    data = await state.get_data()
    topic = data["topic"]
    await callback.message.answer(f"⏳ Генерирую текст для темы: {topic}...")
    new_text = await text_generator.edit_text(callback.from_user.id, callback.data)
    await callback.message.answer(f"📄 Ваш документ по теме *{topic}*:\n\n{new_text}", parse_mode="Markdown", reply_markup=doc_kb)
    await state.clear()