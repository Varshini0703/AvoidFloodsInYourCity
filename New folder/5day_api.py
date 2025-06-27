import requests
from tkinter import *
from tkintermapview import TkinterMapView
from tkinter import messagebox
from datetime import datetime
from PIL import Image, ImageTk, ImageSequence
import pyttsx3

root = Tk()

# Load the GIF and start the animation
gif_path = r"cartoon.gif"

# uses the PIL (Pillow) library to open the GIF file.
gif_image = Image.open(gif_path)

# Prepare Frames for Animation
frames = [ImageTk.PhotoImage(frame.resize((root.winfo_screenwidth(), root.winfo_screenheight()))) for frame in
          ImageSequence.Iterator(gif_image)]

# Label to display the GIF frames.
label = Label(root)
label.place(relheight=1, relwidth=1)

def update_frame(ind):
    if label.winfo_exists():
        frame = frames[ind]
        ind += 1
        if ind == len(frames):
            ind = 0
        label.configure(image=frame)
    root.after(gif_image.info['duration'], update_frame, ind)

update_frame(0)

def reverseDate(date):
    date_parts = date.split("-")
    return "-".join(reversed(date_parts))

now = datetime.now()
dt_string = now.strftime("%d - %m - %Y")
time = now.strftime("%H:%M:%S")
day = now.strftime("%A")

# Display date, time, and day
DateLabel = Label(root, text=f"{dt_string}", font=("Helvetica", 20), fg="white", bg="black")
DateLabel.place(x=1300, y=100)

timeLabel = Label(root, text=f"{time}", font=("Helvetica", 20), fg="white", bg="black")
timeLabel.place(x=1300, y=140)

dayLabel = Label(root, text=f"{day}", font=("Helvetica", 20), fg="white", bg="black")
dayLabel.place(x=1300, y=180)

# Function to get data from API
def getWeather(cityName):
    try:
        # url - for getting the current weather forecast
        baseUrl = "http://api.openweathermap.org/data/2.5/weather?"
        apiKey = "51d3896b7013940aa5bc057df051cd5b"
        api1 = baseUrl + "&units=metric" + "&appid=" + apiKey + "&q=" + cityName
        # print(api1)

        # getting data from the api
        data1 = requests.get(api1).json()

        cityCode = data1['id']

        # getting the longitude and latitude of the city
        latitude = data1['coord']['lat']
        longitude = data1['coord']['lon']

        # url - for getting the forecast of 5 days
        api2 = f"http://api.openweathermap.org/data/2.5/forecast?id={cityCode}&appid={apiKey}&units=metric"

        # getting data from the api
        # print(api2)
        response = requests.get(api2)
        data2 = response.json()
        # print(data2)
        dataList = []
        for index in range(0, 40):
            date_time, temp, description = threeHrWeather(data2, index)
            dataList.append([date_time, temp, description])
            # print(dataList)

        # temperature
        temp = data1['main']['temp']

        # humidity
        humidity = data1['main']['humidity']

        # pressure
        pressure = data1['main']['pressure']

        # windspeed
        wind = data1['wind']['speed']

        # description
        description = data1['weather'][0]['description']

        return [temp, humidity, pressure, wind, description, dataList, latitude, longitude]

    except requests.exceptions.RequestException:
        # Create a message box with an "OK" button
        messagebox.showerror("ERROR", "Network Error: Please check your internet connection.")

        # Close the root window
        root.destroy()

    except KeyError:
        return

# Getting the 3 hr weather forecast for 5 days
def threeHrWeather(data, index):
    # date and time
    date_time = data['list'][index]['dt_txt']

    # temperature
    temp = data['list'][index]['main']['temp']

    # Description
    description = data['list'][index]['weather'][0]['description']

    return [date_time, temp, description]

def showSearchBar():
    cityLabel.place(relx=0.5, rely=0.05, anchor=CENTER)
    questionField.place(relx=0.5, rely=0.1, anchor=CENTER)
    searchButton.place(relx=0.8, rely=0.1, anchor=CENTER)

    # Hide any other widgets that were added to the root window
    for widget in root.winfo_children():
        if widget not in (label, DateLabel, timeLabel, dayLabel, cityLabel, questionField, searchButton, startButton, closeButton):
            widget.pack_forget()
            widget.place_forget()

def hideSearchBar():
    cityLabel.place_forget()
    questionField.place_forget()
    searchButton.place_forget()

def search():
    cityName = questionField.get()
    data = getWeather(cityName)
    if data:
        showThirdPage(data, cityName)
    else:
        # Create a message box with an "OK" button
        messagebox.showerror("ERROR", "City not found.")
        # Close the root window
        root.destroy()

# Function to show the third page content
def showThirdPage(data, cityName):
    # Hide search bar
    hideSearchBar()
    for widget in root.winfo_children():
        if widget not in (label, DateLabel, timeLabel, dayLabel):
            widget.pack_forget()
            widget.place_forget()

    mapWidget = TkinterMapView(root, width=800, height=600, corner_radius=0)
    mapWidget.pack(fill="both", expand=True)

    lat = data[6]
    lng = data[7]

    # google maps server
    mapWidget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=10)
    mapWidget.set_position(lat, lng)
    mapWidget.set_marker(lat, lng, text=cityName.upper())

    displayInfo(data, cityName)

def displayInfo(data, cityName):
    # Create frame for displaying the current weather forecast
    frame = Frame(root, bd=5, bg='#57adff', highlightbackground='dark gray', highlightthickness=2)
    frame.place(x=850, y=250, width=250, height=250)

    # Temperature
    tempLabel = Label(root, text=f"Temperature : {data[0]} °C", font=("Helvetic", 12), fg="white", bg='black')
    tempLabel.place(x=870, y=280)

    # Humidity
    humidityLabel = Label(root, text=f"Humidity : {data[1]} %", font=("Helvetic", 12), fg="white", bg='black')
    humidityLabel.place(x=870, y=310)

    # Pressure
    pressureLabel = Label(root, text=f"Pressure : {data[2]} hPa", font=("Helvetic", 12), fg="white", bg='black')
    pressureLabel.place(x=870, y=340)

    # Wind Speed
    windLabel = Label(root, text=f"Wind speed : {data[3]} m/s", font=("Helvetic", 12), fg="white", bg='black')
    windLabel.place(x=870, y=370)

    # Description
    descriptionLabel = Label(root, text=f"Description : {data[4]}", font=("Helvetic", 12), fg="white", bg='black')
    descriptionLabel.place(x=870, y=400)

    # Back button
    backButton = Button(root, text="Back", font=("Arial", 15), command=showSearchBar, bg="lightblue")
    backButton.place(x=10, y=800)

    # initializing the index number
    index = 0
    y_co = 25

    # Creating and displaying the frames for 3 hr forecast of 5 days
    for day in range(1, 6):
        # Day
        frame_day = Frame(root, bd=2, bg="yellow", highlightbackground='dark gray', highlightthickness=2)
        frame_day.place(x=500 + (day - 1) * 140, y=575, width=130, height=200)

        date = reverseDate(data[5][index][0][:10])

        dateLabel = Label(root, text=f"{date}", font=("Helvetica", 11), bg="Yellow")
        dateLabel.place(x=510 + (day - 1) * 140, y=580)

        y_co = 25
        index += 1

        while data[5][index][0][11:] != "00:00:00":
            temperature = Label(root, text=f"{data[5][index][0][11:16]} - {data[5][index][1]} °C",
                                font=("Helvetica", 11), bg="Yellow")
            temperature.place(x=510 + (day - 1) * 140, y=575 + y_co)
            index += 1
            y_co += 20

    root.after(1000, lambda: voice(data, cityName))

    def voice(data, cityName):
        engine = pyttsx3.init()
        temp = data[0]
        humidity = data[1]
        pressure = data[2]
        wind = data[3]
        description = data[4]
        str = f"The weather forecast for {cityName}. The temperature is {temp} degree Celsius. The humidity is {humidity} percent. The pressure is {pressure} hpa. The wind speed is {wind} meters per second. The weather description is {description}."
        engine.say(str)
        engine.runAndWait()

    # Back button for weather forecast page
    backButton = Button(root, text="Back", font=("Arial", 15), command=showSearchBar, bg="lightblue")
    backButton.place(x=10, y=800)

# Main page buttons
startButton = Button(root, text="FORECAST", font=("Arial", 25), width=15, height=1, fg="green", bg="lightgreen", command=showSearchBar)
startButton.place(relx=0.4, rely=0.75, anchor=CENTER)

closeButton = Button(root, text="CLOSE", font=("Arial", 25), width=15, height=1, fg="red", bg="pink", command=root.destroy)
closeButton.place(relx=0.6, rely=0.75, anchor=CENTER)

# Search bar widgets (initially hidden)
cityLabel = Label(root, text='Enter your city name', font=('arial', 20, 'bold'), bg="#57adff")
questionField = Entry(root, width=45, font=('arial', 14, 'bold'), bd=4, relief=SUNKEN)
searchButton = Button(root, text="Search", font=("Arial", 15), command=search, bg="Lightblue")

# Set the window to fullscreen
root.attributes('-fullscreen', True)

# Start the Tkinter event loop
root.mainloop()