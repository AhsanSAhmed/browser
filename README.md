

# Vegvísir Browser 🧭  
**A Norse-inspired, fantasy-themed web browser built with PyQt5.**

Vegvísir is a custom lightweight desktop web browser featuring a rune-like aesthetic, mystical soundtrack, and immersive Norse design. It is built using `PyQt5` and `QWebEngineView`, with support for multiple tabs, bookmarks, developer tools, and custom volume-controlled background music — all wrapped in a beautifully styled Mantinia interface.

> **Vegvísir** means *“That Which Shows the Way”* — a magical Icelandic stave for guidance through storms. This browser is your compass through the digital world.

---

### 🎬 Demo Video
📁 (https://github.com/user-attachments/assets/3b93a8f3-c7ee-45ff-9b11-4a7ca494802b) 

---

### 🛠️ Features

- **Custom Title Bar** – Frameless design with custom close, minimize, and maximize buttons.
- **Old Norse Aesthetic** – Uses the **Mantinia** font and parchment-colored theme for UI & web content.
- **Tabs Support** – Multiple tab navigation with a dynamic "+" tab.
- **Bookmarks Bar** – Save & manage your favorite sites; delete with right-click.
- **Developer Tools** – Integrated dev console dock for inspecting pages.
- **Re-open Recently Closed Tabs** – Easily reopen tabs that you closed by using the shortcut Ctrl+Shift+T.
- **Web Navigation** – Back, forward, refresh, home, and direct URL access.
- **Custom Font Injection** – Mantinia font applied to rendered websites via injected CSS.

---

### 🚀 How to Use

#### 1. 🔤 Install Fonts  
Download & install the **Mantinia** font:  
https://www.dafontfree.net/mantinia-f135525.htm  
Also ensure the `.ttf` file is placed in the `/fonts/` folder of the project.

#### 2. 📦 Install Dependencies  
Make sure you have Python and pip installed. Then:

```bash
pip install PyQt5 PyQtWebEngine
```
### 3. ▶️ Run the Browser
```bash
python browser.py
```

### 4.🖱️ Basic Controls
URL Bar: Type a website address and hit Enter.

Back/Forward/Home: Standard navigation tools.

New Tabs: Click the + icon to open a new tab.

Bookmarks: Click the heart icon → name it → see it appear in the bar.

Delete Bookmarks: Right-click any bookmark.

Inspect Element: Click the inspect icon to toggle dev tools.

Re-open recent closed Tabs: Press Ctrl+Shift+T to reopen recently closed tabs

### 5. 📁 Project Structure
bash
```
Vegvísir/
├── browser.py          # Main application script
├── images/             # Navigation & window icons
│   ├── binoculars.png
│   ├── bookmark.png
│   ├── home.png
│   ├── left-arrow.png
│   ├── refresh.png
│   └── right-arrow.png
├── fonts/              # Custom fonts
│   └── Mantinia.ttf
```

### 6. 🔮 Future Enhancements
✅ Rune-based splash screen

🔲 Search bar with DuckDuckGo/Google options

🔲 Bookmark folders and sync

🔲 Extension system for plugins

📜 License
This project is licensed under the MIT License. Feel free to use, fork, and modify it for your own purposes.

🙏 Credits
Developed by Ahsan Shajee Ahmed
Fantasy theming & original concept inspired by Norse mythology.
Special thanks to Ayaan for building the original OR-BIT Browser, which inspired this transformation.
