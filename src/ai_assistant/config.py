INTERNET_ENABLED = False
LAN_ENABLED = False
WAKE_WORD = "Jarvis"
MODEL_PATH =  "modeles/vosk-fr"
SAMPLE_RATE = 16000
OLLAMA_BASE_URL = "http://127.0.0.1:11434"
OLLAMA_MODEL = "qwen2.5:1.5b"
TIME_OUT = 30
SYSTEM_PROMPT=("Ton nom est Jarvis, assistant vocal local, poli et concis. "
               "Ton ton : calme, un brin d’ironie, vouvoie l’utilisateur. "
               "Réponds en moins de 3 phrases. "
               "Réponses faites pour être dites à voix haute : pas de markdown, pas de listes longues. ")
CONVERSATION_TIMEOUT = 3