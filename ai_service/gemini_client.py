import asyncio

import google.generativeai as genai
from fastapi import HTTPException

from prompts import get_system_prompt


async def get_ai_reply(
    message: str,
    history: list[dict],
    lang: str,
    api_key: str,
) -> str:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=get_system_prompt(lang),
    )

    chat_history = []
    for msg in history[-10:]:
        role = "user" if msg.get("direction") == "in" else "model"
        chat_history.append({"role": role, "parts": [msg.get("text", "")]})

    chat = model.start_chat(history=chat_history)
    try:
        response = await asyncio.to_thread(
            chat.send_message,
            message,
            request_options={"timeout": 30},
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Gemini API error: {e}")
    return response.text
