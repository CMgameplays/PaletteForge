# 🎨 PaletteForge

A lightweight, locally-hosted web app for extracting and generating color palettes from images. Built with Flask and Pillow — no cloud required, no data leaves your machine.

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python\&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0%2B-black?logo=flask)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Features

| Tool                | What it does                                             |
| ------------------- | -------------------------------------------------------- |
| **Palette Extract** | Extract dominant colors from an uploaded image           |
| **Palette Preview** | Display clean, usable color palettes                     |
| **Color Utility**   | Generate colors ready for design & development workflows |

---

## Requirements

### Software

| Requirement                                 | Version | Notes    |
| ------------------------------------------- | ------- | -------- |
| [Python](https://www.python.org/downloads/) | 3.11+   | Required |

### Python packages

All listed in `requirements.txt`:

```
flask>=3.0.0
pillow>=10.0.0
flask-limiter>=3.5.0
gunicorn>=21.0.0
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/CMgameplays/PaletteForge.git
cd PaletteForge
```

### 2. Create and activate a virtual environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

---

## Running locally

```bash
python paletteforge.py
```

The server starts on `http://127.0.0.1:5000` and opens in your browser.

---

## Project structure

```
paletteforge/
├── paletteforge.py      # Flask app — routes and palette logic
├── requirements.txt     # Python dependencies
├── templates/
│   └── index.html       # UI (HTML + CSS + JS)
└── static/              # Static assets (if any)
```

---

## API Routes

| Method | Route          | Description                               |
| ------ | -------------- | ----------------------------------------- |
| `GET`  | `/`            | Main UI page                              |
| `POST` | `/api/palette` | Extract color palette from uploaded image |

---

## Deployment

The app is production-ready with Gunicorn and can be deployed to any WSGI-compatible host.

**Render / Railway / Fly.io:**

Example `Procfile`:

```
web: gunicorn paletteforge:app --workers 2 --timeout 120 --bind 0.0.0.0:$PORT
```

Simply connect your GitHub repository and deploy.

---

## License

MIT — see [LICENSE](LICENSE) for details.

© CMG Forge
