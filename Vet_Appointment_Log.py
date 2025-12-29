# -------------------------
#          IMPORT
# -------------------------
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

FILE_NAME = 'appointment_data.txt'

# -------------------------
#       LOGIC CLASS
# -------------------------
class VetAppointmentLogic:
    def __init__(self):
        self.appointment_lists = []
        self.read_file_data() # call a function

    # read file data
    def read_file_data(self): # reading the file data
        self.appointment_lists.clear()
        try:
            with open(FILE_NAME, "r") as f: # try open file success # "r" is reading file
                for line in f:
                    if line.strip():
                        self.appointment_lists.append(line.strip().split('|')) # separate the information
            return True
        except IOError:
            return False

    def save_file(self): # save the file
        try:
            with open(FILE_NAME, "w") as f:
                # loop through current list and rewrite everything with new ID
                for idx, item in enumerate(self.appointment_lists):
                    item[0] = str(idx + 1)
                    # join the list back into a string
                    line = "|".join(item) + "\n"
                    f.write(line)
            return True
        except IOError:
            return False

    def add_data(self, item):
        self.appointment_lists.append(item)
        return self.save_file()

    def edit_data(self, idx, item):
        self.appointment_lists[idx] = item
        return self.save_file()

    def delete_data(self, real_idx):
        if 0 <= real_idx < len(self.appointment_lists):
            del self.appointment_lists[real_idx]
            return self.save_file()
        return False

    def get_list(self):
        return self.appointment_lists


# -------------------------
#        GUI CLASS
# -------------------------
class VetAppointmentApp:
    def __init__(self, master):
        self.master = master
        
        self.logic = VetAppointmentLogic()

        # Create a container/box frame inside the master
        self.container = tk.Frame(self.master)
        self.container.pack(fill="both", expand=True)

        # list data
        self.page_appointment_lists = []  

        self.list_pages = 0  # This Page
        self.pages = 0  # Total Pages
        self.vet_page()

    # -------------------------
    #       FUNCTION
    # -------------------------

    def clear_content(self):
        # Clears the container/box frame only
        for widget in self.container.winfo_children():
            widget.destroy()



    # Show List
    def show_list(self):
        # Refresh data from logic
        current_list = self.logic.get_list()
        self.count_pages(current_list)

        list_frame = tk.LabelFrame(self.container,
                                   padx=5, pady=5, font=("Arial", 10, "bold")
                                   )
        list_frame.pack(padx=5, pady=5, fill="both", expand=True)

        if not current_list: # not record in the page
            text_null = tk.Label(list_frame,
                                 text="Vet Appointment Data is Null",
                                 font=("Arial", 20),
                                 fg='#999',
                                 height=3,
                                 width=25)
            text_null.pack(pady=20)
        else:
            head = self.list_pages * 6 # max 6 record
            tail = 6 + head
            self.page_appointment_lists = current_list[head:tail]
            for i, [id, pet_name, appointment_date, clinic_name, reason_notes] in enumerate(self.page_appointment_lists):
                block_frame = tk.LabelFrame(list_frame,
                                            padx=10,
                                            pady=10,
                                            font=("Arial", 10, "bold")
                                            )
                block_frame.pack(fill="x", padx=10, pady=10)

                
                text = tk.Label(block_frame,
                                text=f"Pet: {pet_name} | Date: {appointment_date}\n"
                                     f"Clinic: {clinic_name} | Note: {reason_notes}",
                                font=("Arial", 9),
                                height=2,
                                justify="left",
                                padx=2)
                text.pack(side="left", fill="x", expand=True)

                btn_frame_inner = tk.Frame(block_frame)
                btn_frame_inner.pack(side="right")

                edit_button = tk.Button(btn_frame_inner,
                                        text="Edit",
                                        font=("Arial", 9),
                                        command=lambda
                                        p=pet_name,
                                        d=appointment_date,
                                        c=clinic_name,
                                        r=reason_notes,
                                        idx=i: self.appointment_page(p, d, c, r, idx)
                                        )
                edit_button.pack(side="left", padx=2)

                del_button = tk.Button(btn_frame_inner,
                                       bg="red",
                                       fg="white",
                                       text=" X ",
                                       font=("Arial", 9, "bold"),
                                       command=lambda idx=i: self.del_list(idx)
                                       )
                del_button.pack(side="left", padx=2)

            btn_frame = tk.LabelFrame(self.container,
                                      padx=5,
                                      pady=5,
                                      )
            btn_frame.pack(padx=5, pady=5)

            for i in range(self.pages):
                if self.list_pages == i:
                    page_button = tk.Button(btn_frame,
                                            text=f"{i + 1}",
                                            fg="#000",
                                            font=("Arial", 9),
                                            command=lambda idx=i: self.change_page(
                                                idx)
                                            )

                    page_button.grid(row=1, column=i)
                else:
                    page_button = tk.Button(btn_frame,
                                            text=f"{i + 1}",
                                            fg="#888",
                                            font=("Arial", 9),
                                            command=lambda idx=i: self.change_page(
                                                idx)
                                            )

                    page_button.grid(row=1, column=i)

    # Reset table
    def reset_table(self, pet, year, month, day, clinic, Reason):
        pet.set("")
        year.set("")
        month.set("")
        day.set("")
        clinic.set("")
        Reason.set("")

    # submit and edit btn
    def submit_data(self, pet, year, month, day, clinic, Reason, idx=None):
        pet_name = pet.get()
        clinic_name = clinic.get()
        reason_note = Reason.get()

        # Validation
        if not pet_name or not clinic_name or not year.get() or not month.get() or not day.get():
            messagebox.showerror("Error", "The required field is empty.\n Please re-enter!")
            return

        try:
            Year = int(year.get())
            Month = int(month.get())
            Day = int(day.get())
            valid_date = datetime(Year, Month, Day)

            if Year > 2035 or Year < 2025:
                messagebox.showerror("Error",
                                     "The entered year is more than 10 years old or has expired.\nPlease re-enter!")
                return

            date = valid_date.strftime("%Y-%m-%d")

        except ValueError:
            messagebox.showerror("Error", "The date input is incorrect or not a number.\nPlease re-enter!")
            return

        check = messagebox.askokcancel("Please Check Message", f"Please Check Message\n"
                                                  f"Pet Name: {pet_name}\n"
                                                  f"Clinic Name: {clinic_name}\n"
                                                  f"Date: {date}")
        if check:
            if not reason_note:
                reason_note = 'null'
            
            success = False
            if idx is None:
                # use placeholder '0' for ID because save_file() fixes ID automatically
                item = ['0', pet_name, date, clinic_name, reason_note]
                success = self.logic.add_data(item)
                if success:
                    messagebox.showinfo("success", 'Added Successfully!')
            else:
                # Update list in memory then save
                item = [str(idx + 1), pet_name, date, clinic_name, reason_note]
                success = self.logic.edit_data(idx, item)
                if success:
                    messagebox.showinfo("success", 'Edit Successfully!')

            if not success:
                messagebox.showerror("Error", "Failed to save data to file.")

            self.vet_page()

    # del btn with confirmation
    def del_list(self, idx):
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this appointment?")

        if confirm:
            real_idx = (self.list_pages * 6) + idx
            
            success = self.logic.delete_data(real_idx)
            
            if success:
                self.vet_page()
            else:
                messagebox.showerror("Error", "Could not find item to delete or File Error.")

    # page break
    def change_page(self, idx):
        self.list_pages = idx
        self.vet_page()

    # calculate the number of pages
    def count_pages(self, current_list):
        self.pages = len(current_list) // 6
        if self.pages == 0 or len(current_list) % 6 != 0:
            self.pages = self.pages + 1

    # -------------------------
    #          GUI
    # -------------------------

    # show appointment page
    def vet_page(self):
        self.clear_content()
        label_frame = tk.Frame(self.container)
        label_frame.pack(pady=5)


        self.show_list()

        btn_frame_btns = tk.Frame(self.container)
        btn_frame_btns.pack(pady=5)
        btn_add = tk.Button(btn_frame_btns,
                            text="Add Appointment",
                            bg="#1dbc5f",
                            fg="#fff",
                            font=("Arial", 12),
                            width=18,
                            height=2,
                            command=lambda: self.appointment_page())
        btn_add.pack(pady=10)

    # add and edit appointment page 
    def appointment_page(self, name=None, date=None, clinic=None, Notes=None, idx=None):
        self.clear_content()

        label_frame = tk.Frame(self.container)
        label_frame.pack(pady=10)

        # return button
        btn_return = tk.Button(
            label_frame,
            text=" < ",
            relief="solid",
            fg="#999",
            font=("Arial", 12),
            command=lambda: self.vet_page()
        )
        btn_return.grid(row=1, column=1)
        
        title_text = "Edit Appointment" if name else "Add Appointment"

        # Label
        label1 = tk.Label(label_frame,
                          text=title_text,
                          relief="solid",
                          font=("Arial", 18),
                          width=20,
                          )
        label1.grid(row=1, column=2)

        table_frame = tk.LabelFrame(self.container,
                                    font=("Arial", 10, "bold"),
                                    )
        table_frame.pack(padx=10, pady=10, fill="x")

        pet_name_label = tk.Label(table_frame,
                                  text="*Pet Name : ",
                                  font=("Arial", 12),
                                  )
        pet_name_label.grid(row=1, column=1, pady=5, padx=5, sticky="e")

        petName = tk.StringVar()
        year = tk.StringVar()
        month = tk.StringVar()
        day = tk.StringVar()
        clinicName = tk.StringVar()
        ReasonNote = tk.StringVar()

        if name:
            # Edit mode set values from arguments
            petName.set(name)
            clinicName.set(clinic)
            ReasonNote.set(Notes)
            
            try:
                date_parts = date.split("-")
                year.set(date_parts[0])
                month.set(date_parts[1])
                day.set(date_parts[2])
            except:
                pass 
        else:
            # Add mode Set default today date
            today = datetime.now()
            year.set(today.year)
            month.set(today.month)
            day.set(today.day)

        pet_name_entry = tk.Entry(table_frame,
                                  textvariable=petName,
                                  width=20,
                                  font=("Arial", 12),
                                  )
        pet_name_entry.grid(row=1, column=2, padx=5)

        Date_label = tk.Label(table_frame,
                              text="*Date : ",
                              font=("Arial", 12),
                              )
        Date_label.grid(row=2, column=1, pady=5, padx=5, sticky="e")

        date_frame = tk.Frame(table_frame)
        date_frame.grid(row=2, column=2, pady=5, padx=5, sticky="w")

        year_entry = tk.Entry(date_frame,
                              textvariable=year,
                              width=7,
                              font=("Arial", 12),
                              )
        year_entry.pack(side="left")

        split_label1 = tk.Label(date_frame,
                                text="-",
                                font=("Arial", 12),
                                )
        split_label1.pack(side="left")
        month_entry = tk.Entry(date_frame,
                               textvariable=month,
                               width=5,
                               font=("Arial", 12),
                               )
        month_entry.pack(side="left")
        split_label2 = tk.Label(date_frame,
                                text="-",
                                font=("Arial", 12),
                                )
        split_label2.pack(side="left")
        day_entry = tk.Entry(date_frame,
                             textvariable=day,
                             width=5,
                             font=("Arial", 12),
                             )
        day_entry.pack(side="left")

        clinic_name_label = tk.Label(table_frame,
                                     text="*Clinic Name : ",
                                     font=("Arial", 12),
                                     )
        clinic_name_label.grid(row=3, column=1, pady=5, padx=5, sticky="e")

        clinic_name_entry = tk.Entry(table_frame,
                                     textvariable=clinicName,
                                     width=20,
                                     font=("Arial", 12),
                                     )
        clinic_name_entry.grid(row=3, column=2, padx=5)

        Reason_notes_label = tk.Label(table_frame,
                                      text="Reason Note : ",
                                      font=("Arial", 12),
                                      )
        Reason_notes_label.grid(row=4, column=1, pady=5, padx=5, sticky="e")

        Reason_notes_entry = tk.Entry(table_frame,
                                      textvariable=ReasonNote,
                                      width=20,
                                      font=("Arial", 12),
                                      )
        Reason_notes_entry.grid(row=4, column=2, padx=5)

        # buttons stacked at bottom
        btn_frame = tk.Frame(table_frame)
        btn_frame.grid(row=5, column=1, columnspan=2, pady=10)

        reset_btn = tk.Button(btn_frame,
                              text="reset",
                              fg="#000",
                              font=("Arial", 12),
                              command=lambda: self.reset_table(petName, year, month, day, clinicName, ReasonNote)
                              )
        reset_btn.pack(side="left", padx=10)

        submit_btn = tk.Button(btn_frame,
                               text="submit",
                               fg="#fff",
                               font=("Arial", 12),
                               bg="#1dbc5f",
                               command=lambda: self.submit_data(petName, year, month, day, clinicName, ReasonNote, idx)
                               )
        submit_btn.pack(side="left", padx=10)