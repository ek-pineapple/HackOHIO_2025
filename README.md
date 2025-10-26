# 🌻🧠 Plants vs Zombies – Study Edition
### “Outsmart the undead. Every correct answer plants your defense.”

```
🌻  P L A N T S   V S   Z O M B I E S  –  S T U D Y  E D I T I O N  🧠
```

> “Outsmart the undead. Every correct answer plants your defense.”

---

## 🎮 Overview

**Plants vs Zombies – Study Edition** is an educational, AI-powered twist on the classic *Plants vs Zombies* game.  
Your weapon? Knowledge. Each correct answer spawns a plant to defend your garden from waves of zombies.  

| Difficulty | Plant Type | Effect |
|-------------|-------------|--------|
| Easy | Peashooter 🌿 | Standard attack |
| Medium | Freeze Peashooter ❄️ | Slows zombies |
| Hard | Mine 💣 | Explodes on contact |

Upload your notes or study material, and the game generates **30 AI-powered quiz questions** (10 easy, 10 medium, 10 hard) based on your content.  
Learn faster — or get eaten slower.

---

## 🧩 Features

- 🧠 **AI Question Generation** — Turns any `.txt` or `.pdf` into quiz questions.  
- 🌱 **Dynamic Learning Gameplay** — Plants spawn by difficulty.  
- 💾 **Automatic Caching** — Saves questions to `generated_questions.json`.  
- 🧰 **Cross-Platform Upload** — Fully macOS-safe (no Tkinter).  
- 🎓 **Gamified Studying** — Makes your notes interactive and fun.

---

## 🧠 How It Works

1. **Start Screen** – Press **SPACE** to continue.  
2. **Upload Screen** – Press **U** and enter your file path (example below).  
   ```bash
   ➡️ File path: assets/sample_study_material.txt
   ```
   - The system extracts your text.  
   - Sends it to OpenAI to generate **30 balanced quiz questions**.  
   - Saves them automatically as:
     ```
     generated_questions.json
     ```
3. Press **N** to start the game.  
   - Correct answers → spawn plants 🌿  
   - Wrong answers → zombies advance 💀  
4. Game ends when a zombie reaches the left edge.

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/plants-vs-zombies-study-edition.git
cd plants-vs-zombies-study-edition
```

### 2️⃣ Create a Virtual Environment - This step is not required
```bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Add Your OpenAI API Key
Create a `.env` file in the project root:
```
OPENAI_API_KEY=sk-your-secret-key-here
```

### 5️⃣ Run the Game
```bash
python3 main.py
```

---

## 💾 File Structure

```
📂 PlantsVsZombiesStudyEdition/
 ┣ 📂 Logistics/
 ┃ ┣ ai_question_gen.py          # Generates 30 AI questions from text
 ┃ ┣ file_loader.py              # Extracts text from PDF/TXT
 ┃ ┣ upload_manager.py           # Handles upload & LLM generation
 ┃ ┣ constants.py                # Window/game constants
 ┃ ┣ loading.py                  # Loads assets
 ┃ ┗ game_manager.py             # Core gameplay logic
 ┣ 📂 Entities/
 ┃ ┣ plant_types.py              # Plant definitions
 ┃ ┣ plant_manager.py            # Plant/projectile management
 ┃ ┣ projectile.py               # Projectile behavior
 ┃ ┗ zombie.py                   # Zombie movement & logic
 ┣ 📂 UI/
 ┃ ┗ sidebar.py                  # Question UI
 ┣ 📂 assets/
 ┃ ┣ questions.json              # Static fallback questions
 ┃ ┗ sample_study_material.txt   # Example file
 ┣ main.py                       # Main game loop
 ┣ generated_questions.json      # AI-generated question cache
 ┣ requirements.txt              # Dependencies
 ┗ README.md                     # Project documentation
```

---

## 🧪 Example Run

```bash
📂 Please enter the full path to your study file (.pdf or .txt):
➡️ File path: assets/sample_study_material.txt
✅ Uploaded and processed file: assets/processed_upload.txt
🧠 Generating 30 quiz questions from text with OpenAI...
🧩 30 AI-generated questions saved to generated_questions.json
✅ Questions generated from this file: sample_study_material.txt
🚀 Starting game...
```

---

## ⚔️ Future Features

- ⚡ Power-ups for streaks of correct answers  
- 🧩 Co-op “Study Mode” for shared gameplay  
- 📊 Leaderboards and analytics  
- 🧠 Adaptive difficulty scaling  
- 🗣️ Voice-based answering  

---

## 👩‍💻 Team

**Team:** HackOhio 2025  - Ekumjyot Kaur, Daniel Shim, Jaewoo Jung, Eryn Todd
Developed by students who decided to weaponize knowledge.  

> “Because the brain *is* mightier than the sword.”  

---

## 🧟‍♂️ License

This project is open-source.  
Use it, study with it, or fork it — just don’t let the zombies win.

---

## 📦 Requirements

```txt
pygame==2.6.1
openai>=1.3.0
python-dotenv>=1.0.1
PyMuPDF>=1.23.5
```

---

> 🧩 **HackOhio 2025 Submission**  
> *Plants vs Zombies – Study Edition*  
> Learn fast. Think faster. Survive the undead.
