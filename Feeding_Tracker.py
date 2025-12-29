import tkinter as tk
from tkinter import messagebox

# Pet 
class Pet:
    def __init__(self, name, age, weight): # Stores the pet information 
        self.name = name  
        self.age = age # Pet's age 
        self.weight = weight  # Pet"s weight in kg
        self.schedules = []  # feeding records

    def show_info(self): # Returns full information of the pet, including all feeding schedules.
        return f"{self.name} | Age: {self.age} | Weight: {self.weight}kg" 

    def show_full_info(self):  # Returns full information of the pet, including all feeding schedules.
        info = self.show_info()
        if self.schedules:
            schedules_info = "\n  ".join(
                [f"Time:{s.time_str} - Food:{s.food} Amount({s.amount}kg)" for s in self.schedules]
            )
            return f"{info}\n  Feeding Schedule:\n  {schedules_info}"
        else:
            return info 

# Schedule
class Schedule:
    def __init__(self, time, food, amount):
        self.time_str = time # Feeding time as a string in HH:MM format.
        self.food = food # Name of the food
        self.amount = amount # Amount of food in kilograms
    
    def show_row(self):
        return f"{self.time_str} | {self.food} | {self.amount}kg"

# Time format validation 
def valid_time(t):
    if ":" not in t: # Check if the string contains :
        return False
    parts = t.split(":") # Split the string by : ensure are hour and minute.
    
    if len(parts) != 2:
        return False
    hour_str, minute_str = parts

    if not hour_str.isdigit() or not minute_str.isdigit(): # Check if both parts are digits.
        return False
    
    hour = int(hour_str) # Convert the parts to hour
    minute = int(minute_str) # Convert the parts to minute
    return 0 <= hour <= 23 and 0 <= minute <= 59 # Validate ranges: hour 0–23, minute 0–59.

# GUI + event handling class
class FeedingTrackerApp:
    def __init__(self, master):
        self.pets = [] # Maintain a list of all pets in self.pets.
        self.master = master
        self.selected_pet_index = None # Track which pet is selected
        
        # Variables for inputs
        self.pet_name = tk.StringVar()
        self.pet_age = tk.StringVar()
        self.pet_weight = tk.StringVar()
        
        self.schedule_time = tk.StringVar()
        self.schedule_food = tk.StringVar()
        self.schedule_amount = tk.StringVar()

        main_frame = tk.Frame(master)  
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Top Add Pet
        frame_pet = tk.LabelFrame(main_frame, text="Pet entry")
        frame_pet.pack(fill=tk.X, pady=5) 

        tk.Label(frame_pet, text="Name:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(frame_pet, textvariable=self.pet_name, width=15).grid(row=0, column=1)

        tk.Label(frame_pet, text="Age (y):").grid(row=0, column=2, sticky="e", padx=5, pady=5)
        tk.Entry(frame_pet, textvariable=self.pet_age, width=10).grid(row=0, column=3)

        tk.Label(frame_pet, text="Weight (kg):").grid(row=0, column=4, sticky="e", padx=5, pady=5)
        tk.Entry(frame_pet, textvariable=self.pet_weight, width=10).grid(row=0, column=5)

        tk.Button(frame_pet, text="Add Pet",  bg="#1dbc5f", fg="white", command=self.add_pet).grid(row=0, column=6, padx=10, pady=5)

        frame_view = tk.Frame(main_frame)
        frame_view.pack(fill=tk.BOTH, expand=True, pady=5)

        # Left Pet List
        frame_left = tk.LabelFrame(frame_view, text="Select a Pet")
        frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.list_pets = tk.Listbox(frame_left, height=10, exportselection=False)
        self.list_pets.pack(fill=tk.BOTH, expand=True)
        
        # Bind click event to update schedule list
        self.list_pets.bind('<<ListboxSelect>>', self.on_pet_select)

        tk.Button(frame_left, text="Delete Selected", bg="#d52424",
                  fg="white", command=self.delete_pet).pack(pady=5)

        # Right Schedule List (for selected pet)
        frame_right = tk.LabelFrame(frame_view, text="Schedules (for Selected)")
        frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        self.list_schedules = tk.Listbox(frame_right, height=10, exportselection=False)
        self.list_schedules.pack(fill=tk.BOTH, expand=True)

        tk.Button(frame_right, text="Delete Selected", bg="#d52424",
                  fg="white", command=self.delete_schedule).pack(pady=5)

        # Bottom Add Schedule
        frame_schedules = tk.LabelFrame(main_frame, text="Add Schedule to Selected Pet")
        frame_schedules.pack(fill=tk.X, pady=5)

        tk.Label(frame_schedules, text="Time (HH:MM):").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(frame_schedules, textvariable=self.schedule_time, width=20).grid(row=0, column=1)

        tk.Label(frame_schedules, text="Food:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(frame_schedules, textvariable=self.schedule_food, width=20).grid(row=1, column=1)

        tk.Label(frame_schedules, text="Amount (kg):").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(frame_schedules, textvariable=self.schedule_amount, width=20).grid(row=2, column=1)

        tk.Button(frame_schedules, text="Add Schedule",  bg="#1dbc5f", fg="white", command=self.add_schedule).grid(row=3, column=1, pady=10, sticky="w")
        
        # Bottom Save Buttons
        frame_save = tk.Frame(main_frame)
        frame_save.pack(fill=tk.X, pady=5)
        tk.Button(frame_save, text="Save to File", command=self.save_to_file).pack(side=tk.RIGHT, padx=5)

        # load saved data automatically
        self.load_from_file()


    # Logic Functions
    def refresh_pet_list(self):
        self.list_pets.delete(0, tk.END)
        for pet in self.pets:
            self.list_pets.insert(tk.END, pet.show_info())
        
        # Clear schedule list if no pet selected
        self.list_schedules.delete(0, tk.END)
        self.selected_pet_index = None

    def on_pet_select(self, event):
        # when user clicks a pet
        selection = self.list_pets.curselection()
        if selection:
            index = selection[0]
            self.selected_pet_index = index
            self.refresh_schedule_list(index)

    def refresh_schedule_list(self, pet_index):
        self.list_schedules.delete(0, tk.END)
        if pet_index < len(self.pets):
            pet = self.pets[pet_index]
            for schedules in pet.schedules:
                self.list_schedules.insert(tk.END, schedules.show_row())

    # add pet 
    def add_pet(self):
        name = self.pet_name.get().strip()
        age_str = self.pet_age.get().strip()
        weight_str = self.pet_weight.get().strip()

        if not name: 
            messagebox.showwarning("Warning", "Pet name is required!")
            return

        try:
            age = int(age_str)
            if age < 1:
                raise ValueError
            elif age > 100:
                messagebox.showwarning("Warning", "What kind of pet do you have? That is too old!")
                return 
        except ValueError:
            messagebox.showwarning("Warning", "Age must be at least 1 year!")
            return
        
        try:
            weight = float(weight_str)
            if weight <= 0:
                raise ValueError
            elif weight >= 1000:
                messagebox.showwarning("Warning", "What kind of pet do you have? That is too heavy!")
                return
        except ValueError:
            messagebox.showwarning("Warning", "Please enter a valid positive weight!")
            return
    
        pet = Pet(name, age, weight)
        self.pets.append(pet)
        
        # Update list
        self.refresh_pet_list()
        
        self.pet_name.set("")
        self.pet_age.set("")
        self.pet_weight.set("")
        messagebox.showinfo("Success", f"{name} added successfully!")

    # add feeding schedule
    def add_schedule(self):
        # Check if pet is selected
        if self.selected_pet_index is None:
            messagebox.showwarning("Warning", "Please select a Pet from the list first!")
            return

        time_str = self.schedule_time.get().strip()
        food = self.schedule_food.get().strip()
        amt_str = self.schedule_amount.get().strip()

        if not time_str:
            messagebox.showwarning("Warning", "No time entered.")
            return

        if not valid_time(time_str):
            messagebox.showerror("Error","Invalid time format , Example: 23:59")
            return
         
        if not food:
            messagebox.showwarning("Warning", "Food is required!")
            return

        try:
            amount = float(amt_str)
        except ValueError:
            messagebox.showwarning("Warning", "Amount is required and must be a number!")
            return

        # Add to selected pet
        pet = self.pets[self.selected_pet_index]
        schedule = Schedule(time_str, food, amount)
        pet.schedules.append(schedule)
        
        self.refresh_schedule_list(self.selected_pet_index)
        
        self.schedule_time.set("")
        self.schedule_food.set("")
        self.schedule_amount.set("")
        messagebox.showinfo("Success", "Schedule added!")

    # delete pet
    def delete_pet(self):
        selection = self.list_pets.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Select a pet to delete.")
            return

        idx = selection[0]
        name = self.pets[idx].name
        
        if messagebox.askyesno("Confirm", f"Delete {name}?"):
            del self.pets[idx]
            self.refresh_pet_list()
            self.selected_pet_index = None
            self.list_schedules.delete(0, tk.END)

    # delete schedule
    def delete_schedule(self):
        if self.selected_pet_index is None:
            return
            
        selection = self.list_schedules.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Select a schedule to delete.")
            return

        idx = selection[0]
        pet = self.pets[self.selected_pet_index]
        
        if messagebox.askyesno("Confirm", "Delete this schedule?"):
            del pet.schedules[idx]
            self.refresh_schedule_list(self.selected_pet_index)

    # Saves pets and their schedules to a text file.
    def save_to_file(self): 
        with open("feeding_data.txt", "w") as f:
            for pet in self.pets:
                f.write(f"PET|{pet.name}|{pet.age}|{pet.weight}\n")
                for s in pet.schedules:
                    f.write(f"SCHEDULE|{s.time_str}|{s.food}|{s.amount}\n")
                f.write("\n")  # separate pets
        messagebox.showinfo("Saved", "Data saved to feeding_data.txt")

    # load file
    def load_from_file(self):
        self.pets.clear()
        try:
            with open("feeding_data.txt", "r") as f:
                lines = f.readlines()

            pet = None
            for line in lines:
                line = line.strip()
                if not line:
                    continue

                parts = line.split("|")
                if parts[0] == "PET":
                    name, age, weight = parts[1], int(parts[2]), float(parts[3])
                    pet = Pet(name, age, weight)
                    self.pets.append(pet)
                
                elif parts[0] == "SCHEDULE" and pet:
                    time_str, food, amount = parts[1], parts[2], float(parts[3])
                    pet.schedules.append(Schedule(time_str, food, amount))

            self.refresh_pet_list()
        
        except FileNotFoundError:
            pass  # first time no file