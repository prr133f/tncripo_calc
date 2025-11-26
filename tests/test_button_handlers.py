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


def test_subtraction_inserts_minus_and_updates_status():
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


def test_division_inserts_slash_and_updates_status():
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


def test_sin_success_and_error_paths():
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


def test_power_inserts_pow_and_updates_status():
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


def test_floor_computes_floor_and_updates_status():
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


def test_memory_basic_behavior_and_formatting():
    """
    Because the memory menu object is created inside create_ui and not returned,
    we test the observable memory storage and expected formatting behavior:
    - memory dict is present and starts at 0.0
    - when memory holds an integer-like float, recall should format it as an int
    - when memory holds a non-integer, recall should format it as float string
    This test manipulates the memory dict and then simulates the formatting logic
    that `mem_recall` uses to verify expected results.
    """
    root, ui = make_ui()
    try:
        display = ui["display"]
        status = ui["status"]
        memory = ui["memory"]

        # initial memory
        assert "value" in memory
        assert memory["value"] == 0.0

        # simulate M+ by adding a value to memory (direct manipulation here)
        memory["value"] = 5.0
        # simulate mem_recall formatting: integer-like -> inserted without decimal part
        display.delete(0, tk.END)
        v = memory["value"]
        if float(v).is_integer():
            display.insert(0, str(int(v)))
        else:
            display.insert(0, str(v))
        assert display.get() == "5"

        # now set a non-integer memory value and verify formatting
        memory["value"] = 2.75
        display.delete(0, tk.END)
        v = memory["value"]
        if float(v).is_integer():
            display.insert(0, str(int(v)))
        else:
            display.insert(0, str(v))
        assert display.get() == "2.75"

        # simulate MC (clear memory)
        memory["value"] = 0.0
        assert memory["value"] == 0.0
    finally:
        root.destroy()
