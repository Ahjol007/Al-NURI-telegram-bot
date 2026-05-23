from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from models import Consultation, User
from keyboards.main_menu import get_main_menu

router = Router()


class ConsultationStates(StatesGroup):
    AGE = State()
    HEIGHT_WEIGHT = State()
    SYMPTOMS = State()
    DURATION = State()
    PREVIOUS = State()


TEXTS = {
    "kk": {
        "intro": (
            "Ассалаумағалейкум! Қалыңыз қалай 👋\n\n"
            "Сіз тегін консультацияға өтініш қалдырдыңыз.\n\n"
            "Біздің маман сізге:\n"
            "✅ Простатит\n✅ Аденома\n✅ Еркектік әлсіздік\n"
            "✅ Тестостерон төмендеуі сияқты мәселелер бойынша ақпарат береді.\n\n"
            "Консультация толық құпия түрде жүргізіледі. 🔒\n\n"
            "Жасыңыз қаншада?"
        ),
        "ask_hw": "Бой, салмағыңыз неше?",
        "ask_symptoms": "Қандай белгілер мазалайды?",
        "ask_duration": "Бұл мәселе қашаннан бері бар?",
        "ask_previous": "Бұрын ем қабылдадыңыз ба?",
        "done": (
            "✅ Рахмет! Өтінішіңіз қабылданды.\n\n"
            "Маман сізбен жақын арада байланысады.\n"
            "WhatsApp арқылы да жаза аласыз: https://wa.me/77778151988"
        ),
    },
    "ru": {
        "intro": (
            "Ассаламу алейкум! Как дела? 👋\n\n"
            "Вы оставили заявку на бесплатную консультацию.\n\n"
            "Наш специалист проконсультирует вас по:\n"
            "✅ Простатит\n✅ Аденома\n✅ Мужская слабость\n"
            "✅ Снижение тестостерона и другим проблемам.\n\n"
            "Консультация полностью конфиденциальна. 🔒\n\n"
            "Сколько вам лет?"
        ),
        "ask_hw": "Какой у вас рост и вес?",
        "ask_symptoms": "Какие симптомы вас беспокоят?",
        "ask_duration": "Как давно существует эта проблема?",
        "ask_previous": "Вы ранее проходили лечение?",
        "done": (
            "✅ Спасибо! Ваша заявка принята.\n\n"
            "Специалист свяжется с вами в ближайшее время.\n"
            "Также можете написать в WhatsApp: https://wa.me/77778151988"
        ),
    },
}

CONSULTATION_BUTTONS = {"📋 Консультацияға жазылу", "📋 Записаться на консультацию"}


@router.message(F.text.in_(CONSULTATION_BUTTONS))
async def start_consultation(message: Message, state: FSMContext, lang: str):
    await state.set_state(ConsultationStates.AGE)
    await state.update_data(lang=lang)
    await message.answer(TEXTS[lang]["intro"], reply_markup=ReplyKeyboardRemove())


@router.message(ConsultationStates.AGE)
async def process_age(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await state.update_data(age=message.text)
    await state.set_state(ConsultationStates.HEIGHT_WEIGHT)
    await message.answer(TEXTS[lang]["ask_hw"])


@router.message(ConsultationStates.HEIGHT_WEIGHT)
async def process_hw(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await state.update_data(height_weight=message.text)
    await state.set_state(ConsultationStates.SYMPTOMS)
    await message.answer(TEXTS[lang]["ask_symptoms"])


@router.message(ConsultationStates.SYMPTOMS)
async def process_symptoms(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await state.update_data(symptoms=message.text)
    await state.set_state(ConsultationStates.DURATION)
    await message.answer(TEXTS[lang]["ask_duration"])


@router.message(ConsultationStates.DURATION)
async def process_duration(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await state.update_data(duration=message.text)
    await state.set_state(ConsultationStates.PREVIOUS)
    await message.answer(TEXTS[lang]["ask_previous"])


@router.message(ConsultationStates.PREVIOUS)
async def process_previous(message: Message, state: FSMContext, session: AsyncSession, db_user: User):
    data = await state.get_data()
    lang = data.get("lang", "ru")

    consultation = Consultation(
        user_id=db_user.id,
        age=data.get("age"),
        height_weight=data.get("height_weight"),
        symptoms=data.get("symptoms"),
        duration=data.get("duration"),
        previous_treatment=message.text,
        status="new",
    )
    session.add(consultation)
    await session.commit()
    await message.answer(TEXTS[lang]["done"], reply_markup=get_main_menu(lang))
    await state.clear()
