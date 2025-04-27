import os
import tkinter as tk
from tkinter import messagebox, filedialog
import webbrowser
import pygame
import time
import subprocess

def find_yanix_launcher():
    home_dir = os.path.expanduser("~")
    for root, dirs, files in os.walk(home_dir):
        if "yanix-launcher" in dirs:
            return os.path.join(root, "yanix-launcher")
    return None


YANIX_PATH = find_yanix_launcher()

CONFIG_PATH = os.path.join(YANIX_PATH, "binary/data/game_path.txt")
LANG_PATH = os.path.join(YANIX_PATH, "binary/data/multilang.txt")
VERSION_PATH = os.path.join(YANIX_PATH, "binary/data/version.txt")
GITHUB_REPO = "https://github.com/NikoYandere/Yanix-Launcher"
SUPPORT_URL = "https://github.com/NikoYandere/Yanix-Launcher/issues"
DISCORD_URL = "https://discord.gg/7JC4FGn69U"
ICON_PATH = os.path.join(YANIX_PATH, "binary/data/Yanix-Launcher.png")
BG_PATH = os.path.join(YANIX_PATH, "binary/data/Background.png")
BACKGROUND_OPTION_PATH = os.path.join(YANIX_PATH, "binary/data/background.txt")

def select_background():
    def save_background_choice(choice):
        with open(BACKGROUND_OPTION_PATH, "w") as f:
            f.write(choice)
        messagebox.showinfo("Success", f"{LANGUAGES[current_lang]['select_background']}: {choice}")
        bg_image.config(file=os.path.join(YANIX_PATH, f"data/{choice}"))
        bg_win.destroy()

    bg_win = tk.Toplevel(top)
    bg_win.title(LANGUAGES[current_lang]["select_background"])
    bg_win.geometry("300x150")

    tk.Button(bg_win, text="Background.png", command=lambda: save_background_choice("Background.png")).pack(pady=10)
    tk.Button(bg_win, text="Background2.png", command=lambda: save_background_choice("Background2.png")).pack(pady=10)

LANGUAGES = {
    "en": {"welcome": "Welcome to Yanix Launcher", "loading": "Loading", "play": "Play", "github": "GitHub", "settings": "Settings", "download": "Download Game", "select_language": "Select Language", "select_exe": "Select .exe for WINE", "support": "Support", "discord": "Discord", "lang_changed": "Language changed! Restart the launcher.", "exit": "Exit", "missing_path": "Uh oh, try extract in home folder", "select_background": "Select Background Image"},
    "es": {"welcome": "Bienvenido a Yanix Launcher", "loading": "Cargando", "play": "Jugar", "github": "GitHub", "settings": "Configuración", "download": "Descargar Juego", "select_language": "Seleccionar Idioma", "select_exe": "Seleccionar .exe para WINE", "support": "Soporte", "discord": "Discord", "lang_changed": "¡Idioma cambiado! Reinicie el lanzador.", "exit": "Salir", "missing_path": "Uh oh, intenta extraerlo en tu carpeta personal", "select_background": "Seleccionar Imagen de Fondo"},
    "pt": {"welcome": "Bem-vindo ao Yanix Launcher", "loading": "Carregando", "play": "Jogar", "github": "GitHub", "settings": "Configurações", "download": "Baixar Jogo", "select_language": "Selecionar Idioma", "select_exe": "Selecionar .exe para WINE", "support": "Suporte", "discord": "Discord", "lang_changed": "Idioma alterado! Reinicie o lançador.", "exit": "Sair", "missing_path": "Uh oh... tente extrai-lo na sua pasta pessoal.", "select_background": "Selecionar Imagem de Fundo"},
    "ru": {"welcome": "Добро пожаловать в Yanix Launcher", "loading": "Загрузка", "play": "Играть", "github": "GitHub", "settings": "Настройки", "download": "Скачать игру", "select_language": "Выбрать язык", "select_exe": "Выбрать .exe для WINE", "support": "Поддержка", "discord": "Discord", "lang_changed": "Язык изменен! Перезапустите лаунчер.", "exit": "Выход", "missing_path": "Упс, попробуйте извлечь в домашнюю папку", "select_background": "Выбрать изображение фона"},
    "ja": {"welcome": "Yanix Launcherへようこそ", "loading": "読み込み中", "play": "プレイ", "github": "GitHub", "settings": "設定", "download": "ゲームをダウンロード", "select_language": "言語を選択", "select_exe": "WINE用の.exeを選択", "support": "サポート", "discord": "Discord", "lang_changed": "言語が変更されました！ランチャーを再起動してください。", "exit": "終了", "missing_path": "うーん、ホームフォルダに抽出してみてください", "select_background": "背景画像を選択"},
    "zh": {"welcome": "欢迎使用 Yanix Launcher", "loading": "加载中", "play": "游戏", "github": "GitHub", "settings": "设置", "download": "下载游戏", "select_language": "选择语言", "select_exe": "选择 WINE 的 .exe 文件", "support": "支持", "discord": "Discord", "lang_changed": "语言已更改！请重新启动启动器。", "exit": "退出", "missing_path": "哎呀，请尝试将其解压到主文件夹", "select_background": "选择背景图片"},
    "fr": {"welcome": "Bienvenue sur Yanix Launcher", "loading": "Chargement", "play": "Jouer", "github": "GitHub", "settings": "Paramètres", "download": "Télécharger le jeu", "select_language": "Sélectionner la langue", "select_exe": "Sélectionner .exe pour WINE", "support": "Support", "discord": "Discord", "lang_changed": "Langue changée ! Redémarrez le lanceur.", "exit": "Quitter", "missing_path": "Oups, essayez de l'extraire dans votre dossier personnel", "select_background": "Sélectionner l'image de fond"},
    "ar": {"welcome": "مرحبًا بك في Yanix Launcher", "loading": "جار التحميل", "play": "تشغيل", "github": "GitHub", "settings": "الإعدادات", "download": "تنزيل اللعبة", "select_language": "اختيار اللغة", "select_exe": "اختيار .exe لـ WINE", "support": "الدعم", "discord": "Discord", "lang_changed": "تم تغيير اللغة! أعد تشغيل المشغل.", "exit": "خروج", "missing_path": "أوه، حاول استخراجها في المجلد الرئيسي", "select_background": "اختيار صورة الخلفية"},
    "ko": {"welcome": "Yanix Launcher에 오신 것을 환영합니다", "loading": "로딩 중", "play": "플레이", "github": "GitHub", "settings": "설정", "download": "게임 다운로드", "select_language": "언어 선택", "select_exe": "WINE용 .exe 선택", "support": "지원", "discord": "Discord", "lang_changed": "언어가 변경되었습니다! 런처를 재시작하십시오.", "exit": "종료", "missing_path": "오류, 홈 폴더에 압축을 풀어 보세요", "select_background": "배경 이미지 선택"},
    "ndk": {"welcome": "niko Niko-Launcher!", "loading": "You Activated the Nikodorito Easter-egg!", "play": "Niko", "github": "GitHub", "settings": "Meow", "download": "Dalad Gaem", "select_language": "niko to to ni", "select_exe": "niko to to ni WINE", "support": "niko to to ni", "discord": "Discorda", "lang_changed": "Niko DOrito! Niko dorito kimegasu", "exit": "nikotorito", "missing_path": "Uh oh,}try extract in home foldar,stupid", "select_background": "Niko dorito... select the back."}
}

def load_language():
    return open(LANG_PATH).read().strip() if os.path.exists(LANG_PATH) else "en"

def load_version():
    if os.path.exists(VERSION_PATH):
        with open(VERSION_PATH, 'r') as version_file:
            return version_file.read().strip()
    return "0.2.2.6"

def open_support():
    webbrowser.open(SUPPORT_URL)

def open_discord():
    webbrowser.open(DISCORD_URL)

def launch_game():
    if os.path.exists(CONFIG_PATH):
        game_path = open(CONFIG_PATH).read().strip()
        if os.path.exists(game_path):
            top.withdraw()

            subprocess.run(["wine", game_path], check=True)
            
            top.deiconify()
            return
    messagebox.showerror("Error", "No valid executable selected!")

def open_github():
    webbrowser.open(GITHUB_REPO)

def open_settings():
    settings_window = tk.Toplevel(top)
    settings_window.title(LANGUAGES[current_lang]["settings"])
    settings_window.geometry("248x430")
    
    tk.Button(settings_window, text=LANGUAGES[current_lang]["select_language"], command=select_language).pack(pady=10)
    tk.Button(settings_window, text=LANGUAGES[current_lang]["select_exe"], command=select_exe).pack(pady=10)
    tk.Button(settings_window, text=LANGUAGES[current_lang]["select_background"], command=select_background).pack(pady=10)

def exit_launcher():
    top.quit()

def select_language():
    lang_window = tk.Toplevel(top)
    lang_window.title("Select Language")
    lang_window.geometry("268x429")
    
    def set_language(lang):
        with open(LANG_PATH, "w") as f:
            f.write(lang)
        messagebox.showinfo("Success", LANGUAGES[lang]["lang_changed"])
        lang_window.destroy()
    
    for lang in ["en", "es", "pt","ru","zh","fr","ja","ko","ar"]:
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
    for button, pos in zip(buttons, [(0.5, 0.3), (0.5, 0.4), (0.5, 0.5), (0.5, 0.6), (0.5, 0.7)]):  
        button.place(relx=pos[0], rely=pos[1], anchor=tk.CENTER)
    
    exit_button.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

def animate_welcome(duration=4):
    step_time = duration * 1000 // 40
    def update_text(step=0):
        if step < 40:
            dots = "." * (step % 4)
            loading_label.config(text=f"{LANGUAGES[current_lang]['loading']}{dots}")
            top.after(step_time, update_text, step + 1)
        else:
            show_buttons()
    update_text()

def play_startup_sound():
    pygame.mixer.init()
    sound_path = os.path.join(YANIX_PATH, "binary/data/startup.mp3")
    if os.path.exists(sound_path):
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()

top = tk.Tk()
top.title("Yanix-Launcher")
top.geometry("400x600")
top.resizable(False,False)

if not os.path.exists(YANIX_PATH):
    messagebox.showerror("Error", LANGUAGES[load_language()]["missing_path"])
    top.destroy()
else:
    if os.path.exists(ICON_PATH):
        top.iconphoto(True, tk.PhotoImage(file=ICON_PATH))
    
    if os.path.exists(BG_PATH):
        bg_image = tk.PhotoImage(file=BG_PATH)
        bg_label = tk.Label(top, image=bg_image)
        bg_label.place(relwidth=1, relheight=1)
    
    current_lang = load_language()
    
    welcome_label = tk.Label(top, text=LANGUAGES[current_lang]["welcome"], font=("", 20, "normal"), bg="white")
    welcome_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
    
    loading_label = tk.Label(top, text=LANGUAGES[current_lang]["loading"], font=("Futura", 14, "normal"), bg="white")
    loading_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    buttons = [
        tk.Button(top, text=LANGUAGES[current_lang]["play"], font=("Futura", 30, "normal"), command=launch_game),
        tk.Button(top, text=LANGUAGES[current_lang]["download"], font=("Futura", 10, "normal"), command=lambda: subprocess.run([ "wget", "https://yanderesimulator.com/dl/latest.zip"], check=True)),
        tk.Button(top, text=LANGUAGES[current_lang]["github"], font=("Futura", 10, "normal"), command=open_github),
        tk.Button(top, text=LANGUAGES[current_lang]["discord"], font=("Futura", 10, "normal"), command=open_discord),
        tk.Button(top, text=LANGUAGES[current_lang]["settings"], font=("Futura", 10, "normal"), command=open_settings)
    ]
    
    exit_button = tk.Button(top, text=LANGUAGES[current_lang]["exit"], font=("Futura", 10, "normal"), command=exit_launcher)

    version_label = tk.Label(top, text=f"Version: {load_version()}", font=("Futura", 8), bg="white")
    version_label.place(relx=0.5, rely=0.95, anchor=tk.CENTER)

    play_startup_sound()
    animate_welcome()
    top.mainloop() 
