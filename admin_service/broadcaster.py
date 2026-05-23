import asyncio
import logging

import httpx

logger = logging.getLogger(__name__)


async def broadcast_message(bot_token: str, telegram_ids: list[int], text: str) -> int:
    sent = 0
    async with httpx.AsyncClient(timeout=10.0) as client:
        for tg_id in telegram_ids:
            while True:
                try:
                    resp = await client.post(
                        f"https://api.telegram.org/bot{bot_token}/sendMessage",
                        json={"chat_id": tg_id, "text": text},
                    )
                    if resp.status_code == 429:
                        retry_after = resp.json().get("parameters", {}).get("retry_after", 5)
                        logger.warning(f"Rate limited, sleeping {retry_after}s")
                        await asyncio.sleep(retry_after)
                        continue
                    if resp.status_code == 200:
                        sent += 1
                    break
                except Exception as e:
                    logger.warning(f"Failed to send to {tg_id}: {e}")
                    break
            await asyncio.sleep(0.05)
    return sent
