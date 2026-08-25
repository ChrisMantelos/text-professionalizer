# Text Professionalizer

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B)
![Anthropic API](https://img.shields.io/badge/powered%20by-Anthropic%20API-D97757)

Converts informal draft text into clear, professional communication -
available both as a CLI tool and a web app.

**[Try it live](https://text-professionalizer-cm5su4jbqzwfcevd9p6vjk.streamlit.app)**

---

## Why I built this

I wanted a quick way to turn rushed messages (emails, Slack, notes) into
something I could confidently send to a client or manager, without
rewriting them by hand every time.

## Features

- Three communication tones: formal, friendly, concise, depending on the situation
- Language-aware: Greek input stays Greek, English input stays English
- Two interfaces: CLI for quick terminal use, web UI for a visual experience
- Proper error handling: clear messages for empty input, invalid tone, or connection issues
- Logic and UI are separated: `professionalizer.py` is a standalone module, easy to extend (for example, wrap it in a REST API for a Flutter frontend)

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

Output (concise):
```
Report is delayed - will send it later today.
```

---

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
Opens automatically at localhost:8501.

## Deploying the web demo

1. Push this repo to GitHub (already done).
2. Go to share.streamlit.io and sign in with your GitHub account.
3. Select this repository and set the main file to `app.py`.
4. Deploy. You will get a public URL.
5. Replace the note at the top of this README with a link to that URL.

## Project structure

```
text-professionalizer/
    professionalizer.py   core logic: API call, prompts, error handling
    main.py                CLI interface
    app.py                 Streamlit web interface
    requirements.txt
    .env.example
```

## Testing status

Verified with automated checks: all modules compile and import cleanly, and
the error-handling paths were exercised directly - empty input, an invalid
tone, a missing API key, and an invalid API key all raise the correct
ProfessionalizerError with a clear message instead of crashing.

The end-to-end success path (a valid key producing a real rewritten
response) has not been run against a live key yet. Confirm that once with
your own key before you demo or share this project.

## Possible extensions

- Conversion history (session state)
- Batch mode: process multiple paragraphs or emails at once
- Export to .docx or .pdf
- REST API endpoint (FastAPI) so a Flutter app could call it

## Tech stack

Python, Anthropic SDK, Streamlit, python-dotenv
