import customtkinter, subprocess, os, sys
from tkinter import *
from tkinter import messagebox

def Messagebox(title, message) : 
    messagebox.showinfo(title = title, message = message)

def BypassAdmin(command) : 
    sudoPassword = open("rootpassword", "r").read()
    run = os.system("echo %s|sudo -S %s" % (sudoPassword, command))
    
    if run == 256 : 
        Messagebox("Permission denied", "The root password is incorrect!")
        sys.exit()

def GetGenerations() : 
    BypassAdmin("nix-env --list-generations --profile /nix/var/nix/profiles/system > genlist")
    with open("genlist") as file:
        lines = [line.rstrip() for line in file]

    os.remove("genlist")
    return lines

class MyScrollableCheckboxFrame(customtkinter.CTkScrollableFrame) :
    def __init__(self, master, title, values):
        super().__init__(master, label_text = title, fg_color = "#46383C", bg_color = "#0F0F0F")
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.checkboxes = []

        for i, value in enumerate(self.values):
            checkbox = customtkinter.CTkCheckBox(self, text = value, text_color = "#C7C7C7", fg_color = "#29232E", hover_color = "#878082", border_color="#29232E")
            checkbox.grid(row = i, column = 0, padx = 10, pady = (10, 0), sticky = "w")
            self.checkboxes.append(checkbox)

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes

class App(customtkinter.CTk) :
    def __init__(self):
        super().__init__()

        self.title("my app")
        self.geometry("400x220")
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)
        self.config(bg="#0F0F0F")

        values = GetGenerations()

        self.scrollable_checkbox_frame = MyScrollableCheckboxFrame(self, title="Values", values=values)
        self.scrollable_checkbox_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")

        self.button = customtkinter.CTkButton(self, text="Delete", fg_color = "#29232E", hover_color = "#191922", bg_color = "#0F0F0F", command=self.button_callback)
        self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

    def button_callback(self):
        line = self.scrollable_checkbox_frame.get()
        generation_number = line[0].split()[0]

        BypassAdmin(f"sudo nix-env --delete-generations {generation_number} --profile /nix/var/nix/profiles/system")
        Messagebox("Nix info",f"The generation {generation_number} has been deleted!")

app = App()
app.mainloop()