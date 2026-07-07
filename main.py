"""Application entry point."""

from __future__ import annotations

import sys
import tkinter as tk
from tkinter import messagebox

from calculator import Calculator
from history import HistoryManager
from ui import CalculatorUI


def _validate_python_version() -> bool:
    if sys.version_info >= (3, 12):
        return True

    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(
        "Python Version Error",
        "This application requires Python 3.12 or newer.",
    )
    root.destroy()
    return False


def main() -> None:
    if not _validate_python_version():
        return

    root = tk.Tk()
    calculator = Calculator()
    history_manager = HistoryManager("history.json")
    CalculatorUI(root, calculator, history_manager)
    root.mainloop()


if __name__ == "__main__":
    main()
