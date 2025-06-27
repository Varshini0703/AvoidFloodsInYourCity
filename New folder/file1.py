import tkinter as tk
from tkinter import font as tkFont
from PIL import Image, ImageTk, ImageSequence
import cv2
import webbrowser
import os
import requests
from tkinter import messagebox
from datetime import datetime
from tkintermapview import TkinterMapView
import pyttsx3

class VideoPlayer(tk.Tk):
    def __init__(self):

        super().__init__()
        self.title("Weather Forecast Introduction")
        self.attributes('-fullscreen', True)  # Open in full screen mode

        self.video_path = 'video1.mp4'  # Update with the path to your video
        self.cap = cv2.VideoCapture(self.video_path)

        # Create a canvas for the video and text
        self.canvas = tk.Canvas(self)
        self.canvas.pack(expand=True, fill='both')

        # Add the main title in the middle with Freestyle Script font
        self.text_id = self.canvas.create_text(400, 300, text="WEATHER FORECAST", font=("Freestyle Script", 60, "bold"),
                                               fill="white", anchor='center')

        # Create custom font for the button
        button_font = tkFont.Font(family="Helvetica", size=16, weight="bold")

        # Add a button to go to the weather app
        self.weather_button = tk.Button(self, text="Weather App", command=self.open_weather_app,
                                        font=button_font, fg="white", bg="blue", borderwidth=5, relief="raised", padx=10,
                                        pady=5)
        self.weather_button.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor='se')

        # Add another button to open the weather HTML page
        self.html_button = tk.Button(self, text="World Map", command=self.open_html_page,
                                     font=button_font, fg="white", bg="green", borderwidth=5, relief="raised", padx=10,
                                     pady=5)
        self.html_button.place(relx=1.0, rely=1.0, x=-220, y=-20, anchor='se')

        # Bind the configure event to update the video size and center the text
        self.bind('<Configure>', self.update_video_size)

        # Start the video playback
        self.play_video()

    def play_video(self):
        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Loop the video
            ret, frame = self.cap.read()

        if ret:
            # Resize the frame to fit the window
            frame = cv2.resize(frame, (self.canvas.winfo_width(), self.canvas.winfo_height()))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_image = ImageTk.PhotoImage(Image.fromarray(frame))

            # Update the canvas with the new frame
            self.canvas.create_image(0, 0, anchor=tk.NW, image=frame_image)
            self.canvas.image = frame_image

            # Ensure the text is always on top
            self.canvas.tag_raise(self.text_id)

        # Call this method again after 33 ms (approx. 30 frames per second)
        self.after(33, self.play_video)

    def update_video_size(self, event):
        self.canvas.config(width=event.width, height=event.height)
        # Center the text in the canvas
        self.canvas.coords(self.text_id, event.width // 2, event.height // 2)

    def open_weather_app(self):
        self.destroy()
        start_weather_app(fullscreen=True)

    def open_html_page(self):
        self.destroy()
        start_weather_html_app(fullscreen=True)

def start_weather_app(fullscreen=False):
    import weather_app
    weather_app.run_weather_app(fullscreen=fullscreen)

def start_weather_html_app(fullscreen=False):
    app = WeatherHTMLApp(fullscreen=fullscreen)
    app.mainloop()

class WeatherHTMLApp(tk.Tk):
    def __init__(self, fullscreen=False):
        super().__init__()
        self.fullscreen = fullscreen
        self.title("Weather Map and Forecast")
        self.attributes('-fullscreen', self.fullscreen)

        self.gif_path = r"cartoon.gif"
        self.gif_image = Image.open(self.gif_path)
        self.frames = [ImageTk.PhotoImage(frame.resize((self.winfo_screenwidth(), self.winfo_screenheight())))
                       for frame in ImageSequence.Iterator(self.gif_image)]

        self.label = tk.Label(self)
        self.label.place(relheight=1, relwidth=1)
        self.update_frame(0)

        now = datetime.now()
        dt_string = now.strftime("%d - %m - %Y")
        time = now.strftime("%H:%M:%S")
        day = now.strftime("%A")

        self.DateLabel = tk.Label(self, text=f"{dt_string}", font=("Helvetica", 20), fg="white", bg="black")
        self.DateLabel.place(x=1300, y=100)

        self.timeLabel = tk.Label(self, text=f"{time}", font=("Helvetica", 20), fg="white", bg="black")
        self.timeLabel.place(x=1300, y=140)

        self.dayLabel = tk.Label(self, text=f"{day}", font=("Helvetica", 20), fg="white", bg="black")
        self.dayLabel.place(x=1300, y=180)

        self.startButton = tk.Button(self, text="FORECAST", font=("Arial", 25), width=15, height=1, fg="green", bg="lightgreen", command=self.showSearchBar)
        self.startButton.place(relx=0.4, rely=0.75, anchor='center')

        self.closeButton = tk.Button(self, text="CLOSE", font=("Arial", 25), width=15, height=1, fg="red", bg="pink", command=self.destroy)
        self.closeButton.place(relx=0.6, rely=0.75, anchor='center')

        self.cityLabel = tk.Label(self, text='Enter your city name', font=('arial', 20, 'bold'), bg="#57adff")
        self.questionField = tk.Entry(self, width=45, font=('arial', 14, 'bold'), bd=4, relief=tk.SUNKEN)
        self.searchButton = tk.Button(self, text="Search", font=("Arial", 15), command=self.search, bg="Lightblue")

    def update_frame(self, ind):
        if self.label.winfo_exists():
            frame = self.frames[ind]
            ind += 1
            if ind == len(self.frames):
                ind = 0
            self.label.configure(image=frame)
        self.after(self.gif_image.info['duration'], self.update_frame, ind)

    def reverseDate(self, date):
        date_parts = date.split("-")
        return "-".join(reversed(date_parts))

    def getWeather(self, cityName):
        try:
            baseUrl = "http://api.openweathermap.org/data/2.5/weather?"
            apiKey = "51d3896b7013940aa5bc057df051cd5b"
            api1 = baseUrl + "&units=metric" + "&appid=" + apiKey + "&q=" + cityName

            data1 = requests.get(api1).json()
            cityCode = data1['id']
            latitude = data1['coord']['lat']
            longitude = data1['coord']['lon']

            api2 = f"http://api.openweathermap.org/data/2.5/forecast?id={cityCode}&appid={apiKey}&units=metric"
            response = requests.get(api2)
            data2 = response.json()

            dataList = []
            for index in range(0, 40):
                date_time, temp, description = self.threeHrWeather(data2, index)
                dataList.append([date_time, temp, description])

            temp = data1['main']['temp']
            humidity = data1['main']['humidity']
            pressure = data1['main']['pressure']
            wind = data1['wind']['speed']
            description = data1['weather'][0]['description']

            return [temp, humidity, pressure, wind, description, dataList, latitude, longitude]

        except requests.exceptions.RequestException:
            messagebox.showerror("ERROR", "Network Error: Please check your internet connection.")
            self.destroy()
        except KeyError:
            return

    def threeHrWeather(self, data, index):
        date_time = data['list'][index]['dt_txt']
        temp = data['list'][index]['main']['temp']
        description = data['list'][index]['weather'][0]['description']
        return [date_time, temp, description]

    def showSearchBar(self):
        self.cityLabel.place(relx=0.5, rely=0.05, anchor='center')
        self.questionField.place(relx=0.5, rely=0.1, anchor='center')
        self.searchButton.place(relx=0.8, rely=0.1, anchor='center')
        self.startButton.place(relx=0.4, rely=0.75, anchor='center')
        self.closeButton.place(relx=0.6, rely=0.75, anchor='center')

        # Hide any other widgets that were added to the root window
        for widget in self.winfo_children():
            if widget not in (self.label, self.DateLabel,self. timeLabel, self.dayLabel,self.cityLabel, self.questionField, self.searchButton,self.startButton, self.closeButton):
                widget.pack_forget()
                widget.place_forget()

    def hideSearchBar(self):
        self.cityLabel.place_forget()
        self.questionField.place_forget()
        self.searchButton.place_forget()

    def search(self):
        cityName = self.questionField.get()
        data = self.getWeather(cityName)
        if data:
            self.showThirdPage(data, cityName)
        else:
            messagebox.showerror("ERROR", "City not found.")
            self.destroy()

    def showThirdPage(self, data, cityName):
        self.hideSearchBar()
        for widget in self.winfo_children():
            if widget not in (self.label, self.DateLabel, self.timeLabel, self.dayLabel):
                widget.pack_forget()
                widget.place_forget()

        mapWidget = TkinterMapView(self, width=800, height=600, corner_radius=0)
        mapWidget.pack(fill="both", expand=True)

        lat = data[6]
        lng = data[7]

        mapWidget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=10)
        mapWidget.set_position(lat, lng)
        mapWidget.set_marker(lat, lng, text=cityName.upper())

        self.displayInfo(data, cityName)

    def displayInfo(self, data, cityName):
        frame = tk.Frame(self, bd=5, bg='#57adff', highlightbackground='dark gray', highlightthickness=2)
        frame.place(x=850, y=250, width=250, height=250)

        tempLabel = tk.Label(self, text=f"Temperature : {data[0]} °C", font=("Helvetic", 12), fg="white", bg='black')
        tempLabel.place(x=870, y=280)

        humidityLabel = tk.Label(self, text=f"Humidity : {data[1]} %", font=("Helvetic", 12), fg="white", bg='black')
        humidityLabel.place(x=870, y=310)

        pressureLabel = tk.Label(self, text=f"Pressure : {data[2]} hPa", font=("Helvetic", 12), fg="white", bg='black')
        pressureLabel.place(x=870, y=340)

        windLabel = tk.Label(self, text=f"Wind speed : {data[3]} m/s", font=("Helvetic", 12), fg="white", bg='black')
        windLabel.place(x=870, y=370)

        descriptionLabel = tk.Label(self, text=f"Description : {data[4]}", font=("Helvetic", 12), fg="white", bg='black')
        descriptionLabel.place(x=870, y=400)

        backButton = tk.Button(self, text="Back", font=("Arial", 15), command=self.showSearchBar, bg="lightblue")
        backButton.place(x=10, y=800)

        index = 0
        y_co = 25

        for day in range(1, 6):
            frame_day = tk.Frame(self, bd=2, bg="yellow", highlightbackground='dark gray', highlightthickness=2)
            frame_day.place(x=500 + (day - 1) * 140, y=575, width=130, height=200)

            date = self.reverseDate(data[5][index][0][:10])
            dateLabel = tk.Label(self, text=f"{date}", font=("Helvetica", 11), bg="Yellow")
            dateLabel.place(x=510 + (day - 1) * 140, y=580)

            y_co = 25
            index += 1

            while data[5][index][0][11:] != "00:00:00":
                temperature = tk.Label(self, text=f"{data[5][index][0][11:16]} - {data[5][index][1]} °C",
                                       font=("Helvetica", 11), bg="Yellow")
                temperature.place(x=510 + (day - 1) * 140, y=575 + y_co)
                index += 1
                y_co += 20

        self.after(1100, lambda: self.voice(data, cityName))

    def voice(self, data, cityName):
        engine = pyttsx3.init()
        temp = data[0]
        humidity = data[1]
        pressure = data[2]
        wind = data[3]
        description = data[4]
        str = f"The weather forecast for {cityName}. The temperature is {temp} degree Celsius. The humidity is {humidity} percent. The pressure is {pressure} hpa. The wind speed is {wind} meters per second. The weather description is {description}."
        engine.say(str)
        engine.runAndWait()

if __name__ == "__main__":
    app = VideoPlayer()
    app.mainloop()
