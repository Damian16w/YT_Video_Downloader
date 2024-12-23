import os
import yt_dlp
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess

def download_content(url, output_directory, output_filename, platform, resolution, audio_only=False):
    output_path = os.path.join(output_directory, f"{output_filename}.%(ext)s")
    
    ydl_opts = {
        'outtmpl': output_path,
        'progress_hooks': [hook],
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
        if resolution == "Best":
            ydl_opts.update({'format': 'best'})
        else:
            ydl_opts.update({'format': f'bestvideo[height<={resolution}]+bestaudio/best'})

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            messagebox.showinfo("Success", "Download completed successfully!")
            open_directory(output_directory)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def hook(d):
    if d['status'] == 'downloading':
        percent = d.get('downloaded_bytes', 0) / d.get('total_bytes', 1) * 100
        progress_var.set(percent)
    elif d['status'] == 'finished':
        progress_var.set(100)

def open_directory(directory):
    if os.name == 'nt':
        os.startfile(directory)
    elif os.name == 'posix':
        subprocess.Popen(['open', directory] if sys.platform == 'darwin' else ['xdg-open', directory])

def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        dir_entry.delete(0, tk.END)
        dir_entry.insert(0, directory)

def start_download():
    url = url_entry.get()
    output_directory = dir_entry.get()
    output_filename = filename_entry.get()
    platform = platform_var.get()
    audio_only = audio_var.get()
    resolution = resolution_var.get()

    if not url or not output_directory or not output_filename:
        messagebox.showwarning("Warning", "Please fill in all fields.")
        return

    download_content(url, output_directory, output_filename, platform, resolution, audio_only)

root = tk.Tk()
root.title("Social Media Video Downloader")
root.geometry("650x800")
root.configure(bg="#282828")

copyright_label = tk.Label(
    root, text="© DrJunkHoofd", font=("Roboto", 10), bg="#282828", fg="#ffffff", anchor="w"
)
copyright_label.pack(pady=(5, 10), padx=20)

title_label = tk.Label(
    root, text="Social Media Video Downloader", font=("Roboto", 30),
    bg="#282828", fg="#FF0000", height=2
)
title_label.pack()

platform_frame = tk.Frame(root, bg="#282828")
platform_frame.pack(pady=10)
platform_label = tk.Label(platform_frame, text="Select Platform:", font=("Roboto", 12), bg="#282828", fg="#ffffff")
platform_label.grid(row=0, column=0, padx=10)

platform_var = tk.StringVar()
platform_choices = ["YouTube", "Twitter", "Instagram", "TikTok", "Reddit"]
platform_menu = ttk.Combobox(platform_frame, textvariable=platform_var, values=platform_choices, font=("Roboto", 12), state="readonly")
platform_menu.grid(row=0, column=1, padx=10)
platform_menu.current(0)

url_frame = tk.Frame(root, bg="#282828", pady=5)
url_frame.pack()
url_label = tk.Label(url_frame, text="Video URL:", font=("Roboto", 12), bg="#282828", fg="#ffffff")
url_label.grid(row=0, column=0, padx=(20, 10))
url_entry = tk.Entry(url_frame, width=40, font=("Roboto", 14), bg="#333333", fg="#ffffff", insertbackground="#ffffff")
url_entry.grid(row=0, column=1)

dir_frame = tk.Frame(root, bg="#282828", pady=5)
dir_frame.pack()
dir_label = tk.Label(dir_frame, text="Output Directory:", font=("Roboto", 12), bg="#282828", fg="#ffffff")
dir_label.grid(row=0, column=0, padx=(20, 10))
dir_entry = tk.Entry(dir_frame, width=30, font=("Roboto", 14), bg="#333333", fg="#ffffff", insertbackground="#ffffff")
dir_entry.grid(row=0, column=1)
browse_button = tk.Button(
    dir_frame, text="Browse", command=browse_directory, font=("Roboto", 12),
    bg="#FF0000", fg="#282828", relief="flat", padx=10, pady=2
)
browse_button.grid(row=0, column=2, padx=10)

filename_frame = tk.Frame(root, bg="#282828", pady=5)
filename_frame.pack()
filename_label = tk.Label(filename_frame, text="Output File Name:", font=("Roboto", 12), bg="#282828", fg="#ffffff")
filename_label.grid(row=0, column=0, padx=(20, 10))
filename_entry = tk.Entry(filename_frame, width=40, font=("Roboto", 14), bg="#333333", fg="#ffffff", insertbackground="#ffffff")
filename_entry.grid(row=0, column=1)

resolution_frame = tk.Frame(root, bg="#282828", pady=5)
resolution_frame.pack()
resolution_label = tk.Label(resolution_frame, text="Select Resolution:", font=("Roboto", 12), bg="#282828", fg="#ffffff")
resolution_label.grid(row=0, column=0, padx=(20, 10))

resolution_var = tk.StringVar()
resolution_choices = ["Best", "2160p", "1440p", "1080p", "720p", "480p", "360p", "240p", "144p"]
resolution_menu = ttk.Combobox(resolution_frame, textvariable=resolution_var, values=resolution_choices, font=("Roboto", 12), state="readonly")
resolution_menu.grid(row=0, column=1, padx=10)
resolution_menu.current(0)

audio_var = tk.BooleanVar()
audio_check = tk.Checkbutton(root, text="Download Audio Only", variable=audio_var, font=("Roboto", 12), bg="#282828", fg="#ffffff", selectcolor="#282828")
audio_check.pack(pady=10)

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=400)
progress_bar.pack(pady=20)

download_button = tk.Button(
    root, text="Download", command=start_download, font=("Roboto", 14),
    bg="#FF0000", fg="#282828", relief="flat", padx=10, pady=5
)
download_button.pack(pady=10)

root.mainloop()
