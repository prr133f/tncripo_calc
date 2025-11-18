import tkinter as tk

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


def create_ui(root: tk.Tk):
    root.title("Калькулятор")
    root.resizable(False, False)

    main_frame = tk.Frame(root, padx=8, pady=8)
    main_frame.pack(fill=tk.BOTH, expand=True)

    display = tk.Entry(main_frame, font=("Arial", 20), justify="right")
    display.grid(row=0, column=0, columnspan=3, sticky="we", pady=(0, 8))

    buttons = []
    for index, label in enumerate(BUTTON_LABELS):
        row = 1 + (index // 3)  # строки 1..4
        col = index % 3  # столбцы 0..2

        btn = tk.Button(
            main_frame,
            text=label,
            width=6,
            height=2,
            font=("Arial", 14),
            # command=
        )
        btn.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
        buttons.append(btn)

    for c in range(3):
        main_frame.grid_columnconfigure(c, weight=1)

    return {"root": root, "display": display, "buttons": buttons}


def main():
    root = tk.Tk()
    ui = create_ui(root)

    ui["display"].focus_set()

    root.mainloop()


if __name__ == "__main__":
    main()
