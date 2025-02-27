import subprocess
import os
import tkinter as tk
from tkinter import messagebox, filedialog
import webbrowser
from datetime import datetime

YANIX_PATH = os.path.expanduser("~/yanix-launcher")
CONFIG_PATH = os.path.join(YANIX_PATH, "binary/data/game_path.txt")
LOG_PATH = os.path.join(YANIX_PATH, "yanix_log.txt")
GITHUB_REPO = "https://github.com/NikoYandere/Yanix-Launcher"

def log_event(message):
    """Logs events, but does not make logging mandatory."""
    try:
        with open(LOG_PATH, "a") as log_file:
            timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
            log_file.write(f"{timestamp} {message}\n")
    except Exception:
        pass  # Ignore errors if logging fails

def check_yanix_folder():
    """Checks if the Yanix folder exists, otherwise clones it from GitHub."""
    if not os.path.exists(YANIX_PATH):
        log_event("Yanix-launcher folder not found! Cloning from GitHub...")
        subprocess.run(["git", "clone", GITHUB_REPO, YANIX_PATH], check=True)
        log_event("Repository successfully cloned.")

def load_game_path():
    """Loads the previously saved .exe path."""
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as file:
            return file.read().strip()
    return None

def save_game_path(path):
    """Saves the selected .exe path."""
    with open(CONFIG_PATH, "w") as file:
        file.write(path)
    log_event(f"Game executable saved: {path}")

def select_exe():
    """Opens file explorer to select the .exe and saves the choice."""
    exe_path = filedialog.askopenfilename(title="Select the game executable", filetypes=[("Executables", "*.exe")])
    if exe_path:
        save_game_path(exe_path)
        messagebox.showinfo("Success", "Executable saved!")

def launch_game():
    """Launches the game with the selected executable."""
    game_path = load_game_path()

    if not game_path or not os.path.exists(game_path):
        messagebox.showerror("Error", "No valid executable selected!\nGo to Settings and select a .exe.")
        log_event("Error: No valid executable found.")
        return
    
    try:
        log_event(f"Launching game: {game_path}")
        subprocess.run(["wine", game_path], check=True)
    except subprocess.CalledProcessError as e:
        log_event(f"Error launching game: {e}")
        messagebox.showerror("Error", f"Error launching game: {e}")

def download_latest_version():
    """Downloads the latest version of Yandere Simulator."""
    log_event("Downloading the latest version of Yandere Simulator...")
    terminal_command = "cd Downloads && wget https://yanderesimulator.com/dl/latest.zip && mv ~/Downloads/latest.zip ~/yanix-launcher"
    subprocess.run(["x-terminal-emulator", "-e", "bash", "-c", terminal_command])
    log_event("Download completed.")

def open_github():
    """Opens the Yanix-Launcher repository on GitHub."""
    log_event("Opening GitHub.")
    webbrowser.open(GITHUB_REPO)

def update_loading_text():
    """Updates the 'Loading...' text with an animated effect."""
    global loading_index
    dots = "." * (loading_index % 4)  # Cycles between '', '.', '..', '...'
    loading_label.config(text=f"Loading{dots}")
    loading_index += 1
    if loading_index <= 40:  # 40 cycles of 250ms = 10 seconds
        top.after(250, update_loading_text)
    else:
        show_buttons()

def show_buttons():
    """Removes the animation and displays the buttons."""
    welcome_label.destroy()
    loading_label.destroy()

    play_button.place(relx=0.5, rely=0.35, anchor=tk.CENTER)
    download_button.place(relx=0.5, rely=0.55, anchor=tk.CENTER)
    github_button.place(relx=0.5, rely=0.70, anchor=tk.CENTER)
    settings_button.place(relx=0.05, rely=0.95, anchor=tk.SW)

# Check if the yanix-launcher folder exists
check_yanix_folder()

# Create the interface
top = tk.Tk()
top.title("Yanix-Launcher")
os.environ["WM_CLASS"] = "Yanix-Launcher"
os.environ["XDG_CURRENT_DESKTOP"] = "Yanix-Launcher"
top.geometry("400x600")
top.resizable(False, False)

# Set background
bg_path = os.path.join(YANIX_PATH, "binary/data/Background.png")
if os.path.exists(bg_path):
    bg_image = tk.PhotoImage(file=bg_path)
    bg_label = tk.Label(top, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)

# Set icon
icon_path = os.path.join(YANIX_PATH, "binary/data/Yanix-Launcher.png")
if os.path.exists(icon_path):
    top.iconphoto(True, tk.PhotoImage(file=icon_path))

# Welcome message
welcome_label = tk.Label(top, text="Welcome to Yanix Launcher", font=("Arial", 20, "bold"), fg="black", bg="white")
welcome_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

# Loading text
loading_label = tk.Label(top, text="Loading", font=("Arial", 14, "bold"), fg="black", bg="white")
loading_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Create buttons but do not display them yet
play_button = tk.Button(top, text="Play", font=("Arial", 30, "bold"), fg="black", bg="white", command=launch_game)
download_button = tk.Button(top, text="Download latest version of Yandere Simulator (extract after complete!)", font=("Arial", 10, "bold"), fg="black", bg="white", wraplength=300, command=download_latest_version)
github_button = tk.Button(top, text="GitHub", font=("Arial", 10, "bold"), fg="black", bg="white", command=open_github)
settings_button = tk.Button(top, text="Settings", font=("Arial", 10, "bold"), fg="black", bg="white", command=select_exe)

# Start Loading animation
loading_index = 0
update_loading_text()

# Start the interface loop
top.mainloop()

