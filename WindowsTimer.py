import tkinter as tk
from tkinter import messagebox, ttk
import os
import json
import ctypes
import sys
def resource_path(relative_path):
    try:

        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


icon_path = resource_path("icon.png")
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except:
        pass
CONFIG_FILE = "timer_settings.json"

LANGS = {
    "UA": {
        "title": "⚡ WINDOWS TIMER",
        "subtitle": "Керування часом роботи ПК",
        "action_lbl": "Оберіть дію:",
        "force_chk": "Примусово закрити вікна",
        "start_btn": "ЗАПУСТИТИ ТАЙМЕР",
        "stop_btn": "СКАСУВАТИ ВСЕ",
        "settings_btn": "⚙ Налаштування",
        "settings_title": "Налаштування",
        "lang": "Мова:",
        "save_last": "Зберігати останні значення",
        "default_h": "Години:",
        "default_m": "Хвилини:",
        "default_s": "Секунди:",
        "save_btn": "Зберегти",
        "h": "ГОД",
        "m": "ХВ",
        "s": "СЕК",
        "status_ready": "● Система готова.",
        "status_active": "● {} активовано",
        "status_stop": "● Таймер зупинено",
        "err_title": "Помилка формату",
        "err_msg": "Введіть тільки числа!\nПриклад: 0.5 або 10",
        "actions": ["Вимкнення", "Перезавантаження", "Сон"]
    },

    "EN": {
        "title": "⚡ WINDOWS TIMER",
        "subtitle": "PC Time Management",
        "action_lbl": "Select action:",
        "force_chk": "Force close apps",
        "start_btn": "START TIMER",
        "stop_btn": "CANCEL ALL",
        "settings_btn": "⚙ Settings",
        "settings_title": "Settings",
        "lang": "Language:",
        "save_last": "Save last values",
        "default_h": "Hours:",
        "default_m": "Minutes:",
        "default_s": "Seconds:",
        "save_btn": "Save",
        "h": "HRS",
        "m": "MIN",
        "s": "SEC",
        "status_ready": "● System ready",
        "status_active": "● {} activated",
        "status_stop": "● Timer stopped",
        "err_title": "Format Error",
        "err_msg": "Enter numbers only!\nExample: 0.5 or 10",
        "actions": ["Shutdown", "Restart", "Sleep"]
    }
}

BG_COLOR, CARD_COLOR, ACCENT, DANGER, TEXT, SUBTEXT, INPUT_BG = \
    "#0F172A", "#1E293B", "#38BDF8", "#F43F5E", "#F8FAFC", "#94A3B8", "#020617"

COMMANDS_MAP = {
    0: "shutdown -s -t",
    1: "shutdown -r -t",
    2: "rundll32.exe powrprof.dll,SetSuspendState 0,1,0"
}

remaining_seconds = 0
timer_job = None
current_lang = "UA"

save_last_values = True
default_values = {"h": "0", "m": "0", "s": "0"}

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
def validate_input(value):

    if value == "":
        return True

    allowed = "0123456789"

    return all(c in allowed for c in value)


def save_settings():
    data = {
        "lang": current_lang,
        "action_idx": combo_action.current(),
        "force": var_force.get(),
        "save_last": save_last_values,
        "default_values": default_values
    }


    if save_last_values:
        data["h"] = ent_hrs.get()
        data["m"] = ent_mins.get()
        data["s"] = ent_secs.get()


    else:
        data["h"] = default_values["h"]
        data["m"] = default_values["m"]
        data["s"] = default_values["s"]

    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f)

def load_settings():
    global current_lang, save_last_values, default_values

    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                d = json.load(f)

                current_lang = d.get("lang", "UA")
                var_force.set(d.get("force", False))

                save_last_values = d.get("save_last", True)

                default_values = d.get("default_values", {
                    "h": "0",
                    "m": "0",
                    "s": "0"
                })


                if save_last_values:
                    values = {
                        "h": d.get("h", "0"),
                        "m": d.get("m", "0"),
                        "s": d.get("s", "0")
                    }


                else:
                    values = default_values

                for e, k in zip(
                    [ent_hrs, ent_mins, ent_secs],
                    ["h", "m", "s"]
                ):
                    e.delete(0, "end")
                    e.insert(0, values[k])

                combo_action.current(d.get("action_idx", 0))

        except:
            pass

    update_ui_text()
def update_ui_text():
    l = LANGS[current_lang]

    lbl_title.config(text=l["title"])
    lbl_subtitle.config(text=l["subtitle"])
    lbl_act_title.config(text=l["action_lbl"])
    chk_force.config(text=l["force_chk"])
    btn_start.config(text=l["start_btn"])
    btn_stop.config(text=l["stop_btn"])
    btn_settings.config(text=l["settings_btn"])

    combo_action['values'] = l["actions"]
    if combo_action.current() == -1:
        combo_action.current(0)

    for lbl, k in zip(unit_labels, ["h", "m", "s"]):
        lbl.config(text=l[k])

    if remaining_seconds == 0:
        lbl_status.config(text=l["status_ready"])


def switch_lang(lang):
    global current_lang
    current_lang = lang
    update_ui_text()
    save_settings()


def sync_command():
    if remaining_seconds > 0:

        os.system("shutdown -a")

        idx = combo_action.current()

        if idx != 2:
            f = "-f" if var_force.get() else ""
            os.system(f"{COMMANDS_MAP[idx]} {remaining_seconds} {f}")

        lbl_status.config(
            text=LANGS[current_lang]["status_active"].format(combo_action.get()),
            fg=ACCENT
        )


def update_timer():
    global remaining_seconds, timer_job

    if remaining_seconds > 0:

        hrs, rem = divmod(remaining_seconds, 3600)
        mins, secs = divmod(rem, 60)

        lbl_countdown.config(text=f"{hrs:02}:{mins:02}:{secs:02}")

        remaining_seconds -= 1

        timer_job = root.after(1000, update_timer)

    else:

        lbl_countdown.config(text="00:00:00")

        if combo_action.current() == 2:
            os.system(COMMANDS_MAP[2])


def start_timer(m_val=None):
    global remaining_seconds

    try:
        h = float(ent_hrs.get().replace(",", ".") or 0) if m_val is None else 0
        m = float(ent_mins.get().replace(",", ".") or 0) if m_val is None else m_val
        s = float(ent_secs.get().replace(",", ".") or 0) if m_val is None else 0

        total = int(h * 3600 + m * 60 + s)

        if total <= 0:
            return

        cancel_timer(True)

        remaining_seconds = total

        sync_command()

        update_timer()

        save_settings()

    except:
        messagebox.showerror(
            LANGS[current_lang]["err_title"],
            LANGS[current_lang]["err_msg"]
        )


def cancel_timer(silent=False):
    global timer_job, remaining_seconds

    os.system("shutdown -a")

    if timer_job:
        root.after_cancel(timer_job)
        timer_job = None

    remaining_seconds = 0

    lbl_countdown.config(text="--:--:--")

    if not silent:
        lbl_status.config(
            text=LANGS[current_lang]["status_stop"],
            fg=SUBTEXT
        )


def open_settings():
    win = tk.Toplevel(root)
    win.title(LANGS[current_lang]["settings_title"])
    win.geometry("320x399")
    win.configure(bg=BG_COLOR)


    icon_path_settings = resource_path("icon.png")
    try:
        settings_icon = tk.PhotoImage(file=icon_path_settings)
        win.iconphoto(False, settings_icon)
        win.settings_icon = settings_icon
    except Exception as e:
        print(f"Не вдалося завантажити іконку налаштувань: {e}")

    tk.Label(
        win,
        text=LANGS[current_lang]["lang"],
        bg=BG_COLOR,
        fg=TEXT,
        font=("Inter", 10, "bold")
    ).pack(anchor="w", padx=20, pady=(20, 5))

    lang_combo = ttk.Combobox(
        win,
        values=["UA", "EN"],
        state="readonly"
    )

    lang_combo.pack(fill="x", padx=20)

    lang_combo.set(current_lang)

    save_var = tk.BooleanVar(value=save_last_values)

    tk.Checkbutton(
        win,
        text=LANGS[current_lang]["save_last"],
        variable=save_var,
        bg=BG_COLOR,
        fg=TEXT,
        activebackground=BG_COLOR,
        selectcolor=INPUT_BG
    ).pack(anchor="w", padx=20, pady=15)

    entries = {}

    for key, label in [
        ("h", LANGS[current_lang]["default_h"]),
        ("m", LANGS[current_lang]["default_m"]),
        ("s", LANGS[current_lang]["default_s"])
    ]:

        tk.Label(
            win,
            text=label,
            bg=BG_COLOR,
            fg=TEXT
        ).pack(anchor="w", padx=20)

        e = tk.Entry(
            win,
            bg=INPUT_BG,
            fg=TEXT,
            relief="flat",
            validate="key",
            validatecommand=(root.register(validate_input), "%P")
        )

        e.pack(fill="x", padx=20, pady=(0, 10))

        e.insert(0, default_values[key])

        entries[key] = e

    def save_all():

        global save_last_values, default_values

        save_last_values = save_var.get()

        default_values = {
            "h": entries["h"].get() or "0",
            "m": entries["m"].get() or "0",
            "s": entries["s"].get() or "0"
        }

        switch_lang(lang_combo.get())
        if not save_last_values:
            ent_hrs.delete(0, "end")
            ent_hrs.insert(0, default_values["h"])

            ent_mins.delete(0, "end")
            ent_mins.insert(0, default_values["m"])

            ent_secs.delete(0, "end")
            ent_secs.insert(0, default_values["s"])

        save_settings()

        save_settings()

        win.destroy()

    tk.Button(
        win,
        text=LANGS[current_lang]["save_btn"],
        command=save_all,
        bg=ACCENT,
        fg=BG_COLOR,
        relief="flat",
        font=("Segoe UI", 10, "bold")
    ).pack(fill="x", padx=20, pady=20)


root = tk.Tk()
icon_path = resource_path("icon.png")

icon = tk.PhotoImage(file=icon_path)
root.iconphoto(True, icon)
root.title("Windows Timer")

root.geometry("400x680")

root.configure(bg=BG_COLOR)




lbl_title = tk.Label(
    root,
    font=("Segoe UI", 10, "bold"),
    bg=BG_COLOR,
    fg=ACCENT
)

lbl_title.pack(pady=(15, 5))

lbl_subtitle = tk.Label(
    root,
    font=("Segoe UI", 10, "bold"),
    bg=BG_COLOR,
    fg=SUBTEXT
)

lbl_subtitle.pack()

btn_settings = tk.Button(
    root,
    command=open_settings,
    bg=CARD_COLOR,
    fg=TEXT,
    relief="flat",
    cursor="hand2",
    font=("Segoe UI", 10, "bold")
)

btn_settings.pack(pady=10)

card = tk.Frame(
    root,
    bg=CARD_COLOR,
    bd=0,
    highlightthickness=1,
    highlightbackground="#334155"
)

card.pack(padx=30, pady=20, fill="x")

inner = tk.Frame(card, bg=CARD_COLOR)

inner.pack(padx=20, pady=20)

lbl_act_title = tk.Label(
    inner,
    font=("Segoe UI", 10, "bold"),
    bg=CARD_COLOR,
    fg=SUBTEXT
)

lbl_act_title.pack(anchor="w")

style = ttk.Style()

style.theme_use('clam')

style.configure(
    "TCombobox",
    fieldbackground=INPUT_BG,
    background=CARD_COLOR,
    foreground=TEXT,
    bordercolor=CARD_COLOR,
    arrowcolor=ACCENT
)

style.map(
    "TCombobox",
    fieldbackground=[("readonly", INPUT_BG)],
    foreground=[("readonly", TEXT)]
)

combo_action = ttk.Combobox(
    inner,
    state="readonly",
    font=("Segoe UI", 10, "bold")
)

combo_action.pack(fill="x", pady=(8, 15))

combo_action.bind(
    "<<ComboboxSelected>>",
    lambda e: [sync_command(), save_settings()]
)

var_force = tk.BooleanVar()

chk_force = tk.Checkbutton(
    inner,
    variable=var_force,
    bg=CARD_COLOR,
    fg=TEXT,
    activebackground=CARD_COLOR,
    selectcolor=INPUT_BG,
    font=("Inter", 9),
    command=lambda: [sync_command(), save_settings()]
)

chk_force.pack(anchor="w")

time_frame = tk.Frame(root, bg=BG_COLOR)

time_frame.pack(pady=10)
quick_frame = tk.Frame(root, bg=BG_COLOR)
quick_frame.pack(pady=5)

def quick_start(minutes):
    ent_hrs.delete(0, "end")
    ent_mins.delete(0, "end")
    ent_secs.delete(0, "end")

    ent_hrs.insert(0, "0")
    ent_mins.insert(0, str(minutes))
    ent_secs.insert(0, "0")

    start_timer()
tk.Button(
    quick_frame,
    text="15 MIN",
    command=lambda: quick_start(15),
    bg=CARD_COLOR,
    fg=TEXT,
    relief="flat",
    cursor="hand2"
).pack(side="left", padx=5)

tk.Button(
    quick_frame,
    text="30 MIN",
    command=lambda: quick_start(30),
    bg=CARD_COLOR,
    fg=TEXT,
    relief="flat",
    cursor="hand2"
).pack(side="left", padx=5)

tk.Button(
    quick_frame,
    text="60 MIN",
    command=lambda: quick_start(60),
    bg=CARD_COLOR,
    fg=TEXT,
    relief="flat",
    cursor="hand2"
).pack(side="left", padx=5)
unit_labels = []


def create_input(label):

    f = tk.Frame(time_frame, bg=BG_COLOR)

    f.pack(side="left", padx=10)

    l = tk.Label(
        f,
        text=label,
        font=("Inter", 7, "bold"),
        bg=BG_COLOR,
        fg=SUBTEXT
    )

    l.pack()

    unit_labels.append(l)

    e = tk.Entry(
        f,
        font=("Segoe UI", 10, "bold"),
        justify="center",
        width=4,
        bg=INPUT_BG,
        fg=TEXT,
        relief="flat",
        insertbackground=ACCENT,
        validate="key",
        validatecommand=(root.register(validate_input), "%P")
    )

    e.pack(pady=5)

    return e


ent_hrs = create_input("H")
ent_mins = create_input("M")
ent_secs = create_input("S")

btn_start = tk.Button(
    root,
    command=start_timer,
    bg=ACCENT,
    fg=BG_COLOR,
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    height=2,
    cursor="hand2"
)

btn_start.pack(padx=30, pady=(20, 10), fill="x")

btn_stop = tk.Button(
    root,
    command=cancel_timer,
    bg=BG_COLOR,
    fg=DANGER,
    font=("Inter", 10, "bold"),
    relief="flat",
    cursor="hand2"
)

btn_stop.pack(padx=30, fill="x")

lbl_status = tk.Label(
    root,
    font=("Inter", 9),
    bg=BG_COLOR,
    fg=SUBTEXT
)

lbl_status.pack(side="bottom", pady=(0, 10))

lbl_countdown = tk.Label(
    root,
    text="--:--:--",
    font=("Segoe UI", 10, "bold"),
    bg=BG_COLOR,
    fg=TEXT
)

lbl_countdown.pack(side="bottom", pady=10)

load_settings()

def on_close():

    save_settings()

    cancel_timer(True)

    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()