import tkinter as tk
from tkinter import messagebox, filedialog
from yt_dlp import YoutubeDL
import os
import pyperclip
import threading
import time

def download_audio():
    youtube_url = url_entry.get()
    output_format = format_var.get()
    ffmpeg_location = ffmpeg_path.get()
    
    if not youtube_url:
        messagebox.showwarning("Input Error", "Please enter a YouTube URL.")
        return

    if not output_format:
        messagebox.showwarning("Input Error", "Please select an output format.")
        return

    if not os.path.isdir(ffmpeg_location):
        messagebox.showwarning("Input Error", "The specified ffmpeg location is not valid.")
        return

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,  # Estää soittolistan lataamisen
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': output_format,
            'preferredquality': '192',
        }],
        'outtmpl': '%(title)s.%(ext)s',
        'ffmpeg_location': ffmpeg_location
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
            messagebox.showinfo("Success", f"Downloaded and converted to {output_format}.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def monitor_clipboard():
    recent_value = ""
    while True:
        tmp_value = pyperclip.paste()
        if tmp_value != recent_value and ("youtube.com/watch" in tmp_value or "youtu.be/" in tmp_value):
            recent_value = tmp_value
            url_entry.delete(0, tk.END)
            url_entry.insert(0, recent_value)
        time.sleep(1)  # Tarkistaa leikepöydän joka sekunti

def browse_ffmpeg():
    folder_selected = filedialog.askdirectory()
    ffmpeg_path.set(folder_selected)

# Luodaan pääikkuna
root = tk.Tk()
root.title("YouTube Audio Downloader")

# URL-kenttä
tk.Label(root, text="YouTube URL:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Muoto-valitsin
tk.Label(root, text="Select Output Format:").pack(pady=5)
format_var = tk.StringVar(value="mp3")
tk.Radiobutton(root, text="MP3", variable=format_var, value="mp3").pack(pady=5)
tk.Radiobutton(root, text="WAV", variable=format_var, value="wav").pack(pady=5)

# FFmpeg-polku
tk.Label(root, text="FFmpeg Location:").pack(pady=5)
ffmpeg_path = tk.StringVar(value=r"C:\Users\pkarj\ffmpeg-2024-08-04-git-eb3cc508d8-full_build\bin")
tk.Entry(root, textvariable=ffmpeg_path, width=50).pack(pady=5)
tk.Button(root, text="Browse", command=browse_ffmpeg).pack(pady=5)

# Lataa-painike
tk.Button(root, text="Download Audio", command=download_audio).pack(pady=20)

# Käynnistetään leikepöydän seuranta säikeessä
clipboard_thread = threading.Thread(target=monitor_clipboard, daemon=True)
clipboard_thread.start()

# Käynnistetään GUI
root.mainloop()

