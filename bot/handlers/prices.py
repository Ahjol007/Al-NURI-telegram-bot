from aiogram import Router, F
from aiogram.types import Message, LinkPreviewOptions

router = Router()

PRICES_KK = (
    "💰 <b>Өнім бағалары</b>\n\n"
    "🌿 <b>Al-Nuri Фитогель:</b>\n"
    "• 1 шт: 50 000 тг\n"
    "• 2 шт: 85 500 тг\n"
    "• 3 шт: 110 500 тг\n"
    "• 4 шт: 125 000 тг\n"
    "• 5 шт: 145 000 тг\n"
    "• 6 шт: 170 500 тг\n"
    "• 7 шт: 198 500 тг\n"
    "• 8 шт: 227 500 тг\n\n"
    "⚫ <b>Black Kinger (Қара имбирь):</b>\n"
    "• 1 шт: 15 000 тг\n"
    "• 2 шт: 28 000 тг\n"
    "• 3 шт: 42 000 тг\n"
    "• 4 шт: 55 500 тг\n"
    "• 5 шт: 66 000 тг\n"
    "• 6 шт: 74 000 тг\n"
    "• 7 шт: 86 000 тг\n"
    "• 8 шт: 98 000 тг\n\n"
    "💊 <b>Био Лайф:</b> 24 990 тг\n"
    "💪 <b>Master Gel:</b> 19 990 тг\n"
    "🕯 <b>Свеча:</b> 19 990 тг\n\n"
    'Тапсырыс беру үшін: <a href="https://wa.me/77778151988">WhatsApp</a>'
)

PRICES_RU = (
    "💰 <b>Цены на продукты</b>\n\n"
    "🌿 <b>Al-Nuri Фитогель:</b>\n"
    "• 1 шт: 50 000 тг\n"
    "• 2 шт: 85 500 тг\n"
    "• 3 шт: 110 500 тг\n"
    "• 4 шт: 125 000 тг\n"
    "• 5 шт: 145 000 тг\n"
    "• 6 шт: 170 500 тг\n"
    "• 7 шт: 198 500 тг\n"
    "• 8 шт: 227 500 тг\n\n"
    "⚫ <b>Black Kinger (Чёрный имбирь):</b>\n"
    "• 1 шт: 15 000 тг\n"
    "• 2 шт: 28 000 тг\n"
    "• 3 шт: 42 000 тг\n"
    "• 4 шт: 55 500 тг\n"
    "• 5 шт: 66 000 тг\n"
    "• 6 шт: 74 000 тг\n"
    "• 7 шт: 86 000 тг\n"
    "• 8 шт: 98 000 тг\n\n"
    "💊 <b>Био Лайф:</b> 24 990 тг\n"
    "💪 <b>Master Gel:</b> 19 990 тг\n"
    "🕯 <b>Свеча:</b> 19 990 тг\n\n"
    'Для заказа: <a href="https://wa.me/77778151988">WhatsApp</a>'
)

PRICE_BUTTONS = {"💰 Өнім бағалары", "💰 Цены на продукты"}


@router.message(F.text.in_(PRICE_BUTTONS))
async def show_prices(message: Message, lang: str):
    text = PRICES_KK if lang == "kk" else PRICES_RU
    await message.answer(text, link_preview_options=LinkPreviewOptions(is_disabled=True))
