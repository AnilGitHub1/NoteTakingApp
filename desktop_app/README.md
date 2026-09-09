# DSA Note-Taking Desktop App

A 100% local, offline desktop application designed specifically for software engineers to track, organize, and review Data Structures & Algorithms (DSA) interview problems.

## Highlights & Strict Requirements Satisfied
- **Zero Cloud / No Internet / No Auth**: Runs 100% offline on your local computer.
- **Python 3 GUI**: Built with PyQt6 (with automatic fallback to PySide6).
- **Embedded SQLite Persistence**: Local `dsa_notes.db` database automatically created upon first launch with indexed search tables.
- **Local Asset Isolation**: Attached images/diagrams are safely copied, uniquely renamed, and placed in `./dsa_assets/` relative to the application directory.
- **Code Highlighting & Monospace Reader**: Syntax-highlighted code editor and viewer with an instant 1-click **Copy Code** clipboard action.
- **Ergonomic Dark Mode**: Modern dark-theme aesthetic designed for extended study sessions.

---

## Quick Start (Run Locally)

### 1. Requirements
- Python 3.9, 3.10, 3.11, or 3.12
- Windows, macOS, or Linux

### 2. Setup Virtual Environment
```bash
# Clone or navigate to the directory
cd desktop_app

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS / Linux:
source venv/bin/activate
# On Windows (cmd):
venv\Scripts\activate.bat
# On Windows (PowerShell):
venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
*(Or `pip install PyQt6` or `pip install PySide6`)*

### 4. Run the Application
```bash
python main.py
```

---

## 🍏 Building a macOS `.app` Desktop Bundle

You can package this project into a native **`DSANoteTaker.app`** bundle that you can put in `/Applications` or launch from Launchpad and Dock:

### Option A: Using the Automated Build Script (Quickest)
```bash
cd desktop_app
chmod +x build_mac.sh
./build_mac.sh
```

### Option B: Manual Build via PyInstaller
```bash
cd desktop_app
pip install pyinstaller PyQt6
pyinstaller --clean DSANoteTaker.spec
```

The compiled application bundle will be generated at:
```
desktop_app/dist/DSANoteTaker.app
```

### Launch and Install
- To launch immediately:
  ```bash
  open dist/DSANoteTaker.app
  ```
- To install in your Mac's Applications folder:
  ```bash
  cp -r dist/DSANoteTaker.app /Applications/
  ```

---

## Project Structure
```text
desktop_app/
├── main.py             # Main GUI application window, sidebar, and view router
├── database.py         # SQLite schema initialization, CRUD, and asset manager
├── highlighter.py      # QSyntaxHighlighter for code blocks
├── theme.py            # Professional QSS dark-mode stylesheet
├── requirements.txt    # PyQt6 dependency specification
└── dsa_assets/         # Automatically created directory for local diagram attachments
```

---

## Core Features
1. **Sidebar Navigation**:
   - Fast switching between **All Questions**, **Categories/Topics**, and **Add New Question**.
   - Live difficulty filter pills: **Easy (🟢)**, **Medium (🟡)**, and **Hard (🔴)** with real-time question counts.
2. **Add / Edit Question Form Panel**:
   - Title input, problem statement, categories dropdown, difficulty selectors.
   - Examples & test cases section.
   - Personal notes & algorithmic intuition / time-space trade-offs.
   - Monospace solution code area with syntax coloring.
   - **Browse Image** attachment button that copies files into `./dsa_assets/` with UUID-based filenames.
3. **Question Explorer & Read-Only View Panel**:
   - Instant search across title, problem, notes, and topic.
   - Dedicated read-only review pane with formatted text, scaled diagram preview, and 1-click **Copy Code** button.
