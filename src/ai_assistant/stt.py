from speech_recognition import Recognizer, AudioSource, WaitTimeoutError
from speech_recognition.exceptions import SetupError, UnknownValueError

from ai_assistant.config import WAKE_WORD, CONVERSATION_TIMEOUT
from ai_assistant.llm import chat
from ai_assistant.tts import speak

keywords: list[tuple[str, int]] = [(f"{WAKE_WORD}", 1), (f"Hey {WAKE_WORD}", 1)]

def check_wake_word(text: str) -> bool:
    return any(word.lower() in text.lower() for word, _ in keywords)

def remove_wake_word(text: str) -> str:
    return text.lower().replace(WAKE_WORD.lower(), "").strip()

def transcribe(recognizer: Recognizer, audio_source: AudioSource, time_out: int | None) -> str | None:
    try:
        audio = recognizer.listen(audio_source, timeout=time_out, phrase_time_limit=None)
        print("\rReconnaissance...", end="", flush=True)
    except WaitTimeoutError as exc:
        print(f"Silence... retour en veille...: {exc}")
        return None

    try:
        data = recognizer.recognize_vosk(audio)
        print(f"\rEntendu (brut) : {data}")
    except UnknownValueError:
        print("\rAudio incompréhensible")
        return None
    except SetupError as exc:
        print(f"\rModèle Vosk manquant : {exc}")
        return None

    if not data or not data.strip():
        return None

    return data

def respond(text: str, messages: list[dict[str, str]]) -> str | None:
    text = remove_wake_word(text)
    user_message = {"role": "user", "content": text}

    r = chat([*messages, user_message])
    if r is not None:
        messages.append(user_message)
        messages.append({"role": "assistant", "content": r})
        return r
    else:
        return None


def recognize(recognizer: Recognizer, audio_source: AudioSource, messages: list[dict[str, str]]):
    data = transcribe(recognizer, audio_source)
    if data is not None:
        if check_wake_word(data):
            r = respond(data, messages)
            if r is not None:
                speak(r)