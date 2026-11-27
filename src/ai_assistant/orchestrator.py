import asyncio
import time
from enum import Enum

from ai_assistant.config import CONVERSATION_TIMEOUT
from ai_assistant.stt import transcribe, respond, check_wake_word

import speech_recognition as sr

from ai_assistant.tts import speak


class State(Enum):
    VEILLE="Veille"
    ECOUTE="Ecoute"
    REFLEXION="Reflexion"
    PAROLE="Parole"

async def start_orchestrator(r: sr.Recognizer, source: sr.AudioSource, messages: list[dict]):
    state = State.VEILLE
    text: str = ""

    while True:
        if state in (State.VEILLE, State.ECOUTE):
            time_out = CONVERSATION_TIMEOUT if state is State.ECOUTE else None
            data = await asyncio.to_thread(transcribe, r, source, time_out)

            if data is None:
                if state is State.ECOUTE:
                    state = State.VEILLE
                continue

            if state is State.VEILLE and not check_wake_word(data):
                continue

            # REFLEXION ZONE
            text = data
            state = State.REFLEXION
            print(f"Reflexion à propos de '{text}'...")

        elif state is State.REFLEXION:
            reply = await asyncio.to_thread(respond, text, messages)
            state = State.PAROLE if reply else State.VEILLE
        else:
            # PAROLE Zone
            await asyncio.to_thread(speak, reply)
            print("Parle et passe à nouveau en mode écoute...")
            state = State.ECOUTE
