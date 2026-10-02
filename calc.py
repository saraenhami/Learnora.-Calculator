import tkinter as tk
from tkinter import messagebox
import math
import re

root = tk.Tk()
root.title("Learnora. Calculator")
root.iconbitmap("bd870471-eb4a-492f-adb1-7e8de085a510-8.ico")
root.geometry("360x610")
root.resizable(False, False)

LIGHT_THEME = {
    "bg": "#A77FCC",
    "entry_bg": "#FFFFFF",
    "history_bg": "#D8C7E6",
    "btn": "#9e83b1",
    "hover": "#b19ec0",
    "special": "#664E76",
    "text": "black"
}

DARK_THEME = {
    "bg": "#2E2A3B",
    "entry_bg": "#3C3750",
    "history_bg": "#4A4560",
    "btn": "#5E5A78",
    "hover": "#6F6A8F",
    "special": "#8E86B5",
    "text": "white"
}

current_theme = LIGHT_THEME

def apply_theme():
    root.configure(bg=current_theme["bg"])
    entry.configure(bg=current_theme["entry_bg"], fg=current_theme["text"])
    history_box.configure(bg=current_theme["history_bg"], fg=current_theme["text"])
    history_label.configure(bg=current_theme["bg"], fg=current_theme["text"])
    frame.configure(bg=current_theme["bg"])
    bottom_label.configure(bg=current_theme["bg"], fg=current_theme["text"])
    top_bar.configure(bg=current_theme["bg"])
    learnora_label.configure(bg=current_theme["bg"], fg=current_theme["text"])
    sticker_label.configure(bg=current_theme["bg"], fg=current_theme["text"])

def toggle_theme():
    global current_theme
    current_theme = DARK_THEME if current_theme == LIGHT_THEME else LIGHT_THEME
    apply_theme()

entry = tk.Entry(
    root,
    bd=0,
    highlightthickness=4,
    font=("Arial", 26),
    justify="right"
)
entry.pack(padx=10, pady=20, fill="x", ipady=20)

top_bar = tk.Frame(root)
top_bar.pack(fill="x", padx=10)

tk.Button(top_bar, text="🌙", command=toggle_theme).pack(side="left")

learnora_label = tk.Label(
    top_bar,
    text="✨ Learnora. ✨",
    font=("Comic Sans MS", 14, "bold")
)
learnora_label.pack(side="left", expand=True)

tk.Button(
    top_bar,
    text="ℹ️",
    command=lambda: messagebox.showinfo(
        "About Learnora.",
        "💜 Learnora. Calculator 💜\n"
        "Made with love using Python & Tkinter.\n"
        "Designed to make math fun, friendly, and cute! 😎✨"
    )
).pack(side="right")

history = []

history_label = tk.Label(root, text="History", font=("Arial", 11, "bold"))
history_label.pack()

history_box = tk.Listbox(root, height=5, font=("Arial", 10), bd=0)
history_box.pack(padx=10, pady=5, fill="x")

def clear_history():
    history.clear()
    history_box.delete(0, tk.END)

tk.Button(root, text="🗑 Clear History", command=clear_history).pack(pady=5)

facts = {
    0: "Zero represents nothing, but changed math forever! 🔢",
    1: "One is the loneliest number, but also the start of everything!🌟",
    2: "There are 2 eyes, 2 ears, 2 hands… symmetry is everywhere!👀✋",
    3: "3 is a magical number in many cultures! ✨",
    3.14: "Pi! The ratio of a circle’s circumference to its diameter.🥧🔵",
    4: "Four seasons make our year colorful!🍁❄️🌸☀️",
    5: "High five!🖐️ Did you know humans have 5 fingers per hand?",
    6: "Six legs? Ants have them! 🐜",
    6.7: "Interesting! 6.7 cm is roughly the length of a baby hummingbird at birth!🐦",
    7: "There are 7 continents on Earth!🌎",
    7.5: "The average human walking speed is about 7.5 km/h! 🚶",
    8: "Spiders have 8 legs!🕷️",
    9: "Cats supposedly have 9 lives!🐱",
    9.81: "Earth’s gravity pulls objects down at about 9.81 m/s²!🌍",
    10: "10 fingers and 10 toes – perfect for counting!🖐️🖐️",
    12: "12 months in a year, 12 zodiac signs!📅♈",
    24: "24 hours in a day – time waits for no one!⏰",
    32: "32 teeth in a full adult human mouth!😁",
    42: "42 is the Answer to the Ultimate Question of Life, the Universe, and Everything!😏",
    50: "There are 50 stars on the United States flag! 🇺🇸",
    60: "There are 60 seconds in a minute and 60 minutes in an hour!⏱️",
    100: "100°C is the boiling point of water!💧",
    360: "360 degrees complete a full circle!🔵",
    365: "365 days in a year – time flies!⏳",
    6371: "The approximate radius of Earth in km!🌍",
    149600000: "The distance from Earth to the Sun is about 149.6 million km!☀️",
    1000: "1,000 is a thousand! Big numbers, big dreams!💫",
    1000000: "1 million! That’s a lot of stars in a small patch of the night sky!✨",
    42.195: "The length of a marathon in kilometers!🏃‍♀️",
    299792458: "The speed of light in m/s – literally the fastest thing in the universe!⚡"
}

def show_fact(result):
    try:
        number = float(result)
        if number in facts:
            messagebox.showinfo("Fun Fact!", facts[number])
    except:
        pass

def add_to_history(expr, result):
    history.append(f"{expr} = {result}")
    if len(history) > 5:
        history.pop(0)
    history_box.delete(0, tk.END)
    for item in history:
        history_box.insert(tk.END, item)

def is_safe(expr):
    return re.fullmatch(r"[0-9+\-*/(). ]+", expr)

def button_clicked(value):
    if value == "x":
        value = "*"
    entry.insert(tk.END, value)

def clear():
    entry.delete(0, tk.END)

def backspace():
    entry.delete(len(entry.get()) - 1, tk.END)

def calculate():
    expr = entry.get()
    if not expr or not is_safe(expr):
        entry.delete(0, tk.END)
        entry.insert(0, "Invalid input")
        return
    try:
        result = eval(expr)
        add_to_history(expr, result)
        entry.delete(0, tk.END)
        entry.insert(0, result)
        show_fact(result)
    except ZeroDivisionError:
        entry.delete(0, tk.END)
        entry.insert(0, "Division by zero")
    except:
        entry.delete(0, tk.END)
        entry.insert(0, "Math error")

def square():
    try:
        v = float(entry.get())
        r = v ** 2
        add_to_history(f"{v}²", r)
        entry.delete(0, tk.END)
        entry.insert(0, r)
        show_fact(r)
    except:
        entry.insert(0, "Invalid")

def sqrt():
    try:
        v = float(entry.get())
        r = math.sqrt(v)
        add_to_history(f"√{v}", r)
        entry.delete(0, tk.END)
        entry.insert(0, r)
        show_fact(r)
    except:
        entry.insert(0, "Invalid")

def percent():
    try:
        v = float(entry.get())
        r = v / 100
        add_to_history(f"{v}%", r)
        entry.delete(0, tk.END)
        entry.insert(0, r)
        show_fact(r)
    except:
        entry.insert(0, "Invalid")

frame = tk.Frame(root)
frame.pack(expand=True, fill="both", padx=5, pady=5)

for i in range(6):
    frame.rowconfigure(i, weight=1)
for j in range(4):
    frame.columnconfigure(j, weight=1)

def make_button(text, row, col, cmd, color=None):
    b = tk.Button(
        frame,
        text=text,
        fg="white",
        bg=color if color else current_theme["btn"],
        activebackground=current_theme["hover"],
        font=("Arial", 15, "bold"),
        command=cmd
    )
    b.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
    return b

buttons = [
    ("x²", 0, 0, square, None),
    ("√", 0, 1, sqrt, None),
    ("%", 0, 2, percent, None),
    ("⌫", 0, 3, backspace, None),

    ("(", 1, 0, lambda: button_clicked("("), None),
    (")", 1, 1, lambda: button_clicked(")"), None),
    ("/", 1, 2, lambda: button_clicked("/"), None),
    ("C", 1, 3, clear, "#d88d8d"),

    ("7", 2, 0, lambda: button_clicked("7"), None),
    ("8", 2, 1, lambda: button_clicked("8"), None),
    ("9", 2, 2, lambda: button_clicked("9"), None),
    ("x", 2, 3, lambda: button_clicked("x"), None),

    ("4", 3, 0, lambda: button_clicked("4"), None),
    ("5", 3, 1, lambda: button_clicked("5"), None),
    ("6", 3, 2, lambda: button_clicked("6"), None),
    ("-", 3, 3, lambda: button_clicked("-"), None),

    ("1", 4, 0, lambda: button_clicked("1"), None),
    ("2", 4, 1, lambda: button_clicked("2"), None),
    ("3", 4, 2, lambda: button_clicked("3"), None),
    ("+", 4, 3, lambda: button_clicked("+"), None),

    ("0", 5, 0, lambda: button_clicked("0"), None),
    (".", 5, 1, lambda: button_clicked("."), None),
    ("=", 5, 2, calculate, current_theme["special"]),
]

for t, r, c, cmd, color in buttons:
    make_button(t, r, c, cmd, color)

sticker_label = tk.Label(
    frame,
    text="🧸",
    font=("Arial", 30)
)
sticker_label.grid(row=5, column=3, sticky="nsew")

bottom_label = tk.Label(
    root,
    text="💖 ૮₍ ˶ᵔ ᵕ ᵔ˶ ₎ა  Made with love & math fun! ✨",
    font=("Arial", 10)
)
bottom_label.pack(pady=8)

root.bind("<Return>", lambda e: calculate())
root.bind("<BackSpace>", lambda e: backspace())

apply_theme()
root.mainloop()
