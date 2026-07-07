# Calculator Desktop App (Tkinter)

A professional desktop calculator application built with Python and Tkinter.
This project is organized with a modular architecture, clean separation of concerns, persistent calculation history, and a polished user interface suitable for a portfolio.

## Features

- Desktop GUI application (Tkinter)
- Core arithmetic operations: addition, subtraction, multiplication, division
- Decimal and negative number support
- Theme switcher (Light/Dark)
- Keyboard input support:
	- Numbers and operators from keyboard
	- Enter for calculation
	- Backspace to delete
	- T key for quick theme toggle
- Clean and modern calculator layout
- Hover effects for calculator buttons
- User-friendly error handling (including division by zero)
- Persistent calculation history stored in `history.json`
- In-app history viewer with clear history option
- Automatic creation of history file if missing
- Unit tests for business logic and history storage
- Windows executable build support using PyInstaller

## Technologies Used

- Python 3.12+
- Tkinter (standard library GUI toolkit)
- JSON (for local history persistence)

## Project Structure

```text
calculator-app/
|
|- main.py
|- calculator.py
|- history.py
|- ui.py
|- history.json
|- build_exe.ps1
|- tests/
|  |- test_calculator.py
|  |- test_history.py
|- README.md
|- requirements.txt
|- .gitignore
```

### Architecture Overview

- `main.py`: Application entry point and startup wiring
- `calculator.py`: Business logic and expression evaluation
- `history.py`: History persistence (load/save/clear)
- `ui.py`: Tkinter user interface and event handling
- `tests/`: Unit tests for core modules
- `build_exe.ps1`: Build script for generating a Windows `.exe`

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/calculator-app.git
cd calculator-app
```

2. Ensure Python 3.12+ is installed:

```bash
python --version
```

3. Install dependencies (none required beyond standard library):

```bash
pip install -r requirements.txt
```

## Run Tests

```bash
pytest
```

## How to Run

Run the app with:

```bash
python main.py
```

## Build Windows Executable

Use the provided PowerShell script:

```powershell
.\build_exe.ps1
```

After build completes, the executable is generated at:

```text
dist/CalculatorApp.exe
```

## Screenshot Placeholders

Add screenshots in this section once you run the app:

- Main Calculator Window: `docs/screenshots/main-window.png`
- History Dialog: `docs/screenshots/history-window.png`

## Future Improvements

- Add memory buttons (M+, M-, MR, MC)
- Add calculation export (CSV/TXT)
- Package app as executable for Windows/macOS/Linux

## License

This project is licensed under the terms in `LICENSE`.
