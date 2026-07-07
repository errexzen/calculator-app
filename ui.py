"""Tkinter user interface for the calculator application."""

from __future__ import annotations

import tkinter as tk
from decimal import Decimal
from tkinter import messagebox

from calculator import Calculator, CalculatorError, DivisionByZeroError
from history import HistoryManager


THEMES = {
    "light": {
        "window_bg": "#f1f5f9",
        "panel_bg": "#f1f5f9",
        "text": "#0f172a",
        "display_bg": "#ffffff",
        "display_fg": "#0f172a",
        "digit_bg": "#e2e8f0",
        "digit_hover": "#cbd5e1",
        "operator_bg": "#0ea5e9",
        "operator_hover": "#0369a1",
        "equals_bg": "#0284c7",
        "action_bg": "#334155",
        "action_hover": "#1e293b",
        "history_bg": "#f8fafc",
        "danger_bg": "#ef4444",
        "danger_hover": "#dc2626",
    },
    "dark": {
        "window_bg": "#0b1220",
        "panel_bg": "#111827",
        "text": "#e5e7eb",
        "display_bg": "#1f2937",
        "display_fg": "#f9fafb",
        "digit_bg": "#334155",
        "digit_hover": "#475569",
        "operator_bg": "#0284c7",
        "operator_hover": "#0369a1",
        "equals_bg": "#0ea5e9",
        "action_bg": "#1e293b",
        "action_hover": "#334155",
        "history_bg": "#111827",
        "danger_bg": "#dc2626",
        "danger_hover": "#b91c1c",
    },
}


class CalculatorUI:
    """Builds and manages the calculator desktop interface."""

    def __init__(self, root: tk.Tk, calculator: Calculator, history_manager: HistoryManager) -> None:
        self.root = root
        self.calculator = calculator
        self.history_manager = history_manager
        self.theme_name = "light"
        self.theme = THEMES[self.theme_name]

        self.current_input = ""
        self.display_var = tk.StringVar(value="0")

        self._configure_root()
        self._render_ui()
        self._bind_keyboard()

    def _configure_root(self) -> None:
        self.root.title("Calculator")
        width, height = 380, 540
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_x = (screen_width - width) // 2
        position_y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{position_x}+{position_y}")
        self.root.minsize(340, 500)
        self.root.configure(bg=self.theme["window_bg"])

    def _render_ui(self) -> None:
        for child in self.root.winfo_children():
            child.destroy()
        self.root.configure(bg=self.theme["window_bg"])
        self._build_ui()

    def _build_ui(self) -> None:
        container = tk.Frame(self.root, bg=self.theme["panel_bg"], padx=16, pady=16)
        container.pack(expand=True, fill="both")

        header = tk.Frame(container, bg=self.theme["panel_bg"])
        header.pack(fill="x", pady=(0, 12))

        title = tk.Label(
            header,
            text="Calculator",
            font=("Segoe UI", 20, "bold"),
            bg=self.theme["panel_bg"],
            fg=self.theme["text"],
        )
        title.pack(side="left")

        theme_button = tk.Button(
            header,
            text=f"Theme: {'Dark' if self.theme_name == 'light' else 'Light'}",
            command=self.toggle_theme,
            font=("Segoe UI", 10, "bold"),
            bg=self.theme["action_bg"],
            fg="#ffffff",
            activebackground=self.theme["action_hover"],
            activeforeground="#ffffff",
            bd=0,
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=6,
        )
        theme_button.pack(side="right")
        theme_button.bind(
            "<Enter>",
            lambda _event, btn=theme_button: btn.configure(bg=self.theme["action_hover"]),
        )
        theme_button.bind(
            "<Leave>",
            lambda _event, btn=theme_button: btn.configure(bg=self.theme["action_bg"]),
        )

        display = tk.Entry(
            container,
            textvariable=self.display_var,
            justify="right",
            font=("Consolas", 24, "bold"),
            bd=0,
            relief="flat",
            bg=self.theme["display_bg"],
            fg=self.theme["display_fg"],
            state="readonly",
            readonlybackground=self.theme["display_bg"],
        )
        display.pack(fill="x", ipady=14, pady=(0, 14))

        buttons_frame = tk.Frame(container, bg=self.theme["panel_bg"])
        buttons_frame.pack(expand=True, fill="both")

        for index in range(4):
            buttons_frame.grid_columnconfigure(index, weight=1, uniform="calculator")
        for index in range(5):
            buttons_frame.grid_rowconfigure(index, weight=1)

        button_layout = [
            ("7", "8", "9", "/"),
            ("4", "5", "6", "*"),
            ("1", "2", "3", "-"),
            ("0", ".", "=", "+"),
        ]

        for row_idx, row in enumerate(button_layout):
            for col_idx, label in enumerate(row):
                self._create_button(
                    parent=buttons_frame,
                    text=label,
                    command=lambda value=label: self._on_button_click(value),
                    row=row_idx,
                    column=col_idx,
                    padx=6,
                    pady=6,
                    is_operator=label in {"+", "-", "*", "/", "="},
                )

        self._create_button(
            parent=buttons_frame,
            text="C",
            command=self.clear,
            row=4,
            column=0,
            columnspan=1,
            padx=6,
            pady=6,
            is_action=True,
        )
        self._create_button(
            parent=buttons_frame,
            text="Backspace",
            command=self.backspace,
            row=4,
            column=1,
            columnspan=2,
            padx=6,
            pady=6,
            is_action=True,
        )
        self._create_button(
            parent=buttons_frame,
            text="History",
            command=self.show_history,
            row=4,
            column=3,
            columnspan=1,
            padx=6,
            pady=6,
            is_action=True,
        )

    def _create_button(
        self,
        parent: tk.Widget,
        text: str,
        command,
        row: int,
        column: int,
        columnspan: int = 1,
        padx: int = 4,
        pady: int = 4,
        is_operator: bool = False,
        is_action: bool = False,
    ) -> None:
        if is_operator:
            bg = self.theme["operator_bg"] if text != "=" else self.theme["equals_bg"]
            fg = "#ffffff"
            hover = self.theme["operator_hover"]
        elif is_action:
            bg = self.theme["action_bg"]
            fg = "#ffffff"
            hover = self.theme["action_hover"]
        else:
            bg = self.theme["digit_bg"]
            fg = self.theme["text"]
            hover = self.theme["digit_hover"]

        button = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 13, "bold"),
            bg=bg,
            fg=fg,
            activebackground=hover,
            activeforeground=fg,
            bd=0,
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=10,
        )
        button.grid(
            row=row,
            column=column,
            columnspan=columnspan,
            sticky="nsew",
            padx=padx,
            pady=pady,
        )

        button.bind("<Enter>", lambda _event, btn=button, color=hover: btn.configure(bg=color))
        button.bind("<Leave>", lambda _event, btn=button, color=bg: btn.configure(bg=color))

    def _bind_keyboard(self) -> None:
        self.root.bind("<Key>", self._on_key_press)

    def _on_key_press(self, event: tk.Event) -> str | None:
        char = event.char
        keysym = event.keysym

        if char.isdigit() or char in {"+", "-", "*", "/", ".", "(" , ")"}:
            self._append_to_input(char)
            return "break"

        if keysym in {"Return", "KP_Enter"}:
            self.calculate()
            return "break"

        if keysym == "BackSpace":
            self.backspace()
            return "break"

        if keysym in {"Escape", "Delete"}:
            self.clear()
            return "break"

        if keysym.lower() == "h":
            self.show_history()
            return "break"

        if keysym.lower() == "t":
            self.toggle_theme()
            return "break"

        return None

    def toggle_theme(self) -> None:
        self.theme_name = "dark" if self.theme_name == "light" else "light"
        self.theme = THEMES[self.theme_name]
        self._render_ui()

    def _on_button_click(self, value: str) -> None:
        if value == "=":
            self.calculate()
            return

        self._append_to_input(value)

    def _append_to_input(self, value: str) -> None:
        self.current_input += value
        self.display_var.set(self.current_input)

    def clear(self) -> None:
        self.current_input = ""
        self.display_var.set("0")

    def backspace(self) -> None:
        self.current_input = self.current_input[:-1]
        self.display_var.set(self.current_input if self.current_input else "0")

    def calculate(self) -> None:
        expression = self.current_input.strip()
        if not expression:
            return

        try:
            result = self.calculator.evaluate_expression(expression)
            formatted = self._format_decimal(result)
            self.display_var.set(formatted)
            self.history_manager.add_record(expression, formatted)
            self.current_input = formatted
        except DivisionByZeroError:
            messagebox.showerror("Calculation Error", "Cannot divide by zero.")
        except CalculatorError:
            messagebox.showerror("Calculation Error", "Please enter a valid expression.")
        except Exception:
            messagebox.showerror("Unexpected Error", "Something went wrong. Please try again.")

    def _format_decimal(self, value: Decimal) -> str:
        normalized = value.normalize()
        text = format(normalized, "f")
        if "." in text:
            text = text.rstrip("0").rstrip(".")
        return text or "0"

    def show_history(self) -> None:
        history_window = tk.Toplevel(self.root)
        history_window.title("Calculation History")
        history_window.geometry("420x360")
        history_window.configure(bg=self.theme["history_bg"])
        history_window.transient(self.root)
        history_window.grab_set()

        wrapper = tk.Frame(history_window, bg=self.theme["history_bg"], padx=12, pady=12)
        wrapper.pack(expand=True, fill="both")

        title = tk.Label(
            wrapper,
            text="History",
            font=("Segoe UI", 16, "bold"),
            bg=self.theme["history_bg"],
            fg=self.theme["text"],
        )
        title.pack(anchor="w", pady=(0, 10))

        list_frame = tk.Frame(wrapper, bg=self.theme["history_bg"])
        list_frame.pack(expand=True, fill="both")

        listbox = tk.Listbox(
            list_frame,
            font=("Consolas", 12),
            bg=self.theme["display_bg"],
            fg=self.theme["display_fg"],
            bd=0,
            relief="flat",
            selectbackground=self.theme["operator_bg"],
            selectforeground="#ffffff",
        )
        listbox.pack(side="left", expand=True, fill="both")

        scrollbar = tk.Scrollbar(list_frame, command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.configure(yscrollcommand=scrollbar.set)

        entries = self.history_manager.load_history()
        if entries:
            for item in reversed(entries):
                listbox.insert("end", item)
        else:
            listbox.insert("end", "No history yet.")

        actions = tk.Frame(wrapper, bg=self.theme["history_bg"])
        actions.pack(fill="x", pady=(10, 0))

        clear_button = tk.Button(
            actions,
            text="Clear History",
            font=("Segoe UI", 11, "bold"),
            bg=self.theme["danger_bg"],
            fg="#ffffff",
            activebackground=self.theme["danger_hover"],
            activeforeground="#ffffff",
            bd=0,
            relief="flat",
            cursor="hand2",
            command=lambda: self._clear_history_listbox(listbox),
        )
        clear_button.pack(side="left")

        close_button = tk.Button(
            actions,
            text="Close",
            font=("Segoe UI", 11, "bold"),
            bg=self.theme["action_bg"],
            fg="#ffffff",
            activebackground=self.theme["action_hover"],
            activeforeground="#ffffff",
            bd=0,
            relief="flat",
            cursor="hand2",
            command=history_window.destroy,
        )
        close_button.pack(side="right")

        clear_button.bind(
            "<Enter>",
            lambda _event, btn=clear_button: btn.configure(bg=self.theme["danger_hover"]),
        )
        clear_button.bind(
            "<Leave>",
            lambda _event, btn=clear_button: btn.configure(bg=self.theme["danger_bg"]),
        )
        close_button.bind(
            "<Enter>",
            lambda _event, btn=close_button: btn.configure(bg=self.theme["action_hover"]),
        )
        close_button.bind(
            "<Leave>",
            lambda _event, btn=close_button: btn.configure(bg=self.theme["action_bg"]),
        )

    def _clear_history_listbox(self, listbox: tk.Listbox) -> None:
        should_clear = messagebox.askyesno(
            "Clear History",
            "Are you sure you want to clear all history?",
        )
        if not should_clear:
            return

        self.history_manager.clear_history()
        listbox.delete(0, "end")
        listbox.insert("end", "No history yet.")
