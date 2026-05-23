from aiogram import Router, F
from aiogram.types import Message, LinkPreviewOptions

router = Router()

PRICES_KK = (
    "💰 *Өнім бағалары*\n\n"
    "🌿 *Al-Nuri Фитогель:*\n"
    "• 1 шт: 50 000 тг\n"
    "• 2 шт: 85 500 тг\n"
    "• 3 шт: 110 500 тг\n"
    "• 4 шт: 125 000 тг\n"
    "• 5 шт: 145 000 тг\n"
    "• 6 шт: 170 500 тг\n"
    "• 7 шт: 198 500 тг\n"
    "• 8 шт: 227 500 тг\n\n"
    "⚫ *Black Kinger (Қара имбирь):*\n"
    "• 1 шт: 15 000 тг\n"
    "• 2 шт: 28 000 тг\n"
    "• 3 шт: 42 000 тг\n"
    "• 4 шт: 55 500 тг\n"
    "• 5 шт: 66 000 тг\n"
    "• 6 шт: 74 000 тг\n"
    "• 7 шт: 86 000 тг\n"
    "• 8 шт: 98 000 тг\n\n"
    "💊 *Био Лайф:* 24 990 тг\n"
    "💪 *Master Gel:* 19 990 тг\n"
    "🕯 *Свеча:* 19 990 тг\n\n"
    "Тапсырыс беру үшін: [WhatsApp](https://wa.me/77778151988)"
)

PRICES_RU = (
    "💰 *Цены на продукты*\n\n"
    "🌿 *Al-Nuri Фитогель:*\n"
    "• 1 шт: 50 000 тг\n"
    "• 2 шт: 85 500 тг\n"
    "• 3 шт: 110 500 тг\n"
    "• 4 шт: 125 000 тг\n"
    "• 5 шт: 145 000 тг\n"
    "• 6 шт: 170 500 тг\n"
    "• 7 шт: 198 500 тг\n"
    "• 8 шт: 227 500 тг\n\n"
    "⚫ *Black Kinger (Чёрный имбирь):*\n"
    "• 1 шт: 15 000 тг\n"
    "• 2 шт: 28 000 тг\n"
    "• 3 шт: 42 000 тг\n"
    "• 4 шт: 55 500 тг\n"
    "• 5 шт: 66 000 тг\n"
    "• 6 шт: 74 000 тг\n"
    "• 7 шт: 86 000 тг\n"
    "• 8 шт: 98 000 тг\n\n"
    "💊 *Био Лайф:* 24 990 тг\n"
    "💪 *Master Gel:* 19 990 тг\n"
    "🕯 *Свеча:* 19 990 тг\n\n"
    "Для заказа: [WhatsApp](https://wa.me/77778151988)"
)

PRICE_BUTTONS = {"💰 Өнім бағалары", "💰 Цены на продукты"}


@router.message(F.text.in_(PRICE_BUTTONS))
async def show_prices(message: Message, lang: str):
    text = PRICES_KK if lang == "kk" else PRICES_RU
    await message.answer(text, parse_mode="Markdown", link_preview_options=LinkPreviewOptions(is_disabled=True))
