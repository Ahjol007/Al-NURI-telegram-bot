from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def get_stats(session: AsyncSession) -> dict:
    total_users = await session.scalar(text("SELECT COUNT(*) FROM users"))
    new_consults = await session.scalar(
        text("SELECT COUNT(*) FROM consultations WHERE status = 'new'")
    )
    return {"total_users": total_users or 0, "new_consultations": new_consults or 0}


async def get_recent_users(session: AsyncSession, limit: int = 10) -> list[dict]:
    result = await session.execute(
        text("SELECT first_name, username, created_at FROM users ORDER BY created_at DESC LIMIT :limit"),
        {"limit": limit},
    )
    rows = result.fetchall()
    return [{"first_name": r[0], "username": r[1], "created_at": r[2]} for r in rows]


async def get_new_consultations(session: AsyncSession) -> list[dict]:
    result = await session.execute(
        text(
            "SELECT id, age, symptoms, created_at FROM consultations "
            "WHERE status = 'new' ORDER BY created_at DESC"
        )
    )
    rows = result.fetchall()
    return [{"id": r[0], "age": r[1], "symptoms": r[2], "created_at": r[3]} for r in rows]


async def get_all_user_telegram_ids(session: AsyncSession) -> list[int]:
    result = await session.execute(text("SELECT telegram_id FROM users"))
    return [row[0] for row in result.fetchall()]
