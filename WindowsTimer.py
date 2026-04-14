import tkinter as tk
from tkinter import messagebox, ttk
import os


BG_COLOR = "#0F172A"
CARD_COLOR = "#1E293B"
ACCENT = "#38BDF8"
SUCCESS = "#10B981"
DANGER = "#F43F5E"
TEXT = "#F8FAFC"
SUBTEXT = "#94A3B8"
INPUT_BG = "#020617"

COMMANDS = {
    "Вимкнення": "shutdown -s -t",
    "Перезавантаження": "shutdown -r -t",
    "Сон (Sleep)": "rundll32.exe powrprof.dll,SetSuspendState 0,1,0"
}

remaining_seconds = 0
timer_job = None


def update_countdown():
    global remaining_seconds, timer_job
    if remaining_seconds > 0:
        mins = remaining_seconds // 60
        secs = remaining_seconds % 60
        lbl_countdown.config(text=f"{mins:02}:{secs:02}")
        remaining_seconds -= 1
        timer_job = root.after(1000, update_countdown)
    else:
        lbl_countdown.config(text="00:00")
        timer_job = None
        action_name = combo_action.get()
        if action_name == "Сон (Sleep)":
            os.system(COMMANDS["Сон (Sleep)"])

def cancel_timer(silent=False):
    global timer_job, remaining_seconds
    os.system("shutdown -a")
    if timer_job:
        root.after_cancel(timer_job)
        timer_job = None
    remaining_seconds = 0
    lbl_countdown.config(text="--:--")
    if not silent:
        lbl_status.config(text="● Таймер зупинено", fg=SUBTEXT)

def start_logic(minutes):
    global remaining_seconds, timer_job
    try:
        minutes = int(minutes)
        if minutes < 0: raise ValueError
        cancel_timer(True)
        action_name = combo_action.get()
        seconds = minutes * 60
        force = "-f" if var_force.get() else ""

        if action_name == "Сон (Sleep)":
            lbl_status.config(text=f"● Сон через {minutes} хв", fg=ACCENT)
        else:
            action_cmd = COMMANDS[action_name]
            os.system(f"{action_cmd} {seconds} {force}")
            lbl_status.config(text=f"● {action_name} активовано", fg=DANGER)

        remaining_seconds = seconds
        update_countdown()
    except ValueError:
        messagebox.showerror("Помилка", "Введи число хвилин")


root = tk.Tk()
root.title("Windows Timer")
root.geometry("400x620")
root.configure(bg=BG_COLOR)
root.resizable(False, False)


style = ttk.Style()
style.theme_use('clam')
style.configure("TCombobox", fieldbackground=INPUT_BG, background=CARD_COLOR,
                foreground=TEXT, bordercolor=CARD_COLOR, arrowcolor=ACCENT)


tk.Label(root, text="⚡ WINDOWS TIMER", font=("Inter", 18, "bold"),
         bg=BG_COLOR, fg=ACCENT).pack(pady=(25, 5))
tk.Label(root, text="Керування часом роботи ПК", font=("Inter", 9),
         bg=BG_COLOR, fg=SUBTEXT).pack(pady=(0, 20))


card = tk.Frame(root, bg=CARD_COLOR, bd=0, highlightthickness=1, highlightbackground="#334155")
card.pack(padx=30, pady=10, fill="x")

inner = tk.Frame(card, bg=CARD_COLOR)
inner.pack(padx=20, pady=20)

tk.Label(inner, text="Оберіть дію:", font=("Inter", 9, "bold"),
         bg=CARD_COLOR, fg=SUBTEXT).pack(anchor="w")

combo_action = ttk.Combobox(inner, values=list(COMMANDS.keys()), state="readonly", font=("Inter", 10))
combo_action.current(0)
combo_action.pack(fill="x", pady=(8, 15))

var_force = tk.BooleanVar()
chk = tk.Checkbutton(inner, text="Примусове закриття", variable=var_force,
                     bg=CARD_COLOR, fg=TEXT, activebackground=CARD_COLOR,
                     activeforeground=ACCENT, selectcolor=INPUT_BG,
                     font=("Inter", 9), cursor="hand2")
chk.pack(anchor="w")


tk.Label(root, text="ХВИЛИНИ", font=("Inter", 8, "bold"),
         bg=BG_COLOR, fg=SUBTEXT).pack(pady=(20, 0))

entry = tk.Entry(root, font=("Consolas", 28, "bold"), justify="center",
                 bg=INPUT_BG, fg=TEXT, insertbackground=ACCENT,
                 relief="flat", borderwidth=0)
entry.insert(0, "60")
entry.pack(pady=10, padx=80, fill="x")


btn_frame = tk.Frame(root, bg=BG_COLOR)
btn_frame.pack(pady=5)

for t in [15, 30, 60]:
    b = tk.Button(btn_frame, text=f"{t}m", command=lambda x=t: start_logic(x),
                  bg=CARD_COLOR, fg=TEXT, font=("Inter", 9, "bold"),
                  relief="flat", width=6, cursor="hand2",
                  activebackground=ACCENT, activeforeground=BG_COLOR)
    b.pack(side="left", padx=4)

btn_start = tk.Button(root, text="ЗАПУСТИТИ ТАЙМЕР",
                      command=lambda: start_logic(entry.get()),
                      bg=ACCENT, fg=BG_COLOR, font=("Inter", 10, "bold"),
                      relief="flat", height=2, cursor="hand2",
                      activebackground=TEXT)
btn_start.pack(padx=30, pady=(25, 10), fill="x")

btn_stop = tk.Button(root, text="СКАСУВАТИ ВСЕ", command=cancel_timer,
                     bg=BG_COLOR, fg=DANGER, font=("Inter", 10, "bold"),
                     relief="flat", cursor="hand2", activeforeground=TEXT,
                     activebackground=BG_COLOR)
btn_stop.pack(padx=30, pady=0, fill="x")


status_frame = tk.Frame(root, bg=BG_COLOR)
status_frame.pack(side="bottom", fill="x", pady=20)

lbl_status = tk.Label(status_frame, text="● Система готова", font=("Inter", 9),
                      bg=BG_COLOR, fg=SUBTEXT)
lbl_status.pack()

lbl_countdown = tk.Label(status_frame, text="--:--",
                         font=("Consolas", 24, "bold"),
                         bg=BG_COLOR, fg=TEXT)
lbl_countdown.pack()

def privet():
    messagebox.showinfo("🇺🇦", "Слава Україні!")

tk.Button(root, text="🇺🇦", command=privet, bg=BG_COLOR, fg="#EAB308",
          relief="flat", font=("Inter", 12), cursor="hand2",
          activebackground=BG_COLOR).place(x=10, y=575)

root.mainloop()