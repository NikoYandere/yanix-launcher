import subprocess
import os
import tkinter as tk
from tkinter import messagebox, filedialog
import webbrowser
import pygame
import requests
from bs4 import BeautifulSoup

SEARCH_DIRS = [
    os.path.expanduser("~"),
    os.path.expanduser("~/Documents"),
    os.path.expanduser("~/Downloads"),
    os.path.expanduser("~/Desktop"),
    os.path.expanduser("~/.local/share")
]

def find_yanix_launcher():
    for directory in SEARCH_DIRS:
        possible_path = os.path.join(directory, "yanix-launcher")
        if os.path.exists(possible_path):
            return possible_path
    return None

def get_yanderedev_posts():
    url = "https://yanderedev.wordpress.com/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        posts = soup.find_all("h2", class_="entry-title")
        return [(post.text, post.a["href"]) for post in posts[:5]]  # Pegando os últimos 5 posts
    except:
        return [("Error loading posts", "#")]

def open_post(url):
    webbrowser.open(url)

def show_posts():
    posts = get_yanderedev_posts()
    for post in posts:
        btn = tk.Button(posts_frame, text=post[0], font=("Arial", 10), wraplength=250, command=lambda p=post[1]: open_post(p))
        btn.pack(pady=5)

def play_startup_sound():
    pygame.mixer.init()
    sound_path = os.path.join(YANIX_PATH, "binary/data/startup.wav")
    if os.path.exists(sound_path):
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()

YANIX_PATH = find_yanix_launcher()
if not YANIX_PATH:
    exit()

top = tk.Tk()
top.title("Yanix-Launcher")
top.geometry("600x800")
top.resizable(False, False)

main_frame = tk.Frame(top)
main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

posts_frame = tk.Frame(top, width=250, bg="lightgray")
posts_frame.pack(side=tk.RIGHT, fill=tk.Y)

tk.Label(posts_frame, text="YandereDev Blog", font=("Arial", 14, "bold"), bg="lightgray").pack(pady=10)
show_posts()

play_startup_sound()
top.mainloop()
