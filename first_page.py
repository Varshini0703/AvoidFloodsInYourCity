import tkinter as tk
from PIL import Image, ImageTk
import cv2
import threading

# Function to play the video as background
def play_video(canvas, text_id):
    video_path = 'video1.mp4'  # Update with the path to your video
    cap = cv2.VideoCapture(video_path)

    while True:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Loop the video
            continue

        # Resize the frame to fit the window
        frame = cv2.resize(frame, (canvas.winfo_width(), canvas.winfo_height()))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_image = ImageTk.PhotoImage(Image.fromarray(frame))

        # Update the canvas with the new frame
        canvas.create_image(0, 0, anchor=tk.NW, image=frame_image)
        canvas.image = frame_image

        # Ensure the text is always on top
        canvas.tag_raise(text_id)

        # Add a small delay to mimic video frame rate
        canvas.after(33)

    cap.release()

# Function to update the video size dynamically
def update_video_size(event):
    canvas.config(width=event.width, height=event.height)
    # Center the text in the canvas
    canvas.coords(text_id, event.width // 2, event.height // 2)

# Create the main window
root = tk.Tk()
root.title("WeatherWise Introduction")
root.geometry("800x600")

# Create a canvas for the video and text
canvas = tk.Canvas(root)
canvas.pack(expand=True, fill='both')

# Add the main title in the middle with Freestyle Script font
text_id = canvas.create_text(400, 300, text="WEATHER WISE", font=("Freestyle Script", 60, "bold"), fill="white", anchor='center')

# Bind the configure event to update the video size and center the text
root.bind('<Configure>', update_video_size)

# Start playing the video in a separate thread
threading.Thread(target=play_video, args=(canvas, text_id), daemon=True).start()

# Run the Tkinter event loop
root.mainloop()