from aiogram import Router, F
from aiogram.types import Message, LinkPreviewOptions

router = Router()

CONTACT_KK = (
    "📞 <b>Байланыс</b>\n\n"
    "💬 WhatsApp: https://wa.me/77058712377\n"
    "📸 Instagram: https://www.instagram.com/al_nuri_kz\n"
    "🎵 TikTok: https://www.tiktok.com/@alnuri.kz"
)

CONTACT_RU = (
    "📞 <b>Контакты</b>\n\n"
    "💬 WhatsApp: https://wa.me/77058712377\n"
    "📸 Instagram: https://www.instagram.com/al_nuri_kz\n"
    "🎵 TikTok: https://www.tiktok.com/@alnuri.kz"
)

CONTACT_BUTTONS = {"📞 Байланыс", "📞 Контакты"}


@router.message(F.text.in_(CONTACT_BUTTONS))
async def show_contact(message: Message, lang: str):
    text = CONTACT_KK if lang == "kk" else CONTACT_RU
    await message.answer(text, parse_mode="HTML", link_preview_options=LinkPreviewOptions(is_disabled=True))
