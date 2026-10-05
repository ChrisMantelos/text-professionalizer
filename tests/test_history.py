from history import add_to_history


def test_adds_entry_to_front():
    history = []
    updated = add_to_history(history, "hi", "formal", "Hello.")
    assert len(updated) == 1
    assert updated[0]["original"] == "hi"


def test_newest_entry_is_first():
    history = [{"original": "old", "tone": "formal", "result": "Old."}]
    updated = add_to_history(history, "new", "formal", "New.")
    assert updated[0]["original"] == "new"
    assert updated[1]["original"] == "old"


def test_respects_max_items():
    history = [{"original": f"item{i}", "tone": "formal", "result": "x"} for i in range(5)]
    updated = add_to_history(history, "newest", "formal", "x", max_items=5)
    assert len(updated) == 5
    assert updated[0]["original"] == "newest"
    assert "item4" not in [e["original"] for e in updated]
