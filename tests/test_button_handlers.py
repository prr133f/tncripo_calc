import tkinter as tk

import pytest

from main import create_ui


def make_ui():
    """
    Create the UI for tests. We withdraw the root window so no GUI is shown.
    Returns (root, ui_dict).
    """
    root = tk.Tk()
    root.withdraw()
    ui = create_ui(root)
    return root, ui


def get_button(ui, label: str):
    """
    Find a button by its text label from the created UI.
    Raises StopIteration if not found which will surface as a test failure.
    """
    return next(b for b in ui["buttons"] if b.cget("text") == label)


def test_on_subtract_inserts_minus_and_updates_status():
    root, ui = make_ui()
    try:
        display = ui["display"]
        status = ui["status"]
        display.delete(0, tk.END)

        btn = get_button(ui, "-")
        btn.invoke()

        assert display.get() == "-"
        assert status.cget("text") == "Вставлен '-'"
    finally:
        root.destroy()


def test_on_divide_inserts_slash_and_updates_status():
    root, ui = make_ui()
    try:
        display = ui["display"]
        status = ui["status"]
        display.delete(0, tk.END)

        btn = get_button(ui, "/")
        btn.invoke()

        assert display.get() == "/"
        assert status.cget("text") == "Вставлен '/'"
    finally:
        root.destroy()


def test_on_power_inserts_pow_and_updates_status():
    root, ui = make_ui()
    try:
        display = ui["display"]
        status = ui["status"]
        display.delete(0, tk.END)

        btn = get_button(ui, "^")
        btn.invoke()

        # the power button inserts Python's exponent operator "**"
        assert display.get() == "**"
        assert status.cget("text") == "Вставлен '**' (степень)"
    finally:
        root.destroy()


def test_on_sin_success_and_error_paths():
    root, ui = make_ui()
    try:
        display = ui["display"]
        status = ui["status"]
        display.delete(0, tk.END)

        # success case: sin(0) == 0 -> shown as integer "0"
        display.insert(0, "0")
        btn = get_button(ui, "sin")
        btn.invoke()
        assert display.get() == "0"
        assert status.cget("text") == "sin вычислен"

        # error case: invalid expression -> display shows Error and status starts with "sin:"
        display.delete(0, tk.END)
        display.insert(0, "abc")
        btn.invoke()
        assert display.get() == "Error"
        assert status.cget("text").startswith("sin:")
    finally:
        root.destroy()


def test_on_floor_computes_floor_and_updates_status():
    root, ui = make_ui()
    try:
        display = ui["display"]
        status = ui["status"]
        display.delete(0, tk.END)

        display.insert(0, "3.7")
        btn = get_button(ui, "floor")
        btn.invoke()

        assert display.get() == "3"
        assert status.cget("text") == "floor выполнен"
    finally:
        root.destroy()
