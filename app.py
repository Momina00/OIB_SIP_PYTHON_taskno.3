# ==============================
# INSTALL (run once in terminal)
# pip install requests pillow
# ==============================

import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO

# 🔑 Add your API key here
API_KEY = "bd5e378503939ddaee76f12ad7a97608"


# ==============================
# FUNCTION: GET WEATHER
# ==============================
def get_weather():
    city = city_entry.get()

    if city == "":
        messagebox.showerror("Error", "Please enter a city name")
        return

    try:
        # ---------- CURRENT WEATHER ----------
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        data = requests.get(url).json()

        if data["cod"] != 200:
            messagebox.showerror("Error", "City not found")
            return

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        desc = data["weather"][0]["description"]
        icon_code = data["weather"][0]["icon"]

        # ---------- ICON ----------
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url)

        img_data = icon_response.content
        img = Image.open(BytesIO(img_data))
        icon = ImageTk.PhotoImage(img)

        icon_label.config(image=icon)
        icon_label.image = icon  # prevent garbage collection

        # ---------- UPDATE UI ----------
        temp_label.config(text=f"{temp}°C")
        desc_label.config(text=desc.title())
        humidity_label.config(text=f"Humidity: {humidity}%")
        wind_label.config(text=f"Wind: {wind} m/s")

        # ---------- BACKGROUND COLOR ----------
        if temp > 30:
            root.config(bg="#ffcccb")
        elif temp < 15:
            root.config(bg="#add8e6")
        else:
            root.config(bg="#f0f0f0")

        # ---------- FORECAST ----------
        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        forecast_data = requests.get(forecast_url).json()

        forecast_text = ""
        for i in range(5):  # next 5 time slots
            item = forecast_data["list"][i]
            time = item["dt_txt"][11:16]  # only HH:MM
            f_temp = item["main"]["temp"]
            condition = item["weather"][0]["description"]

            forecast_text += f"{time} → {f_temp}°C, {condition}\n"

        forecast_label.config(text=forecast_text)

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ==============================
# GUI SETUP
# ==============================
root = tk.Tk()
root.title("Weather App")
root.geometry("400x550")
root.config(bg="#f0f0f0")

# ---------- TITLE ----------
title = tk.Label(root, text="Weather App", font=("Helvetica", 18, "bold"), bg="#f0f0f0")
title.pack(pady=10)

# ---------- INPUT FRAME ----------
top_frame = tk.Frame(root, bg="#f0f0f0")
top_frame.pack(pady=10)

city_entry = tk.Entry(top_frame, font=("Arial", 12))
city_entry.grid(row=0, column=0, padx=5)

search_btn = tk.Button(top_frame, text="Search", command=get_weather)
search_btn.grid(row=0, column=1, padx=5)

# ---------- WEATHER DISPLAY ----------
middle_frame = tk.Frame(root, bg="#f0f0f0")
middle_frame.pack(pady=10)

icon_label = tk.Label(middle_frame, bg="#f0f0f0")
icon_label.pack()

temp_label = tk.Label(middle_frame, text="", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
temp_label.pack()

desc_label = tk.Label(middle_frame, text="", font=("Arial", 12), bg="#f0f0f0")
desc_label.pack()

humidity_label = tk.Label(middle_frame, text="", font=("Arial", 10), bg="#f0f0f0")
humidity_label.pack()

wind_label = tk.Label(middle_frame, text="", font=("Arial", 10), bg="#f0f0f0")
wind_label.pack()

# ---------- FORECAST ----------
bottom_frame = tk.Frame(root, bg="#f0f0f0")
bottom_frame.pack(pady=15)

forecast_title = tk.Label(bottom_frame, text="Next Hours Forecast", font=("Arial", 12, "bold"), bg="#f0f0f0")
forecast_title.pack()

forecast_label = tk.Label(bottom_frame, text="", font=("Arial", 10), justify="left", bg="#f0f0f0")
forecast_label.pack()

# ---------- RUN APP ----------
root.mainloop()