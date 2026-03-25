# wakapi-github

Small Python service that reads your **this-month** coding time from [Wakapi](https://github.com/muety/wakapi) and updates your **GitHub profile bio** on a schedule (every 15 minutes).

The bio uses a short duration string plus the current calendar month, for example: `⚡2h 30m coding this March 🚀` (exact format is defined in `main.py`).

## Requirements

- Python **or** Docker
- A **Wakapi** account (self-hosted or [wakapi.dev](https://wakapi.dev)) and API key
- A **GitHub** [personal access token](https://github.com/settings/tokens) with the `**user`** scope (to update your profile)

## Environment variables

Create a `.env` file in the project root or export these in your shell:


| Variable         | Description                                                        |
| ---------------- | ------------------------------------------------------------------ |
| `WAKAPI_API_KEY` | Wakapi API key (sent as Basic auth)                                |
| `GITHUB_API_KEY` | GitHub PAT with `user` scope                                       |
| `WAKAPI_URL`     | Wakapi base URL, e.g. `https://wakapi.dev` — **no trailing slash** |


The app uses [python-dotenv](https://pypi.org/project/python-dotenv/) to load `.env` when you run it locally.

## Run locally

```bash
python -m venv .venv
# Windows:
.\.venv\Scripts\activate

# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
python main.py
```

## Run with Docker Compose

From the repo root (uses `.env` automatically):

```bash
docker compose up --build -d
```

`docker-compose.yml` builds the image from this directory and passes the three variables into the container.

More Docker-oriented notes: [README.Docker.md](README.Docker.md).

## VS Code (optional)

The `.vscode` folder is **committed on purpose** so you can debug in a container with a consistent setup:


| File              | Purpose                                                                                            |
| ----------------- | -------------------------------------------------------------------------------------------------- |
| `launch.json`     | **Docker: Python — General** — starts a debug session with **debugpy** inside the container        |
| `tasks.json`      | Builds the image (`docker-build`) and runs the debug container (`docker-run: debug`) before launch |
| `extensions.json` | Suggests the **Docker** extension (`ms-azuretools.vscode-docker`)                                  |


1. Install [Docker](https://docs.docker.com/get-docker/) and the [Docker VS Code extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker).
2. Open this folder in VS Code.
3. **Run and Debug** → choose **Docker: Python — General** → F5.

**Secrets:** `docker compose` is the most straightforward way to run with a `.env` file. The stock Docker launch task builds from `Dockerfile` only; if variables are missing in the container, run via Compose or extend `tasks.json` / launch to pass the same env as `docker-compose.yml`.