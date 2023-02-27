import os
import urllib.request
import zipfile
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess

DEFAULT_FILE_PATH = "C:/Program Files (x86)/Steam/steamapps/common/Kerbal Space Program 2/SpaceWarp"

def add_mod(url, mod_dir, install_dir):
    # Download and extract mod
    mod_zip = os.path.join(install_dir, f"{mod_dir}.zip")
    urllib.request.urlretrieve(url, mod_zip)
    with zipfile.ZipFile(mod_zip, 'r') as zip_ref:
        zip_ref.extractall(install_dir)

    # Delete mod zip file
    os.remove(mod_zip)

    tk.messagebox.showinfo("Successful Install", f"Successfully installed {mod_dir}.")

def add_mod_iva(url, mod_dir, install_dir):
    # Download and extract mod
    mod_zip = os.path.join(install_dir, f"{mod_dir}.zip")
    urllib.request.urlretrieve(url, mod_zip)
    with zipfile.ZipFile(mod_zip, 'r') as zip_ref:
        zip_ref.extractall(install_dir)

    # Delete mod zip file
    os.remove(mod_zip)

    tk.messagebox.showinfo("Successful Install", f"Successfully installed {mod_dir}.")

MOD_LIST = [
    {
            "name": "Lazy Orbit",
            "author": "Halban",
            "url": "https://spacedock.info/mod/3258/Lazy%20Orbit/download/v0.2.0",
            "license": "https://creativecommons.org/licenses/by-sa/4.0/",
            "dir": "lazyOrbit"
        },
        {
            "name": "Custom Flags",
            "author": "adamsogm",
            "url": "https://spacedock.info/mod/3262/Custom%20Flags/download/1.0",
            "license": "https://mit-license.org/",
            "dir": "customFlags"
        },
        {
            "name": "IVA",
            "author": "Mudkip909",
            "url": "https://spacedock.info/mod/3269/IVA%20Mod%20(SpaceWarp%200.1)/download/0.2.1",
            "license": "https://mit-license.org/",
            "dir": "IVA"
        },
        {
            "name": "Cheats Menu",
            "author" : "ShadowDev",
            "url" : "https://spacedock.info/mod/3266/Cheats%20Menu/download/0.0.1",
            "license" : "https://creativecommons.org/licenses/by-nc-nd/4.0",
            "dir": "cheatsMenu"
        }
]

class ModInstallerGUI:
    def __init__(self, master):
        self.master = master
        master.title("KSP2 MOD MGR Installer :: MrCreeps")

        # Create frame for file path selection
        self.path_frame = ttk.LabelFrame(master, text="Select KSP2 directory")
        self.path_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Label and entry widget for file path selection
        self.path_label = ttk.Label(self.path_frame, text="KSP2 directory path:")
        self.path_label.grid(row=0, column=0, sticky="w", padx=(0, 10), pady=10)

        self.path_entry = ttk.Entry(self.path_frame, width=40)
        self.path_entry.grid(row=0, column=1, sticky="w", pady=10)

        # Button for file path selection
        self.path_button = ttk.Button(self.path_frame, text="Browse", command=self.select_directory)
        self.path_button.grid(row=0, column=2, sticky="w", pady=10)

        # Create frame for mod list
        self.mod_frame = ttk.LabelFrame(master, text="Select mods to install")
        self.mod_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Checkboxes for mod selection
        self.mod_vars = []
        self.mod_checkboxes = []
        for i, mod in enumerate(MOD_LIST):
            var = tk.BooleanVar(value=True)
            checkbox = ttk.Checkbutton(self.mod_frame, text=f"{mod['name']} by {mod['author']}", variable=var)
            checkbox.grid(row=i, column=0, sticky="w", padx=(0, 10), pady=5)
            self.mod_vars.append(var)
            self.mod_checkboxes.append(checkbox)

        # Button for installing mods
        self.install_button = ttk.Button(master, text="Install", command=self.install_mods)
        self.install_button.pack(pady=1)

        self.run_ksp_button = ttk.Button(master, text="Launch KSP 2", command=self.run_ksp)
        self.run_ksp_button.pack(pady=10)

        # Set default file path in entry widget
        self.path_entry.insert(0, DEFAULT_FILE_PATH)

    def run_ksp(self):
        shouldRun = tk.messagebox.askquestion("Launch KSP2", "Launch Kerbal Space Program 2?")
        if shouldRun == "yes":
            file_path = self.path_entry.get()
            # Define the path to the executable
            exe_path = file_path[:-9]
            exe_path += "KSP2_x64.exe"

            # Run the executable
            subprocess.run(exe_path)
        else:
            tk.messagebox.showerror("Not Launching KSP2", "Kerbal Space Program 2 launch cancelled.")

    def select_directory(self):
        path = tk.filedialog.askdirectory(initialdir="/", title="Select KSP2 directory")
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, path)

    def install_mods(self):
        # Get file path from entry widget
        file_path = self.path_entry.get()

        # Create Mods directory if it does not exist
        mod_dir = os.path.join(file_path, "Mods")
        if not os.path.exists(mod_dir):
            os.makedirs(mod_dir)

        # Install selected mods
        for i, mod in enumerate(MOD_LIST):
            if self.mod_vars[i].get():
                tk.messagebox.showinfo(f"{mod['name']} Info", f"{mod['name']} by {mod['author']} uses the {mod['license']} license.\nMod page at {mod['url']}")
                confirm = tk.messagebox.askquestion(f"{mod['name']} Install", f"Install {mod['name']} by {mod['author']}?", icon="question")
                if confirm == "yes":
                    if mod['name'] == "Custom Flags":
                        tk.messagebox.showerror("Make `flags/` Warning", "You will need to create a `flags/` folder in the KSP2 directory to add custom flags.")
                    if mod['name'] == "IVA":
                        tk.messagebox.showerror("Currently Broken", "IVA mod does not currently work on KSP 0.2.0 -- :)")
                    add_mod(mod['url'], mod['dir'], mod_dir)
                else:
                    tk.messagebox.showerror(f"Not Installing {mod['name']}", f"Not installing {mod['name']} by {mod['author']}.")

        # Show completion message
        tk.messagebox.showinfo("Installation completed", "The mods have been installed successfully!")

root = tk.Tk()  # Create main window
gui = ModInstallerGUI(root)  # Pass main window as argument to create instance of ModInstallerGUI
root.mainloop()  # Start event loop for main window
