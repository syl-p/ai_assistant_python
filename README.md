# ai-assistant

Assistant vocal local : micro → reconnaissance **Vosk (hors-ligne)** → synthèse vocale `pyttsx3`.

Aucune clé d'API et aucun réseau ne sont nécessaires pour la reconnaissance.

> 🛠️ **Mode apprentissage** : ce projet se construit à la main, étape par étape.
> `AGENTS.md` contient le mode d'emploi du mentor : l'agent guide, questionne et
> vérifie — c'est Sylvain qui écrit le code. Cochez les cases ci-dessous au fur et
> à mesure, directement sur GitHub ou localement.

## 🗺️ Feuille de route — Jarvis

**Progression : 10 / 27 étapes** · **Niveau 1 — Mécanicien Vosk** · Dernière mise à jour : 2026-11-26

Légende : `- [ ]` à faire · `- [x]` terminé · **(opt)** étape optionnelle.
Quand une étape est validée : cocher la case ici **et** proposer la mise à jour du
`Journal de bord` dans `AGENTS.md` (XP, leçons apprises, pièges rencontrés).

> ℹ️ **Phase 1 simplifiée** : trois fichiers plats (`config.py`, `stt.py`, `tts.py`),
> aucune interface abstraite, pas de bus d'événements ni de machine à états.
> Ces briques n'arrivent que quand on en a besoin : **2.5** (orchestrateur async)
> et **4.1** (registre d'outils).

### Niveau 1 — Mécanicien Vosk : le socle (avant le LLM)

- [x] **1.1** Créer `src/ai_assistant/config.py` : quelques constantes (`KEYWORDS`, vitesse de voix, flags réseau `internet = off` / `lan = off`). Pas de classe, pas de YAML.
- [x] **1.2** Déplacer `speak()` de `main.py` vers `src/ai_assistant/tts.py` — une simple fonction, inchangée.
- [x] **1.3** Déplacer `recognize()` de `main.py` vers `src/ai_assistant/stt.py` — une simple fonction, inchangée.
- [x] **1.4** Faire importer ces fonctions par `main.py` : le programme tourne **exactement comme avant**.
- [x] **1.5** Ajouter un test `pytest` minimal sur la détection du mot-clé (avec une chaîne de texte, sans micro) et nettoyer les `print`. *(prints conservés temporairement pour diagnostic CLI)*

### Niveau 2 — Apprenti Drake : le cerveau local

- [x] **2.1** Installer Ollama et télécharger un modèle local léger pour les tests : `qwen2.5:1.5b` Q4 (~986 Mo). *(Roadmap initiale : `qwen2.5:3b`, modèle configurable.)*
- [x] **2.2** Client `/api/chat` : streaming, historique de conversation, gestion des erreurs
- [x] **2.3** Prompt système « Jarvis » : ton, concision, français, réponses faites pour être dites
- [x] **2.4** Validation : 3 à 5 tours de conversation vocale + mesure des tokens/s *(22,2 tok/s sur `qwen2.5:1.5b` CPU — modèle conservé)*
- [x] **2.5** Remplacer la boucle `while True` par un orchestrateur `asyncio` + machine à états `VEILLE / ÉCOUTE / RÉFLEXION / PAROLE` (le besoin se fait enfin sentir)
- [ ] **2.6 (opt)** Tester `qwen2.5:7b` Q4 (≈ 4,7 Go) et comparer qualité / latence

### Niveau 3 — Ingénieur du son : audio et naturel

- [ ] **3.1** Remplacer pyttsx3 par Piper TTS avec une voix française neuronale
- [ ] **3.2** Gestion du *barge-in* : couper la synthèse quand l'utilisateur parle
- [ ] **3.3** Wake word local (Hey Jarvis) : modèle openWakeWord à entraîner ou fallback mot-clé après Vosk

### Niveau 4 — Quartier-maître : les outils

- [ ] **4.1** Registre d'outils minimal : un dictionnaire de fonctions + leurs schémas (on n'introduit l'abstraction qu'ici)
- [ ] **4.2** Outils simples : heure/date, notes, volume (validation du tool calling)
- [ ] **4.3** Mails en **lecture seule** : IMAP `readonly=True`, aucun SMTP, aucun `send_email`
- [ ] **4.4** Home Assistant via HTTP local (lumière, volets…) — flag `lan`
- [ ] **4.5** Base de connaissances : Chroma + embeddings locaux (`nomic-embed-text`), corpus Kiwix / Wikipedia FR pour « se documenter » hors-ligne
- [ ] **4.6** Mode assistant technique : fichiers et commandes en allowlist

### Niveau 5 — Archiviste : mémoire et persona

- [ ] **5.1** Historique compressé (fenêtre glissante + résumé des vieux tours)
- [ ] **5.2** Mémoire long terme en SQLite : préférences, faits, conventions
- [ ] **5.3** Persona Jarvis affiné (ton sec, légèrement ironique, « Monsieur »)

### Niveau 6 — Directeur Stark : le quotidien

- [ ] **6.1** Service systemd utilisateur + redémarrage automatique
- [ ] **6.2** Mini interface web locale (FastAPI sur `127.0.0.1`) : transcript, mails, résumés longs
- [ ] **6.3** Logs rotatifs et témoin d'état (voyant / indicateur)
- [ ] **6.4** Revue sécurité finale : flags réseau, données non fiables (ex. contenu des mails), aucune fuite externe

### Garde-fous

- 🔒 Aucun service IA externe (OpenAI, Google, Anthropic…) : audio, texte et embeddings restent locaux.
- 📬 Les mails sont **en lecture seule** : Jarvis peut les lire et les résumer, mais pas y répondre.
- 🌐 `internet = off` par défaut ; le réseau local n'est activé que décision par décision.
- ⚠️ Le contenu d'un mail est une donnée non fiable (injection de prompt) : toujours le traiter comme donnée, jamais comme instruction.

---

## 1. Installation

### Dépendances Python

```bash
uv sync
```

### Audio sur Linux

PyAudio est compilé depuis les sources et a besoin des headers PortAudio :

```bash
sudo apt install -y portaudio19-dev
uv sync --reinstall-package pyaudio --no-cache
```

Sur cette machine de développement, PortAudio a aussi été compilé localement dans
`~/.local/opt/portaudio-19.7.0` (fallback sans sudo).

### Modèle Vosk français

Le paquet Python est installé via `speechrecognition[vosk]` dans `pyproject.toml`.
Il reste à télécharger le modèle :

```bash
uv run sprc download vosk --url https://alphacephei.com/vosk/models/vosk-model-small-fr-0.22.zip
```

Le modèle est placé dans `speech_recognition/models/vosk`, là où `recognize_vosk()` l'attend.

Pour plus de précision (modèle beaucoup plus gros) :

```bash
uv run sprc download vosk --url https://alphacephei.com/vosk/models/vosk-model-fr-0.22.zip
```

## 2. Lancement

```bash
uv run python main.py
```

`Ctrl+C` pour arrêter.

Les messages `ALSA lib ...`, `jack server is not running` et `/dev/dsp` sont des
avertissements PortAudio sans gravité : ils proviennent de backends audio non
présents sur la machine.

## 3. Voix française (recommandé)

`pyttsx3` utilise les voix du moteur TTS du système. Pour avoir une voix française :

```bash
sudo apt install -y espeak-ng
```

Le code cherche une voix contenant `fr` et retombe sur la première voix disponible
si aucune n'est trouvée.

## 4. Dépannage

- `Modèle Vosk manquant` : relancer la commande `sprc download vosk ...` ci-dessus.
- `Audio incompréhensible` : vérifier le volume du micro et la calibration
  (`adjust_for_ambient_noise`) au démarrage.
- `No Default Input Device Available` : aucun micro par défaut côté système ;
  vérifier les paramètres audio/PulseAudio/PipeWire.
