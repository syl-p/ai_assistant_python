from ai_assistant.config import WAKE_WORD
from ai_assistant.stt import check_wake_word

def test_check_wake_word():
    assert check_wake_word(f"Hey {WAKE_WORD}")
    assert check_wake_word(f"Hey {WAKE_WORD.lower()}")
    assert check_wake_word(WAKE_WORD)
    assert not check_wake_word("Hey")