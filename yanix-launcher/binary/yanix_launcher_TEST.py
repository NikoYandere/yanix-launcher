import subprocess
import os
import tkinter as tk
from tkinter import messagebox, filedialog
import webbrowser
from datetime import datetime

YANIX_PATH = os.path.expanduser("~/yanix-launcher")
CONFIG_PATH = os.path.join(YANIX_PATH, "binary/data/game_path.txt")
LANG_PATH = os.path.join(YANIX_PATH, "binary/data/multilang.txt")
LOG_PATH = os.path.join(YANIX_PATH, "yanix_log.txt")
GITHUB_REPO = "https://github.com/NikoYandere/Yanix-Launcher"
ICON_PATH = os.path.join(YANIX_PATH, "binary/data/Yanix-Launcher.png")
BG_PATH = os.path.join(YANIX_PATH, "binary/data/Background.png")

LANGUAGES = {
    "en": {"welcome": "Welcome to Yanix Launcher", "loading": "Loading", "play": "Play", "github": "GitHub", "settings": "Settings", "download": "Download Game"},
    "es": {"welcome": "Bienvenido a Yanix Launcher", "loading": "Cargando", "play": "Jugar", "github": "GitHub", "settings": "Configuración", "download": "Descargar Juego"},
    "pt": {"welcome": "Bem-vindo ao Yanix Launcher", "loading": "Carregando", "play": "Jogar", "github": "GitHub", "settings": "Configurações", "download": "Baixar Jogo"}
}

def load_language():
    if os.path.exists(LANG_PATH):
        with open(LANG_PATH, "r") as file:
            lang = file.read().strip()
            if lang in LANGUAGES:
                return lang
    return "en"

def save_language(lang):
    with open(LANG_PATH, "w") as file:
        file.write(lang)

def log_event(message):
    try:
        with open(LOG_PATH, "a") as log_file:
            timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
            log_file.write(f"{timestamp} {message}\n")
    except Exception:
        pass

def check_yanix_folder():
    if not os.path.exists(YANIX_PATH):
        log_event("Folder not found! Cloning from GitHub...")
        subprocess.run(["git", "clone", GITHUB_REPO, YANIX_PATH], check=True)
        log_event("Repository cloned successfully.")

def select_exe():
    exe_path = filedialog.askopenfilename(title="Select .exe", filetypes=[["Executables", "*.exe"]])
    if exe_path:
        with open(CONFIG_PATH, "w") as file:
            file.write(exe_path)
        log_event(f"Game executable saved: {exe_path}")
        messagebox.showinfo("Success", "Executable saved!")

def launch_game():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as file:
            game_path = file.read().strip()
            if os.path.exists(game_path):
                subprocess.run(["wine", game_path], check=True)
                return
    messagebox.showerror("Error", "No valid executable selected!")

def open_github():
    webbrowser.open(GITHUB_REPO)

def download_game():
    subprocess.run(["x-terminal-emulator", "-e", "sh", "-c", "cd yanix-launcher && wget https://yanderesimulator.com/dl/latest.zip"], check=True)
    messagebox.showinfo("Success", "Download started!")

def update_loading_text():
    global loading_index
    dots = "." * (loading_index % 4)
    loading_label.config(text=f"{LANGUAGES[current_lang]['loading']}{dots}")
    loading_index += 1
    if loading_index <= 40:
        top.after(250, update_loading_text)
    else:
        show_buttons()

def show_buttons():
    welcome_label.destroy()
    loading_label.destroy()
    play_button.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
    download_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
    github_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    settings_button.place(relx=0.05, rely=0.95, anchor=tk.SW)

check_yanix_folder()
current_lang = load_language()

top = tk.Tk()
top.title("Yanix-Launcher")
top.geometry("400x600")
top.resizable(False, False)

# Definir ícone
if os.path.exists(ICON_PATH):
    top.iconphoto(True, tk.PhotoImage(file=ICON_PATH))

# Definir fundo
if os.path.exists(BG_PATH):
    bg_image = tk.PhotoImage(file=BG_PATH)
    bg_label = tk.Label(top, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)

welcome_label = tk.Label(top, text=LANGUAGES[current_lang]["welcome"], font=("Arial", 20, "bold"), bg="white")
welcome_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

loading_label = tk.Label(top, text=LANGUAGES[current_lang]["loading"], font=("Arial", 14, "bold"), bg="white")
loading_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

play_button = tk.Button(top, text=LANGUAGES[current_lang]["play"], font=("Arial", 30, "bold"), command=launch_game)
download_button = tk.Button(top, text=LANGUAGES[current_lang]["download"], font=("Arial", 10, "bold"), command=download_game)
github_button = tk.Button(top, text=LANGUAGES[current_lang]["github"], font=("Arial", 10, "bold"), command=open_github)
settings_button = tk.Button(top, text=LANGUAGES[current_lang]["settings"], font=("Arial", 10, "bold"), command=select_exe)

loading_index = 0
update_loading_text()

top.mainloop()

