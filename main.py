import tkinter as tk
from tkinter import messagebox
import Feeding_Tracker
import Grooming_Schedule
import Vet_Appointment_Log
import Pet_Expense_Tracker

# setup the main window example from chapter 8
root = tk.Tk()
root.title("Pet Assistant")
root.geometry("600x800")
root.resizable(False, False)


def clear_window():
    # Clears the window to switch pages
    for widget in root.winfo_children():
        widget.destroy()


# GUI main menu

def main_menu():
    clear_window()

    title_label = tk.Label(root, text="Pet Assistant App", font=(
        "Arial", 28, "bold"))
    title_label.pack(pady=50)

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    # create buttons for modules
    btn1 = tk.Button(btn_frame, text="Feeding Tracker", bg="#2265c2", fg="white", font=(
        "Arial", 14), width=22, height=2, command=feeding_page)
    btn1.pack(pady=10)

    btn2 = tk.Button(btn_frame, text="Vet Appointment Log", bg="#d52424", fg="white", font=(
        "Arial", 14), width=22, height=2, command=vet_page)
    btn2.pack(pady=10)

    btn3 = tk.Button(btn_frame, text="Grooming Schedule", bg="#9620c5", fg="white", font=(
        "Arial", 14), width=22, height=2, command=grooming_page)
    btn3.pack(pady=10)

    btn4 = tk.Button(btn_frame, text="Pet Expenses Tracker", bg="#1dbc5f", fg="white", font=(
        "Arial", 14), width=22, height=2, command=expenses_page)
    btn4.pack(pady=10)


def feeding_page():
    clear_window()

    header = tk.Label(root, text="Feeding Tracker", bg="#2265c2",
                      fg="white", font=("Arial", 24, "bold"), width=30, height=2)
    header.pack(fill="x")

    btn_back = tk.Button(root, text="Back", bg="#555555", fg="white", font=(
        "Arial", 12), width=12, command=main_menu)
    btn_back.pack(side="bottom", pady=20)

    content_frame = tk.Frame(root)
    content_frame.pack(fill="both", expand=True)

    Feeding_Tracker.FeedingTrackerApp(content_frame)


def vet_page():
    clear_window()

    header = tk.Label(root, text="Vet Appointment Log", bg="#d52424",
                      fg="white", font=("Arial", 24, "bold"), width=30, height=2)
    header.pack(fill="x")

    btn_back = tk.Button(root, text="Back", bg="#555555", fg="white", font=(
        "Arial", 12), width=12, command=main_menu)
    btn_back.pack(side="bottom", pady=20)

    content_frame = tk.Frame(root)
    content_frame.pack(fill="both", expand=True)

    Vet_Appointment_Log.VetAppointmentApp(content_frame)


def grooming_page():
    clear_window()

    header = tk.Label(root, text="Grooming Schedule", bg="#9620c5",
                      fg="white", font=("Arial", 24, "bold"), width=30, height=2)
    header.pack(fill="x")

    btn_back = tk.Button(root, text="Back", bg="#555555", fg="white", font=(
        "Arial", 12), width=12, command=main_menu)
    btn_back.pack(side="bottom", pady=20)

    content_frame = tk.Frame(root)
    content_frame.pack(fill="both", expand=True)
    Grooming_Schedule.GroomingApp(content_frame)


def expenses_page():
    clear_window()
    header = tk.Label(root, text="Pet Expenses Tracker", bg="#1dbc5f",
                      fg="white", font=("Arial", 24, "bold"), width=30, height=2)
    header.pack(fill="x")

    btn_back = tk.Button(root, text="Back", bg="#555555", fg="white", font=(
        "Arial", 12), width=12, command=main_menu)
    btn_back.pack(side="bottom", pady=20)

    content_frame = tk.Frame(root)
    content_frame.pack(fill="both", expand=True)

    Pet_Expense_Tracker.PetExpenseTrackerApp(content_frame)


main_menu()
root.mainloop()
