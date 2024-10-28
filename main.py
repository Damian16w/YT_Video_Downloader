import os
import yt_dlp
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import subprocess  # To open the directory

def download_youtube_content(url, output_directory, output_filename, audio_only=False):
    output_path = os.path.join(output_directory, f"{output_filename}.%(ext)s")
    
    ydl_opts = {
        'outtmpl': output_path,
        'progress_hooks': [hook],  # Hook for progress updates
    }

    if audio_only:
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:
        ydl_opts.update({
            'format': 'best',
        })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading: {url}")
            ydl.download([url])
            print("Download completed!")
            messagebox.showinfo("Success", "Download completed successfully!")
            open_directory(output_directory)  # Open the directory when done
    except Exception as e:
        print(f"An error occurred: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")

def hook(d):
    if d['status'] == 'downloading':
        percent = d['downloaded_bytes'] / d['total_bytes'] * 100
        progress_var.set(percent)  # Update progress bar
    elif d['status'] == 'finished':
        progress_var.set(100)  # Complete

def open_directory(directory):
    # Open the output directory using the default file explorer
    if os.name == 'nt':  # For Windows
        os.startfile(directory)
    elif os.name == 'posix':  # For macOS and Linux
        subprocess.Popen(['open', directory]) if sys.platform == 'darwin' else subprocess.Popen(['xdg-open', directory])

def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        dir_entry.delete(0, tk.END)
        dir_entry.insert(0, directory)

def start_download():
    url = url_entry.get()
    output_directory = dir_entry.get()
    output_filename = filename_entry.get()
    audio_only = audio_var.get()
    
    if not url or not output_directory or not output_filename:
        messagebox.showwarning("Warning", "Please fill in all fields.")
        return

    download_youtube_content(url, output_directory, output_filename, audio_only)

# Create the main window
root = tk.Tk()
root.title("YouTube Video Downloader")
root.geometry("650x550")
root.configure(bg="#2e2e2e")  # Set background color

# Set the application icon (ensure you have an icon.ico file in the same directory)
root.iconbitmap(default='logo.ico')  # Replace 'icon.ico' with your icon file name or path

# Title Label
title_label = tk.Label(root, text="YouTube Video Downloader", font=("Helvetica", 16), bg="#2e2e2e", fg="#ffffff")
title_label.pack(pady=10)

# URL Entry
url_label = tk.Label(root, text="YouTube Video URL:", font=("Helvetica", 12), bg="#2e2e2e", fg="#ffffff")
url_label.pack(pady=5)
url_entry = tk.Entry(root, width=50, font=("Helvetica", 12))
url_entry.pack(pady=5)

# Output Directory
dir_label = tk.Label(root, text="Output Directory:", font=("Helvetica", 12), bg="#2e2e2e", fg="#ffffff")
dir_label.pack(pady=5)
dir_entry = tk.Entry(root, width=40, font=("Helvetica", 12))
dir_entry.pack(pady=5)
tk.Button(root, text="Browse", command=browse_directory, font=("Helvetica", 12), bg="#4CAF50", fg="#ffffff").pack(pady=5)

# Output File Name
filename_label = tk.Label(root, text="Output File Name (without extension):", font=("Helvetica", 12), bg="#2e2e2e", fg="#ffffff")
filename_label.pack(pady=5)
filename_entry = tk.Entry(root, width=50, font=("Helvetica", 12))
filename_entry.pack(pady=5)

# Audio Only Option
audio_var = tk.BooleanVar()
audio_check = tk.Checkbutton(root, text="Download Audio Only", variable=audio_var, font=("Helvetica", 12), bg="#2e2e2e", fg="#ffffff")
audio_check.pack(pady=5)

# Fixed Width Progress Bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=400)  # Fixed length of 400
progress_bar.pack(pady=20)

# Download Button
download_button = tk.Button(root, text="Download", command=start_download, font=("Helvetica", 12), bg="#2196F3", fg="#ffffff")
download_button.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()
