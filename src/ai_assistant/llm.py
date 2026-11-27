import json

import httpx

from ai_assistant.config import OLLAMA_BASE_URL, OLLAMA_MODEL, TIME_OUT, SYSTEM_PROMPT


def load_system_prompt(messages: list[dict]) -> list[dict]:
    payload = [{"role": "system", "content": SYSTEM_PROMPT}, *messages]
    return payload

def chat_stream(messages: list[dict]) -> str | None:
    messages = load_system_prompt(messages)
    parts = []
    try:
        with httpx.stream(
                "POST", f"{OLLAMA_BASE_URL}/api/chat", json={
                    "model": OLLAMA_MODEL, "messages": messages, "stream": True
                }, timeout=TIME_OUT) as r:
            r.raise_for_status()
            for line in r.iter_lines():
                if not line:
                    continue
                chunk = json.loads(line)
                piece = chunk.get("message", {}).get("content", "")
                print(piece, end="", flush=True)
                parts.append(piece)
                if chunk.get("done"):
                    break
            return "".join(parts)
    except httpx.ConnectError as e:
        print(f"Httpx Connect Error: {e}")
    except httpx.TimeoutException as e:
        print(f"Httpx Timeout: {e}")
    except httpx.HTTPStatusError as e:
        print(f"Httpx HTTPError: {e}")
    except httpx.RequestError as e:
        print(f"Httpx Request Error: {e}")



def chat(messages: list[dict]) -> str | None:
    messages = load_system_prompt(messages)
    try:
        r = httpx.post(f"{OLLAMA_BASE_URL}/api/chat", json={
            "model": OLLAMA_MODEL,
            "messages": messages,
            "stream": False
        }, timeout=TIME_OUT)

        r.raise_for_status()

        return r.json()["message"]["content"]
    except httpx.ConnectError as e:
        print(f"Httpx Connect Error: {e}")
    except httpx.TimeoutException as e:
        print(f"Httpx Timeout: {e}")
    except httpx.HTTPStatusError as e:
        print(f"Httpx HTTPError: {e}")
    except httpx.RequestError as e:
        print(f"Httpx Request Error: {e}")