#!/usr/bin/env python3
"""
CMG Forge — PaletteForge  |  app.py
=====================================
Game palette extraction and management toolkit.

LOCAL:      python app.py        → starts server, opens browser automatically
PRODUCTION: gunicorn app:app     → Render / Railway / Fly.io / any WSGI host

Routes
------
  GET  /                    → main UI page
  POST /api/extract         → extract palette from image; returns JSON + PNG strip
  POST /api/build/export    → accepts palette JSON; returns .gpl / .hex / PNG / JSON
  POST /api/swap            → remap image colors            (Tab 2 — TODO)
  POST /api/swap/batch      → batch remap via ZIP           (Tab 2 — TODO)
  POST /api/reduce          → reduce image color count      (Tab 4 — TODO)

© CMG Forge
"""

import base64
import io
import json as _json
import os
import socket
import threading
import webbrowser
from collections import Counter

from flask import Flask, jsonify, render_template, request, send_file
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from PIL import Image, ImageDraw

# ── App setup ─────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"))
app.config["SECRET_KEY"]         = os.environ.get("SECRET_KEY", os.urandom(32))
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024   # 50 MB

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=[],
    storage_uri="memory://",
)

ALLOWED_MIME = {"image/png", "image/jpeg", "image/webp", "image/gif"}


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def _rgb_to_hsv(r: int, g: int, b: int) -> tuple:
    rf, gf, bf = r / 255.0, g / 255.0, b / 255.0
    mx = max(rf, gf, bf)
    mn = min(rf, gf, bf)
    df = mx - mn
    if df == 0:
        h = 0.0
    elif mx == rf:
        h = (60.0 * ((gf - bf) / df)) % 360.0
    elif mx == gf:
        h = (60.0 * ((bf - rf) / df) + 120.0) % 360.0
    else:
        h = (60.0 * ((rf - gf) / df) + 240.0) % 360.0
    return h, (0.0 if mx == 0 else df / mx), mx


def _build_strip(palette: list, swatch: int = 48) -> bytes:
    """Render palette as a horizontal PNG strip of `swatch`×`swatch` tiles."""
    n = max(1, len(palette))
    img = Image.new("RGB", (swatch * n, swatch))
    draw = ImageDraw.Draw(img)
    for i, c in enumerate(palette):
        x = i * swatch
        draw.rectangle([x, 0, x + swatch - 1, swatch - 1],
                       fill=(c["r"], c["g"], c["b"]))
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return buf.getvalue()


def _open_image(stream) -> Image.Image:
    img = Image.open(stream)
    # For animated GIFs use the first frame
    if getattr(img, "is_animated", False):
        img.seek(0)
    return img.convert("RGB")


# ══════════════════════════════════════════════════════════════════════════════
# ROUTES
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/")
def index():
    return render_template("index.html")


# ── Tab 1: Extract ────────────────────────────────────────────────────────────

@app.route("/api/extract", methods=["POST"])
@limiter.limit("30/minute")
def api_extract():
    file = request.files.get("image")
    if not file or not file.filename:
        return jsonify(error="No image uploaded."), 400

    if file.content_type and file.content_type not in ALLOWED_MIME:
        return jsonify(error="Unsupported file type. Please upload PNG, JPG, WEBP, or GIF."), 400

    try:
        max_colors = max(1, min(256, int(request.form.get("max_colors", 32))))
    except (ValueError, TypeError):
        max_colors = 32

    try:
        img = _open_image(file.stream)
    except Exception:
        return jsonify(error="Could not open image. Please upload a valid PNG, JPG, WEBP, or GIF."), 400

    # Downsample large images for speed without distorting colour distribution
    if max(img.size) > 800:
        img.thumbnail((800, 800), Image.LANCZOS)

    pixels = list(img.getdata())
    total  = len(pixels)

    raw_counts = Counter(pixels)

    if len(raw_counts) > max_colors:
        q = img.quantize(colors=max_colors, dither=Image.Dither.NONE)
        q_rgb = q.convert("RGB")
        pixels = list(q_rgb.getdata())
        raw_counts = Counter(pixels)

    palette = []
    for (r, g, b), count in raw_counts.items():
        h, _s, _v = _rgb_to_hsv(r, g, b)
        brightness = round(0.299 * r + 0.587 * g + 0.114 * b, 2)
        palette.append({
            "hex":        f"#{r:02x}{g:02x}{b:02x}",
            "r":          r,
            "g":          g,
            "b":          b,
            "count":      count,
            "frequency":  round(count / total, 4),
            "hue":        round(h, 2),
            "brightness": brightness,
        })

    # Default order: most-frequent first
    palette.sort(key=lambda c: -c["count"])

    strip_b64 = base64.b64encode(_build_strip(palette)).decode()

    return jsonify(palette=palette, strip_png=strip_b64, total_pixels=total)


# ── Tab 1+3: Export palette ───────────────────────────────────────────────────

@app.route("/api/build/export", methods=["POST"])
@limiter.limit("30/minute")
def api_build_export():
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify(error="Invalid JSON body."), 400

    if not data or "palette" not in data:
        return jsonify(error="Missing palette data."), 400

    palette = data["palette"]
    fmt     = data.get("format", "hex").lower()

    if not palette:
        return jsonify(error="Palette is empty."), 400

    # Validate palette entries have the required fields
    for c in palette:
        if not all(k in c for k in ("hex", "r", "g", "b")):
            return jsonify(error="Invalid palette entry — each color needs hex, r, g, b."), 400

    if fmt == "hex":
        content = "\n".join(c["hex"] for c in palette)
        buf = io.BytesIO(content.encode())
        return send_file(buf, mimetype="text/plain",
                         as_attachment=True, download_name="palette.hex")

    if fmt == "gpl":
        lines = ["GIMP Palette", "Name: PaletteForge Export", "Columns: 8", "#"]
        for c in palette:
            name = c["hex"].lstrip("#").upper()
            lines.append(f"{c['r']:3d} {c['g']:3d} {c['b']:3d}\t{name}")
        content = "\n".join(lines) + "\n"
        buf = io.BytesIO(content.encode())
        return send_file(buf, mimetype="text/plain",
                         as_attachment=True, download_name="palette.gpl")

    if fmt == "json":
        out = [{"hex": c["hex"], "r": c["r"], "g": c["g"], "b": c["b"]}
               for c in palette]
        buf = io.BytesIO(_json.dumps(out, indent=2).encode())
        return send_file(buf, mimetype="application/json",
                         as_attachment=True, download_name="palette.json")

    if fmt == "png":
        buf = io.BytesIO(_build_strip(palette))
        return send_file(buf, mimetype="image/png",
                         as_attachment=True, download_name="palette.png")

    return jsonify(error=f"Unknown format '{fmt}'. Use: hex, gpl, json, png."), 400


# ══════════════════════════════════════════════════════════════════════════════
# DEV SERVER
# ══════════════════════════════════════════════════════════════════════════════

def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("", 0))
        return s.getsockname()[1]


if __name__ == "__main__":
    port = int(os.environ.get("PORT", _free_port()))
    threading.Timer(0.9, lambda: webbrowser.open(f"http://127.0.0.1:{port}")).start()
    app.run(host="0.0.0.0", port=port, debug=False)
