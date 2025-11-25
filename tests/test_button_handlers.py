import tkinter as tk
import pytest

from main import create_ui


@pytest.fixture
def ui():
    root = tk.Tk()
    # avoid showing the window during tests
    root.withdraw()
    ui = create_ui(root)
    yield ui
    try:
        root.destroy()
    except Exception:
        pass


def _get_button(ui, label: str):
    for btn in ui["buttons"]:
        if str(btn.cget("text")) == label:
            return btn
    raise AssertionError(f"Button with label {label!r} not found")


def test_add_inserts_plus(ui):
    btn = _get_button(ui, "+")
    btn.invoke()
    assert ui["display"].get() == "+"


def test_multiply_inserts_star(ui):
    btn = _get_button(ui, "*")
    btn.invoke()
    assert ui["display"].get() == "*"


def test_modulo_inserts_percent(ui):
    btn = _get_button(ui, "%")
    btn.invoke()
    assert ui["display"].get() == "%"


def test_cos_with_zero_does_not_error(ui):
    ui["display"].delete(0, tk.END)
    ui["display"].insert(0, "0")
    btn = _get_button(ui, "cos")
    btn.invoke()
    assert ui["display"].get() == "0"


def test_sqrt_of_9_shows_3(ui):
    ui["display"].delete(0, tk.END)
    ui["display"].insert(0, "9")
    btn = _get_button(ui, "√")
    btn.invoke()
    assert ui["display"].get() == "3"


def test_ceil_of_2_point_1_shows_3(ui):
    ui["display"].delete(0, tk.END)
    ui["display"].insert(0, "2.1")
    btn = _get_button(ui, "ceil")
    btn.invoke()
    assert ui["display"].get() == "3"
