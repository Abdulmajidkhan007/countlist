"""Voice message to expense via OpenAI Whisper."""
import io
from typing import Optional

import aiohttp

from bot.config import settings


async def transcribe_voice(file_bytes: bytes, file_name: str = "voice.ogg") -> Optional[str]:
    if not settings.openai_api_key:
        return None

    try:
        import openai
        client = openai.AsyncOpenAI(api_key=settings.openai_api_key)
        audio_file = io.BytesIO(file_bytes)
        audio_file.name = file_name

        transcript = await client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language="uz",
        )
        return transcript.text
    except Exception:
        return None
