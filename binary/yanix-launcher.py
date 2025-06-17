#!/usr/bin/env python3
import os
import subprocess
import webbrowser
import shutil
import time
import threading
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout,
    QWidget, QLabel, QMessageBox, QComboBox, QDialog, QHBoxLayout
)
from PyQt5.QtGui import QFont, QPalette, QLinearGradient, QColor, QBrush, QIcon
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

try:
    from pypresence import Presence
    presence_enabled = True
except ImportError:
    presence_enabled = False
    print("pypresence library not found. Discord Rich Presence will be disabled.")
    print("Install it with: pip install pypresence")

CLIENT_ID = '1383809366460989490'

def find_yanix_launcher():
    home_dir = os.path.expanduser("~")
    for root, dirs, files in os.walk(home_dir):
        if "yanix-launcher" in dirs:
            return os.path.join(root, "yanix-launcher")
    return None

YANIX_PATH = find_yanix_launcher()
if not YANIX_PATH:
    print("Warning: yanix-launcher folder not found in home directory. Using current directory as fallback.")
    YANIX_PATH = os.getcwd()

CONFIG_PATH = os.path.join(YANIX_PATH, "binary/data/game_path.txt")
LANG_PATH = os.path.join(YANIX_PATH, "binary/data/multilang.txt")
VERSION_PATH = os.path.join(YANIX_PATH, "binary/data/version.txt")
BACKGROUND_PATH = os.path.join(YANIX_PATH, "binary/data/background.txt")
ICON_PATH = os.path.join(YANIX_PATH, "binary/data/Yanix-Launcher.png")

os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)

LANGUAGES = {
    "en": {"welcome": "Welcome to Yanix Launcher", "loading": "Loading", "play": "Play", "github": "GitHub", "settings": "Settings", "download": "Download Game", "select_language": "Select Language", "select_exe": "Select .exe for WINE", "support": "Support", "discord": "Discord", "lang_changed": "Language changed!", "exit": "Exit", "missing_path": "Uh oh, try extract in home folder", "select_background": "Select Background Image", "winetricks": "Winetricks"},
    "es": {"welcome": "Bienvenido a Yanix Launcher", "loading": "Cargando", "play": "Jugar", "github": "GitHub", "settings": "Configuración", "download": "Descargar Juego", "select_language": "Seleccionar Idioma", "select_exe": "Seleccionar .exe para WINE", "support": "Soporte", "discord": "Discord", "lang_changed": "¡Idioma cambiado!", "exit": "Salir", "missing_path": "Uh oh, intenta extraerlo en tu carpeta personal", "select_background": "Seleccionar Imagen de Fondo", "winetricks": "Winetricks"},
    "pt": {"welcome": "Bem-vindo ao Yanix Launcher", "loading": "Carregando", "play": "Jogar", "github": "GitHub", "settings": "Configurações", "download": "Baixar Jogo", "select_language": "Selecionar Idioma", "select_exe": "Selecionar .exe para WINE", "support": "Suporte", "discord": "Discord", "lang_changed": "Idioma alterado!", "exit": "Sair", "missing_path": "Uh oh... tente extrai-lo na sua pasta pessoal.", "select_background": "Selecionar Imagem de Fundo", "winetricks": "Winetricks"},
    "ru": {"welcome": "Добро пожаловать в Yanix Launcher", "loading": "Загрузка", "play": "Играть", "github": "GitHub", "settings": "Настройки", "download": "Скачать игру", "select_language": "Выбрать язык", "select_exe": "Выбрать .exe для WINE", "support": "Поддержка", "discord": "Discord", "lang_changed": "Язык изменен!", "exit": "Выход", "missing_path": "Упс, попробуйте извлечь в домашнюю папку", "select_background": "Выбрать изображение фона", "winetricks": "Winetricks"},
    "ja": {"welcome": "Yanix Launcherへようこそ", "loading": "読み込み中", "play": "プレイ", "github": "GitHub", "settings": "設定", "download": "ゲームをダウンロード", "select_language": "言語を選択", "select_exe": "WINE用の.exeを選択", "support": "サポート", "discord": "Discord", "lang_changed": "言語が変更されました！", "exit": "終了", "missing_path": "うーん、ホームフォルダに抽出してみてください", "select_background": "背景画像を選択", "winetricks": "Winetricks"},
    "zh": {"welcome": "欢迎使用 Yanix Launcher", "loading": "加载中", "play": "游戏", "github": "GitHub", "settings": "设置", "download": "下载游戏", "select_language": "选择语言", "select_exe": "选择 WINE 的 .exe 文件", "support": "支持", "discord": "Discord", "lang_changed": "语言已更改！", "exit": "退出", "missing_path": "哎呀，请尝试将其解压到主文件夹", "select_background": "选择背景图片", "winetricks": "Winetricks"},
    "fr": {"welcome": "Bienvenue sur Yanix Launcher", "loading": "Chargement", "play": "Jouer", "github": "GitHub", "settings": "Paramètres", "download": "Télécharger le jeu", "select_language": "Sélectionner la langue", "select_exe": "Sélectionner .exe pour WINE", "support": "Support", "discord": "Discord", "lang_changed": "Langue changée !", "exit": "Quitter", "missing_path": "Oups, essayez de l'extraire dans votre dossier personnel", "select_background": "Sélectionner l'image de fond", "winetricks": "Winetricks"},
    "ar": {"welcome": "مرحبًا بك في Yanix Launcher", "loading": "جار التحميل", "play": "تشغيل", "github": "GitHub", "settings": "الإعدادات", "download": "تنزيل اللعبة", "support": "الدعم", "discord": "Discord", "lang_changed": "تم تغيير اللغة!", "exit": "خروج", "missing_path": "أوه، حاول استخراجها في المجلد الرئيسي", "select_background": "اختيار صورة الخلفية", "winetricks": "Winetricks"},
    "ko": {"welcome": "Yanix Launcher에 오신 것을 환영합니다", "loading": "로딩 중", "play": "플레이", "github": "GitHub", "settings": "설정", "download": "게임 다운로드", "select_language": "언어 선택", "select_exe": "WINE용 .exe 선택", "support": "지원", "discord": "Discord", "lang_changed": "언어가 변경되었습니다!", "exit": "종료", "missing_path": "오류, 홈 폴더에 압축을 풀어 보세요", "select_background": "배경 이미지 선택", "winetricks": "Winetricks"},
    "ndk": {"welcome": "niko Niko-Launcher!", "loading": "You Activated the Nikodorito Easter-egg!", "play": "Niko", "github": "GitHub", "settings": "Meow", "download": "Dalad Gaem", "select_language": "niko to to ni", "select_exe": "niko to to ni WINE", "support": "niko to to ni", "discord": "Discorda", "lang_changed": "Niko DOrito! Niko dorito kimegasu", "exit": "nikotorito", "missing_path": "Uh oh,}try extract in home foldar,stupid", "select_background": "Niko dorito... select the back.", "winetricks": "manage the fucking winetricks"}
}

def get_language():
    try:
        if os.path.exists(LANG_PATH):
            with open(LANG_PATH, "r") as f:
                return f.read().strip()
    except IOError as e:
        print(f"Error reading language file: {e}")
    return "en"


class SettingsDialog(QDialog):
    def __init__(self, lang_code, lang_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle(lang_data["settings"])
        self.setFixedSize(300, 180)

        layout = QVBoxLayout()
        self.lang_selector = QComboBox()
        self.lang_selector.addItems(LANGUAGES.keys())
        self.lang_selector.setCurrentText(lang_code)

        lang_label = QLabel(lang_data["select_language"])

        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(self.apply_settings)
        apply_btn.setStyleSheet("color: black")

        layout.addWidget(lang_label)
        layout.addWidget(self.lang_selector)
        layout.addWidget(apply_btn)

        self.setLayout(layout)

    def apply_settings(self):
        lang = self.lang_selector.currentText()
        try:
            with open(LANG_PATH, "w") as f:
                f.write(lang)

            message = LANGUAGES[lang]["lang_changed"]
            if lang not in ["en", "pt", "ndk"]:
                message += "\n\nthis launguage is 100% AI and may have malfunctions"

            QMessageBox.information(self, "Info", message)

            if self.parent():
                self.parent().retranslate_ui()

            self.accept()
        except IOError as e:
            QMessageBox.critical(self, "Error", f"Could not save language setting: {e}")


class YanixLauncher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lang_code = get_language()
        self.lang = LANGUAGES.get(self.lang_code, LANGUAGES["en"])

        self.setWindowTitle("Yanix Launcher")
        self.setFixedSize(1100, 600)

        if os.path.exists(ICON_PATH):
            self.setWindowIcon(QIcon(ICON_PATH))

        self.set_gradient_background()
        self.setup_ui()

        self.rpc = None
        self.start_time = int(time.time())
        if presence_enabled:
            self.init_rpc()

    def init_rpc(self):
        try:
            self.rpc = Presence(CLIENT_ID)
            self.rpc.connect()
            self.update_rpc(details="In the launcher", state="Browsing...")
            print("Discord Rich Presence connected.")
        except Exception as e:
            print(f"Failed to connect to Discord RPC: {e}")
            self.rpc = None

    def update_rpc(self, details, state=None):
        if not self.rpc:
            return
        try:
            self.rpc.update(
                details=details,
                state=state,
                start=self.start_time,
                large_image="yanix_logo",
                large_text="Yanix Launcher"
            )
        except Exception as e:
            print(f"Failed to update Discord RPC: {e}")
            self.rpc.close()
            self.rpc = None

    def set_gradient_background(self):
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#ff4da6"))
        gradient.setColorAt(1, QColor("#6666ff"))
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

    def setup_ui(self):
        main_layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.left_layout.setAlignment(Qt.AlignTop)

        font = QFont("Futura", 16)
        version_font = QFont("Futura", 10)

        button_style = """
            QPushButton {
                color: black;
                background-color: white;
                padding: 8px;
                border-radius: 6px;
                border: 1px solid #ccc;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """

        self.play_button = QPushButton()
        self.play_button.setFont(font)
        self.play_button.setStyleSheet(button_style)
        self.play_button.clicked.connect(self.launch_game)
        self.left_layout.addWidget(self.play_button)

        self.settings_button = QPushButton()
        self.settings_button.setFont(font)
        self.settings_button.setStyleSheet(button_style)
        self.settings_button.clicked.connect(self.open_settings)
        self.left_layout.addWidget(self.settings_button)

        self.select_exe_button = QPushButton()
        self.select_exe_button.setFont(font)
        self.select_exe_button.setStyleSheet(button_style)
        self.select_exe_button.clicked.connect(self.select_exe)
        self.left_layout.addWidget(self.select_exe_button)

        self.download_button = QPushButton()
        self.download_button.setFont(font)
        self.download_button.setStyleSheet(button_style)
        self.download_button.clicked.connect(self.download_game)
        self.left_layout.addWidget(self.download_button)

        self.winetricks_button = QPushButton()
        self.winetricks_button.setFont(font)
        self.winetricks_button.setStyleSheet(button_style)
        self.winetricks_button.clicked.connect(self.manage_winetricks)
        self.left_layout.addWidget(self.winetricks_button)

        self.support_button = QPushButton()
        self.support_button.setFont(font)
        self.support_button.setStyleSheet(button_style)
        self.support_button.clicked.connect(lambda: webbrowser.open("https://github.com/NikoYandere/Yanix-Launcher/issues"))
        self.left_layout.addWidget(self.support_button)

        self.discord_button = QPushButton()
        self.discord_button.setFont(font)
        self.discord_button.setStyleSheet(button_style)
        self.discord_button.clicked.connect(lambda: webbrowser.open("https://discord.gg/7JC4FGn69U"))
        self.left_layout.addWidget(self.discord_button)

        self.version_label = QLabel()
        self.version_label.setFont(version_font)
        self.version_label.setStyleSheet("color: white; margin-top: 20px;")
        self.left_layout.addWidget(self.version_label)

        blog_view = QWebEngineView()
        blog_view.load(QUrl("https://yanix-launcher.blogspot.com"))

        main_layout.addLayout(self.left_layout, 1)
        main_layout.addWidget(blog_view, 2)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.retranslate_ui()

    def retranslate_ui(self):
        self.lang_code = get_language()
        self.lang = LANGUAGES.get(self.lang_code, LANGUAGES["en"])

        self.play_button.setText(self.lang["play"])
        self.settings_button.setText(self.lang["settings"])
        self.select_exe_button.setText(self.lang["select_exe"])
        self.download_button.setText(self.lang["download"])
        self.winetricks_button.setText(self.lang["winetricks"])
        self.support_button.setText(self.lang["support"])
        self.discord_button.setText(self.lang["discord"])
        self.version_label.setText(f"{self.lang['welcome']} V 0.7")


    def open_settings(self):
        dlg = SettingsDialog(self.lang_code, self.lang, self)
        dlg.exec_()

    def _wait_for_game_exit(self, process):
        process.wait()
        self.update_rpc(details="In the launcher", state="Browsing...")

    def launch_game(self):
        if not os.path.exists(CONFIG_PATH):
            QMessageBox.critical(self, "Error", "Game executable not set. Please select the .exe file in Settings.")
            return

        with open(CONFIG_PATH) as f:
            path = f.read().strip()

        if os.path.exists(path):
            try:
                self.update_rpc(details="Playing Yandere Simulator", state="In-Game")
                game_process = subprocess.Popen(["wine", path])

                monitor_thread = threading.Thread(
                    target=self._wait_for_game_exit,
                    args=(game_process,),
                    daemon=True
                )
                monitor_thread.start()

            except FileNotFoundError:
                 QMessageBox.critical(self, "Error", "WINE is not installed or not in your system's PATH.")
                 self.update_rpc(details="In the launcher", state="Browsing...")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred while launching the game: {e}")
                self.update_rpc(details="In the launcher", state="Browsing...")
        else:
            QMessageBox.critical(self, "Error", "Saved game path is invalid. Please re-select the executable.")

    def select_exe(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Game Executable", "", "EXE Files (*.exe)")
        if file:
            try:
                with open(CONFIG_PATH, "w") as f:
                    f.write(file)
                QMessageBox.information(self, "Success", "Executable path saved successfully.")
            except IOError as e:
                 QMessageBox.critical(self, "Error", f"Could not save executable path: {e}")

    def download_game(self):
        webbrowser.open("https://yanderesimulator.com/dl/latest.zip")

    def manage_winetricks(self):
        if not shutil.which("winetricks"):
            QMessageBox.critical(self, "Error", "Winetricks is not installed or not in your PATH.")
        else:
            try:
                subprocess.Popen(["winetricks"])
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to start Winetricks: {e}")

    def closeEvent(self, event):
        if self.rpc:
            self.rpc.close()
            print("Discord Rich Presence connection closed.")
        event.accept()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    launcher = YanixLauncher()
    launcher.show()
    sys.exit(app.exec_())
