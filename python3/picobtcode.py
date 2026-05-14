import serial
import subprocess
import os
import glob
import time
import random # <--- Added for random positioning
import tkinter as tk
from PIL import Image, ImageTk

PORT = '/dev/rfcomm0'
BAUD = 9600

# Initialize hidden root engine
root = tk.Tk()
root.withdraw()

# Get your screen's width and height for random placement
SCREEN_WIDTH = root.winfo_screenwidth()
SCREEN_HEIGHT = root.winfo_screenheight()

def show_borderless_image(img_path, index):
    """Creates a borderless window at a random screen location."""
    try:
        window = tk.Toplevel(root)
        window.overrideredirect(True) 
        
        img = Image.open(img_path)
        # Resizing to 300x300 so more can fit randomly
        img.thumbnail((300, 300))
        photo = ImageTk.PhotoImage(img)
        
        label = tk.Label(window, image=photo, bg='black')
        label.image = photo 
        label.pack()
        
        # --- RANDOM POSITIONING ---
        # We subtract 300 so the window doesn't go off the edge
        rand_x = random.randint(0, max(0, SCREEN_WIDTH - 300))
        rand_y = random.randint(0, max(0, SCREEN_HEIGHT - 300))
        
        window.geometry(f"+{rand_x}+{rand_y}")
        
        # Auto-destroy after 5 seconds
        window.after(5000, window.destroy)
        window.update()
    except Exception as e:
        print(f"Error drawing window: {e}")

def expose_data():
    # 1. Show the "Exposing" warning
    cmd = 'zenity --info --title="CODE HAS BEAN GUESSED" --text="exposing secret data"'
    subprocess.run(cmd, shell=True)

    # 2. Find images
    path = os.path.expanduser("~/Scripts/secrets/DCIM/*/*")
    images = glob.glob(path)

    # 3. Rapidly pop windows in random spots
    for i, img in enumerate(images):
        show_borderless_image(img, i)
        time.sleep(0.05)

print(f"Listening on {PORT}...")

try:
    with serial.Serial(PORT, BAUD, timeout=0.1) as ser:
        while True:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            
            if line:
                print(f"Pico: {line}")
                
                if "ALERT:WRONG_CODE:" in line:
                    new_code = line.split(":")[-1]
                    msg = f"someone entered an incorrect code, new code is: {new_code}"
                    zenity_cmd = f'zenity --info --title="INVALID CODE" --text="{msg}"'
                    subprocess.Popen(zenity_cmd, shell=True)

                elif "STATUS:ACCESS_GRANTED" in line:
                    expose_data()
            
            root.update()
                
except Exception as e:
    print(f"Critical Serial Error: {e}")
