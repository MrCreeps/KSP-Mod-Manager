import os
import urllib.request
import zipfile
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import shutil
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def dynamic_getter():
    MOD_LIST = []

    # Gets the content from the mods page
    url = "https://spacedock.info/kerbal-space-program-2/browse/new"
    search_term = "mod"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Gets the links and formats them into separate variables for later use
    for link in (soup.find_all("a")):
        href = link.get("href")
        if href and search_term in href and href.endswith("/download"):
            download_link = urljoin(url, href).replace("%20", "")
            last_slash_index = download_link.rfind('/')
            mod_page_link = download_link[:last_slash_index]
            mod_response = requests.get(mod_page_link)
            mod_text = mod_response.text
            mod_soup = BeautifulSoup(mod_text, 'html.parser')
            mod_text = mod_soup.get_text()
            lines = mod_text.split("\n")
            mod_name = mod_page_link[32:]

            # Checks if it supports SpaceWarp and gets the Author and License
            supportsSpaceWarp = False
            for i in range(len(lines)):
                if "spacewarp" in lines[i].lower():
                    supportsSpaceWarp = True
            if supportsSpaceWarp:
                for i in range(len(lines)):
                    if "Author:" in lines[i]:
                        author = lines[i+3].strip()
                        break
                for i in range(len(lines)):
                    if "License:" in lines[i]:
                        license = lines[i+2].strip()
                        break
                # Adds the mod to MOD_LIST
                MOD_LIST.append({
                    "name" : f"{mod_name}",
                    "author" : f"{author}",
                    "url" : f"{download_link}",
                    "license" : f"{license}",
                    "dir" : f"{mod_name}",
                    "fulldir" : "False"
                })
    return MOD_LIST

# Sets constants
MOD_LIST = dynamic_getter()
print(MOD_LIST)

DEFAULT_FILE_PATH = "C:/Program Files (x86)/Steam/steamapps/common/Kerbal Space Program 2/"
vers = "0.4.1"

# Initializes ModInstallerGUI
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

        # Create frame for mod list
        self.mod_frame = ttk.LabelFrame(master, text="Select mods to install")
        self.mod_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Checkboxes for mod selection
        self.mod_vars = []
        self.mod_checkboxes = []
        row = 0
        column = 0
        for i, mod in enumerate(MOD_LIST):
            if mod['name'] != "SpaceWarp":
                var = tk.BooleanVar(value=False)
                checkbox = ttk.Checkbutton(self.mod_frame, text=f"{mod['name']} by {mod['author']}", variable=var)
                checkbox.grid(row=row, column=column, sticky="w", padx=(0, 10), pady=5)
                self.mod_vars.append(var)
                self.mod_checkboxes.append(checkbox)
                # Extend columns
                row += 1
                if row == 8:
                    row = 0
                    column += 1

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
        # Intalls SpaceWarp
        shouldInstall = tk.messagebox.askquestion("Install SW", "Install SpaceWarp?")
        if shouldInstall == "yes":
            file_path = self.path_entry.get()
            mod_zip = os.path.join(file_path, f"SPACEWARP.zip")
            urllib.request.urlretrieve("https://spacedock.info/mod/3257/SpaceWarp/download", mod_zip)
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

    def select_directory(self):
        path = tk.filedialog.askdirectory(initialdir="/", title="Select KSP2 directory")
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, path)

    def remove_mods(self):
        # Get file path from entry widget
        file_path = self.path_entry.get() + "/SpaceWarp/"

        # Checks if the mod directory has mods in it
        mod_dir = f"{file_path}/mods/"
        if not os.path.exists(mod_dir):
            tk.messagebox.showerror("Nonexistant Mod Directory", "Try installing mods before removing them ;)")
            return
        
        # Remove selected mods
        for i, mod in enumerate(MOD_LIST):
            if self.mod_vars[i].get():
                confirm = tk.messagebox.askquestion(f"{mod['name']} Remove", f"Remove {mod['name']} by {mod['author']}?", icon="question")
                if confirm == "yes":
                    mod_path = f"{mod_dir}{mod['name']}" ########################## CHANGED FROM DIR TO NAME #############################
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
                    
                    # Downloads the mod zip
                    mod_zip = mod_dir + "/" + mod['dir'] + ".zip"
                    urllib.request.urlretrieve(mod['url'], mod_zip)
                    
                    # Checks what's in the folder
                    with zipfile.ZipFile(mod_zip, 'r') as zip_ref:
                        folder_name = None
                        for file_name in zip_ref.namelist():
                            if '/' in file_name:
                                current_folder = file_name.split('/')[0]
                                if folder_name is None or current_folder != folder_name:
                                    folder_name = current_folder
                                    break
                    
                    # Checks where to unzip
                    if folder_name == "SpaceWarp":
                        extract_dir = self.path_entry.get()
                    else:
                        extract_dir = mod_dir

                    # Unzips
                    with zipfile.ZipFile(mod_zip, 'r') as zip_ref:
                        zip_ref.extractall(extract_dir)
                        
                     
                    # Rename the newly extracted folder to mod['name']



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
icon = tk.PhotoImage(file = "alphaLauncherlogo.png")
root.iconphoto(False, icon)  
root.mainloop()  # Start event loop for main window
