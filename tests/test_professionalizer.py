from unittest.mock import patch, MagicMock
import pytest

from professionalizer import professionalize, ProfessionalizerError


def fake_response(text: str) -> MagicMock:
    response = MagicMock()
    response.content = [MagicMock(text=text)]
    return response


def test_empty_text_raises():
    with pytest.raises(ProfessionalizerError):
        professionalize("", tone="formal", api_key="fake-key")


def test_invalid_tone_raises():
    with pytest.raises(ProfessionalizerError):
        professionalize("hello", tone="sarcastic", api_key="fake-key")


def test_missing_key_raises(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(ProfessionalizerError):
        professionalize("hello there", tone="formal", api_key=None)


@patch("professionalizer.Anthropic")
def test_successful_call_returns_text(mock_anthropic_cls):
    mock_client = mock_anthropic_cls.return_value
    mock_client.messages.create.return_value = fake_response("I am writing to inform you.")

    result = professionalize("hey sorry im late", tone="formal", api_key="fake-key")

    assert result == "I am writing to inform you."
    mock_client.messages.create.assert_called_once()


@patch("professionalizer.Anthropic")
def test_sends_correct_tone_prompt(mock_anthropic_cls):
    mock_client = mock_anthropic_cls.return_value
    mock_client.messages.create.return_value = fake_response("Short version.")

    professionalize("this is a long message", tone="concise", api_key="fake-key")

    _, kwargs = mock_client.messages.create.call_args
    assert "short, direct" in kwargs["system"]
    assert kwargs["messages"][0]["content"] == "this is a long message"


@patch("professionalizer.Anthropic")
def test_api_error_is_wrapped(mock_anthropic_cls):
    from anthropic import APIConnectionError

    mock_client = mock_anthropic_cls.return_value
    mock_client.messages.create.side_effect = APIConnectionError(request=MagicMock())

    with pytest.raises(ProfessionalizerError, match="Could not connect"):
        professionalize("hello", tone="formal", api_key="fake-key")


@patch("professionalizer.Anthropic")
def test_result_is_stripped_of_whitespace(mock_anthropic_cls):
    mock_client = mock_anthropic_cls.return_value
    mock_client.messages.create.return_value = fake_response("  spaced out text  \n")

    result = professionalize("hi", tone="formal", api_key="fake-key")

    assert result == "spaced out text"
