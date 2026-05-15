import tkinter as tk
from tkinter import messagebox, ttk
import os
import json


CONFIG_FILE = "timer_settings.json"
LANGS = {
    "UA": {
        "title": "⚡ WINDOWS TIMER",
        "subtitle": "Керування часом роботи ПК",
        "action_lbl": "Оберіть дію:",
        "force_chk": "Примусово закрити вікна",
        "start_btn": "ЗАПУСТИТИ ТАЙМЕР",
        "stop_btn": "СКАСУВАТИ ВСЕ",
        "h": "ГОД", "m": "ХВ", "s": "СЕК",
        "status_ready": "● Система готова",
        "status_active": "● {} активовано",
        "status_stop": "● Таймер зупинено",
        "err_title": "Помилка формату",
        "err_msg": "Введіть число!\nПриклад: 0.5 або 10",
        "actions": ["Вимкнення", "Перезавантаження", "Сон"]
    },
    "EN": {
        "title": "⚡ WINDOWS TIMER",
        "subtitle": "PC Time Management",
        "action_lbl": "Select action:",
        "force_chk": "Force close apps",
        "start_btn": "START TIMER",
        "stop_btn": "CANCEL ALL",
        "h": "HRS", "m": "MIN", "s": "SEC",
        "status_ready": "● System ready",
        "status_active": "● {} activated",
        "status_stop": "● Timer stopped",
        "err_title": "Format Error",
        "err_msg": "Enter a number!\nExample: 0.5 or 10",
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


def save_settings():
    data = {
        "lang": current_lang,
        "action_idx": combo_action.current(),
        "force": var_force.get(),
        "h": ent_hrs.get(), "m": ent_mins.get(), "s": ent_secs.get()
    }
    with open(CONFIG_FILE, "w") as f: json.dump(data, f)


def load_settings():
    global current_lang
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                d = json.load(f)
                current_lang = d.get("lang", "UA")
                var_force.set(d.get("force", False))
                for e, k in zip([ent_hrs, ent_mins, ent_secs], ["h", "m", "s"]):
                    e.delete(0, "end");
                    e.insert(0, d.get(k, "0"))
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
    combo_action['values'] = l["actions"]
    for lbl, k in zip(unit_labels, ["h", "m", "s"]): lbl.config(text=l[k])
    if remaining_seconds == 0: lbl_status.config(text=l["status_ready"])


def switch_lang(lang):
    global current_lang
    current_lang = lang
    update_ui_text()
    save_settings()


def sync_command():
    if remaining_seconds > 0:
        os.system("shutdown -a")
        idx = combo_action.current()
        if idx != 2:  # Не Сон
            f = "-f" if var_force.get() else ""
            os.system(f"{COMMANDS_MAP[idx]} {remaining_seconds} {f}")
        lbl_status.config(text=LANGS[current_lang]["status_active"].format(combo_action.get()), fg=ACCENT)


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
        if combo_action.current() == 2: os.system(COMMANDS_MAP[2])


def start_timer(m_val=None):
    global remaining_seconds
    try:
        h = float(ent_hrs.get().replace(",", ".") or 0) if m_val is None else 0
        m = float(ent_mins.get().replace(",", ".") or 0) if m_val is None else m_val
        s = float(ent_secs.get().replace(",", ".") or 0) if m_val is None else 0

        total = int(h * 3600 + m * 60 + s)
        if total <= 0: return

        cancel_timer(True)
        remaining_seconds = total
        sync_command()
        update_timer()
        save_settings()
    except:
        messagebox.showerror(LANGS[current_lang]["err_title"], LANGS[current_lang]["err_msg"])


def cancel_timer(silent=False):
    global timer_job, remaining_seconds
    os.system("shutdown -a")
    if timer_job: root.after_cancel(timer_job); timer_job = None
    remaining_seconds = 0
    lbl_countdown.config(text="--:--:--")
    if not silent: lbl_status.config(text=LANGS[current_lang]["status_stop"], fg=SUBTEXT)



root = tk.Tk()
root.title("Windows Timer")
root.geometry("400x680")
root.configure(bg=BG_COLOR)


try:
    root.iconbitmap("icon.ico")
except:
    pass

lang_frame = tk.Frame(root, bg=BG_COLOR)
lang_frame.pack(anchor="ne", padx=10, pady=5)
for l in ["UA", "EN"]:
    tk.Button(lang_frame, text=l, command=lambda x=l: switch_lang(x), font=("Inter", 8, "bold"),
              bg=CARD_COLOR, fg=SUBTEXT, relief="flat", cursor="hand2").pack(side="left", padx=2)

lbl_title = tk.Label(root, font=("Inter", 18, "bold"), bg=BG_COLOR, fg=ACCENT)
lbl_title.pack(pady=(10, 5))
lbl_subtitle = tk.Label(root, font=("Inter", 9), bg=BG_COLOR, fg=SUBTEXT)
lbl_subtitle.pack()

card = tk.Frame(root, bg=CARD_COLOR, bd=0, highlightthickness=1, highlightbackground="#334155")
card.pack(padx=30, pady=20, fill="x")
inner = tk.Frame(card, bg=CARD_COLOR)
inner.pack(padx=20, pady=20)

lbl_act_title = tk.Label(inner, font=("Inter", 9, "bold"), bg=CARD_COLOR, fg=SUBTEXT)
lbl_act_title.pack(anchor="w")

style = ttk.Style()
style.theme_use('clam')
style.configure("TCombobox", fieldbackground=INPUT_BG, background=CARD_COLOR, foreground=TEXT, bordercolor=CARD_COLOR,
                arrowcolor=ACCENT)
style.map("TCombobox", fieldbackground=[("readonly", INPUT_BG)], foreground=[("readonly", TEXT)])

combo_action = ttk.Combobox(inner, state="readonly", font=("Inter", 10))
combo_action.pack(fill="x", pady=(8, 15))
combo_action.bind("<<ComboboxSelected>>", lambda e: [sync_command(), save_settings()])

var_force = tk.BooleanVar()
chk_force = tk.Checkbutton(inner, variable=var_force, bg=CARD_COLOR, fg=TEXT, activebackground=CARD_COLOR,
                           selectcolor=INPUT_BG, font=("Inter", 9), command=lambda: [sync_command(), save_settings()])
chk_force.pack(anchor="w")

time_frame = tk.Frame(root, bg=BG_COLOR)
time_frame.pack(pady=10)
unit_labels = []


def create_input(label):
    f = tk.Frame(time_frame, bg=BG_COLOR)
    f.pack(side="left", padx=10)
    l = tk.Label(f, text=label, font=("Inter", 7, "bold"), bg=BG_COLOR, fg=SUBTEXT)
    l.pack();
    unit_labels.append(l)
    e = tk.Entry(f, font=("Consolas", 18, "bold"), justify="center", width=4, bg=INPUT_BG, fg=TEXT, relief="flat",
                 insertbackground=ACCENT)
    e.pack(pady=5);
    return e


ent_hrs, ent_mins, ent_secs = create_input("H"), create_input("M"), create_input("S")

btn_start = tk.Button(root, command=start_timer, bg=ACCENT, fg=BG_COLOR, font=("Inter", 10, "bold"), relief="flat",
                      height=2, cursor="hand2")
btn_start.pack(padx=30, pady=(20, 10), fill="x")
btn_stop = tk.Button(root, command=cancel_timer, bg=BG_COLOR, fg=DANGER, font=("Inter", 10, "bold"), relief="flat",
                     cursor="hand2")
btn_stop.pack(padx=30, fill="x")

lbl_status = tk.Label(root, font=("Inter", 9), bg=BG_COLOR, fg=SUBTEXT)
lbl_status.pack(side="bottom", pady=(0, 10))
lbl_countdown = tk.Label(root, text="--:--:--", font=("Consolas", 28, "bold"), bg=BG_COLOR, fg=TEXT)
lbl_countdown.pack(side="bottom", pady=10)

load_settings()
root.protocol("WM_DELETE_WINDOW", lambda: [cancel_timer(True), root.destroy()])
root.mainloop()