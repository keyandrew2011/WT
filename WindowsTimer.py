import tkinter as tk
from tkinter import messagebox
import os


def set_timer():
    try:

        minutes = int(entry.get())
        if minutes <= 0:
            raise ValueError


        seconds = minutes * 60


        os.system(f"shutdown -s -t {seconds}")

        lbl_status.config(text=f" Вимкнення через {minutes} хв", fg="red")
        messagebox.showinfo("Готово", f"Комп'ютер вимкнеться через {minutes} хвилин.")
    except ValueError:
        messagebox.showerror("Помилка", "Будь ласка, введіть ціле число більше нуля!")


def cancel_timer():

    os.system("shutdown -a")
    lbl_status.config(text=" Таймер скасовано", fg="green")
    messagebox.showwarning("Скасовано", "Заплановане вимкнення скасовано.")

def privet():
    messagebox.showwarning("Подивіться в консоль", "Слава Україні!")
    print("Героям слава")
root = tk.Tk()
root.title("WindowsTimer")
root.geometry("300x250")

tk.Label(root, text="Введіть час у хвилинах:", font=("Arial", 10)).pack(pady=10)

entry = tk.Entry(root, font=("Arial", 14), justify='center')
entry.pack(pady=5)

btn_start = tk.Button(root, text="Старт", command=set_timer,
                      bg="#4CAF50", fg="white", width=20)
btn_start.pack(pady=10)

btn_stop = tk.Button(root, text="Скасувати", command=cancel_timer,
                     bg="#f44336", fg="white", width=20)
btn_stop.pack(pady=5)


lbl_status = tk.Label(root, text=" Очікування", font=("Arial", 9))
lbl_status.pack(pady=10)
btn_privet = tk.Button(root, text="???", command=privet,
                     bg="#191970", fg="#FFD700", width=20)
btn_privet.pack(pady=5)
root.mainloop()