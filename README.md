
![Futura](https://github.com/user-attachments/assets/767e0497-fcf7-4345-8458-cc757a35280a)


# Yanix-Launcher 
Yanix-Launcher is an independent, open-source launcher for Yandere Simulator on Linux systems. This launcher is not affiliated with or supported by YandereDev.

Yanix runs the game via WINE (version 8.0 or newer is required). Some graphical issues may appear depending on your WINE version, but most major display bugs were fixed in the Unity 6 build. Known issue: some letters may not display correctly — this must be fixed by YandereDev in the game's source, not by the launcher team.

This launcher is built and tested for Linux.
- A MacOS version has already received optimizations.
- A Windows version is planned, but not available yet.

If you are experiencing bugs like "letters not showing", do not report them to us — it's a WINE rendering issue tied to the game, not the launcher. You may try using GE-Proton instead of regular WINE.


Dependencies

Before running Yanix-Launcher, make sure the following dependencies are installed:


Required Packages

1. PyQt5 – GUI Framework
2. PyQtWebEngine – Web rendering support
3. requests – For HTTP operations (e.g., updates)
4. WINE – To run Yandere Simulator
5. Winetricks – WINE helper scripts


Installation Guide

Ubuntu/Debian:
```
sudo apt install python3-pyqt5 python3-pyqt5.qtwebengine python3-requests wine winetricks
```
Arch Linux:
```
sudo pacman -S python-pyqt5 python-pyqtwebengine python-requests wine winetricks
```
Fedora:
```
sudo dnf install python3-qt5 python3-qt5-webengine python3-requests wine winetricks
```
How to Run
```
git clone https://github.com/NikoYandere/yanix-launcher
cd yanix-launcher
python3 binary/yanix-launcher.py
```
Contact

Email: nikoyandere@proton.me  
GitHub: https://github.com/NikoYandere/yanix-launcher
Note: Feel free to fork the repository and adapt the launcher to your own Linux/Unix-based distribution.

AUR package:https://aur.archlinux.org/packages/yanix-launcher-git
