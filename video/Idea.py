import tkinter as tk
from tkinter import font as tkFont
from PIL import Image, ImageTk
import cv2
import webbrowser
import os
 
class VideoPlayer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weather Today Introduction")
        self.attributes('-fullscreen', True)  # Open in full screen mode

        self.video_path = 'video1.mp4'  # Update with the path to your video
        self.cap = cv2.VideoCapture(self.video_path)

        # Create a canvas for the video and text
        self.canvas = tk.Canvas(self)
        self.canvas.pack(expand=True, fill='both')

        # Add the main title in the middle with Freestyle Script font
        self.text_id = self.canvas.create_text(400, 300, text="WEATHER TODAY", font=("Freestyle Script", 60, "bold"),
                                               fill="white", anchor='center')

        # Create custom font for the button
        button_font = tkFont.Font(family="Helvetica", size=16, weight="bold")

        # Add a button to go to the weather app
        self.weather_button = tk.Button(self, text="Weather App", command=self.open_weather_app,
                                        font=button_font, fg="white", bg="blue", borderwidth=5, relief="raised", padx=10,
                                        pady=5)
        self.weather_button.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor='se')

        # Add another button to open an HTML page
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
        webbrowser.open('file:///' + os.path.realpath("file:///C:/Users/91832/PycharmProjects/map/weather.html"))

def start_weather_app(fullscreen=False):
    import weather_app
    weather_app.run_weather_app(fullscreen=fullscreen)


def run_weather_app(fullscreen=False):
    app = VideoPlayer(fullscreen=fullscreen)  # Create an instance of the WeatherApp class
    app.mainloop()

if __name__ == "__main__":
    app = VideoPlayer()
    app.mainloop()
