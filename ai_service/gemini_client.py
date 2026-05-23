import google.generativeai as genai


async def get_ai_reply(
    message: str,
    history: list[dict],
    lang: str,
    api_key: str,
) -> str:
    from ai_service.prompts import get_system_prompt

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
    response = chat.send_message(message)
    return response.text
