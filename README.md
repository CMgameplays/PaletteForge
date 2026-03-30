# 🎨 PaletteForge

PaletteForge is a lightweight web-based tool for extracting, generating, and visualizing color palettes from images. Built with Python and Flask, it provides a fast and intuitive way for developers, designers, and artists to work with color data directly in the browser.

---

## 🚀 Features

* 🎯 Extract dominant colors from uploaded images
* 🎨 Generate clean, usable color palettes
* ⚡ Fast image processing using Pillow
* 🌐 Simple and responsive web interface
* 🛡️ Rate limiting for stability and abuse prevention
* 📦 Lightweight and easy to deploy

---

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **Image Processing:** Pillow
* **Server:** Gunicorn
* **Security:** Flask-Limiter

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/CMgameplays/PaletteForge.git
cd PaletteForge
```

---

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install flask pillow flask-limiter gunicorn
```

---

## ▶️ Running the Application

### Development mode

```bash
python app.py
```

Open your browser at:

```
http://127.0.0.1:5000
```

---

### Production mode (recommended)

```bash
gunicorn app:app
```

---

## 🌐 Deployment

PaletteForge can be deployed on:

* VPS (recommended)
* Docker environments
* Cloud platforms (Railway, Render, etc.)

For production, it is recommended to use:

* **NGINX** as a reverse proxy
* **Gunicorn** as the application server

---

## 📁 Project Structure

```
PaletteForge/
│── app.py
│── requirements.txt
│── static/
│── templates/
```

---

## ⚙️ Usage

1. Upload an image
2. The app processes the image
3. Extracted color palette is displayed
4. Use the colors in your workflow

---

## 🔒 Notes

* File size limits may apply depending on server configuration
* Rate limiting is enabled to prevent abuse
* Temporary files may be used during processing

---

## 🚧 Future Improvements

* Export palettes (JSON, CSS, etc.)
* Advanced palette algorithms
* UI/UX enhancements
* Batch image processing
* Integration with other CMG Forge tools

---

## 🤝 Contributing

Contributions are welcome.

* Fork the repository
* Create a feature branch
* Submit a pull request

---

## 📄 License

This project is open-source and available under the MIT License.

---

## 🌍 CMG Forge Ecosystem

PaletteForge is part of the **CMG Forge** ecosystem — a growing collection of developer tools designed to simplify workflows and boost productivity.

---

## 👤 Author

**CMG Forge**
GitHub: https://github.com/CMgameplays
