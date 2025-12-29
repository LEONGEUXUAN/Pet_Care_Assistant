import tkinter as tk
from tkinter import messagebox
from datetime import datetime 

class GroomingApp:
    
    def __init__(self, parent_frame, filename="grooming_data.txt"):
        self.parent = parent_frame
        self.filename = filename

        #store raw lines "pet|date|task"
        self.schedules = []

        #Main frame for the module 
        self.frame = tk.Frame(self.parent)
        self.frame.pack(fill="both", expand=True)

        #Form area to get user input
        form = tk.Frame(self.frame)
        form.pack(padx=20, pady=12, fill="x")

        tk.Label(form, text="Pet Name:", anchor="w").grid(row=0, column=0, sticky="w", pady=6)
        self.pet_entry = tk.Entry(form, width=40)
        self.pet_entry.grid(row=0, column=1, sticky="w", pady=6)

        tk.Label(form, text="Date (YYYY-MM-DD HH:MM):", anchor="w").grid(row=1, column=0, sticky="w", pady=6)
        self.date_entry = tk.Entry(form, width=40)
        self.date_entry.grid(row=1, column=1, sticky="w", pady=6)

        tk.Label(form, text="Grooming Task:", anchor="w").grid(row=2, column=0, sticky="w", pady=6)
        self.task_entry = tk.Entry(form, width=40)
        self.task_entry.grid(row=2, column=1, sticky="w", pady=6)

        #Buttons
        btns = tk.Frame(self.frame)
        btns.pack(padx=20, pady=8, fill="x")

        tk.Button(btns, text="Add (Save New)", width=16, command=self.add_schedule).pack(side="left", padx=5)
        tk.Button(btns, text="Update Selected", width=16, command=self.update_selected).pack(side="left", padx=5)
        tk.Button(btns, text="Delete Selected", width=16, command=self.delete_selected).pack(side="left", padx=5)
        tk.Button(btns, text="Clear", width=10, command=self.clear_form).pack(side="left", padx=5)
        tk.Button(btns, text="Refresh", width=10, command=self.refresh_list).pack(side="left", padx=5)

        #List area
        list_area = tk.Frame(self.frame)
        list_area.pack(padx=20, pady=10, fill="both", expand=True)

        tk.Label(list_area, text="Schedules (click to load into form):", anchor="w").pack(anchor="w")

        self.listbox = tk.Listbox(list_area, height=12)
        self.listbox.pack(side="left", fill="both", expand=True, pady=6)

        scrollbar = tk.Scrollbar(list_area, command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y", pady=6)
        self.listbox.config(yscrollcommand=scrollbar.set)

        

        #load data
        self.load_from_file()
        self.refresh_list()
        self.clear_form()

    #File

    def load_from_file(self):
        self.schedules = []
        try:
            with open(self.filename, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        # basic format check: must have 2 | at least
                        if line.count("|") >= 2: 
                            self.schedules.append(line) #add the content to schedules
        except FileNotFoundError:
            self.schedules = []

    def save_to_file(self):
        with open(self.filename, "w") as f:
            for row in self.schedules:
                f.write(row + "\n") 

    #Helpers
    #assign all the value
    def safe_split(self, row):
        parts = row.split("|", 2) #split the value by using the |
        if len(parts) != 3: #if the splitted velue not equal to 3
            return "", "", row  #return "" to avoid crash
        pet = parts[0].strip()
        date = parts[1].strip() 
        task = parts[2].strip()
        return pet, date, task

    def get_selected_index(self):  #check if the user select the listbox
        sel = self.listbox.curselection()
        if not sel:
            return None
        return sel[0]
        
        #clear the content in the entry box
    def clear_form(self):
        self.pet_entry.delete(0, tk.END)
        self.task_entry.delete(0, tk.END)
        self.listbox.selection_clear(0, tk.END)
        
        #set default Date/Time
        self.date_entry.delete(0, tk.END)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.date_entry.insert(0, current_time)
          
    def refresh_list(self):   
        self.listbox.delete(0, tk.END) #delete all content from listbox
        for i, row in enumerate(self.schedules, start=1): #start from 1, insert all value("include new one")
            pet, date, task = self.safe_split(row)
            self.listbox.insert(tk.END, f"{i}. {date} | {pet} | {task}")

    
    # validation pet name and task

    def validate_pet_task(self, pet, task):
        pet = pet.strip()
        task = task.strip()
 
        if pet == "":
            messagebox.showerror("Invalid", "Pet name cannot be empty.")
            return None
        if task == "":
            messagebox.showerror("Invalid", "Grooming task cannot be empty.")
            return None

        return pet, task

    #validate date and time
    def validate_datetime(self, date_text):
        date_text = date_text.strip()
        try:
            #check format Year-Month-Day Hour:Minute
            #check if hour is > 23 or minute > 59
            valid_dt = datetime.strptime(date_text, "%Y-%m-%d %H:%M")
            
            #check if year is between 2025 and 2035
            if valid_dt.year < 2025 or valid_dt.year > 2035:
                messagebox.showerror("Invalid Date", "Year must be between 2025 and 2035.")
                return None
                
            return date_text # Return valid string
            
        except ValueError:
            messagebox.showerror("Invalid Format", "Please enter format: YYYY-MM-DD HH:MM\nExample: 2025-05-20 13:14")
            return None

    #Create,Read,Update,Delete function

    def add_schedule(self):
        pet_raw = self.pet_entry.get()
        date_raw = self.date_entry.get()
        task_raw = self.task_entry.get()

        validated = self.validate_pet_task(pet_raw, task_raw)
        if validated is None:
            return
        pet, task = validated

        #check date and time
        clean_date = self.validate_datetime(date_raw)
        if clean_date is None:
            return  

        row = f"{pet}|{clean_date}|{task}"
        self.schedules.append(row)
        self.save_to_file()
        self.refresh_list()
        self.clear_form()
        messagebox.showinfo("Success", "Schedule added.")

    def update_selected(self):
        idx = self.get_selected_index()
        if idx is None:
            messagebox.showwarning("No selection", "Please select a schedule to update.")
            return

        pet_raw = self.pet_entry.get()
        date_raw = self.date_entry.get()
        task_raw = self.task_entry.get()

        validated = self.validate_pet_task(pet_raw, task_raw)
        if validated is None:
            return
        pet, task = validated

        clean_date = self.validate_datetime(date_raw)
        if clean_date is None:
            return

        self.schedules[idx] = f"{pet}|{clean_date}|{task}"
        self.save_to_file()
        self.refresh_list()
        self.listbox.selection_set(idx)
        messagebox.showinfo("Success", "Schedule updated.")

    def delete_selected(self):
        idx = self.get_selected_index()
        if idx is None:
            messagebox.showwarning("No selection", "Please select a schedule to delete.")
            return

        pet, date, task = self.safe_split(self.schedules[idx])
        ok = messagebox.askyesno(
            "Confirm Delete",
            f"Delete this schedule?\n\nDate: {date}\nPet: {pet}\nTask: {task}"
        )
        if not ok:
            return

        self.schedules.pop(idx)
        self.save_to_file()
        self.refresh_list()
        self.clear_form()
        messagebox.showinfo("Success", "Schedule deleted.")