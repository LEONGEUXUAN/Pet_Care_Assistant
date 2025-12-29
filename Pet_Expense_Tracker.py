import tkinter as tk
from tkinter import messagebox

EXP_FILE = "expenses_data.txt"
CATEGORIES = ["Food", "Medical", "Grooming", "Others"]


def max_check(month, year):
    # Returns max day for a given month and year (leap year aware)
    # selection statement (chapter 3 match case)
    match month:
        case 2:
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                return 29
            return 28
        case 4 | 6 | 9 | 11:
            return 30
        case _:
            return 31


def check_date_format_logic(date_text):
    # Check format structure (Chapter 4A split)
    parts = date_text.split("-")

    # Explicit comparison (Chapter 3)
    if len(parts) != 3:
        messagebox.showerror("Error", "Format must be YYYY-MM-DD")
        return False

    # List Indexing (Chapter 4 List)
    y_str = parts[0]
    m_str = parts[1]
    d_str = parts[2]

    # Check if they are numbers (Chapter 4A isdigit)
    if not y_str.isdigit():
        messagebox.showerror("Error", "Year must be a number")
        return False
    if not m_str.isdigit():
        messagebox.showerror("Error", "Month must be a number")
        return False
    if not d_str.isdigit():
        messagebox.showerror("Error", "Day must be a number")
        return False

    # Check lengths (Chapter 5 len)
    if len(y_str) != 4:
        messagebox.showerror("Error", "Year must be 4 digits")
        return False
    if len(m_str) != 2:
        messagebox.showerror("Error", "Month must be 2 digits")
        return False
    if len(d_str) != 2:
        messagebox.showerror("Error", "Day must be 2 digits")
        return False

    # Logic Range Check (Chapter 3 Comparison)
    year = int(y_str)
    month = int(m_str)
    day = int(d_str)

    if month < 1 or month > 12:
        messagebox.showerror("Error", "Month must be 1-12")
        return False

    limit = max_check(month, year)
    if day < 1 or day > limit:
        messagebox.showerror("Error", f"Invalid day. Max is {limit}")
        return False

    return True


class PetExpenseTrackerApp:
    def __init__(self, master):
        self.master = master

        # e for entry, lst for list, lbl for label, v for variable
        self.current_filter = ""
        self.e_filter = None
        self.e_name = None
        self.v_cat = None
        self.e_amount = None
        self.e_date = None
        self.lst_history = None
        self.lbl_total = None

        self.build_ui()
        self.refresh_list()

    def load_records(self):
        # Reads data from file (Chapter 4C)
        records = []
        try:
            with open(EXP_FILE, "r") as f:
                for line in f:
                    parts = line.strip().split("|")
                    if len(parts) >= 5:
                        records.append(parts)
        except IOError:
            pass
        return records

    def save_data(self):
        # Get values (Chapter 8)
        name = self.e_name.get().strip()
        cat = self.v_cat.get()
        amt_str = self.e_amount.get().strip()
        date_str = self.e_date.get().strip()

        # Validation (Chapter 3)
        if len(name) == 0:
            messagebox.showerror("Error", "Name cannot be empty")
            return

        if not name.replace(" ", "").isalpha():
            messagebox.showerror("Error", "Name must be letters only")
            return

        try:
            amt = float(amt_str)
            if amt <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Amount must be a positive number")
            return

        # Date Check (Chapter 4A String Processing)
        if not check_date_format_logic(date_str):
            return

        # ID generator (Chapter 5 and 6)
        data = self.load_records()

        # Standard loop to find max ID
        max_id = 0
        if len(data) > 0:
            for row in data:
                # row[0] is the ID
                curr_id = int(row[0])
                if curr_id > max_id:
                    max_id = curr_id
            new_id = max_id + 1
        else:
            new_id = 1

        # Append to file (Chapter 4C)
        try:
            with open(EXP_FILE, "a") as f:
                # String formatting (Chapter 4A)
                line = f"{new_id}|{date_str}|{name}|{cat}|{amt:.2f}\n"
                f.write(line)
        except IOError:
            messagebox.showerror("Error", "File error")
            return

        # Clear inputs
        self.e_name.delete(0, tk.END)
        self.e_amount.delete(0, tk.END)
        messagebox.showinfo("Success", "Saved successfully")
        self.refresh_list()

    def delete_item(self):
        # Get selected index (Chapter 8)
        sel = self.lst_history.curselection()

        # Check for empty tuple
        if len(sel) == 0:
            messagebox.showerror("Error", "Select an item to delete")
            return

        idx = sel[0]
        data = self.load_records()

        if idx < len(data):
            # Access ID using explicit index row[0]
            item = data[idx]
            confirm = messagebox.askyesno(
                "Confirm", f"Delete record ID {item[0]}?")

            if confirm:
                data.pop(idx)  # Remove item (Chapter 5)

                # Rewrite file (Chapter 4C)
                with open(EXP_FILE, "w") as f:
                    for row in data:
                        f.write("|".join(row) + "\n")
                self.refresh_list()

    def refresh_list(self):
        self.lst_history.delete(0, tk.END)
        data = self.load_records()
        total = 0.0

        for row in data:
            try:
                # row[4] is the amount RM
                val = float(row[4])
            except:
                val = 0.0

            # Filter logic (Chapter 4A String methods)
            if self.current_filter != "":
                if self.current_filter.lower() not in row[2].lower():
                    continue

            total += val

            # Use Explicit List Indexing row[0], row[1]...
            text = f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | RM {val:.2f}"
            self.lst_history.insert(tk.END, text)

        self.lbl_total.config(text=f"Total: RM {total:.2f}")

    def apply_filter(self):
        self.current_filter = self.e_filter.get().strip()
        self.refresh_list()

    def reset_filter(self):
        self.current_filter = ""
        self.e_filter.delete(0, tk.END)
        self.refresh_list()

    def build_ui(self):
        self.build_input_form()
        self.build_record_list()

    def build_input_form(self):
        # Input Form (Chapter 8 Frame & Grid)
        f_input = tk.LabelFrame(self.master, text="New Entry",
                                padx=10, pady=10, font=("Arial", 10, "bold"))
        f_input.pack(pady=10, padx=10, fill="x")

        # Name
        tk.Label(f_input, text="Pet Name:").grid(row=0, column=0, sticky="e")
        self.e_name = tk.Entry(f_input, width=25)
        self.e_name.grid(row=0, column=1, padx=5, pady=5)

        # Category (Chapter 8 Radiobuttons)
        tk.Label(f_input, text="Category:").grid(row=1, column=0, sticky="ne")
        f_radio = tk.Frame(f_input)
        f_radio.grid(row=1, column=1, sticky="w")

        self.v_cat = tk.StringVar(value=CATEGORIES[0])
        for cat in CATEGORIES:
            tk.Radiobutton(f_radio, text=cat, variable=self.v_cat,
                           value=cat).pack(anchor="w")

        # Amount
        tk.Label(f_input, text="Amount (RM):").grid(
            row=2, column=0, sticky="e")
        self.e_amount = tk.Entry(f_input, width=25)
        self.e_amount.grid(row=2, column=1, padx=5, pady=5)

        # Date
        tk.Label(f_input, text="Date (YYYY-MM-DD):").grid(row=3,
                                                          column=0, sticky="e")
        self.e_date = tk.Entry(f_input, width=25)
        self.e_date.grid(row=3, column=1, padx=5, pady=5)

        # Save Btn
        tk.Button(f_input, text="Save Record", bg="#1dbc5f", fg="white", font=("Arial", 10),
                  command=self.save_data).grid(row=4, column=1, pady=10, sticky="w")

    def build_record_list(self):
        # History List
        f_list = tk.LabelFrame(self.master, text="Records",
                               padx=10, pady=10, font=("Arial", 10, "bold"))
        f_list.pack(fill="both", expand=True, padx=10)

        self.lst_history = tk.Listbox(f_list, height=8)
        self.lst_history.pack(fill="both", expand=True)

        # Filters
        f_ctrl = tk.Frame(f_list)
        f_ctrl.pack(fill="x", pady=5)

        tk.Label(f_ctrl, text="Filter by Name:").pack(side="left")
        self.e_filter = tk.Entry(f_ctrl, width=15)
        self.e_filter.pack(side="left", padx=5)
        tk.Button(f_ctrl, text="Check",
                  command=self.apply_filter).pack(side="left")
        tk.Button(f_ctrl, text="Reset", command=self.reset_filter).pack(
            side="left", padx=5)

        # Bottom Controls
        f_bot = tk.Frame(f_list)
        f_bot.pack(fill="x", pady=5)

        tk.Button(f_bot, text="Delete Selected", bg="#d52424",
                  fg="white", command=self.delete_item).pack(side="left")
        self.lbl_total = tk.Label(
            f_bot, text="Total: RM 0.00", font=("Arial", 12, "bold"))
        self.lbl_total.pack(side="right")
