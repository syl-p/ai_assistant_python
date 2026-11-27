import pyttsx3 # to speek

def speak(text: str):
    rate = 150
    engine = pyttsx3.init()
    voices = engine.getProperty('voices') or []
    voice_id = None
    for voice in voices:
        langs = " ".join(str(lang) for lang in getattr(voice, "languages", [])).lower()
        if "fr" in langs:
            voice_id = voice.id
            break
    if voice_id is None and voices:
        voice_id = voices[0].id
    if voice_id:
        engine.setProperty("voice", voice_id)

    engine.setProperty('rate', rate + 50)
    engine.say(text)
    engine.runAndWait()
