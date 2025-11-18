import math
import tkinter as tk
from typing import Any, Dict

BUTTON_LABELS = [
    "+",
    "-",
    "*",
    "/",
    "%",
    "sin",
    "cos",
    "^",
    "√",
    "floor",
    "ceil",
    "M",
]


def safe_eval(expr: str):
    expr = expr.strip()
    if not expr:
        raise ValueError("Пустое выражение")
    try:
        # запрещаем встроенные функции
        return eval(expr, {"__builtins__": None}, {})
    except Exception as e:
        raise ValueError(f"Ошибка вычисления: {e}") from e


def create_ui(root: tk.Tk):
    root.title("Калькулятор")
    root.resizable(False, False)

    main_frame = tk.Frame(root, padx=8, pady=8)
    main_frame.pack(fill=tk.BOTH, expand=True)

    display = tk.Entry(main_frame, font=("Arial", 20), justify="right")
    display.grid(row=0, column=0, columnspan=3, sticky="we", pady=(0, 6))

    status = tk.Label(main_frame, text="Готово", anchor="w")
    status.grid(row=5, column=0, columnspan=3, sticky="we", pady=(8, 0))

    memory = {"value": 0.0}

    # Вспомогательные функции
    def set_status(text: str):
        status.config(text=text)

    def insert_text(text: str):
        display.insert(tk.END, text)
        display.focus_set()

    def parse_display_value() -> float:
        expr = display.get().strip()
        if expr == "":
            raise ValueError("Пусто")
        val = safe_eval(expr)
        if not isinstance(val, (int, float)):
            raise ValueError("Результат не число")
        return float(val)

    def on_add():
        insert_text("+")
        set_status("Вставлен '+'")

    def on_multiply():
        insert_text("*")
        set_status("Вставлен '*'")

    def on_modulo():
        insert_text("%")
        set_status("Вставлен '%' (остаток)")

    def on_cos():
        try:
            val = parse_display_value()
            res = math.cos(val)
        except Exception as e:
            display.delete(0, tk.END)
            display.insert(0, "Error")
            set_status(f"cos: {e}")
    def on_subtract():
        insert_text("-")
        set_status("Вставлен '-'")

    def on_divide():
        insert_text("/")
        set_status("Вставлен '/'")

    def on_power():
        insert_text("**")
        set_status("Вставлен '**' (степень)")

    def on_sin():
        try:
            val = parse_display_value()
            res = math.sin(val)
        except Exception as e:
            display.delete(0, tk.END)
            display.insert(0, "Error")
            set_status(f"sin: {e}")
            return
        if float(res).is_integer():
            display.delete(0, tk.END)
            display.insert(0, str(int(res)))
        else:
            display.delete(0, tk.END)
            display.insert(0, str(res))
        set_status("cos вычислен")

    def on_sqrt():
        try:
            val = parse_display_value()
            if val < 0:
                raise ValueError("Корень из отрицательного числа")
            res = math.sqrt(val)
        except Exception as e:
            display.delete(0, tk.END)
            display.insert(0, "Error")
            set_status(f"√: {e}")
            return
        if float(res).is_integer():
            display.delete(0, tk.END)
            display.insert(0, str(int(res)))
        else:
            display.delete(0, tk.END)
            display.insert(0, str(res))
        set_status("√ вычислен")

    def on_ceil():
        try:
            val = parse_display_value()
            res = math.ceil(val)
        except Exception as e:
            display.delete(0, tk.END)
            display.insert(0, "Error")
            set_status(f"ceil: {e}")
            return
        display.delete(0, tk.END)
        display.insert(0, str(res))
        set_status("ceil выполнен")
        set_status("sin вычислен")

    def on_floor():
        try:
            val = parse_display_value()
            res = math.floor(val)
        except Exception as e:
            display.delete(0, tk.END)
            display.insert(0, "Error")
            set_status(f"floor: {e}")
            return
        display.delete(0, tk.END)
        display.insert(0, str(res))
        set_status("floor выполнен")

    mem_menu = tk.Menu(root, tearoff=0)

    def mem_add():
        try:
            val = parse_display_value()
            memory["value"] += val
            set_status(f"M+ : {memory['value']}")
        except Exception as e:
            set_status(f"M+: {e}")

    def mem_sub():
        try:
            val = parse_display_value()
            memory["value"] -= val
            set_status(f"M- : {memory['value']}")
        except Exception as e:
            set_status(f"M-: {e}")

    def mem_recall():
        display.delete(0, tk.END)
        v = memory["value"]
        if float(v).is_integer():
            display.insert(0, str(int(v)))
        else:
            display.insert(0, str(v))
        set_status("MR: значение вставлено")

    def mem_clear():
        memory["value"] = 0.0
        set_status("MC: память очищена")

    mem_menu.add_command(label="M+", command=mem_add)
    mem_menu.add_command(label="M-", command=mem_sub)
    mem_menu.add_command(label="MR", command=mem_recall)
    mem_menu.add_command(label="MC", command=mem_clear)

    def on_memory_button(event=None, widget=None):
        if widget is None:
            widget = root
        try:
            x = widget.winfo_rootx()
            y = widget.winfo_rooty() + widget.winfo_height()
            mem_menu.tk_popup(x, y)
        finally:
            mem_menu.grab_release()

    buttons = []
    for index, label in enumerate(BUTTON_LABELS):
        row = 1 + (index // 3)
        col = index % 3

        btn = tk.Button(
            main_frame,
            text=label,
            width=6,
            height=2,
            font=("Arial", 14),
        )

        if label == "+":
            btn.config(command=on_add)
        elif label == "*":
            btn.config(command=on_multiply)
        elif label == "%":
            btn.config(command=on_modulo)
        elif label == "cos":
            btn.config(command=on_cos)
        elif label == "√":
            btn.config(command=on_sqrt)
        elif label == "ceil":
            btn.config(command=on_ceil)
        if label == "-":
            btn.config(command=on_subtract)
        elif label == "/":
            btn.config(command=on_divide)
        elif label == "sin":
            btn.config(command=on_sin)
        elif label == "^":
            btn.config(command=on_power)
        elif label == "floor":
            btn.config(command=on_floor)
        elif label == "M":
            btn.bind("<Button-1>", lambda e, w=btn: on_memory_button(e, w))

        btn.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
        buttons.append(btn)

    for c in range(3):
        main_frame.grid_columnconfigure(c, weight=1)
    for r in range(1, 3):
        main_frame.grid_rowconfigure(r, weight=1)

    def on_enter(event=None):
        expr = display.get().strip()
        if not expr:
            set_status("Пусто")
            return "break"
        try:
            val = safe_eval(expr)
        except Exception as e:
            display.delete(0, tk.END)
            display.insert(0, "Error")
            set_status(str(e))
            return "break"
        if isinstance(val, (int, float)) and float(val).is_integer():
            display.delete(0, tk.END)
            display.insert(0, str(int(val)))
        else:
            display.delete(0, tk.END)
            display.insert(0, str(val))
        set_status("Вычислено")
        return "break"

    display.bind("<Return>", on_enter)
    display.bind("<KP_Enter>", on_enter)

    return {
        "root": root,
        "display": display,
        "buttons": buttons,
        "memory": memory,
        "status": status,
    }


def main():
    root = tk.Tk()
    ui = create_ui(root)
    ui["display"].focus_set()
    root.mainloop()


if __name__ == "__main__":
    main()
