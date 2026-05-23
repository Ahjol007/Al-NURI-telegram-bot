import asyncio
import logging

import httpx

logger = logging.getLogger(__name__)


async def broadcast_message(bot_token: str, telegram_ids: list[int], text: str) -> int:
    sent = 0
    async with httpx.AsyncClient(timeout=10.0) as client:
        for tg_id in telegram_ids:
            try:
                resp = await client.post(
                    f"https://api.telegram.org/bot{bot_token}/sendMessage",
                    json={"chat_id": tg_id, "text": text},
                )
                if resp.status_code == 200:
                    sent += 1
                await asyncio.sleep(0.05)
            except Exception as e:
                logger.warning(f"Failed to send to {tg_id}: {e}")
    return sent
