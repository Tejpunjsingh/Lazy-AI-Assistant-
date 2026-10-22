# LazyDesk AI

**A local-first, low-friction workspace for the Slow & Steady challenge.**  
Tasks, notes, focus timer, and workspace backups work on your own computer. Optionally connect Ollama for open-weight AI assistance without a hosted AI API.

## Features

- Polished responsive dashboard with dark mode
- Task list with categories, energy levels, completion, filtering and search
- Quick notes saved locally in the browser
- Focus timer with 5 / 15 / 25 minute presets
- Optional AI chat powered by a model running in Ollama
- Built-in rule-based fallback helpers when no model is installed
- JSON export/import for your workspace
- Offline app shell cache after first visit over localhost

## Run it

Requirements: Python 3.9+ (no Python packages required).

1. Extract this folder.
2. Open a terminal in the `lazydesk-ai` folder.
3. Run:

   ```bash
   python3 server.py
   ```

   On Windows, use `py server.py` if `python` isn't available.

4. Open **http://127.0.0.1:8000** in your browser.
5. Keep the terminal running while using the website.

No npm install, build step, database, account, or API key is required for the core app.

## Enable local AI (optional)

1. Install Ollama from [ollama.com](https://ollama.com) while online.
2. Download a model suitable for your machine, for example:

   ```bash
   ollama pull llama3.2
   ```

   The model's license and hardware requirements vary; review the specific model's page/license before use. Larger models need more RAM and disk space. A small model is a practical starting point.

3. Make sure Ollama is running. On many installations, running `ollama run llama3.2` starts it and opens a chat; you can exit that chat while leaving the Ollama service running.
4. Start or restart LazyDesk with `python3 server.py`, then reload the page.
5. In **Settings & privacy**, set the model name to the exact name shown by `ollama list` (e.g. `llama3.2`).

LazyDesk's local Python server talks to Ollama at `http://127.0.0.1:11434` by default. If your Ollama endpoint differs, set `OLLAMA_HOST` before starting the server:

```bash
OLLAMA_HOST=http://127.0.0.1:11434 python3 server.py
```

PowerShell:

```powershell
$env:OLLAMA_HOST="http://127.0.0.1:11434"
py server.py
```

The browser sends AI prompts only to the LazyDesk server on your own computer. The Python server forwards them to the local Ollama endpoint. There is no cloud AI integration in this project. Do not expose the local server or Ollama port to an untrusted network.

## Offline behavior — honest notes

- **Works offline:** task and note editing, local storage, timer, theme, import/export, and built-in fallback suggestions. The project itself uses no external CDN assets.
- **Offline after setup:** the app is served from localhost and caches its app shell after the first visit. Browser storage is local to that browser/profile. If you clear browser data, your workspace may be removed; export backups regularly.
- **AI offline:** AI can work offline after Ollama and a model are installed, provided the local model is available and running. The initial Ollama/model download requires internet.
- **Not magic:** without Ollama, assistant responses are simple rule-based helpers—not a language model. The connection badge shows when no local model is detected.
- **Privacy scope:** there is no telemetry or external API in the code. The browser's local storage is not encrypted; use a trusted device and OS account. AI prompts are processed by your local Ollama service.

## Open-source choices

- **LazyDesk AI:** MIT License (see `LICENSE`).
- **Ollama:** local model runner; review its current project/license and install it from its official site.
- **Model licenses vary:** “open-weight” does not always mean OSI-approved open-source. Check the exact model license and usage terms.

## Troubleshooting

- **Website doesn't open:** ensure the terminal says it is serving `127.0.0.1:8000`; try `http://127.0.0.1:8000`.
- **AI says not connected:** check `ollama list`, make sure Ollama is running, and verify the model name in settings.
- **Port 8000 is busy:** run `PORT=8001 python3 server.py` (PowerShell: `$env:PORT="8001"; py server.py`) and open `http://127.0.0.1:8001`.
- **Data backup:** use Settings → Export data. Import accepts a LazyDesk JSON backup.

## Project layout

```text
lazydesk-ai/
├── index.html
├── styles.css
├── app.js
├── server.py
├── manifest.webmanifest
├── sw.js
├── LICENSE
└── README.md
```

## Challenge-ready summary

LazyDesk AI uses a local-first design to reduce busywork without requiring an account or a cloud AI subscription. Its everyday features are local and useful immediately; optional open-weight inference is provided by Ollama on the user's own machine. This makes privacy, model choice, and offline use practical rather than just marketing claims.
