#!/usr/bin/python3
import os
import subprocess
import webbrowser
import shutil
import time
import threading
import requests
import zipfile
import sys
import socket
import json

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout,
    QWidget, QLabel, QMessageBox, QComboBox, QDialog, QHBoxLayout,
    QSplashScreen, QProgressDialog
)
from PyQt5.QtGui import QFont, QPalette, QLinearGradient, QColor, QBrush, QIcon, QPainter, QPixmap
from PyQt5.QtCore import Qt, QUrl, QRect, QTimer, QCoreApplication


try:
    from pypresence import Presence
    presence_enabled = True
except ImportError:
    presence_enabled = False


CLIENT_ID = '1383809366460989490'
USER_AGENT = 'YanixLauncher/1.0.0'

YANIX_PATH = os.path.expanduser("~/.local/share/yanix-launcher")
DATA_DOWNLOAD_URL = "https://nikoyandere.github.io/data.zip"
TEMP_ZIP_PATH = os.path.join(YANIX_PATH, "data.zip")
EXTRACT_BASE_PATH = YANIX_PATH


CONFIG_PATH = os.path.join(YANIX_PATH, "data/game_path.txt")
LANG_PATH = os.path.join(YANIX_PATH, "data/multilang.txt")
VERSION_PATH = os.path.join(YANIX_PATH, "data/version.txt")
ICON_PATH = os.path.join(YANIX_PATH, "data/Yanix-Launcher.png")
WINEPREFIX_PATH = os.path.join(YANIX_PATH, "data/wineprefix_path.txt")
THEME_PATH = os.path.join(YANIX_PATH, "data/theme.txt")
CUSTOM_THEMES_DIR = os.path.join(YANIX_PATH, "themes")

YAN_SIM_DOWNLOAD_URL = "https://yanderesimulator.com/dl/latest.zip"
YAN_SIM_INSTALL_PATH = os.path.join(YANIX_PATH, "game")
YAN_SIM_EXE_NAME = "YandereSimulator.exe"
YAN_SIM_NATIVE_EXE_PATH = os.path.join(YAN_SIM_INSTALL_PATH, YAN_SIM_EXE_NAME)


os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
os.makedirs(CUSTOM_THEMES_DIR, exist_ok=True)


LANGUAGES = {
    "en": {"welcome": "Welcome to Yanix Launcher", "loading": "Loading", "play": "Play", "github": "GitHub", "settings": "Settings", "download": "Download Game", "select_language": "Select Language", "select_exe": "Select .exe for WINE", "support": "Support", "discord": "Discord", "lang_changed": "Language changed!", "exit": "Exit", "missing_path": "Uh oh, try extract in home folder", "winetricks": "Winetricks", "no_internet": "No internet connection. Please check your network and try again.", "downloading_data": "Downloading Data File....", "extracting_data": "Extracting Files....", "download_failed": "Failed to download data.", "extract_failed": "Failed to extract data.", "download_success": "Data downloaded and extracted successfully!", "wineprefix": "Manage Wineprefix", "wineprefix_selected": "Wineprefix path saved successfully.", "wineprefix_error": "Could not save Wineprefix path.", "select_theme": "Select Theme", "theme_changed": "Theme changed!", "load_custom_theme": "Load Custom Theme"},
    "es": {"welcome": "Bienvenido a Yanix Launcher", "loading": "Cargando", "play": "Jugar", "github": "GitHub", "settings": "Configuración", "download": "Descargar Juego", "select_language": "Seleccionar Idioma", "select_exe": "Seleccionar .exe para WINE", "support": "Soporte", "discord": "Discord", "lang_changed": "¡Idioma cambiado!", "exit": "Salir", "missing_path": "Uh oh, intenta extraerlo en tu carpeta personal", "winetricks": "Winetricks", "no_internet": "Sin conexión de internet. Por favor, revisa tu red e inténtalo de nuevo.", "downloading_data": "Descargando archivo de datos....", "extracting_data": "Extrayendo archivos....", "download_failed": "Fallo al descargar datos.", "extract_failed": "Fallo al extraer datos.", "download_success": "Datos descargados y extraídos exitosamente!", "wineprefix": "Administrar Wineprefix", "wineprefix_selected": "Ruta de Wineprefix guardada exitosamente.", "wineprefix_error": "No se pudo guardar la ruta de Wineprefix.", "select_theme": "Seleccionar Tema", "theme_changed": "¡Tema cambiado!", "load_custom_theme": "Cargar Tema Personalizado"},
    "pt": {"welcome": "Bem-vindo ao Yanix Launcher", "loading": "Carregando", "play": "Jogar", "github": "GitHub", "settings": "Configurações", "download": "Baixar Jogo", "select_language": "Selecionar Idioma", "select_exe": "Selecionar .exe para WINE", "support": "Suporte", "discord": "Discord", "lang_changed": "Idioma alterado!", "exit": "Sair", "missing_path": "Uh oh... tente extrai-lo na sua pasta pessoal.", "winetricks": "Winetricks", "no_internet": "Sem conexão com a internet. Por favor, verifique sua rede e tente novamente.", "downloading_data": "Baixando arquivo de dados....", "extracting_data": "Extraindo arquivos....", "download_failed": "Falha ao baixar dados.", "extract_failed": "Falha ao extrair dados.", "download_success": "Dados baixados e extraídos com sucesso!", "wineprefix": "Gerenciar Wineprefix", "wineprefix_selected": "Caminho do Wineprefix salvo com sucesso!", "wineprefix_error": "Não foi possível salvar o caminho do Wineprefix.", "select_theme": "Selecionar Tema", "theme_changed": "Tema alterado!", "load_custom_theme": "Carregar Tema Personalizado"},
    "ru": {"welcome": "Добро пожаловать в Yanix Launcher", "loading": "Загрузка", "play": "Играть", "github": "GitHub", "settings": "Настройки", "download": "Скачать игру", "select_language": "Выбрать язык", "select_exe": "Выбрать .exe para WINE", "support": "Поддержка", "discord": "Discord", "lang_changed": "Язык изменен!", "exit": "Выход", "missing_path": "Упс, попробуйте извлечь в домашнюю папку", "winetricks": "Winetricks", "no_internet": "Нет подключения к интернету. Пожалуйста, проверьте свою сеть и повторите попытку.", "downloading_data": "Загрузка файла данных....", "extracting_data": "Извлечение файлов....", "download_failed": "Не удалось загрузить данные.", "extract_failed": "Не удалось извлечь данные.", "download_success": "Данные успешно загружены и извлечены!", "wineprefix": "Управление Wineprefix", "wineprefix_selected": "Путь Wineprefix успешно сохранен.", "wineprefix_error": "Не удалось сохранить путь Wineprefix.", "select_theme": "Выбрать тему", "theme_changed": "Тема изменена!", "load_custom_theme": "Загрузить пользовательскую тему"},
    "ja": {"welcome": "Yanix Launcherへようこそ", "loading": "読み込み中", "play": "プレイ", "github": "GitHub", "settings": "設定", "download": "ゲームをダウンロード", "select_language": "言語を選択", "select_exe": "WINE用の.exeを選択", "support": "サポート", "discord": "Discord", "lang_changed": "言語が変更されました！", "exit": "終了", "missing_path": "うーん、ホームフォルダに抽出してみてください", "winetricks": "Winetricks", "no_internet": "インターネット接続がありません。ネットワークを確認してもう一度お試しください。", "downloading_data": "データファイルをダウンロード中....", "extracting_data": "ファイルを展開中....", "download_failed": "データのダウンロードに失敗しました。", "extract_failed": "データの抽出に失敗しました。", "download_success": "データが正常にダウンロードされ、抽出されました！", "wineprefix": "Wineprefixを管理", "wineprefix_selected": "Wineprefixパスが正常に保存されました。", "wineprefix_error": "Wineprefixパスを保存できませんでした。", "select_theme": "テーマを選択", "theme_changed": "テーマが変更されました！", "load_custom_theme": "カスタムテーマをロード"},
    "zh": {"welcome": "欢迎使用 Yanix Launcher", "loading": "加载中", "play": "游戏", "github": "GitHub", "settings": "设置", "download": "下载游戏", "select_language": "选择语言", "select_exe": "选择 WINE 的 .exe 文件", "support": "支持", "discord": "Discord", "lang_changed": "语言已更改！", "exit": "退出", "missing_path": "哎呀，请尝试将其解压到主文件夹", "winetricks": "Winetricks", "no_internet": "无网络连接。请检查您的网络并重试。", "downloading_data": "正在下载数据文件....", "extracting_data": "正在解压文件....", "download_failed": "下载数据失败。", "extract_failed": "解压数据失败。", "download_success": "数据已成功下载和解压！", "wineprefix": "管理 Wineprefix", "wineprefix_selected": "Wineprefix 路径保存成功。", "wineprefix_error": "无法保存 Wineprefix 路径。", "select_theme": "选择主题", "theme_changed": "主题已更改！", "load_custom_theme": "加载自定义主题"},
    "fr": {"welcome": "Bienvenue sur Yanix Launcher", "loading": "Chargement", "play": "Jouer", "github": "GitHub", "settings": "Paramètres", "download": "Télécharger le jeu", "select_language": "Sélectionner la langue", "select_exe": "Sélectionner .exe pour WINE", "support": "Support", "discord": "Discord", "lang_changed": "Langue changée !", "exit": "Quitter", "missing_path": "Oups, essayez de l'extraire dans votre dossier personnel", "winetricks": "Winetricks", "no_internet": "Pas de connexion internet. Veuillez vérifier votre réseau et réessayer.", "downloading_data": "Téléchargement du fichier de données....", "extracting_data": "Extraction des fichiers....", "download_failed": "Échec du téléchargement des données.", "extract_failed": "Échec de l'extraction des données.", "download_success": "Données téléchargées et extraites avec succès !", "wineprefix": "Gérer Wineprefix", "wineprefix_selected": "Chemin Wineprefix enregistré avec succès.", "wineprefix_error": "Impossible d'enregistrer le chemin Wineprefix.", "select_theme": "Sélectionner un thème", "theme_changed": "Thème changé !", "load_custom_theme": "Charger un thème personnalisé"},
    "ar": {"welcome": "مرحبًا بك في Yanix Launcher", "loading": "جار التحميل", "play": "تشغيل", "github": "GitHub", "settings": "الإعدادات", "download": "تنزيل اللعبة", "select_language": "اختر اللغة", "select_exe": "حدد ملف .exe لـ WINE", "support": "الدعم", "discord": "Discord", "lang_changed": "تم تغيير اللغة!", "exit": "خروج", "missing_path": "أوه، حاول استخراجها في المجلد الرئيسي", "winetricks": "Winetricks", "no_internet": "لا يوجد اتصال بالإنترنت. يرجى التحقق من شبكتك والمحاولة مرة أخرى.", "downloading_data": " جارٍ تنزيل ملف البيانات....", "extracting_data": " جارٍ استخراج الملفات....", "download_failed": "فشل تنزيل البيانات.", "extract_failed": "فشل استخراج البيانات.", "download_success": "تم تنزيل البيانات واستخراجها بنجاح!", "wineprefix": "إدارة Wineprefix", "wineprefix_selected": "تم حفظ مسار Wineprefix بنجاح.", "wineprefix_error": "تعذر حفظ مسار Wineprefix.", "select_theme": "اختر سمة", "theme_changed": "تم تغيير السمة!", "load_custom_theme": "تحميل سمة مخصصة"},
    "ko": {"welcome": "Yanix Launcher에 오신 것을 환영합니다", "loading": "로딩 중", "play": "플레이", "github": "GitHub", "settings": "설정", "download": "게임 다운로드", "select_language": "언어 선택", "select_exe": "WINE용 .exe 선택", "support": "지원", "discord": "Discord", "lang_changed": "언어가 변경되었습니다!", "exit": "종료", "missing_path": "오류, 홈 폴더에 압축을 풀어 보세요", "winetricks": "Winetricks", "no_internet": "인터넷 연결이 없습니다. 네트워크를 확인하고 다시 시도하십시오.", "downloading_data": "데이터 파일 다운로드 중....", "extracting_data": "파일 압축 해제 중....", "download_failed": "데이터 다운로드 실패.", "extract_failed": "데이터 추출 실패.", "download_success": "데이터가 성공적으로 다운로드 및 추출되었습니다!", "wineprefix": "Wineprefix 관리", "wineprefix_selected": "Wineprefix 경로가 성공적으로 저장되었습니다.", "wineprefix_error": "Wineprefix 경로를 저장할 수 없습니다.", "select_theme": "테마 선택", "theme_changed": "테마가 변경되었습니다!", "load_custom_theme": "사용자 지정 테마 로드"},
    "ndk": {"welcome": "niko Niko-Launcher!", "loading": "You Activated the Nikodorito Easter-egg!", "play": "Niko", "github": "GitHub", "settings": "Meow", "download": "Dalad Gaem", "select_language": "niko to to ni", "select_exe": "niko to to ni WINE", "support": "niko to to ni", "discord": "Discorda", "lang_changed": "Niko DOrito! Niko dorito kimegasu", "exit": "nikotorito", "missing_path": "Uh oh,}try extract in home foldar,stupid", "winetricks": "manage the fucking winetricks", "no_internet": "no internet. check your network, stupid.", "downloading_data": "downloading daka file....", "extracting_data": "extracting files....", "download_failed": "fail to download daka.", "extract_failed": "fail to extract daka.", "download_success": "daka downloaded and extracted successfully!", "wineprefix": "manage the fucking wineprefix", "wineprefix_selected": "wineprefix path saved successfully, stupid.", "wineprefix_error": "could not save wineprefix path, stupid.", "select_theme": "niko select theme", "theme_changed": "niko theme changed!", "load_custom_theme": "load custom niko theme"},
    "he": {"welcome": "ברוכים הבאים ל-Yanix Launcher", "loading": "טוען", "play": "שחק", "github": "גיטהאב", "settings": "הגדרות", "download": "הורד משחק", "select_language": "בחר שפה", "select_exe": "בחר קובץ .exe עבור WINE", "support": "תמיכה", "discord": "דיסקורד", "lang_changed": "השפה שונתה!", "exit": "יציאה", "missing_path": "אופס, נסה לחלץ לתיקיית הבית", "winetricks": "ווינטריקס", "no_internet": "אין חיבור לאינטרנט. אנא בדוק את הרשת שלך ונסה שוב.", "downloading_data": "מוריד קובץ נתונים....", "extracting_data": "מחזיר קבצים....", "download_failed": "הורדת הנתונים נכשלה.", "extract_failed": "חילוץ הנתונים נכשל.", "download_success": "הנתונים הורדו וחולצו בהצלחה!", "wineprefix": "נהל Wineprefix", "wineprefix_selected": "נתיב Wineprefix נשמר בהצלחה.", "wineprefix_error": "לא ניתן לשמור נתיב Wineprefix.", "select_theme": "בחר ערכת נושא", "theme_changed": "ערכת הנושא שונתה!", "load_custom_theme": "טען ערכת נושא מותאמת אישית"}
}

THEMES = {
    "yanix-default": {
        "background_color_start": "#ff4da6",
        "background_color_end": "#6666ff",
        "button_bg_color": "white",
        "button_text_color": "black",
        "button_hover_bg_color": "#f0f0f0",
        "label_text_color": "white",
        "border_color": "#ccc"
    },
    "dark": {
        "background_color_start": "#333333",
        "background_color_end": "#1a1a1a",
        "button_bg_color": "#555555",
        "button_text_color": "white",
        "button_hover_bg_color": "#777777",
        "label_text_color": "white",
        "border_color": "#666666"
    },
    "light": {
        "background_color_start": "#f0f0f0",
        "background_color_end": "#ffffff",
        "button_bg_color": "#e0e0e0",
        "button_text_color": "black",
        "button_hover_bg_color": "#cccccc",
        "label_text_color": "black",
        "border_color": "#aaaaaa"
    },
    "ocean-blue": {
        "background_color_start": "#007bff",
        "background_color_end": "#0056b3",
        "button_bg_color": "#6c757d",
        "button_text_color": "white",
        "button_hover_bg_color": "#5a6268",
        "label_text_color": "white",
        "border_color": "#495057"
    },
    "forest-green": {
        "background_color_start": "#28a745",
        "background_color_end": "#1e7e34",
        "button_bg_color": "#ffc107",
        "button_text_color": "black",
        "button_hover_bg_color": "#e0a800",
        "label_text_color": "white",
        "border_color": "#d39e00"
    }
}

def load_custom_theme(filepath):
    try:
        with open(filepath, 'r') as f:
            theme_data = json.load(f)
        required_keys = ["background_color_start", "background_color_end",
                         "button_bg_color", "button_text_color",
                         "button_hover_bg_color", "label_text_color", "border_color"]
        if not all(key in theme_data for key in required_keys):
            raise ValueError("Invalid .yltheme file: missing required keys.")
        return theme_data
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        QMessageBox.critical(None, "Error Loading Theme", f"Failed to load custom theme from {filepath}: {e}")
        return None

def get_language():
    try:
        if os.path.exists(LANG_PATH):
            with open(LANG_PATH, "r") as f:
                return f.read().strip()
    except IOError:
        pass
    return "en"

def get_theme():
    try:
        if os.path.exists(THEME_PATH):
            with open(THEME_PATH, "r") as f:
                theme_setting = f.read().strip()
                if theme_setting.endswith(".yltheme") and os.path.exists(theme_setting):
                    return theme_setting
                elif theme_setting in THEMES:
                    return theme_setting
    except IOError:
        pass
    return "yanix-default"

def get_wineprefix_path():
    try:
        if os.path.exists(WINEPREFIX_PATH):
            with open(WINEPREFIX_PATH, "r") as f:
                return f.read().strip()
    except IOError:
        pass
    return None

def check_internet_connection():
    try:
        socket.create_connection(("www.google.com", 80), timeout=0.1)
        return True
    except OSError:
        return False


class YanixSplashScreen(QSplashScreen):
    def __init__(self, current_lang_data):
        super().__init__()
        self.current_lang = current_lang_data
        self.setFixedSize(600, 300)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.message = ""
        self.progress_text = ""

        self.update_splash_content(self.current_lang["downloading_data"])

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()

        gradient = QLinearGradient(0, 0, 0, rect.height())
        gradient.setColorAt(0, QColor(THEMES["yanix-default"]["background_color_start"]))
        gradient.setColorAt(1, QColor(THEMES["yanix-default"]["background_color_end"]))
        painter.fillRect(rect, gradient)

        painter.setPen(QColor(0, 0, 0))
        painter.drawRect(rect.adjusted(20, 20, -20, -20))

        text_rect = QRect(rect.width() // 2 - 200, rect.height() // 2 - 50, 400, 100)

        font_title = QFont("Futura", 32, QFont.Bold)
        painter.setFont(font_title)
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(text_rect, Qt.AlignCenter, "Yanix Launcher")

        font_message = QFont("Futura", 16)
        painter.setFont(font_message)
        painter.setPen(QColor(0, 0, 0))
        message_rect = QRect(rect.width() // 2 - 200, rect.height() // 2 + 10, 400, 50)
        painter.drawText(message_rect, Qt.AlignCenter, self.message)

        font_progress = QFont("Futura", 12)
        painter.setFont(font_progress)
        painter.setPen(QColor(0, 0, 0))
        progress_rect = QRect(rect.width() - 150, rect.height() - 50, 100, 30)
        painter.drawText(progress_rect, Qt.AlignRight | Qt.AlignBottom, self.progress_text)

    def update_splash_content(self, message, progress=""):
        self.message = message
        self.progress_text = progress
        self.repaint()


def download_and_extract_data(splash_screen, current_lang_data):
    target_data_folder = os.path.join(YANIX_PATH, "data")

    if os.path.exists(target_data_folder) and os.listdir(target_data_folder):
        splash_screen.update_splash_content(current_lang_data["download_success"])
        return

    if not check_internet_connection():
        if os.path.exists(target_data_folder):
            splash_screen.update_splash_content(current_lang_data["download_success"])
            return
        else:
            QMessageBox.critical(None, current_lang_data["no_internet"], current_lang_data["no_internet"])
            splash_screen.hide()
            sys.exit(1)

    splash_screen.update_splash_content(current_lang_data["downloading_data"])
    try:
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(DATA_DOWNLOAD_URL, stream=True, timeout=10, headers=headers)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0
        with open(TEMP_ZIP_PATH, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded_size += len(chunk)
                splash_screen.update_splash_content(current_lang_data["downloading_data"], f"{downloaded_size / (1024 * 1024):.1f}MB / {total_size / (1024 * 1024):.1f}MB" if total_size > 0 else "...")
                QApplication.processEvents()

    except requests.exceptions.Timeout:
        QMessageBox.critical(None, current_lang_data["download_failed"], f"{current_lang_data['download_failed']} (Connection timeout).")
        if os.path.exists(TEMP_ZIP_PATH):
            os.remove(TEMP_ZIP_PATH)
        splash_screen.hide()
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        QMessageBox.critical(None, current_lang_data["download_failed"], f"{current_lang_data['download_failed']} (Connection error. Check URL or internet connection).")
        if os.path.exists(TEMP_ZIP_PATH):
            os.remove(TEMP_ZIP_PATH)
        splash_screen.hide()
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        QMessageBox.critical(None, current_lang_data["download_failed"], f"{current_lang_data['download_failed']} (Error: {e}).")
        if os.path.exists(TEMP_ZIP_PATH):
            os.remove(TEMP_ZIP_PATH)
        splash_screen.hide()
        sys.exit(1)
    except Exception as e:
        QMessageBox.critical(None, current_lang_data["download_failed"], f"{current_lang_data['download_failed']} (Unexpected error during download: {e}).")
        if os.path.exists(TEMP_ZIP_PATH):
            os.remove(TEMP_ZIP_PATH)
        splash_screen.hide()
        sys.exit(1)


    splash_screen.update_splash_content(current_lang_data["extracting_data"])
    QApplication.processEvents()
    try:
        os.makedirs(target_data_folder, exist_ok=True)
        with zipfile.ZipFile(TEMP_ZIP_PATH, 'r') as zip_ref:
            zip_ref.extractall(target_data_folder)
    except zipfile.BadZipFile as e:
        QMessageBox.critical(None, current_lang_data["extract_failed"], f"{current_lang_data['extract_failed']} (Corrupted or invalid ZIP file: {e}).")
        if os.path.exists(TEMP_ZIP_PATH):
            os.remove(TEMP_ZIP_PATH)
        shutil.rmtree(target_data_folder, ignore_errors=True)
        splash_screen.hide()
        sys.exit(1)
    except Exception as e:
        QMessageBox.critical(None, current_lang_data["extract_failed"], f"{current_lang_data['extract_failed']} (Unexpected error during extraction: {e}).")
        if os.path.exists(TEMP_ZIP_PATH):
            os.remove(TEMP_ZIP_PATH)
        shutil.rmtree(target_data_folder, ignore_errors=True)
        splash_screen.hide()
        sys.exit(1)
    finally:
        if os.path.exists(TEMP_ZIP_PATH):
            os.remove(TEMP_ZIP_PATH)


class SettingsDialog(QDialog):
    def __init__(self, lang_code, theme_name, lang_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle(lang_data["settings"])
        self.setFixedSize(400, 250)

        self.current_theme_name = theme_name

        layout = QVBoxLayout()

        lang_label = QLabel(lang_data["select_language"])
        layout.addWidget(lang_label)
        self.lang_selector = QComboBox()
        self.lang_selector.addItems(LANGUAGES.keys())
        self.lang_selector.setCurrentText(lang_code)
        layout.addWidget(self.lang_selector)

        theme_label = QLabel(lang_data["select_theme"])
        layout.addWidget(theme_label)
        self.theme_selector = QComboBox()
        self.update_theme_selector_items()
        self.theme_selector.setCurrentText(self.current_theme_name)
        layout.addWidget(self.theme_selector)

        self.load_custom_theme_button = QPushButton(lang_data["load_custom_theme"])
        self.load_custom_theme_button.clicked.connect(self.load_custom_theme_file)
        layout.addWidget(self.load_custom_theme_button)

        self.apply_btn = QPushButton("Apply")
        self.apply_btn.clicked.connect(self.apply_settings)
        layout.addWidget(self.apply_btn)

        self.setLayout(layout)
        self.apply_theme_to_settings_buttons()

    def apply_theme_to_settings_buttons(self):
        theme = self.parent().get_current_theme_data()
        button_style = f"""
            QPushButton {{
                color: {theme["button_text_color"]};
                background-color: {theme["button_bg_color"]};
                padding: 8px;
                border-radius: 6px;
                border: 1px solid {theme["border_color"]};
            }}
            QPushButton:hover {{
                background-color: {theme["button_hover_bg_color"]};
            }}
        """
        self.apply_btn.setStyleSheet(button_style)
        self.load_custom_theme_button.setStyleSheet(button_style)

    def update_theme_selector_items(self):
        self.theme_selector.clear()
        self.theme_selector.addItems(THEMES.keys())
        custom_themes = [f for f in os.listdir(CUSTOM_THEMES_DIR) if f.endswith(".yltheme")]
        for theme_file in custom_themes:
            self.theme_selector.addItem(os.path.join(CUSTOM_THEMES_DIR, theme_file))

    def load_custom_theme_file(self):
        file, _ = QFileDialog.getOpenFileName(self, self.parent().lang["load_custom_theme"], CUSTOM_THEMES_DIR, "Yanix Theme Files (*.yltheme)")
        if file:
            theme_data = load_custom_theme(file)
            if theme_data:
                try:
                    with open(THEME_PATH, "w") as f:
                        f.write(file)
                    self.current_theme_name = file
                    self.update_theme_selector_items()
                    self.theme_selector.setCurrentText(file)
                    QMessageBox.information(self, "Success", self.parent().lang["theme_changed"])
                    if self.parent():
                        self.parent().apply_theme(self.current_theme_name)
                        self.apply_theme_to_settings_buttons()
                except IOError as e:
                    QMessageBox.critical(self, "Error", f"Could not save theme setting: {e}")

    def apply_settings(self):
        new_lang = self.lang_selector.currentText()
        try:
            with open(LANG_PATH, "w") as f:
                f.write(new_lang)

            message = LANGUAGES[new_lang]["lang_changed"]
            if new_lang not in ["en", "pt", "ndk"]:
                message += "\n\nThis language is 100% AI and may have malfunctions."

            QMessageBox.information(self, "Info", message)
        except IOError as e:
            QMessageBox.critical(self, "Error", f"Could not save language setting: {e}")

        new_theme = self.theme_selector.currentText()
        try:
            with open(THEME_PATH, "w") as f:
                f.write(new_theme)
            if self.parent():
                self.parent().apply_theme(new_theme)
                self.apply_theme_to_settings_buttons()
                QMessageBox.information(self, "Info", self.parent().lang["theme_changed"])
        except IOError as e:
            QMessageBox.critical(self, "Error", f"Could not save theme setting: {e}")

        if self.parent():
            self.parent().retranslate_ui()

        self.accept()


class YanixLauncher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lang_code = get_language()
        self.current_theme_name = get_theme()
        self.lang = LANGUAGES.get(self.lang_code, LANGUAGES["en"])
        self.wineprefix = get_wineprefix_path()

        self.setWindowTitle("Yanix Launcher")
        self.setFixedSize(1100, 600)

        if os.path.exists(ICON_PATH):
            self.setWindowIcon(QIcon(ICON_PATH))

        self.setup_ui()
        self.apply_theme(self.current_theme_name)

        self.rpc = None
        self.start_time = int(time.time())
        if presence_enabled:
            self.init_rpc()

    def init_rpc(self):
        try:
            self.rpc = Presence(CLIENT_ID)
            self.rpc.connect()
            self.update_rpc(details="In the launcher", state="Browse...")
        except Exception:
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
        except Exception:
            self.rpc.close()
            self.rpc = None

    def get_current_theme_data(self):
        if self.current_theme_name.endswith(".yltheme") and os.path.exists(self.current_theme_name):
            theme_data = load_custom_theme(self.current_theme_name)
            if theme_data:
                return theme_data
        return THEMES.get(self.current_theme_name, THEMES["yanix-default"])

    def apply_theme(self, theme_name):
        self.current_theme_name = theme_name
        theme = self.get_current_theme_data()

        button_style = f"""
            QPushButton {{
                color: {theme["button_text_color"]};
                background-color: {theme["button_bg_color"]};
                padding: 8px;
                border-radius: 6px;
                border: 1px solid {theme["border_color"]};
            }}
            QPushButton:hover {{
                background-color: {theme["button_hover_bg_color"]};
            }}
        """
        for button in [self.play_button, self.settings_button, self.select_exe_button,
                       self.download_button, self.winetricks_button, self.wineprefix_button,
                       self.support_button, self.discord_button]:
            button.setStyleSheet(button_style)

        self.version_label.setStyleSheet(f"color: {theme['label_text_color']}; margin-top: 20px;")

        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(theme["background_color_start"]))
        gradient.setColorAt(1, QColor(theme["background_color_end"]))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)


    def setup_ui(self):
        main_layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.left_layout.setAlignment(Qt.AlignTop)

        font = QFont("Futura", 16)
        version_font = QFont("Futura", 10)

        self.play_button = QPushButton()
        self.play_button.setFont(font)
        self.play_button.clicked.connect(self.launch_game)
        self.left_layout.addWidget(self.play_button)

        self.settings_button = QPushButton()
        self.settings_button.setFont(font)
        self.settings_button.clicked.connect(self.open_settings)
        self.left_layout.addWidget(self.settings_button)

        self.select_exe_button = QPushButton()
        self.select_exe_button.setFont(font)
        self.select_exe_button.clicked.connect(self.select_exe)
        self.left_layout.addWidget(self.select_exe_button)

        self.download_button = QPushButton()
        self.download_button.setFont(font)
        self.download_button.clicked.connect(self.download_game)
        self.left_layout.addWidget(self.download_button)

        self.winetricks_button = QPushButton()
        self.winetricks_button.setFont(font)
        self.winetricks_button.clicked.connect(self.manage_winetricks)
        self.left_layout.addWidget(self.winetricks_button)

        self.wineprefix_button = QPushButton()
        self.wineprefix_button.setFont(font)
        self.wineprefix_button.clicked.connect(self.select_wineprefix)
        self.left_layout.addWidget(self.wineprefix_button)

        self.support_button = QPushButton()
        self.support_button.setFont(font)
        self.support_button.clicked.connect(lambda: webbrowser.open("https://github.com/NikoYandere/Yanix-Launcher/issues"))
        self.left_layout.addWidget(self.support_button)

        self.discord_button = QPushButton()
        self.discord_button.setFont(font)
        self.discord_button.clicked.connect(lambda: webbrowser.open("https://discord.gg/7JC4FGn69U"))
        self.left_layout.addWidget(self.discord_button)

        self.version_label = QLabel()
        self.version_label.setFont(version_font)
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
        self.wineprefix_button.setText(self.lang["wineprefix"])
        self.support_button.setText(self.lang["support"])
        self.discord_button.setText(self.lang["discord"])
        self.version_label.setText(f"{self.lang['welcome']} V 1.0.0")

        self.apply_theme(self.current_theme_name)


    def open_settings(self):
        dlg = SettingsDialog(self.lang_code, self.current_theme_name, self.lang, self)
        dlg.exec_()

    def _wait_for_game_exit(self, process):
        process.wait()
        self.update_rpc(details="In the launcher", state="Browse...")

    def launch_game(self):
        game_to_launch = None
        game_dir = None
        wine_needed = True

        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH) as f:
                wine_path = f.read().strip()
            if os.path.exists(wine_path):
                game_to_launch = ["wine", wine_path]
                game_dir = os.path.dirname(wine_path)
            else:
                QMessageBox.critical(self, "Error", "The saved game path is invalid. Please select the .exe file for WINE again.")
                return
        elif os.path.exists(YAN_SIM_NATIVE_EXE_PATH):
            game_to_launch = ["wine", YAN_SIM_NATIVE_EXE_PATH]
            game_dir = YAN_SIM_INSTALL_PATH
        else:
            QMessageBox.critical(self, "Error", "Game executable path not defined. Please select the .exe file for WINE or download Yandere Simulator.")
            return

        if game_to_launch:
            try:
                env = os.environ.copy()
                if wine_needed and self.wineprefix:
                    env["WINEPREFIX"] = self.wineprefix

                process = subprocess.Popen(game_to_launch, cwd=game_dir, env=env)

                self.update_rpc(details="Playing Yandere Simulator", state="In-Game")
                monitor_thread = threading.Thread(
                    target=self._wait_for_game_exit,
                    args=(process,),
                    daemon=True
                )
                monitor_thread.start()

            except FileNotFoundError:
                QMessageBox.critical(self, "Error", "WINE is not installed or not in your system's PATH.")
                self.update_rpc(details="In the launcher", state="Browse...")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred while launching the game: {e}")
                self.update_rpc(details="In the launcher", state="Browse...")

    def select_exe(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Game Executable", "", "EXE Files (*.exe)")
        if file:
            try:
                with open(CONFIG_PATH, "w") as f:
                    f.write(file)
                QMessageBox.information(self, "Success", "Executable path saved successfully.")
            except IOError as e:
                QMessageBox.critical(self, "Error", f"Could not save executable path: {e}")

    def select_wineprefix(self):
        directory = QFileDialog.getExistingDirectory(self, self.lang["wineprefix"])
        if directory:
            try:
                with open(WINEPREFIX_PATH, "w") as f:
                    f.write(directory)
                self.wineprefix = directory
                QMessageBox.information(self, "Success", self.lang["wineprefix_selected"])
            except IOError as e:
                QMessageBox.critical(self, "Error", f"{self.lang['wineprefix_error']}: {e}")

    def download_game(self):
        if not check_internet_connection():
            QMessageBox.critical(self, self.lang["no_internet"], self.lang["no_internet"])
            return

        yan_sim_zip_path = os.path.join(YANIX_PATH, "yansim.zip")

        if os.path.exists(YAN_SIM_NATIVE_EXE_PATH):
            QMessageBox.information(self, "Info", "Yandere Simulator is already installed natively.")
            return

        reply = QMessageBox.question(self, self.lang["download"],
                                     "Do you want to download Yandere Simulator?\nThis may take a while.",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return

        try:
            headers = {'User-Agent': USER_AGENT}
            response = requests.get(YAN_SIM_DOWNLOAD_URL, stream=True, timeout=300, headers=headers)
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))

            total_size_kb = total_size // 1024 if total_size > 0 else 0

            progress_dialog = QProgressDialog("Downloading Yandere Simulator...", "Cancel", 0, total_size_kb, self)
            progress_dialog.setWindowTitle("Download Progress")
            progress_dialog.setWindowModality(Qt.WindowModal)
            progress_dialog.show()

            downloaded_size = 0
            with open(yan_sim_zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if progress_dialog.wasCanceled():
                        raise InterruptedError("Download canceled by user.")

                    f.write(chunk)
                    downloaded_size += len(chunk)
                    progress_dialog.setValue(downloaded_size // 1024)
                    QApplication.processEvents()

            progress_dialog.setValue(total_size_kb)

            QMessageBox.information(self, self.lang["download"], "Download complete. Now extracting files...")
            extract_dialog = QProgressDialog("Extracting files...", None, 0, 0, self)
            extract_dialog.setWindowTitle("Extracting")
            extract_dialog.setWindowModality(Qt.WindowModal)
            extract_dialog.setCancelButton(None)
            extract_dialog.show()
            QApplication.processEvents()

            os.makedirs(YAN_SIM_INSTALL_PATH, exist_ok=True)
            with zipfile.ZipFile(yan_sim_zip_path, 'r') as zip_ref:
                zip_ref.extractall(YAN_SIM_INSTALL_PATH)

            extract_dialog.close()
            QMessageBox.information(self, "Success", "Yandere Simulator downloaded and extracted successfully!")

        except InterruptedError as e:
             QMessageBox.warning(self, "Download Canceled", str(e))
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, self.lang["download_failed"], f"{self.lang['download_failed']} (Error: {e}).")
        except zipfile.BadZipFile as e:
            QMessageBox.critical(self, self.lang["extract_failed"], f"{self.lang['extract_failed']} (Corrupted or invalid ZIP file: {e}).")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")
        finally:
            if os.path.exists(yan_sim_zip_path):
                os.remove(yan_sim_zip_path)


    def manage_winetricks(self):
        if not shutil.which("winetricks"):
            QMessageBox.critical(self, "Error", "Winetricks is not installed or not in your PATH.")
        else:
            try:
                env = os.environ.copy()
                if self.wineprefix:
                    env["WINEPREFIX"] = self.wineprefix
                subprocess.Popen(["winetricks"], env=env)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to launch Winetricks: {e}")

    def closeEvent(self, event):
        if self.rpc:
            self.rpc.close()
        event.accept()


if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts, True)
    app = QApplication(sys.argv)

    lang_code = get_language()
    current_lang_data = LANGUAGES.get(lang_code, LANGUAGES["en"])

    splash = YanixSplashScreen(current_lang_data)
    splash.show()

    QApplication.processEvents()

    download_and_extract_data(splash, current_lang_data)

    launcher = YanixLauncher()
    launcher.show()
    splash.finish(launcher)

    sys.exit(app.exec_())
