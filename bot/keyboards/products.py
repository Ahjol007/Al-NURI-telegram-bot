from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

PRODUCTS_KK = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🌿 ФИТОГЕЛЬ", callback_data="product_fitogel")],
    [InlineKeyboardButton(text="⚫ Black Kinger (Қара имбирь)", callback_data="product_black_kinger")],
    [InlineKeyboardButton(text="💊 BIO LIFE", callback_data="product_bio_life")],
    [InlineKeyboardButton(text="💪 MASTER GEL", callback_data="product_master_gel")],
    [InlineKeyboardButton(text="🕯 AL-NURI свеча", callback_data="product_svecha")],
])

PRODUCTS_RU = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🌿 ФИТОГЕЛЬ", callback_data="product_fitogel")],
    [InlineKeyboardButton(text="⚫ Black Kinger (Чёрный имбирь)", callback_data="product_black_kinger")],
    [InlineKeyboardButton(text="💊 BIO LIFE", callback_data="product_bio_life")],
    [InlineKeyboardButton(text="💪 MASTER GEL", callback_data="product_master_gel")],
    [InlineKeyboardButton(text="🕯 AL-NURI свеча", callback_data="product_svecha")],
])


def get_products_keyboard(lang: str) -> InlineKeyboardMarkup:
    return PRODUCTS_KK if lang == "kk" else PRODUCTS_RU
