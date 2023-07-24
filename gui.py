import tkinter as tk
import json
import os
from PIL import Image, ImageDraw
from tkinter import filedialog

def run_bots():
    if os.path.exists("altstart.sh"):
        os.system("bash altstart.sh")
    elif os.path.exists("altstart.ps1"):
        os.system("powershell altstart.ps1")
    else:
        os.system("bash start.sh")

def is_valid_image_size(size):
    try:
        width, height = map(int, size.split())
        return 2000 >= width >= 0 and 2000 >= height >= 0
    except ValueError:
        return False

def is_valid_start_coords(coords):
    try:
        x, y = map(int, coords.split())
        return -1500 <= x <= 999 and -100 <= y <= 999
    except ValueError:
        return False

def is_valid_thread_delay(delay):
    try:
        return 0 <= float(delay) <= 5
    except ValueError:
        return False

def generate_black_image(size):
    width, height = map(int, size.split())
    image = Image.new("RGB", (width, height), color="black")
    image.save("black.png")

def import_accounts():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            input_textbox.delete("1.0", tk.END)
            input_textbox.insert("1.0", file.read())

def import_config():
    file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if file_path:
        with open(file_path, "r") as file:
            data = json.load(file)
            input_textbox.delete("1.0", tk.END)
            input_textbox.insert("1.0", "\n".join([f"{k} {v['password']}" for k, v in data["workers"].items()]))

            # Calculate image size from black.png dimensions
            try:
                black_image = Image.open("black.png")
                width, height = black_image.size
                image_size_entry.delete(0, tk.END)
                image_size_entry.insert(0, f"{width} {height}")
            except Exception as e:
                output_label.config(text="Failed to read black.png dimensions.")
                print(e)
                return

            # Populate start coords and thread delay
            start_coords = " ".join(map(str, data["image_start_coords"]))
            start_coords_entry.delete(0, tk.END)
            start_coords_entry.insert(0, start_coords)

            thread_delay = str(data["thread_delay"])
            thread_delay_entry.delete(0, tk.END)
            thread_delay_entry.insert(0, thread_delay)

def generate_json():
    size = image_size_entry.get()
    if not is_valid_image_size(size):
        output_label.config(text="Invalid void size.")
        return
    
    start_coords = start_coords_entry.get()
    if not is_valid_start_coords(start_coords):
        output_label.config(text="Invalid start coordinates.")
        return
    
    delay = thread_delay_entry.get()
    if not is_valid_thread_delay(delay):
        output_label.config(text="Invalid thread delay.")
        return

    generate_black_image(size)

    input_text = input_textbox.get("1.0", tk.END).strip()
    lines = input_text.split("\n")
    
    workers = {}
    for line in lines:
        if line:
            username, password = line.split()
            workers[username] = {
                "password": password,
                "start_coords": [0, len(workers)]
            }
    
    data = {
        "image_path": "black.png",
        "image_start_coords": list(map(int, start_coords.split())),
        "thread_delay": float(delay),
        "workers": workers
    }

    with open("config.json", "w") as f:
        json.dump(data, f, indent=4)

    if os.path.exists("after_generate.sh"):
        os.system("bash after_generate.sh")
    elif os.path.exists("after_generate.ps1"):
        os.system("powershell after_generate.ps1")

root = tk.Tk()
root.title("2b2t Placer GUI")

watermark_label = tk.Label(root, text="created by The Swarm dev team")
watermark_label.pack(pady=5)

input_label = tk.Label(root, text="Paste accounts (one per line):")
input_label.pack(pady=5)

input_textbox = tk.Text(root, height=40, width=65)
input_textbox.insert("1.0", "exampleusername hunter2")
input_textbox.pack(padx=10, pady=5)

# Image Size
image_size_label = tk.Label(root, text="Void size (e.g 30 30):")
image_size_label.pack(pady=5)
image_size_entry = tk.Entry(root)
image_size_entry.pack(pady=5)

# Start Coords
start_coords_label = tk.Label(root, text="Start Coords (Top left corner):")
start_coords_label.pack(pady=5)
start_coords_entry = tk.Entry(root)
start_coords_entry.pack(pady=5)

# Thread Delay
thread_delay_label = tk.Label(root, text="Thread Delay (0-5 seconds):")
thread_delay_label.pack(pady=5)
thread_delay_entry = tk.Entry(root)
thread_delay_entry.pack(pady=5)

output_label = tk.Label(root, text="")
output_label.pack()

# Import Accounts Button
import_accounts_button = tk.Button(root, text="Import accounts", command=import_accounts)
import_accounts_button.pack(side=tk.LEFT, padx=5)

# Generate JSON Button
submit_button = tk.Button(root, text="Generate jason", command=generate_json)
submit_button.pack(side=tk.LEFT, pady=10, padx=5)

# Import Config Button
import_config_button = tk.Button(root, text="Import config.json", command=import_config)
import_config_button.pack(side=tk.LEFT, padx=5)

# Run button
run_button = tk.Button(root, text="START 'EM", command=run_bots, fg="red")
run_button.pack(side=tk.LEFT, padx=5)

root.mainloop()

