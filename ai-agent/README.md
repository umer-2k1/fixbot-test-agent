# Browser-Use agent (Docker + live preview)

Runs [Browser-Use](https://github.com/browser-use/browser-use) with **Groq** (`ChatGroq`), local Chromium, `Tools`, and the PCPartPicker task.

## Quick start

```bash
cp .env.example .env
# Set GROQ_API_KEY in .env

docker compose up --build
```

Chromium is started automatically by Browser-Use (Playwright). No separate Chrome or CDP setup.

## Live browser preview (KasmVNC)

The compose stack includes KasmVNC. Open:

- `http://localhost:3000`

You will see the browser session live while the agent runs.

## Run locally

```bash
source .venv/bin/activate
pip install -r requirements.docker.txt
python -m playwright install chromium
cp .env.example .env
python app/main.py
```

To watch the browser locally (without Docker): `BROWSER_USE_HEADLESS=false python app/main.py`

## Environment

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Required ([Groq console](https://console.groq.com)) |
| `GROQ_MODEL` | Default `meta-llama/llama-4-maverick-17b-128e-instruct` |
| `BROWSER_USE_HEADLESS` | `false` for live preview, `true` for headless |
| `AGENT_TASK` | Override the default PCPartPicker task |
| `AGENT_MAX_STEPS` | Default `100000` |

## Sample task

The default task builds a sub-$2000 water-cooled ITX PC on [pcpartpicker.com](https://pcpartpicker.com/) and returns parts, prices, and a share link. Override with `AGENT_TASK` in `.env` or:

```bash
AGENT_TASK="Go to example.com and return the title" docker compose run --rm browser-agent
```
