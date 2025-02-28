import subprocess
import os
import tkinter as tk
from tkinter import messagebox, filedialog
import webbrowser

YANIX_PATH = os.path.expanduser("~/yanix-launcher")
CONFIG_PATH = os.path.join(YANIX_PATH, "binary/data/game_path.txt")
LANG_PATH = os.path.join(YANIX_PATH, "binary/data/multilang.txt")
GITHUB_REPO = "https://github.com/NikoYandere/Yanix-Launcher"
YOUTUBE_CHANNEL = "https://www.youtube.com/@NikoYandere"
ICON_PATH = os.path.join(YANIX_PATH, "binary/data/Yanix-Launcher.png")
BG_PATH = os.path.join(YANIX_PATH, "binary/data/Background.png")

LANGUAGES = {
    "en": {"welcome": "Welcome to Yanix Launcher", "loading": "Loading", "play": "Play", "github": "GitHub", "settings": "Settings", "download": "Download Game", "select_language": "Select Language", "select_exe": "Select .exe for WINE", "support": "Support my channel", "lang_changed": "Language changed! Restart the launcher."},
    "es": {"welcome": "Bienvenido a Yanix Launcher", "loading": "Cargando", "play": "Jugar", "github": "GitHub", "settings": "Configuración", "download": "Descargar Juego", "select_language": "Seleccionar Idioma", "select_exe": "Seleccionar .exe para WINE", "support": "¡apoya mi trabajo!", "lang_changed": "¡Idioma cambiado! Reinicie el lanzador."},
    "pt": {"welcome": "Bem-vindo ao Yanix Launcher", "loading": "Carregando", "play": "Jogar", "github": "GitHub", "settings": "Configurações", "download": "Baixar Jogo", "select_language": "Selecionar Idioma", "select_exe": "Selecionar .exe para WINE", "support": "Apoie meu canal!", "lang_changed": "Idioma alterado! Reinicie o lançador."}
}

def load_language():
    return open(LANG_PATH).read().strip() if os.path.exists(LANG_PATH) else "en"

def open_support():
    webbrowser.open(YOUTUBE_CHANNEL)

def launch_game():
    if os.path.exists(CONFIG_PATH):
        game_path = open(CONFIG_PATH).read().strip()
        if os.path.exists(game_path):
            subprocess.run(["wine", game_path], check=True)
            return
    messagebox.showerror("Error", "No valid executable selected!")

def open_github():
    webbrowser.open(GITHUB_REPO)

def open_settings():
    settings_window = tk.Toplevel(top)
    settings_window.title(LANGUAGES[current_lang]["settings"])
    settings_window.geometry("300x200")
    
    tk.Button(settings_window, text=LANGUAGES[current_lang]["select_language"], command=select_language).pack(pady=10)
    tk.Button(settings_window, text=LANGUAGES[current_lang]["select_exe"], command=select_exe).pack(pady=10)

def select_language():
    lang_window = tk.Toplevel(top)
    lang_window.title("Select Language")
    lang_window.geometry("200x150")
    
    def set_language(lang):
        with open(LANG_PATH, "w") as f:
            f.write(lang)
        messagebox.showinfo("Success", LANGUAGES[lang]["lang_changed"])
        lang_window.destroy()
    
    for lang in ["en", "es", "pt"]:
        tk.Button(lang_window, text=lang.upper(), command=lambda l=lang: set_language(l)).pack(pady=5)

def select_exe():
    file_path = filedialog.askopenfilename(title=LANGUAGES[current_lang]["select_exe"], filetypes=[["Executables", "*.exe"]])
    if file_path:
        with open(CONFIG_PATH, "w") as file:
            file.write(file_path)
        messagebox.showinfo("Success", "Executable saved!")

def show_buttons():
    welcome_label.destroy()
    loading_label.destroy()
    for button, pos in zip(buttons, [(0.5, 0.3), (0.5, 0.4), (0.5, 0.5), (0.05, 0.95), (0.95, 0.95)]):
        button.place(relx=pos[0], rely=pos[1], anchor=tk.CENTER if pos[0] == 0.5 else tk.SW if pos[0] == 0.05 else tk.SE)

def animate_welcome(duration=10):
    step_time = duration * 1000 // 40
    def update_text(step=0):
        if step < 40:
            dots = "." * (step % 4)
            loading_label.config(text=f"{LANGUAGES[current_lang]['loading']}{dots}")
            top.after(step_time, update_text, step + 1)
        else:
            show_buttons()
    update_text()

top = tk.Tk()
top.title("Yanix-Launcher")
top.geometry("400x600")
top.resizable(False, False)

if os.path.exists(ICON_PATH):
    top.iconphoto(True, tk.PhotoImage(file=ICON_PATH))

if os.path.exists(BG_PATH):
    bg_image = tk.PhotoImage(file=BG_PATH)
    bg_label = tk.Label(top, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)

current_lang = load_language()

welcome_label = tk.Label(top, text=LANGUAGES[current_lang]["welcome"], font=("Arial", 20, "bold"), bg="white")
welcome_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

loading_label = tk.Label(top, text=LANGUAGES[current_lang]["loading"], font=("Arial", 14, "bold"), bg="white")
loading_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

buttons = [
    tk.Button(top, text=LANGUAGES[current_lang]["play"], font=("Arial", 30, "bold"), command=launch_game),
    tk.Button(top, text=LANGUAGES[current_lang]["download"], font=("Arial", 10, "bold"), command=lambda: subprocess.run(["x-terminal-emulator", "-e", "sh", "-c", "cd yanix-launcher && wget https://yanderesimulator.com/dl/latest.zip"], check=True)),
    tk.Button(top, text=LANGUAGES[current_lang]["github"], font=("Arial", 10, "bold"), command=open_github),
    tk.Button(top, text=LANGUAGES[current_lang]["settings"], font=("Arial", 10, "bold"), command=open_settings),
    tk.Button(top, text=LANGUAGES[current_lang]["support"], font=("Arial", 10, "bold"), command=open_support)
]

animate_welcome()
top.mainloop()

