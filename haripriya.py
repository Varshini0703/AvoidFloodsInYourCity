import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkFont
from PIL import Image, ImageTk
import requests
import pycountry
from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder
import ttkbootstrap as ttk
import pygame

# Initialize pygame for sound playback
pygame.mixer.init()

# Load sound files
wind_sound = pygame.mixer.Sound("wind.mp3")
rain_sound = pygame.mixer.Sound("rain.mp3")
heavy_rain_sound = pygame.mixer.Sound("rain.mp3.mp3")
thunderstorm_sound = pygame.mixer.Sound("thunderstorm.mp3.mp3")
sunny_sound = pygame.mixer.Sound("sunny.mp3")

def stop_all_sounds():
    wind_sound.stop()
    rain_sound.stop()
    heavy_rain_sound.stop()
    thunderstorm_sound.stop()
    sunny_sound.stop()

def show_flood_warning():
    flood_warning = tk.Toplevel(root)
    flood_warning.attributes('-fullscreen', True)
    flood_warning.configure(bg="red")
    warning_label = tk.Label(flood_warning, text="FLOOD DANGER", font=("Helvetica", 70, "bold"), fg="black", bg="red")
    warning_label.pack(expand=True)



