# Text Professionalizer

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B)
![Anthropic API](https://img.shields.io/badge/powered%20by-Anthropic%20API-D97757)
![Tests](https://img.shields.io/badge/tests-pytest-0A9EDC)

Converts informal draft text into clear, professional communication -
available both as a CLI tool and a web app.

Live demo: [text-professionalizer-cm5su4jbqzwfcevd9p6vjk.streamlit.app](https://text-professionalizer-cm5su4jbqzwfcevd9p6vjk.streamlit.app)

## Why I built this

I wanted a quick way to turn rushed messages (emails, Slack, notes) into
something I could confidently send to a client or manager, without
rewriting them by hand every time.

## Features

- Three communication tones: formal, friendly, concise
- Language-aware: Greek input stays Greek, English input stays English
- Two interfaces: CLI for quick terminal use, web UI for a visual experience
- Recent conversions history in the web app (kept for the current session, not saved to disk)
- Proper error handling: clear messages for empty input, invalid tone, or connection issues
- Logic and UI are separated: `professionalizer.py` is a standalone module

## Example

Input:
```
hey, just wanted to let you know the report is delayed a bit, will send it over later today, sorry
```

Output (formal):
```
I am writing to inform you that the report has been slightly delayed.
I will forward it to you later today. Thank you for your understanding.
```

## Installation

```bash
git clone https://github.com/ChrisMantelos/text-professionalizer.git
cd text-professionalizer
pip install -r requirements.txt
```

Add your API key (create one at console.anthropic.com):

```bash
cp .env.example .env
# open .env and set: ANTHROPIC_API_KEY=sk-ant-...
```

## Usage

CLI:
```bash
python main.py
```

Web UI:
```bash
streamlit run app.py
```

## Project structure

```
text-professionalizer/
    professionalizer.py   core logic: API call, prompts, error handling
    history.py             session history helper, used by the web app
    main.py                 CLI interface
    app.py                  Streamlit web interface
    requirements.txt
    .env.example
    tests/
        test_professionalizer.py   mocked API tests, no real key needed
        test_history.py
```

## Running the tests

```bash
pip install -r requirements.txt
pytest tests/ -v
```

All 10 tests pass, and none of them need a real API key or make a real
network call. The Anthropic client is replaced with a mock object during
testing (`unittest.mock.patch`), so the tests check this project's own
logic - correct tone prompt sent, API errors wrapped into clear
messages, whitespace stripped from results - without depending on the
live API, its cost, or its response time. One test also confirms the
exact tone instruction text is included in the request sent to the
(mocked) API, which a passing test without mocking could not verify.

## Testing status

Backend logic: fully tested via the mocked pytest suite above - this is
the first project where testing did not require a real API key, since
mocking stands in for the live service. The actual live API call (a
real key producing a real rewritten response) was confirmed separately
in earlier testing via the Swagger-style manual run, and is also
exercised continuously by the deployed Streamlit app at the live demo
link above.

## Possible extensions

- Persist conversion history across sessions (e.g. in a small SQLite file)
- Batch mode: process multiple paragraphs or emails at once
- Export to .docx or .pdf

## Tech stack

Python, Anthropic SDK, Streamlit, python-dotenv, pytest
