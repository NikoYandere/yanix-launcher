import subprocess
import os
import tkinter as tk
from tkinter import messagebox

def launch_game():
    game_path = os.path.expanduser("~/yanix-launcher/YandereSimulator.exe")
    
    if not os.path.exists(game_path):
        messagebox.showerror("Erro", "O arquivo do jogo não foi encontrado!")
        return
    
    try:
        subprocess.run(["wine", game_path], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erro", f"Erro ao iniciar o jogo: {e}")

def download_latest_version():
    terminal_command = "cd Downloads && wget https://yanderesimulator.com/dl/latest.zip && mv ~/Downloads/latest.zip ~/yanix-launcher"
    subprocess.run(["x-terminal-emulator", "-e", "bash", "-c", terminal_command])

# Criando a interface
top = tk.Tk()
top.title("Yanix-Launcher")  # Nome da janela na dock e DEs
os.environ["WM_CLASS"] = "Yanix-Launcher"
os.environ["XDG_CURRENT_DESKTOP"] = "Yanix-Launcher"
top.geometry("400x600")
top.resizable(False, False)  # Impede redimensionamento da janela

# Definir fundo
bg_path = os.path.expanduser("yanix-launcher/yanixdata/Background.png")
if os.path.exists(bg_path):
    bg_image = tk.PhotoImage(file=bg_path)
    bg_label = tk.Label(top, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)

# Definir ícone
icon_path = os.path.expanduser("yanix-launcher/yanixdata/Yanix-Launcher.png")
if os.path.exists(icon_path):
    top.iconphoto(True, tk.PhotoImage(file=icon_path))

# Botão Play
play_button = tk.Button(top, text="Play", font=("Arial", 30, "bold"), fg="black", bg="white", command=launch_game)
play_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)  # Ajusta a posição do botão Play

# Botão Download
download_button = tk.Button(top, text="Download latest version of Yandere Simulator (extract after complete!)", font=("Arial", 10, "bold"), fg="black", bg="white", wraplength=300, command=download_latest_version)
download_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)  # Posiciona abaixo do botão Play


# Iniciar loop da interface
top.mainloop()

