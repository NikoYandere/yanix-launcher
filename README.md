

![Yanix-Launcher](https://github.com/user-attachments/assets/a4fdb8c0-fcfa-44d1-94d3-7e9e359c13a9)



# Yanix-Launcher
This Launcher is not supported or created by YandereDev,its a independent initiative for a Launcher of Yandere Simulator for Linux OSes,please,dont beg us a Windows Port,we are optimizing Yanix Launcher for Linux OSes,and please,dont beg us a .deb,.appimage,.snap for a universal package that everyone can use,we will provide a .py that is a python-3 script,this is a Launcher that runs in WINE,but you need WINE  8.0 or newer to work propely,and a disadvantage:WINE may have Display Issues but major display bugs have been Fixed in Unity 6 Build,like full screen bugs,but Some Letters don't display,and to fix that,YandereDev has to investigate it,this launcher is open-source,and we have a GitHub Repository and a Installer too  yanix is builded and tested for Linux,a Mac os or FreeBSD build maybe will be not realsed,but you can   Fork   the Repository for you Unix/Linux Distro.

any bug report like: Letters and not showing for me! will be not listened,its total responsibility of YandereDev,not mine,and know that WINE have Display issues and maybe we will switch to ge-proton

## Dependencies

Before running Yanix-Launcher, you need to make sure that the dependencies are installed on your system.

### Dependencies

1. **playsound** - Library for managing audio and animations.
2. **requests** - To download updates and resources.
3. **python3-tk** - For the graphical interface.
4. **wine** - To run Yandere Simulator on Linux (necessary if you are playing with Wine).

### How to install the dependencies

#### Ubuntu/Debian

Run the following command to install the necessary dependencies:

sudo apt install python3-pygame python3-requests python3-tk wine

Arch Linux

On Arch Linux, you can use pacman to install the dependencies:

sudo pacman -S python-pygame python-requests tk wine

Fedora

On Fedora, use dnf to install the dependencies:

sudo dnf install python3-pygame python3-requests python3-tkinter wine

If you are using another Linux distribution, you may need to adapt the commands to suit your system.
How to run Yanix-Launcher

    Clone the repository:

git clone https://github.com/NikoYandere/Yanix-Launcher.git

    Access the launcher directory:

cd Yanix-Launcher

    Run the launcher:

python3 binary/yanix-launcher.py

    Language choice: The launcher supports multiple languages (English, Spanish, Portuguese) and allows you to change the language directly in the interface.
    one thing:install playsound with pip install playsound.
 
