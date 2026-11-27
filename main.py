import asyncio

import speech_recognition as sr # to recognize

from ai_assistant.orchestrator import start_orchestrator

r = sr.Recognizer()
messages: list[dict[str, str]] = []

try:
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        r.energy_threshold = 10000

        print("Écoute... (Ctrl+C pour arrêter)")
        asyncio.run(start_orchestrator(r, source, messages))
except KeyboardInterrupt:
    print("Au revoir monsieur.")