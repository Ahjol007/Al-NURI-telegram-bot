from aiogram import Router, F
from aiogram.types import Message

router = Router()

VIDEO_KK = "🎥 Видео курстар жақын арада қосылады! Күтіңіз."
VIDEO_RU = "🎥 Видео курсы скоро будут добавлены! Ожидайте."

VIDEO_BUTTONS = {"🎥 Тегін видео курстар", "🎥 Бесплатные видео курсы"}


@router.message(F.text.in_(VIDEO_BUTTONS))
async def handle_video(message: Message, lang: str):
    text = VIDEO_KK if lang == "kk" else VIDEO_RU
    await message.answer(text)
