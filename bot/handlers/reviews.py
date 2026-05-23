from aiogram import Router, F
from aiogram.types import Message

router = Router()

REVIEWS_KK = (
    "⭐ *Пікірлер және Кейстер*\n\n"
    "👶 Бала мәселесі жайлы:\n"
    "https://www.instagram.com/reel/DRMHyWGDI44/\n\n"
    "💊 Өнім туралы:\n"
    "https://www.instagram.com/reel/DE93mWcIw0o/\n\n"
    "💊 Өнім туралы:\n"
    "https://www.instagram.com/reel/DEpCX8zsyTM/"
)

REVIEWS_RU = (
    "⭐ *Отзывы и Кейсы*\n\n"
    "👶 О детском вопросе:\n"
    "https://www.instagram.com/reel/DRMHyWGDI44/\n\n"
    "💊 О продукте:\n"
    "https://www.instagram.com/reel/DE93mWcIw0o/\n\n"
    "💊 О продукте:\n"
    "https://www.instagram.com/reel/DEpCX8zsyTM/"
)

REVIEWS_BUTTONS = {"⭐ Пікір және Кейстер", "⭐ Отзывы и Кейсы"}


@router.message(F.text.in_(REVIEWS_BUTTONS))
async def show_reviews(message: Message, lang: str):
    text = REVIEWS_KK if lang == "kk" else REVIEWS_RU
    await message.answer(text, parse_mode="Markdown")
