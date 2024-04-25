import asyncio
import os
import tkinter as tk
import random
from PIL import Image, ImageTk


BASE_PATH = os.path.join('.', 'codefest-2024', 'KerfusTutor', 'KerfusImg')

TTS_FILE_PATH = os.path.join(os.getcwd(), "output0.mp3")

KerfusBigEyesClosed_IMAGE_PATH = os.path.join(BASE_PATH, "KerfusBigEyesClosed.png")
KerfusBigEyesOpen_IMAGE_PATH = os.path.join(BASE_PATH, "KerfusBigEyesOpen.png")
KerfusBlink_IMAGE_PATH = os.path.join(BASE_PATH, "KerfusBlink.png")
KerfusFilled_IMAGE_PATH = os.path.join(BASE_PATH, "KerfusFilled.png")
KerfusLookL_IMAGE_PATH = os.path.join(BASE_PATH, "KerfusLookL.png")
KerfusLookR_IMAGE_PATH = os.path.join(BASE_PATH, "KerfusLookR.png")
KerfusTalkClosed_IMAGE_PATH = os.path.join(BASE_PATH, "KerfusTalkClosed.png")
KerfusTalkOpen_IMAGE_PATH = os.path.join(BASE_PATH, "KerfusTalkOpen.png")
KerfusWinkR_IMAGE_PATH = os.path.join(BASE_PATH, "KerfusWinkR.png")

def reset(root, image_label, screen_width, screen_height, tts_time=None):
    root.after(1000, lambda: update_image(image_label, KerfusFilled_IMAGE_PATH, screen_width, screen_height))

# IDLE
def look_around(root, image_label, screen_width, screen_height, tts_time=None):
    root.after(0, lambda: update_image(image_label, KerfusLookL_IMAGE_PATH, screen_width, screen_height))
    root.after(1000, lambda: update_image(image_label, KerfusLookR_IMAGE_PATH, screen_width, screen_height))

def blink_and_open_eyes(root, image_label, screen_width, screen_height, tts_time=None):
    root.after(0, lambda: update_image(image_label, KerfusBlink_IMAGE_PATH, screen_width, screen_height))
    root.after(1000, lambda: update_image(image_label, KerfusBigEyesOpen_IMAGE_PATH, screen_width, screen_height))

def wink_and_smile(root, image_label, screen_width, screen_height, tts_time=None):
    root.after(0, lambda: update_image(image_label, KerfusWinkR_IMAGE_PATH, screen_width, screen_height))
    root.after(1000, lambda: update_image(image_label, KerfusFilled_IMAGE_PATH, screen_width, screen_height))

# Completion
async def talk_and_wink(root, image_label, screen_width, screen_height, tts_time=1):
    root.after(0, lambda: update_image(image_label, KerfusTalkOpen_IMAGE_PATH, screen_width, screen_height))
    await asyncio.sleep(tts_time)
    root.after(0, lambda: update_image(image_label, KerfusWinkR_IMAGE_PATH, screen_width, screen_height))
    
async def talk_and_open_eyes(root, image_label, screen_width, screen_height, tts_time=1):
    root.after(0, lambda: update_image(image_label, KerfusTalkOpen_IMAGE_PATH, screen_width, screen_height))
    await asyncio.sleep(tts_time)
    root.after(0, lambda: update_image(image_label, KerfusBigEyesOpen_IMAGE_PATH, screen_width, screen_height))

# Choice Funcs
IDLE_FUNCS = (look_around, blink_and_open_eyes, wink_and_smile)
COMPLETION_FUNCS = (talk_and_wink, talk_and_open_eyes)

def random_expression_from_set(root, image_label, screen_width, screen_height, expression_set, tts_time=0):
    global IDLE_FUNCS, COMPLETION_FUNCS
    selected_func = random.choice(expression_set)
    selected_func(root, image_label, screen_width, screen_height, tts_time)

async def async_random_expression_from_set(root, image_label, screen_width, screen_height, expression_set, tts_time=0):
    global IDLE_FUNCS, COMPLETION_FUNCS
    selected_func = random.choice(expression_set)
    await selected_func(root, image_label, screen_width, screen_height, tts_time)


OLD_IMAGE_PATH = KerfusFilled_IMAGE_PATH

def update_image(image_label, new_image_path, screen_width, screen_height):
    global OLD_IMAGE_PATH
    new_img = Image.open(new_image_path)
    new_img.thumbnail((screen_width, screen_height), Image.Resampling.LANCZOS)

    if hasattr(image_label, 'image'):
        previous_img = Image.open(OLD_IMAGE_PATH)
        previous_img.thumbnail((screen_width, screen_height), Image.Resampling.LANCZOS)
        for alpha in [x / 10.0 for x in range(10)]:
            blended_img = Image.blend(previous_img, new_img, alpha)
            blended_img_tk = ImageTk.PhotoImage(blended_img)
            image_label.config(image=blended_img_tk, background="black")
            image_label.image = blended_img_tk
            image_label.update()
            image_label.after(1)
    
    img_tk = ImageTk.PhotoImage(new_img)
    image_label.config(image=img_tk, background="black")
    image_label.image = img_tk
    OLD_IMAGE_PATH = KerfusFilled_IMAGE_PATH = new_image_path



def create_gui():
    root = tk.Tk()
    root.title("Kerfus Tutor")
    root.configure(bg="black")
    root.attributes("-fullscreen", True)
    root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    img = Image.open(KerfusFilled_IMAGE_PATH)
    img.thumbnail((screen_width, screen_height), Image.Resampling.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)
    image_label = tk.Label(root, image=img_tk, bg="black")
    image_label.image = img_tk
    image_label.pack(expand=True, fill=tk.BOTH)
    return root, image_label, screen_width, screen_height
