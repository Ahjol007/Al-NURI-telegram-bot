from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

MAIN_MENU_KK = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Консультацияға жазылу")],
        [KeyboardButton(text="💊 Өнім туралы ақпарат"), KeyboardButton(text="💰 Өнім бағалары")],
        [KeyboardButton(text="🎥 Тегін видео курстар"), KeyboardButton(text="⭐ Пікір және Кейстер")],
        [KeyboardButton(text="📞 Байланыс")],
    ],
    resize_keyboard=True,
)

MAIN_MENU_RU = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Записаться на консультацию")],
        [KeyboardButton(text="💊 Информация о продукте"), KeyboardButton(text="💰 Цены на продукты")],
        [KeyboardButton(text="🎥 Бесплатные видео курсы"), KeyboardButton(text="⭐ Отзывы и Кейсы")],
        [KeyboardButton(text="📞 Контакты")],
    ],
    resize_keyboard=True,
)


def get_main_menu(lang: str) -> ReplyKeyboardMarkup:
    return MAIN_MENU_KK if lang == "kk" else MAIN_MENU_RU
