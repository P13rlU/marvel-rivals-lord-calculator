# Marvel Rivals - Lord Rank Calculator

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows-green)
![License](https://img.shields.io/badge/License-MIT-lightgray)

A simple, user-friendly GUI tool to calculate how many missions and points you need to reach **Lord rank** for any character in **Marvel Rivals**.

Made with ❤️ by [P13rlU](https://github.com/P13rlU).

Credits for the Original Project go to: [xSkullHD](https://www.nexusmods.com/profile/xSkullHD/mods?gameId=7106)

---

## 📌 Features

- ✅ Full character list with **Vanguard / Duelist / Strategist** roles
- 🔍 **Search-as-you-type** character selection (supports partial/fuzzy matching)
- 📊 Mission tracking per rank (Agent → Lord)
- ⭐ Mark characters or missions as **completed** (saved between sessions)
- 🧮 Auto-calculate missions needed based on:
  - Your current rank & points
  - Hours played (60 pts/hour)
- 🎨 Fully customizable UI (colors, font, size)
- 💾 Data saved locally in `completed.json`

---

## 🚀 How to Use (Windows Users)

1. Go to the **[Releases](https://github.com/P13rlU/marvel-rivals-lord-calculator/releases)** page
2. Download the latest `Marvel Rivals Calculator.exe`
3. Run it!

> ⚠️ **Windows SmartScreen Warning?**  
> Since the app is not digitally signed (no code signing certificate), Windows may show:  
> _“Windows protected your PC”_ or _“Unknown publisher”_.  
> This is **normal** for free/open-source tools.  
> 
> ✅ To run it safely:
> - Click **"More info"**
> - Click **"Run anyway"**
>
> The app is **100% safe** — you can verify by checking the [source code](https://github.com/P13rlU/marvel-rivals-lord-calculator).

---

## 🛠️ How It Works

- **Points to Lord** = Sum of thresholds from your current rank up to Centurion
- **Playtime points** = Hours played × 60
- **Missions needed** = `ceil((Points to Lord - Playtime points) / Points per mission)`
- Missions are **evenly split** among all active missions for the selected rank

Example output:
```
Character:
Spider-Man
Playtime points: 1,200
Points still needed to Lord: 3,500
Total missions required (at 40 pts each): 88
Web-Slinging: 88 missions (3,520 pts)
→ 17,600 required
```

---

## 🧪 For Developers (Build from Source)

### Requirements
- Python 3.8+
- 'tkinter' (usually included with Python)

### Run locally
```
git clone https://github.com/P13rlU/marvel-rivals-lord-calculator.git
cd marvel-rivals-lord-calculator
python RivalsCalculateLord.py
```

### Build Windows EXE (via GitHub Actions)
This repo uses **GitHub Actions** to automatically build and release the '.exe' on every push to 'main'.  
The workflow:
- Runs on a real Windows machine
- Uses PyInstaller (`--onefile --windowed`)
- Uploads the `.exe` to GitHub Releases

---

## 📂 Data Persistence

Your progress is saved in a local file:  
`completed.json` (in the same folder as the executable)

✅ Safe to delete if you want to reset progress.

---

## 🤝 Contributing

Found a bug? Missing a character? Want to improve the UI?

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/your-idea`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-idea`)
5. Open a Pull Request

---

[//]: # (## 📜 License)

[//]: # ()
[//]: # (This project is licensed under the **MIT License** – see the [LICENSE]&#40;LICENSE&#41; file for details.)

[//]: # ()
[//]: # (---)

> 💡 **Note**: This tool is **unofficial** and not affiliated with **Marvel**, **NetEase**, or **Marvel Rivals**.
