import pyautogui
import random
import tkinter as tk
import os
from PIL import Image

x = 1400
cycle = 0
check = 1
idle_num = [1, 2, 3, 4]
walk_left = [5, 6]
walk_right = [7, 8]
idle_num1 = [9, 10]
event_number = random.choice(idle_num + walk_left + walk_right + idle_num1)

impath = os.path.abspath('img') + '\\'

def get_gif_size(filename):
    with Image.open(filename) as img:
        width, height = img.size
    return width, height

def event(cycle, check, event_number, x):
    if event_number in idle_num:
        check = 0
        print('idle')
    elif event_number in walk_left:
        check = 1
        print('left')
    elif event_number in walk_right:
        check = 2
        print('right')
    elif event_number in idle_num1:
        check = 3
        print('idle-1')
    window.after(100, update, cycle, check, event_number, x)


# Making GIF work
def gif_work(cycle, frames, event_number, first_num, last_num):
    if cycle < len(frames) - 1:
        cycle += 1
    else:
        cycle = 0
        event_number = random.randrange(first_num, last_num + 1, 1)
    return cycle, event_number


def update(cycle, check, event_number, x):
    global label
    try:
        # Idle
        if check == 0:
            frame = idle[cycle]
            cycle, event_number = gif_work(cycle, idle, event_number, 1, 10)

        # Walk toward left
        elif check == 1:
            frame = walk_positive[cycle]
            cycle, event_number = gif_work(cycle, walk_positive, event_number, 1, 10)
            x -= 3
            if x <= 0:
                check = 2
                event_number = random.choice(walk_right)

        # Walk towards right
        elif check == 2:
            frame = walk_negative[cycle]
            cycle, event_number = gif_work(cycle, walk_negative, event_number, 1, 10)
            x += 3
            if x >= screen_width - frame.width():
                check = 1
                event_number = random.choice(walk_left)

        # Idle1
        elif check == 3:
            frame = idle1[cycle]
            cycle, event_number = gif_work(cycle, idle, event_number, 1, 10)

        x = max(0, min(x, screen_width - frame.width()))
        window.geometry(f'{frame.width()}x{frame.height()}+{x}+{screen_height - frame.height() - taskbar_height}')
        label.configure(image=frame)
        window.after(1, event, cycle, check, event_number, x)
    except Exception as e:
        print("Error in update function:", e)


window = tk.Tk()

try:
    idle = [tk.PhotoImage(file=impath + 'idle21.gif', format='gif -index %i' % (i)) for i in range(21)]  # idle gif
    walk_positive = [tk.PhotoImage(file=impath + 'walk-12.gif', format='gif -index %i' % (i)) for i in
                     range(12)]  # walk to left gif
    walk_negative = [tk.PhotoImage(file=impath + 'walk+12.gif', format='gif -index %i' % (i)) for i in
                     range(12)]  # walk to right gif
    idle1 = [tk.PhotoImage(file=impath + 'idle-21.gif', format='gif -index %i' % (i)) for i in range(21)]  # idle gif
except Exception as e:
    print("Error loading GIFs:", e)

window.config(highlightbackground='black')
label = tk.Label(window, bd=0, bg='black')
window.overrideredirect(True)
window.wm_attributes('-transparentcolor', 'black')
window.wm_attributes('-topmost', True)
label.pack()

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
taskbar_height = 45

try:
    gif_width, gif_height = get_gif_size(impath + 'idle21.gif')
except Exception as e:
    print("Error getting GIF size:", e)
    gif_width, gif_height = 200, 200

x = (screen_width - 300) - (gif_width // 2)
y = screen_height - gif_height - taskbar_height
window.geometry(f'{gif_width}x{gif_height}+{x}+{y}')

window.after(1, update, cycle, check, event_number, x)
window.mainloop()

