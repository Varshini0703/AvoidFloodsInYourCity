import tkinter as tk
from tkinter import font as tkFont
from PIL import Image, ImageTk
import cv2
import webbrowser
import os

class VideoPlayer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WeatherWise Introduction")
        self.geometry("800x600")

        self.video_path = 'video1.mp4'  # Update with the path to your video
        self.cap = cv2.VideoCapture(self.video_path)

        # Create a canvas for the video and text
        self.canvas = tk.Canvas(self)
        self.canvas.pack(expand=True, fill='both')

        # Add the main title in the middle with Freestyle Script font
        self.text_id = self.canvas.create_text(400, 300, text="WEATHER WISE", font=("Freestyle Script", 60, "bold"),
                                               fill="white", anchor='center')

        # Create custom font for the button
        button_font = tkFont.Font(family="Helvetica", size=16, weight="bold")

        # Add a button to go to the second page
        self.button = tk.Button(self, text="Go to Second Page", command=self.open_html_page,
                                font=button_font, fg="white", bg="blue", borderwidth=5, relief="raised", padx=10,
                                pady=5)
        self.button.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor='se')

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

    def open_html_page(self):
        webbrowser.open('file:///' + os.path.realpath("C:\\Users\\91832\\project1\\templates\\weather.html"))


if __name__ == "__main__":
    app = VideoPlayer()
    app.mainloop()
