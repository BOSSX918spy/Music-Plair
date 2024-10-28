import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import customtkinter as ctk
import pygame
from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3
import io
import serial
import threading

filename = ""
current_image = None
img_display = None
is_playing = False
crt = 0  # Current playback time in seconds
ttm = 0  # Total duration in seconds
motion_detected = "No motion"

def read_serial_data():
    global motion_detected
    ser = serial.Serial('COM3', 9600, timeout=1)
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode().strip()
            print("Motion data: " + data)
            if data == 'Motion detected':
                motion_detected = not motion_detected
                toggle_music()

def toggle_music():
    if is_playing:
        pause_music()
    else:
        play_music()

def update_progress():
    global crt, ttm
    if ttm > 0:
        progress = (crt / ttm) * 100
        progress_bar.set(progress)
        current_time_label.configure(text=str(int(crt // 60)).zfill(2) + ":" + str(int(crt % 60)).zfill(2))
        print("Progress updated to:", "{:.2f}%".format(progress))

def browse_file():
    global filename, ttm
    filename = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
    if filename:
        print("Selected file: " + filename)
        play_button.configure(state="normal")
        update_image()
        display_duration()
        pygame.mixer.music.pause()

def display_duration():
    global ttm
    if filename:
        audio = MP3(filename)
        duration = audio.info.length
        ttm = duration
        total_time_label.configure(text=str(int(ttm // 60)).zfill(2) + ":" + str(int(ttm % 60)).zfill(2))
        progress_bar.set(0)

def change_image():
    global current_image, is_playing
    if current_image == photo1:
        current_image = photo2
        play_button.configure(image=photo2)
        play_music()
    else:
        current_image = photo1
        play_button.configure(image=photo1)
        pause_music()

def pause_music():
    global is_playing
    if filename:
        pygame.mixer.music.pause()
        is_playing = False
        print("Music paused.")

def play_music():
    global is_playing
    if filename:
        try:
            if not is_playing:  # Only load and start if not already playing
                pygame.mixer.music.load(filename)
                pygame.mixer.music.play()
                is_playing = True
                update_playback_time()  # Start updating the playback time
            print("Music started.")
        except Exception as e:
            print("Error playing music: " + str(e))

def extract_album_art(mp3_file_path):
    try:
        audio = ID3(mp3_file_path)
        for tag in audio.values():
            if isinstance(tag, APIC):
                image_data = tag.data
                return Image.open(io.BytesIO(image_data))
    except Exception as e:
        print("Error extracting album art: " + str(e))
    return None

def update_image():
    global img_display
    album_art = extract_album_art(filename)
    if album_art:
        album_art_resized = album_art.resize((200, 200), Image.LANCZOS)
        img_display = ImageTk.PhotoImage(album_art_resized)
        image_label.configure(image=img_display)
        image_label.image = img_display
    else:
        print("No album art found or error loading image.")

def update_playback_time():
    global crt, ttm
    if is_playing:
        current_pos = pygame.mixer.music.get_pos() / 1000  # Get position in seconds
        crt = current_pos
        update_progress()  # Update progress bar based on crt
        print("Current Time: " + "{:.2f} seconds".format(crt))
        app.after(100, update_playback_time)  # Update every 100 milliseconds

def adjust_volume(value):
    volume = float(value) / 100
    pygame.mixer.music.set_volume(volume)
    volume_label.configure(text="Volume: " + "{:.0f}".format(value))
    print("Volume set to: " + "{:.2f}".format(volume))

app = ctk.CTk()
app.geometry("310x500")
app.title("Musik Plair")
app.resizable(False, False)
pygame.mixer.init()

image_frame = ctk.CTkFrame(app, width=200, height=200, fg_color="white", corner_radius=20)
image_frame.pack(padx=11, pady=11)
image_frame.pack_propagate(False)

progress_frame = ctk.CTkFrame(app)
progress_frame.pack(pady=10)

current_time_label = ctk.CTkLabel(progress_frame, text="00:00")
current_time_label.pack(side=tk.LEFT, padx=(10, 5))

progress_bar = ctk.CTkProgressBar(progress_frame, width=200)
progress_bar.pack(side=tk.LEFT, padx=(5, 5))

total_time_label = ctk.CTkLabel(progress_frame, text="00:00")
total_time_label.pack(side=tk.RIGHT, padx=(5, 10))

progress_bar.set(0)  # Initialize progress bar to 0

volume_frame = ctk.CTkFrame(app)
volume_frame.pack(side=tk.BOTTOM, pady=10)

volume_slider = ctk.CTkSlider(volume_frame, from_=0, to=100, command=adjust_volume, corner_radius=100)
volume_slider.pack(side=tk.TOP, padx=20, pady=(0, 5), fill=tk.X)

volume_label = ctk.CTkLabel(volume_frame, text="Volume: 50")
volume_label.pack(side=tk.TOP, padx=20, pady=5)

image_label = ctk.CTkLabel(image_frame, text="", corner_radius=20)
image_label.pack(fill="both", expand=True, padx=5, pady=5)

img = Image.open("F:/DHAI/Musik Plair/da.png")
img = img.resize((128, 18))
pic = ImageTk.PhotoImage(img)
label = ctk.CTkLabel(app, text='', image=pic)
label.pack(padx=10, pady=0)
label.image = pic

browse_button = ctk.CTkButton(app, text="Open Music", font=("Helvetica", 12), command=browse_file)
browse_button.pack(padx=20, pady=10)

photo1 = Image.open("F:/DHAI/Musik Plair/pause.png")
photo2 = Image.open("F:/DHAI/Musik Plair/play.png")

photo1 = photo1.resize((70, 70))
photo2 = photo2.resize((70, 70))

current_image = photo1

photo1 = ImageTk.PhotoImage(photo1)
photo2 = ImageTk.PhotoImage(photo2)

play_button = ctk.CTkButton(app, image=photo1, text="", command=change_image, width=1, state="disabled", corner_radius=500000000)
play_button.pack(padx=1, pady=1)

# Start the thread for reading the serial data
thread = threading.Thread(target=read_serial_data)
thread.daemon = True
thread.start()

app.mainloop()
