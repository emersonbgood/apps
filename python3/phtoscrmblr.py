import os
import glob
import time
import random
import sys
import re
import tkinter as tk
from PIL import Image, ImageTk

# Configuration
IMAGE_PATH = os.path.expanduser("~/Scripts/secrets/DCIM/*/*")
WINDOW_SIZE = 300
SPAWN_INTERVAL = 0.05
GLOBAL_TIMER = 30000 

class PhotoScrambler:
    def __init__(self, args):
        self.root = tk.Tk()
        self.root.withdraw()
        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()
        self.windows_count = 0
        
        arg_str = "".join(args)
        self.stay_mode = 's' in arg_str
        
        # Logic for L/R/LR
        has_l = 'l' in arg_str
        has_r = 'r' in arg_str
        
        if (has_l and has_r) or (not has_l and not has_r):
            self.x_range = (0, self.screen_w)
        elif has_l:
            self.x_range = (0, self.screen_w // 2)
        else: # has_r
            self.x_range = (self.screen_w // 2, self.screen_w)
        
        # Custom Range Regex - Supports -c[0,100] or -c=[0,100]
        self.custom_x = re.search(r'-c=?\[(\d+),(\d+)\]', arg_str)
        self.custom_y = re.search(r'-C=?\[(\d+),(\d+)\]', arg_str)

    def clamp(self, value, min_val, max_val):
        return max(min_val, min(value, max_val))

    def on_close(self, window):
        try:
            window.destroy()
            self.windows_count -= 1
            # Kill script if last window closed (always check this)
            if self.windows_count <= 0:
                self.root.quit()
        except: pass

    def spawn_image(self, img_path):
        try:
            self.windows_count += 1
            window = tk.Toplevel(self.root)
            window.overrideredirect(True)
            window.attributes("-topmost", True)
            
            img = Image.open(img_path)
            img.thumbnail((WINDOW_SIZE, WINDOW_SIZE))
            photo = ImageTk.PhotoImage(img)
            
            label = tk.Label(window, image=photo, bg='black')
            label.image = photo 
            label.pack()

            # Always allow click-to-close
            label.bind("<Button-1>", lambda e: self.on_close(window))

            # X Position
            if self.custom_x:
                x1, x2 = map(int, self.custom_x.groups())
                x1 = self.clamp(x1, 0, self.screen_w - WINDOW_SIZE)
                x2 = self.clamp(x2, x1, self.screen_w)
                rand_x = random.randint(x1, max(x1, x2 - WINDOW_SIZE))
            else:
                rand_x = random.randint(self.x_range[0], max(self.x_range[0], self.x_range[1] - WINDOW_SIZE))

            # Y Position
            if self.custom_y:
                y1, y2 = map(int, self.custom_y.groups())
                y1 = self.clamp(y1, 0, self.screen_h - WINDOW_SIZE)
                y2 = self.clamp(y2, y1, self.screen_h)
                rand_y = random.randint(y1, max(y1, y2 - WINDOW_SIZE))
            else:
                rand_y = random.randint(0, max(0, self.screen_h - WINDOW_SIZE))

            window.geometry(f"+{rand_x}+{rand_y}")
            window.update()
        except Exception as e:
            self.windows_count -= 1

    def run(self):
        images = glob.glob(IMAGE_PATH)
        if not images: 
            self.root.quit(); return

        for img in images:
            self.spawn_image(img)
            time.sleep(SPAWN_INTERVAL)
        
        # 30s auto-kill only if NOT in stay mode
        if not self.stay_mode:
            self.root.after(GLOBAL_TIMER, self.root.quit)
        
        self.root.mainloop()

if __name__ == "__main__":
    # Usage: python3 phtoscrmblr.py -lrs "-c[0,500]"
    scrambler = PhotoScrambler(sys.argv[1:])
    scrambler.run()
