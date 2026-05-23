from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.keyboards.main_menu import get_main_menu

router = Router()

WELCOME_KK = (
    "Ассалаумағалейкум, Аға 🙌\n"
    "Саламатсыз ба?\n"
    "Денсаулығыңыз қалай?\n\n"
    "Al-NURI компаниясына қош келдіңіз!\n"
    "Сіз қандай сұрақ бойынша хабарласып тұрсыз?"
)

WELCOME_RU = (
    "Ассаламу алейкум! 🙌\n"
    "Как вы поживаете?\n"
    "Как ваше здоровье?\n\n"
    "Добро пожаловать в Al-NURI!\n"
    "По какому вопросу вы обращаетесь?"
)


@router.message(CommandStart())
async def cmd_start(message: Message, lang: str):
    text = WELCOME_KK if lang == "kk" else WELCOME_RU
    await message.answer(text, reply_markup=get_main_menu(lang))
