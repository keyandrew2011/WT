import tkinter as tk
from tkinter import messagebox, ttk
import os

BG_COLOR = "#0F172A"
CARD_COLOR = "#1E293B"
ACCENT = "#3B82F6"
SUCCESS = "#22C55E"
DANGER = "#EF4444"
TEXT = "#E2E8F0"
SUBTEXT = "#94A3B8"
BUTTON153060 = "#808080"

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
        lbl_countdown.config(text=f"Залишилось: {mins:02}:{secs:02}")
        remaining_seconds -= 1
        timer_job = root.after(1000, update_countdown)
    else:
        lbl_countdown.config(text="Час вийшов")
        timer_job = None

def cancel_timer(silent=False):
    global timer_job, remaining_seconds
    os.system("shutdown -a")
    if timer_job:
        root.after_cancel(timer_job)
        timer_job = None
    remaining_seconds = 0
    lbl_countdown.config(text="Залишилось: --:--")
    if not silent:
        lbl_status.config(text=" Таймер скасовано", fg=SUCCESS)

def start_logic(minutes):
    global remaining_seconds, timer_job
    try:
        if minutes < 0:
            raise ValueError

        cancel_timer(True)

        action_name = combo_action.get()
        action_cmd = COMMANDS[action_name]
        force = "-f" if var_force.get() else ""
        seconds = minutes * 60

        if action_name == "Сон (Sleep)":
            os.system(action_cmd)
            lbl_status.config(text="● ПК засинає...", fg=ACCENT)
        else:
            cmd = f"{action_cmd} {seconds} {force}"
            os.system(cmd)
            lbl_status.config(text=f"● {action_name} через {minutes} хв", fg=DANGER)
            remaining_seconds = seconds
            update_countdown()
            messagebox.showinfo("Таймер", f"Старий таймер скинуто.\nНовий: {action_name} через {minutes} хв")

    except ValueError:
        messagebox.showerror("Помилка", "Введи коректне число хвилин")

def set_timer15():
    start_logic(15)

def set_timer30():
    start_logic(30)

def set_timer60():
    start_logic(60)

def set_timer_custom():
    try:
        m = int(entry.get())
        start_logic(m)
    except ValueError:
        messagebox.showerror("Помилка", "Введи число (наприклад 60)")

def privet():
    messagebox.showinfo("🇺🇦", "Слава Україні!")
    print("Героям слава!")

root = tk.Tk()
root.title("Windows Timer")
root.geometry("420x600")
root.configure(bg=BG_COLOR)

tk.Label(root, text="⚡ WINDOWS TIMER", font=("Segoe UI", 20, "bold"),
         bg=BG_COLOR, fg=TEXT).pack(pady=15)

card = tk.Frame(root, bg=CARD_COLOR)
card.pack(padx=20, pady=10, fill="x")

inner = tk.Frame(card, bg=CARD_COLOR)
inner.pack(padx=20, pady=20)

tk.Label(inner, text="Дія", font=("Segoe UI", 10, "bold"),
         bg=CARD_COLOR, fg=TEXT).pack(anchor="w")

combo_action = ttk.Combobox(inner, values=list(COMMANDS.keys()), state="readonly")
combo_action.current(0)
combo_action.pack(fill="x", pady=8)

var_force = tk.BooleanVar()
chk = tk.Checkbutton(inner, text="Примусово закрити програми", variable=var_force,
                     bg=CARD_COLOR, fg=SUBTEXT, activebackground=CARD_COLOR,
                     selectcolor=BG_COLOR, font=("Segoe UI", 9))
chk.pack(anchor="w")

tk.Label(root, text="Час (хвилини)", font=("Segoe UI", 11),
         bg=BG_COLOR, fg=TEXT).pack(pady=(15, 5))

entry = tk.Entry(root, font=("Segoe UI", 18, "bold"), justify="center",
                 bg="#020617", fg=TEXT, insertbackground="white", relief="flat")
entry.insert(0, "60")
entry.pack(pady=5, ipadx=10, ipady=8)

button_frame = tk.Frame(root, bg=BG_COLOR)
button_frame.pack(pady=10)

for t in [15, 30, 60]:
    btn = tk.Button(button_frame, text=f"{t} хв",
                    command=lambda x=t: start_logic(x),
                    bg=BUTTON153060, fg="white",
                    font=("Segoe UI", 8, "bold"),
                    relief="flat", width=10, cursor="hand2")
    btn.pack(side="left", padx=5)

btn_start = tk.Button(root, text="Старт", command=set_timer_custom,
                      bg=SUCCESS, fg="white",
                      font=("Segoe UI", 11, "bold"),
                      relief="flat", height=2, cursor="hand2")
btn_start.pack(padx=20, pady=10, fill="x")

btn_stop = tk.Button(root, text="Скасувати", command=cancel_timer,
                     bg=DANGER, fg="white",
                     font=("Segoe UI", 10),
                     relief="flat", cursor="hand2")
btn_stop.pack(padx=20, pady=5, fill="x")

lbl_status = tk.Label(root, text="● Очікування...", font=("Segoe UI", 10),
                      bg=BG_COLOR, fg=SUBTEXT)
lbl_status.pack(pady=10)

lbl_countdown = tk.Label(root, text="Залишилось: --:--",
                         font=("Segoe UI", 14, "bold"),
                         bg=BG_COLOR, fg=ACCENT)
lbl_countdown.pack(pady=5)

tk.Button(root, text="🇺🇦", command=privet,
          bg=BG_COLOR, fg="#FACC15",
          relief="flat", font=("Segoe UI", 12),
          cursor="hand2").pack(side="bottom", pady=5)

root.mainloop()