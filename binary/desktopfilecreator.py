import os
import sys
from pathlib import Path

python_file = "yanix-launcher.py"
png_file = "Yanix-Launcher.png"

current_dir = Path(sys._MEIPASS if getattr(sys, 'frozen', False) else os.getcwd())

home_dir = os.path.expanduser("~")
app_dir = os.path.join(home_dir, ".local", "share", "applications")

python_path = None
png_path = None

for root, dirs, files in os.walk(home_dir):
    if python_file in files:
        python_path = os.path.join(root, python_file)
    if png_file in files:
        png_path = os.path.join(root, png_file)

if python_path and png_path:
    desktop_file_content = f"""
[Desktop Entry]
Name=Yanix Launcher
Comment=Yanix Launcher
Exec=python3 {python_path}
Icon={png_path}
Terminal=false
Type=Application
Categories=Game;
"""

    desktop_file_path = os.path.join(app_dir, "yanix-launcher.desktop")

    os.makedirs(app_dir, exist_ok=True)

    with open(desktop_file_path, "w") as desktop_file:
        desktop_file.write(desktop_file_content.strip())

    os.chmod(desktop_file_path, 0o755)

    print(f"Desktop file created in: {desktop_file_path},see GNOME appgrid/KDE start menu.")
else:
    print("Error in Creating .desktop File Error code:1 (.py or .png not found!) ")

