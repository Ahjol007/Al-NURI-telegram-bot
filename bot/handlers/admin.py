import asyncio
import logging

import httpx
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings

router = Router()
logger = logging.getLogger(__name__)


async def _get_stats(session: AsyncSession) -> dict:
    total_users = await session.scalar(select(func.count()).select_from(text("users")))
    new_consults = await session.scalar(
        select(func.count()).select_from(text("consultations")).where(text("status = 'new'"))
    )
    return {"total_users": total_users or 0, "new_consultations": new_consults or 0}


async def _get_recent_users(session: AsyncSession) -> list[dict]:
    result = await session.execute(
        text("SELECT first_name, username, created_at FROM users ORDER BY created_at DESC LIMIT 10")
    )
    return [dict(row._mapping) for row in result]


async def _get_new_consultations(session: AsyncSession) -> list[dict]:
    result = await session.execute(
        text("SELECT id, age, symptoms FROM consultations WHERE status = 'new' ORDER BY created_at DESC")
    )
    return [dict(row._mapping) for row in result]


async def _get_all_telegram_ids(session: AsyncSession) -> list[int]:
    result = await session.execute(text("SELECT telegram_id FROM users"))
    return [row[0] for row in result]


async def _broadcast(bot_token: str, telegram_ids: list[int], text_msg: str) -> int:
    sent = 0
    async with httpx.AsyncClient(timeout=10.0) as client:
        for tg_id in telegram_ids:
            try:
                resp = await client.post(
                    f"https://api.telegram.org/bot{bot_token}/sendMessage",
                    json={"chat_id": tg_id, "text": text_msg},
                )
                if resp.status_code == 200:
                    sent += 1
                elif resp.status_code == 429:
                    await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"Broadcast error for {tg_id}: {e}")
            await asyncio.sleep(0.05)
    return sent


def _is_admin(message: Message) -> bool:
    return message.from_user and message.from_user.id == settings.admin_telegram_id


@router.message(Command("admin_help"))
async def cmd_admin_help(message: Message):
    if not _is_admin(message):
        return
    await message.answer(
        "Admin командалары:\n"
        "/admin_stats — Статистика\n"
        "/admin_users — Соңғы 10 пайдаланушы\n"
        "/admin_consults — Жаңа өтінімдер\n"
        "/admin_broadcast мәтін — Барлығына жіберу"
    )


@router.message(Command("admin_stats"))
async def cmd_admin_stats(message: Message, session: AsyncSession):
    if not _is_admin(message):
        return
    stats = await _get_stats(session)
    await message.answer(
        f"📊 Статистика:\n"
        f"Пайдаланушылар: {stats['total_users']}\n"
        f"Жаңа өтінімдер: {stats['new_consultations']}"
    )


@router.message(Command("admin_users"))
async def cmd_admin_users(message: Message, session: AsyncSession):
    if not _is_admin(message):
        return
    users = await _get_recent_users(session)
    if not users:
        await message.answer("Пайдаланушылар жоқ.")
        return
    lines = []
    for u in users:
        name = u["first_name"] or "N/A"
        uname = f"@{u['username']}" if u["username"] else "N/A"
        date = u["created_at"].strftime("%d.%m.%Y") if u["created_at"] else "N/A"
        lines.append(f"{name} ({uname}) — {date}")
    await message.answer("👥 Соңғы 10 пайдаланушы:\n" + "\n".join(lines))


@router.message(Command("admin_consults"))
async def cmd_admin_consults(message: Message, session: AsyncSession):
    if not _is_admin(message):
        return
    consults = await _get_new_consultations(session)
    if not consults:
        await message.answer("Жаңа өтінім жоқ.")
        return
    lines = []
    for c in consults:
        symptoms = (c["symptoms"] or "N/A")[:50]
        lines.append(f"#{c['id']} | {c['age'] or 'N/A'} жас | {symptoms}")
    await message.answer("📋 Жаңа өтінімдер:\n" + "\n".join(lines))


@router.message(Command("admin_broadcast"))
async def cmd_admin_broadcast(message: Message, session: AsyncSession):
    if not _is_admin(message):
        return
    broadcast_text = message.text[len("/admin_broadcast"):].strip()
    if not broadcast_text:
        await message.answer("Мәтін енгізіңіз: /admin_broadcast <мәтін>")
        return
    telegram_ids = await _get_all_telegram_ids(session)
    await message.answer(f"Рассылка басталды ({len(telegram_ids)} пайдаланушы)...")
    count = await _broadcast(settings.bot_token, telegram_ids, broadcast_text)
    await message.answer(f"✅ Рассылка аяқталды: {count} пайдаланушыға жіберілді")
