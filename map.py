mapWidget = TkinterMapView(root, width=800, height=600, corner_radius=0)
mapWidget.pack(fill="both", expand=True)

lat = data[6]
lng = data[7]

# google maps server
mapWidget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=10)
mapWidget.set_position(lat, lng)
mapWidget.set_marker(lat, lng, text=cityName.upper())

root.after(13000, lambda: displayInfo())


def displayInfo():
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
    backButton = Button(root, text="Back", font=("Arial", 15), command=showSecondPage, bg="lightblue")
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