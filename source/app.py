import os
import yt_dlp
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import sys

def download_content(url, output_directory, output_filename, platform, resolution, audio_only=False):
    output_path = os.path.join(output_directory, f"{output_filename}.%(ext)s")
    
    ydl_opts = {
        'outtmpl': output_path,
        'progress_hooks': [hook],
        'quiet': True,
        'no_warnings': True,
    }

    if audio_only:
        ydl_opts.update({
            'format': 'bestaudio/best',
        })
    else:
        if resolution == "Best":
            ydl_opts['format'] = 'best'
        else:
            # Try the requested resolution first, then fallback
            requested_height = int(resolution[:-1])
            ydl_opts['format'] = f'best[height<={requested_height}]'
            ydl_opts['format_sort'] = [f'res:{requested_height}', 'res']

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # First check available formats without downloading
            info_dict = ydl.extract_info(url, download=False)
            
            if not audio_only and resolution != "Best":
                available_heights = set()
                if 'formats' in info_dict:
                    for f in info_dict['formats']:
                        if f.get('height'):
                            available_heights.add(f['height'])
                
                if available_heights:
                    requested_height = int(resolution[:-1])
                    if requested_height not in available_heights:
                        closest = min(available_heights, key=lambda x: abs(x - requested_height))
                        messagebox.showinfo(
                            "Info", 
                            f"{resolution} not available. Downloading at {closest}p instead."
                        )
            
            # Proceed with download
            ydl.download([url])
            messagebox.showinfo("Success", "Download completed successfully!")
            open_directory(output_directory)
    except yt_dlp.utils.DownloadError as e:
        if "Requested format is not available" in str(e):
            # Fallback to best available quality
            ydl_opts['format'] = 'best'
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                    messagebox.showinfo("Success", "Download completed with best available quality!")
                    open_directory(output_directory)
            except Exception as fallback_error:
                messagebox.showerror("Error", f"Fallback failed: {fallback_error}")
        else:
            messagebox.showerror("Error", f"Download failed: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def hook(d):
    if d['status'] == 'downloading':
        percent = d.get('downloaded_bytes', 0) / d.get('total_bytes', 1) * 100
        progress_var.set(percent)
        root.update_idletasks()
    elif d['status'] == 'finished':
        progress_var.set(100)

def open_directory(directory):
    if os.path.exists(directory):
        if os.name == 'nt':
            os.startfile(directory)
        elif os.name == 'posix':
            subprocess.Popen(['open', directory] if sys.platform == 'darwin' else ['xdg-open', directory])
    else:
        messagebox.showwarning("Warning", f"Directory not found: {directory}")

def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        dir_entry.delete(0, tk.END)
        dir_entry.insert(0, directory)

def start_download():
    url = url_entry.get().strip()
    output_directory = dir_entry.get().strip()
    output_filename = filename_entry.get().strip()
    platform = platform_var.get()
    audio_only = audio_var.get()
    resolution = resolution_var.get()

    if not url:
        messagebox.showwarning("Warning", "Please enter a URL.")
        return
    if not output_directory:
        messagebox.showwarning("Warning", "Please select an output directory.")
        return
    if not output_filename:
        messagebox.showwarning("Warning", "Please enter an output filename.")
        return

    # Reset progress bar
    progress_var.set(0)
    
    # Start download in a new thread to prevent UI freezing
    import threading
    threading.Thread(
        target=download_content,
        args=(url, output_directory, output_filename, platform, resolution, audio_only),
        daemon=True
    ).start()

# Create main window
root = tk.Tk()
root.title("Social Media Video Downloader")
icon_path = os.path.join(os.path.dirname(__file__), "Logo.ico")
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)
else:
    print("Icon not found:", icon_path)
root.geometry("650x800")
root.configure(bg="#282828")

# Add copyright label
copyright_label = tk.Label(
    root, text="© DrJunkHoofd", font=("Roboto", 10), 
    bg="#282828", fg="#ffffff", anchor="w"
)
copyright_label.pack(pady=(5, 10), padx=20)

# Add title
title_label = tk.Label(
    root, text="Social Media Video Downloader", font=("Roboto", 30),
    bg="#282828", fg="#FF0000", height=2
)
title_label.pack()

# Platform selection
platform_frame = tk.Frame(root, bg="#282828")
platform_frame.pack(pady=10)
platform_label = tk.Label(
    platform_frame, text="Select Platform:", 
    font=("Roboto", 12), bg="#282828", fg="#ffffff"
)
platform_label.grid(row=0, column=0, padx=10)

platform_var = tk.StringVar()
platform_choices = ["YouTube", "Twitter", "Instagram", "TikTok", "Reddit", "Facebook"]
platform_menu = ttk.Combobox(
    platform_frame, textvariable=platform_var, 
    values=platform_choices, font=("Roboto", 12), 
    state="readonly"
)
platform_menu.grid(row=0, column=1, padx=10)
platform_menu.current(0)

# URL entry
url_frame = tk.Frame(root, bg="#282828", pady=5)
url_frame.pack()
url_label = tk.Label(
    url_frame, text="Video URL:", 
    font=("Roboto", 12), bg="#282828", fg="#ffffff"
)
url_label.grid(row=0, column=0, padx=(20, 10))
url_entry = tk.Entry(
    url_frame, width=40, font=("Roboto", 14), 
    bg="#333333", fg="#ffffff", insertbackground="#ffffff"
)
url_entry.grid(row=0, column=1)

# Directory selection
dir_frame = tk.Frame(root, bg="#282828", pady=5)
dir_frame.pack()
dir_label = tk.Label(
    dir_frame, text="Output Directory:", 
    font=("Roboto", 12), bg="#282828", fg="#ffffff"
)
dir_label.grid(row=0, column=0, padx=(20, 10))
dir_entry = tk.Entry(
    dir_frame, width=30, font=("Roboto", 14), 
    bg="#333333", fg="#ffffff", insertbackground="#ffffff"
)
dir_entry.grid(row=0, column=1)
browse_button = tk.Button(
    dir_frame, text="Browse", command=browse_directory, 
    font=("Roboto", 12), bg="#FF0000", fg="#282828", 
    relief="flat", padx=10, pady=2
)
browse_button.grid(row=0, column=2, padx=10)

# Filename entry
filename_frame = tk.Frame(root, bg="#282828", pady=5)
filename_frame.pack()
filename_label = tk.Label(
    filename_frame, text="Output File Name:", 
    font=("Roboto", 12), bg="#282828", fg="#ffffff"
)
filename_label.grid(row=0, column=0, padx=(20, 10))
filename_entry = tk.Entry(
    filename_frame, width=40, font=("Roboto", 14), 
    bg="#333333", fg="#ffffff", insertbackground="#ffffff"
)
filename_entry.grid(row=0, column=1)

# Resolution selection
resolution_frame = tk.Frame(root, bg="#282828", pady=5)
resolution_frame.pack()
resolution_label = tk.Label(
    resolution_frame, text="Select Resolution:", 
    font=("Roboto", 12), bg="#282828", fg="#ffffff"
)
resolution_label.grid(row=0, column=0, padx=(20, 10))

resolution_var = tk.StringVar()
resolution_choices = ["Best", "2160p", "1440p", "1080p", "720p", "480p", "360p", "240p", "144p"]
resolution_menu = ttk.Combobox(
    resolution_frame, textvariable=resolution_var, 
    values=resolution_choices, font=("Roboto", 12), 
    state="readonly"
)
resolution_menu.grid(row=0, column=1, padx=10)
resolution_menu.current(0)

# Audio only checkbox
audio_var = tk.BooleanVar()
audio_check = tk.Checkbutton(
    root, text="Download Audio Only", variable=audio_var, 
    font=("Roboto", 12), bg="#282828", fg="#ffffff", 
    selectcolor="#282828", activebackground="#282828"
)
audio_check.pack(pady=10)

# Progress bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(
    root, variable=progress_var, 
    maximum=100, length=400
)
progress_bar.pack(pady=20)

# Download button
download_button = tk.Button(
    root, text="Download", command=start_download, 
    font=("Roboto", 14), bg="#FF0000", fg="#282828", 
    relief="flat", padx=10, pady=5
)
download_button.pack(pady=10)

# Run the application
root.mainloop()