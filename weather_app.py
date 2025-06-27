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
thunderstorm_sound = pygame.mixer.Sound("thunderstorm.mp3")
sunny_sound = pygame.mixer.Sound("sunny.mp3")

def get_weather(city):
    api_key = "9b44d42714e481be282853dcd4ea3ed1"  # Replace with your API key
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    res = requests.get(url)
    if res.status_code == 404:
        messagebox.showerror("Error", "City not found")
        return None
    weather = res.json()
    icon_id = weather['weather'][0]['icon']
    description = weather['weather'][0]['description']
    temperature = weather['main']['temp'] - 273.15  # Convert temperature from Kelvin to Celsius
    city = weather['name']
    country_code = weather['sys']['country']
    country = pycountry.countries.get(alpha_2=country_code).name
    pressure = weather['main']['pressure']
    humidity = weather['main']['humidity']
    wind = weather['wind']['speed']
    sunrise = weather['sys']['sunrise']
    sunset = weather['sys']['sunset']
    current_time = weather['dt']
    lon = weather['coord']['lon']
    lat = weather['coord']['lat']

    # Get timezone
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lng=lon, lat=lat)
    local_tz = pytz.timezone(timezone_str)
    local_time = datetime.now(local_tz).strftime('%Y-%m-%d %H:%M:%S')

    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    return (icon_url, temperature, description, pressure, humidity, wind, city, country, sunrise, sunset, current_time, local_time)

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

    def blink():
        current_color = warning_label.cget("foreground")
        next_color = "black" if current_color == "red" else "red"
        warning_label.config(foreground=next_color)
        flood_warning.after(500, blink)

    flood_warning.after(0, blink)
    flood_warning.after(3000, flood_warning.destroy)

def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return
    icon_url, temperature, description, pressure, humidity, wind, city, country, sunrise, sunset, current_time, local_time = result
    location_label.configure(text=f"{city}, {country}")
    time_label.configure(text=f"Local Time: {local_time}")

    # Load the icon image
    image = Image.open(requests.get(icon_url, stream=True).raw)
    resized_image = image.resize((150, 150), Image.LANCZOS)  # Resize to 150x150 pixels

    icon = ImageTk.PhotoImage(resized_image)
    icon_label.configure(image=icon)
    icon_label.image = icon

    temperature_label.configure(text=f"Temperature: {temperature:.2f}°C")
    description_label.configure(text=f"Description: {description}")
    pressure_label.configure(text=f"Pressure: {pressure} hPa")
    humidity_label.configure(text=f"Humidity: {humidity}%")
    wind_label.configure(text=f"Wind Speed: {wind} m/s")

    # Determine if it's day, afternoon, evening, or night
    current_time = datetime.utcfromtimestamp(current_time)
    sunrise_time = datetime.utcfromtimestamp(sunrise)
    sunset_time = datetime.utcfromtimestamp(sunset)

    # Calculate midday and afternoon boundaries
    midday_time = sunrise_time + (sunset_time - sunrise_time) / 2
    afternoon_end_time = sunset_time - (sunset_time - sunrise_time) / 4

    if sunrise_time <= current_time < midday_time:
        background_label.config(image=day_bg)
        background_label.image = day_bg
    elif midday_time <= current_time < afternoon_end_time:
        background_label.config(image=afternoon_bg)
        background_label.image = afternoon_bg
    elif afternoon_end_time <= current_time < sunset_time:
        background_label.config(image=evening_bg)
        background_label.image = evening_bg
    else:
        background_label.config(image=night_bg)
        background_label.image = night_bg

    # Stop any currently playing sounds
    stop_all_sounds()

    # Play sound based on weather conditions
    if 'heavy rain' in description.lower() or 'heavy intensity rain' in description.lower():
        show_flood_warning()
        heavy_rain_sound.play()
    elif 'thunderstorm' in description.lower():
        thunderstorm_sound.play()
    elif 'rain' in description.lower():
        show_flood_warning()
        rain_sound.play()
    elif 'wind' in description.lower():
        wind_sound.play()
    elif 'clear' in description.lower() or 'sunny' in description.lower():
        sunny_sound.play()

    # Show all the labels
    location_label.place(relx=0.5, rely=0.28, anchor="center")
    time_label.place(relx=0.5, rely=0.34, anchor="center")
    icon_label.place(relx=0.5, rely=0.46, anchor="center")
    temperature_label.place(relx=0.5, rely=0.56, anchor="center")
    description_label.place(relx=0.5, rely=0.601, anchor="center")
    pressure_label.place(relx=0.5, rely=0.65, anchor="center")
    humidity_label.place(relx=0.5, rely=0.7, anchor="center")
    wind_label.place(relx=0.5, rely=0.75, anchor="center")

root = ttk.Window(themename="morph")
root.title("Weather App")
root.attributes('-fullscreen', True)  # Fullscreen mode

# Load and resize background images
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

day_image = Image.open("day_background.jpg").resize((screen_width, screen_height), Image.LANCZOS)
afternoon_image = Image.open("afternoon_background.jpg").resize((screen_width, screen_height), Image.LANCZOS)
evening_image = Image.open("evening_background.jpg").resize((screen_width, screen_height), Image.LANCZOS)
night_image = Image.open("night_background.jpg").resize((screen_width, screen_height), Image.LANCZOS)
initial_image = Image.open("white.clouds.jpg").resize((screen_width, screen_height), Image.LANCZOS)

day_bg = ImageTk.PhotoImage(day_image)
afternoon_bg = ImageTk.PhotoImage(afternoon_image)
evening_bg = ImageTk.PhotoImage(evening_image)
night_bg = ImageTk.PhotoImage(night_image)
initial_bg = ImageTk.PhotoImage(initial_image)

# Set initial background
background_label = tk.Label(root)
background_label.place(relwidth=1, relheight=1)
background_label.config(image=initial_bg)
background_label.image = initial_bg

# Frame for buttons
button_frame = tk.Frame(root, bg="light grey")
button_frame.place(relx=0, rely=0, relwidth=1, relheight=0.03 )

# Minimize Button
minimize_button = ttk.Button(button_frame, text="-", command=root.iconify, bootstyle="secondary")
minimize_button.pack(side="left", padx=5)

# Maximize/Restore Button
def toggle_fullscreen():
    if root.attributes('-fullscreen'):
        root.attributes('-fullscreen', False)
    else:
        root.attributes('-fullscreen', True)

maximize_button = ttk.Button(button_frame, text="[]", command=toggle_fullscreen, bootstyle="secondary")
maximize_button.pack(side="left", padx=5)

# Exit Button
exit_button = ttk.Button(button_frame, text="X", command=root.quit, bootstyle="danger")
exit_button.pack(side="left", padx=5)

# Entry widget
city_entry = ttk.Entry(root, font=("Helvetica", 30))
city_entry.pack(pady=(screen_height // 8, 10), padx=20)

# Search Button
search_button = ttk.Button(root, text="Search", command=search, bootstyle="warning")
search_button.pack()

# Location Label
location_label = tk.Label(root, font=("Helvetica", 35, "bold"), fg="dark blue", bg=None)
location_label.place(relx=0.5, rely=0.3, anchor="center")

# Time Label
time_label = tk.Label(root, font=("Helvetica", 20), bg=None)
time_label.place(relx=0.5, rely=0.35, anchor="center")

# Icon Label
icon_label = tk.Label(root, bg=None)
icon_label.place(relx=0.5, rely=0.45, anchor="center")

# Temperature Label
temperature_label = tk.Label(root, font=("Helvetica", 20), bg=None)
temperature_label.place(relx=0.5, rely=0.55, anchor="center")

# Description Label
description_label = tk.Label(root, font=("Helvetica", 20), bg=None)
description_label.place(relx=0.5, rely=0.6, anchor="center")

# Pressure Label
pressure_label = tk.Label(root, font=("Helvetica", 20), bg=None)
pressure_label.place(relx=0.5, rely=0.65, anchor="center")

# Humidity Label
humidity_label = tk.Label(root, font=("Helvetica", 20), bg=None)
humidity_label.place(relx=0.5, rely=0.7, anchor="center")

# Wind Label
wind_label = tk.Label(root, font=("Helvetica", 20), bg=None)
wind_label.place(relx=0.5, rely=0.75, anchor="center")

root.mainloop()