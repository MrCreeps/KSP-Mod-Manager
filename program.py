import os
import urllib.request
import zipfile
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import shutil
import json
import webbrowser

DEFAULT_FILE_PATH = "C:/Program Files (x86)/Steam/steamapps/common/Kerbal Space Program 2/"
vers = "0.3.0"

try:
    with open("alpha_launcher_modlist.json", "r") as f:
        MOD_LIST = json.load(f)
except:
    webbrowser.open("https://github.com/MrCreeps/KSP-Mod-Manager/releases/tag/mod-list", new=2)
    MOD_LIST = [
        {
            "name": "You need to download the mod list first or the mod list is in the wrong place. Make sure it is in the same directory as the .exe for this program.",
            "author": "MrCreeps",
            "url": "",
            "lisence": "",
            "fulldir": ","

        }
    ]


class ModInstallerGUI:
    def __init__(self, master):
        self.master = master
        master.title(f"αlpha Launcher {vers} :: MrCreeps")

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

        # Button for installing SpaceWarp
        self.install_button = ttk.Button(master, text="Install SpaceWarp 0.3.0", command=self.install_sw)
        self.install_button.pack(pady=1)

        # Button for opening new mod list menu
        self.modlist_button = ttk.Button(master, text="Download New Mod List", command= webbrowser.open("https://github.com/MrCreeps/KSP-Mod-Manager/releases/tag/mod-list", new=2))
        self.modlist_button.pack(pady=1)

        # Create frame for mod list
        self.mod_frame = ttk.LabelFrame(master, text="Select mods to install")
        self.mod_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Checkboxes for mod selection
        self.mod_vars = []
        self.mod_checkboxes = []
        for i, mod in enumerate(MOD_LIST):
            var = tk.BooleanVar(value=False)
            checkbox = ttk.Checkbutton(self.mod_frame, text=f"{mod['name']} by {mod['author']}", variable=var)
            checkbox.grid(row=i, column=0, sticky="w", padx=(0, 10), pady=5)
            self.mod_vars.append(var)
            self.mod_checkboxes.append(checkbox)

        # Frame for utility buttons
        self.buttons_frame = ttk.LabelFrame(master, text="Utility buttons")
        self.buttons_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Button for installing mods
        self.install_button = ttk.Button(self.buttons_frame, text="Install Selected", command=self.install_mods)
        self.install_button.pack(pady=1)

        # Button for uninstalling mods
        self.remove_button = ttk.Button(self.buttons_frame, text="Remove Selected", command=self.remove_mods)
        self.remove_button.pack(pady=1)

        # Button for Launching KSP
        self.run_ksp_button = ttk.Button(self.buttons_frame, text="Launch KSP 2", command=self.run_ksp)
        self.run_ksp_button.pack(pady=1)
        
        # Button for exiting the launcher
        self.exit_launcher_button = ttk.Button(self.buttons_frame,text="Exit Launcher", command=self.exit_launcher)
        self.exit_launcher_button.pack(pady=10)

        # Set default file path in entry widget
        self.path_entry.insert(0, DEFAULT_FILE_PATH)

    def install_sw(self):
        shouldInstall = tk.messagebox.askquestion("Install SW", "Install SpaceWarp?")
        if shouldInstall == "yes":
            file_path = self.path_entry.get()
            mod_zip = os.path.join(file_path, f"SPACEWARP.zip")
            urllib.request.urlretrieve("https://spacedock.info/mod/3257/Space%20Warp/download/0.3.0", mod_zip)
            with zipfile.ZipFile(mod_zip, 'r') as zip_ref:
                zip_ref.extractall(file_path)
            # Delete mod zip file
            os.remove(mod_zip)
            tk.messagebox.showinfo("Successful Install", f"Successfully installed SpaceWarp.")

    def run_ksp(self):
        shouldRun = tk.messagebox.askquestion("Launch KSP2", "Launch Kerbal Space Program 2?")
        if shouldRun == "yes":
            file_path = self.path_entry.get()
            # Define the path to the executable
            file_path += "KSP2_x64.exe"

            # Run the executable
            subprocess.run(file_path)
        else:
            tk.messagebox.showerror("Not Launching KSP2", "Kerbal Space Program 2 launch cancelled.")

    def add_mod_full_dir(self, url, mod_dir, install_dir):
        # Download and extract mod
        mod_zip = os.path.join(install_dir, f"{mod_dir}.zip")
        urllib.request.urlretrieve(url, mod_zip)
        with zipfile.ZipFile(mod_zip, 'r') as zip_ref:
            zip_ref.extractall(self.path_entry.get())

        # Delete mod zip file
        os.remove(mod_zip)

    def select_directory(self):
        path = tk.filedialog.askdirectory(initialdir="/", title="Select KSP2 directory")
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, path)

    def remove_mods(self):
        # Get file path from entry widget
        file_path = self.path_entry.get() + "/SpaceWarp/"

        mod_dir = f"{file_path}/mods/"
        if not os.path.exists(mod_dir):
            tk.messagebox.showerror("Nonexistant Mod Directory", "Try installing mods before removing them ;)")
            return
        
        # Remove selected mods
        for i, mod in enumerate(MOD_LIST):
            if self.mod_vars[i].get():
                confirm = tk.messagebox.askquestion(f"{mod['name']} Remove", f"Remove {mod['name']} by {mod['author']}?", icon="question")
                if confirm == "yes":
                    mod_path = f"{mod_dir}{mod['dir']}"
                    if os.path.exists(mod_path):
                        shutil.rmtree(mod_path)
                        tk.messagebox.showinfo("Successful Removal", f"Successfully removed {mod_dir}.")
                    else:
                        tk.messagebox.showerror("Removal Failed", f"Removal of {mod_dir} failed because it does not exist.")

                else:
                    tk.messagebox.showerror(f"Not Removing {mod['name']}", f"Not Removing {mod['name']} by {mod['author']}.")

    def install_mods(self):
        # Get file path from entry widget
        file_path = self.path_entry.get() + "/SpaceWarp/"

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

                    if mod['fulldir'] == "True":
                        ksp2_dir = self.path_entry.get()

                        mod_zip = self.path_entry.get() + "/" + mod['dir'] + ".zip"
                        urllib.request.urlretrieve(mod['url'], mod_zip)
                        with zipfile.ZipFile(mod_zip, 'r') as zip_ref:
                            zip_ref.extractall(ksp2_dir)
                    else:
                        mod_zip = mod_dir + "/" + mod['dir'] + ".zip"
                        urllib.request.urlretrieve(mod['url'], mod_zip)
                        with zipfile.ZipFile(mod_zip, 'r') as zip_ref:
                            zip_ref.extractall(mod_dir)

                    # Delete mod zip file
                    os.remove(mod_zip)
                    tk.messagebox.showinfo("Successful Install", f"Successfully installed {mod['name']}.")
                else:
                    tk.messagebox.showerror(f"Not Installing {mod['name']}", f"Not installing {mod['name']} by {mod['author']}.")

        # Show completion message
        tk.messagebox.showinfo("Installation completed", "The mods have been installed successfully!")

    def exit_launcher(self):
        root.quit()

root = tk.Tk()  # Create main window
gui = ModInstallerGUI(root)  # Pass main window as argument to create instance of ModInstallerGUI
root.mainloop()  # Start event loop for main window
