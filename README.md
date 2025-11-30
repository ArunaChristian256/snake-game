
# 🐍 Jeux Nioka  (Pygame)

A modern, polished, and feature-rich Snake game built with **Python** and **Pygame**.
Jeux Nioka introduces levels, obstacles, bonus food, high-score persistence, and a refined UI with overlays (Pause, Game Over, Start Screen).

---

## 🚀 Features

### 🎮 Gameplay

* Smooth snake movement with arrow keys or **W A S D**
* Wrap-around world (edges teleport the snake)
* Food types:

  * 🍎 **Normal food** (+10 points)
  * ⭐ **Bonus food** (+30 points, more growth)
* Level progression every **50 points**
* Increasing speed per level

### 🧱 Advanced Level System

* Each level generates **dynamic obstacles**
* Higher levels = more complex patterns

### 🏆 Highscore System

* Score automatically saved in `highscore.txt`
* Highscore displayed in the top bar

### 🖥️ UI & Design

* Clean top info bar (Score, Level, Highscore)
* Start screen overlay
* Pause overlay
* Game Over overlay
* Smooth color palette & rounded snake body
* Optional grid mode

---

## 📂 Project Structure

```
project/
│── snake.py
│── highscore.txt (auto-created if missing)
```

---

## 🔧 Installation

### 1. Install Python (3.8+ recommended)

Check your version:

```bash
python --version
```

### 2. Install Pygame

```bash
pip install pygame
```

### 3. Run the game

```bash
python snake.py
```

---

## ⌨️ Controls

| Key                        | Action                  |
| -------------------------- | ----------------------- |
| **SPACE**                  | Start game              |
| **↑ ↓ ← →** or **W A S D** | Move snake              |
| **P**                      | Pause / Resume          |
| **R**                      | Restart after Game Over |
| **Q** or **ESC**           | Quit game               |

---

## 🧠 How It Works (Technical Overview)

### Snake System

* The snake is represented as a list of grid coordinates.
* Movement wraps around screen edges (`mod %` logic).
* Self-collision triggers Game Over.

### Food System

* Random spawn avoiding:

  * Snake body
  * Obstacles
* 8% chance of **bonus food**

### Level & Speed System

* Level increases every **50 points**
* Obstacles procedurally generated per level
* Speed increases dynamically

### Rendering

* Custom grid-to-pixel conversion
* Rounded-corner snake sprites
* Semi-transparent overlays

---

## 📈 Highscore Storage

Highscore is stored in:

```
highscore.txt
```

Automatically created in the same directory as `snake.py`.
If deleted, the game recreates it.

---

## 🧩 Code Entry Point

The game starts from:

```python
if __name__ == "__main__":
    main()
```

---

## 🤝 Contributing

Feel free to:

* Add skins, themes or sounds
* Improve obstacle generation
* Add menus or settings
* Fork and make your own version

Pull requests are welcome!

---

## 📜 License

This project is shared for personal and educational use.
You may modify and distribute it with credit.


