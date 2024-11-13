import customtkinter, os, sys
from tkinter import *
from tkinter import messagebox

EIGENGRAU = "#191922"
OLD_BURGUNDY = "#46383C"
NEON_SILVER = "#C7C7C7"
RAISIN_BLACK = "#29232E"
SMOCKY_BLACK = "#0F0F0F"
TAUPE_GRAY = "#878082"

def Messagebox(title, message) : 
    # Function to show a messagebox
    messagebox.showinfo(title = title, message = message)

def BypassAdminAndRun(command) : 
    # Function that write the admin pass from the file and run the command
    try:
        with open("rootpassword", "r") as f:
            sudoPassword = f.read()
            run = os.system("echo %s | sudo -S %s" % (sudoPassword, command))

    except FileNotFoundError:
        Messagebox("Error", "Password file not found!")
        sys.exit()
    
    # One more exception, if we got an error due the password check
    if run != 0 : 
        Messagebox("Permission denied", "The root password is incorrect!")
        sys.exit()

def GetGenerations() : 
    # Function to get a list with all the generations
    BypassAdminAndRun("nix-env --list-generations --profile /nix/var/nix/profiles/system > genlist")
    with open("genlist") as file:
        lines = [line.rstrip() for line in file]

    os.remove("genlist")
    return lines

class MyScrollableCheckboxFrame(customtkinter.CTkScrollableFrame) :
    # Class for checkboxes
    def __init__(self, master, title, values):
        super().__init__(master, label_text = title, fg_color = OLD_BURGUNDY, bg_color = SMOCKY_BLACK)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.checkboxes = []

        for i, value in enumerate(self.values):
            checkbox = customtkinter.CTkCheckBox(self, text = value, text_color = NEON_SILVER, fg_color = RAISIN_BLACK, hover_color = TAUPE_GRAY, border_color = RAISIN_BLACK)
            checkbox.grid(row = i, column = 0, padx = 10, pady = (10, 0), sticky = "w")
            self.checkboxes.append(checkbox)

    def get(self):
        # Function to get the value from the checkbox
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes

class App(customtkinter.CTk) :
    # Class for the app
    def __init__(self):
        super().__init__()

        self.title("Nixgen")
        self.geometry("400x220")
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)
        self.config(bg = SMOCKY_BLACK)

        values = GetGenerations()
        self.scrollable_checkbox_frame = MyScrollableCheckboxFrame(self, title="Values", values=values)
        self.scrollable_checkbox_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")

        self.button = customtkinter.CTkButton(self, text = "Delete", fg_color = RAISIN_BLACK, hover_color = EIGENGRAU, bg_color = SMOCKY_BLACK, command = self.ButtonCallback)
        self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

    def ButtonCallback(self):
        # Function to detele the generations by pressing the button
        lines = self.scrollable_checkbox_frame.get()
        for i in range(0, len(lines)) : 
            lines[i] = lines[i].split()[0]
            BypassAdminAndRun(f"sudo nix-env --delete-generations {lines[i]} --profile /nix/var/nix/profiles/system")

        Messagebox("Nix info",f"The generations have been successfully deleted!")

# Running the app
app = App()
app.mainloop()
