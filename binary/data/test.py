import os
import subprocess
import webbrowser
import shutil
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout,
    QWidget, QLabel, QMessageBox, QComboBox, QDialog, QHBoxLayout
)
from PyQt5.QtGui import QFont, QPalette, QLinearGradient, QColor, QBrush, QIcon
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

def find_yanix_launcher():
    home_dir = os.path.expanduser("~")
    for root, dirs, files in os.walk(home_dir):
        if "yanix-launcher" in dirs:
            return os.path.join(root, "yanix-launcher")
    return None

YANIX_PATH = find_yanix_launcher()
if not YANIX_PATH:
    raise Exception("yanix-launcher folder not found!")

CONFIG_PATH = os.path.join(YANIX_PATH, "binary/data/game_path.txt")
LANG_PATH = os.path.join(YANIX_PATH, "binary/data/multilang.txt")
VERSION_PATH = os.path.join(YANIX_PATH, "binary/data/version.txt")
BACKGROUND_PATH = os.path.join(YANIX_PATH, "binary/data/background.txt")
ICON_PATH = os.path.join(YANIX_PATH, "binary/data/icon.png")

LANGUAGES = {
    "en": {"welcome": "Welcome to Yanix Launcher", "loading": "Loading", "play": "Play", "github": "GitHub",
           "settings": "Settings", "download": "Download Game", "select_language": "Select Language",
           "select_exe": "Select .exe for WINE", "support": "Support", "discord": "Discord",
           "lang_changed": "Language changed! Restart the launcher.", "exit": "Exit",
           "missing_path": "Uh oh, try extract in home folder", "select_background": "Select Background Image",
           "winetricks_missing": "uh,oh... you don't have winetrick installed!", "manage_winetricks": "Manage Winetricks"},
    "pt": {"welcome": "Bem-vindo ao Yanix Launcher", "loading": "Carregando", "play": "Jogar", "github": "GitHub",
           "settings": "Configurações", "download": "Baixar Jogo", "select_language": "Selecionar Idioma",
           "select_exe": "Selecionar .exe para WINE", "support": "Suporte", "discord": "Discord",
           "lang_changed": "Idioma alterado! Reinicie o lançador.", "exit": "Sair",
           "missing_path": "Uh oh... tente extrai-lo na sua pasta pessoal.", "select_background": "Selecionar Imagem de Fundo",
           "winetricks_missing": "uh oh... você não tem o winetricks instalado!", "manage_winetricks": "Gerenciar Winetricks"},
}

def get_language():
    return open(LANG_PATH).read().strip() if os.path.exists(LANG_PATH) else "en"

def get_version():
    return open(VERSION_PATH).read().strip() if os.path.exists(VERSION_PATH) else "1.0.0"

class SettingsDialog(QDialog):
    def __init__(self, lang_code, lang_data):
        super().__init__()
        self.setWindowTitle(lang_data["settings"])
        self.setFixedSize(300, 180)
        layout = QVBoxLayout()
        self.lang_selector = QComboBox()
        self.lang_selector.addItems(LANGUAGES.keys())
        self.lang_selector.setCurrentText(lang_code)
        lang_label = QLabel(lang_data["select_language"])
        bg_button = QPushButton(lang_data["select_background"])
        bg_button.clicked.connect(self.select_background)
        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(self.apply_settings)
        for btn in (bg_button, apply_btn):
            btn.setStyleSheet("color: black")
        layout.addWidget(lang_label)
        layout.addWidget(self.lang_selector)
        layout.addWidget(bg_button)
        layout.addWidget(apply_btn)
        self.setLayout(layout)

    def apply_settings(self):
        lang = self.lang_selector.currentText()
        with open(LANG_PATH, "w") as f:
            f.write(lang)
        QMessageBox.information(self, "Info", LANGUAGES[lang]["lang_changed"])
        self.accept()

    def select_background(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Background", "", "Image Files (*.png *.jpg)")
        if file:
            with open(BACKGROUND_PATH, "w") as f:
                f.write(file)
            QMessageBox.information(self, "Saved", "Background set.")

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

    def set_gradient_background(self):
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#ff4da6"))
        gradient.setColorAt(1, QColor("#6666ff"))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

    def setup_ui(self):
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignTop)
        font = QFont("Futura", 16)
        version_font = QFont("Futura", 10)

        def add_button(label, handler):
            btn = QPushButton(label)
            btn.setFont(font)
            btn.setStyleSheet("color: black; background-color: white; padding: 8px; border-radius: 6px;")
            btn.clicked.connect(handler)
            left_layout.addWidget(btn)

        add_button(self.lang["play"], self.launch_game)
        add_button(self.lang["settings"], self.open_settings)
        add_button(self.lang["select_exe"], self.select_exe)
        add_button(self.lang["download"], self.download_game)
        add_button(self.lang["manage_winetricks"], self.manage_winetricks)
        add_button(self.lang["support"], lambda: webbrowser.open("https://github.com/NikoYandere/Yanix-Launcher/issues"))
        add_button(self.lang["discord"], lambda: webbrowser.open("https://discord.gg/7JC4FGn69U"))

        version = QLabel(f"{self.lang['welcome']} - v{get_version()}")
        version.setFont(version_font)
        version.setStyleSheet("color: white; margin-top: 20px;")
        left_layout.addWidget(version)

        blog_view = QWebEngineView()
        blog_view.load(QUrl("https://yanix-launcher.blogspot.com"))

        main_layout.addLayout(left_layout, 1)
        main_layout.addWidget(blog_view, 2)
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def open_settings(self):
        dlg = SettingsDialog(self.lang_code, self.lang)
        dlg.exec_()

    def launch_game(self):
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH) as f:
                path = f.read().strip()
            if os.path.exists(path):
                subprocess.Popen(["wine", path])
                return
        QMessageBox.critical(self, "Error", self.lang["missing_path"])

    def select_exe(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select .exe", "", "EXE Files (*.exe)")
        if file:
            with open(CONFIG_PATH, "w") as f:
                f.write(file)
            QMessageBox.information(self, "Saved", "Executable saved.")

    def download_game(self):
        webbrowser.open("https://yanderesimulator.com/dl/latest.zip")

    def manage_winetricks(self):
        if not shutil.which("winetricks"):
            QMessageBox.critical(self, "Error", self.lang["winetricks_missing"])
        else:
            subprocess.Popen(["winetricks"])

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    launcher = YanixLauncher()
    launcher.show()
    sys.exit(app.exec_())

