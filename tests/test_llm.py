from ai_assistant.llm import chat

def test_check_llm_history():
    messages = [{"role": "user", "content": "Je m'appelle Sylvain."}]
    r1 = chat(messages)
    assert r1 is not None
    if r1:
        messages.append({"role": "assistant", "content": r1})

    messages.append({"role": "user", "content": "Comment je m'appelle ?"})
    r2 = chat(messages)
    assert r2 is not None
    assert "Sylvain" in r2