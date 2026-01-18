import tkinter as tk
from tkinter import filedialog
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import threading
import pygame
import os
from mutagen.mp3 import MP3
from PIL import Image, ImageTk

# ---------- Global State ----------
is_paused = False
audio_started = threading.Event()
word_delay_ms = 180
current_highlight = None
words = []
word_index = 0
bg_photo = None

# ---------- Themes ----------
THEMES = {
    "cozy": {
        "bg": "#2b1f1a",
        "fg": "#f5e6d3",
        "highlight": "#d9a441"
    },
    "sunny": {
        "bg": "#fff7cc",
        "fg": "#333333",
        "highlight": "#ffd966"
    },
    "rainy": {
        "bg": "#1e1e2e",
        "fg": "#dcdcdc",
        "highlight": "#5dade2"
    },
    "love": {
        "bg": "#3a1f2b",
        "fg": "#ffd6e8",
        "highlight": "#ff6fa5"
    },
    "sad": {
        "bg": "#1a1a1a",
        "fg": "#b0b0b0",
        "highlight": "#6c7a89"
    }
}

# ---------- Setup ----------
load_dotenv()
client = ElevenLabs(api_key=os.getenv("API_KEY"))
pygame.mixer.init()

# ---------- Audio ----------
def generate_and_play_audio(text):
    global word_delay_ms

    audio = client.text_to_speech.convert(
        text=text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

    with open("output.mp3", "wb") as f:
        for chunk in audio:
            f.write(chunk)

    mp3 = MP3("output.mp3")
    duration = mp3.info.length

    if len(words) > 0:
        word_delay_ms = int((duration / len(words)) * 1000)

    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()
    audio_started.set()

# ---------- File Upload ----------
def upload_file():
    global words, word_index, is_paused
    audio_started.clear()
    is_paused = False

    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )

    if not file_path:
        return

    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    words = text.split()
    word_index = 0
    text_box.delete("1.0", tk.END)

    status_label.config(text="Generating audio... 🤖")

    threading.Thread(
        target=generate_and_play_audio,
        args=(text,),
        daemon=True
    ).start()

    check_audio_started()

def check_audio_started():
    if audio_started.is_set():
        status_label.config(text="AI is speaking 🎧")
        speak_words()
    else:
        root.after(50, check_audio_started)

# ---------- Text Highlight ----------
def speak_words():
    global word_index, current_highlight

    if is_paused:
        return

    if word_index >= len(words):
        status_label.config(text="AI finished speaking ✔️")
        return

    start = text_box.index(tk.END)
    text_box.insert(tk.END, words[word_index] + " ")
    end = text_box.index(tk.END)

    if current_highlight:
        text_box.tag_remove("highlight", current_highlight[0], current_highlight[1])

    text_box.tag_add("highlight", start, end)
    current_theme = current_theme_name.get()
    text_box.tag_config(
        "highlight",
        background=THEMES[current_theme]["highlight"],
        foreground=THEMES[current_theme]["fg"]
    )

    current_highlight = (start, end)
    text_box.see(tk.END)

    word_index += 1
    root.after(word_delay_ms, speak_words)

# ---------- Controls ----------
def start_audio():
    global is_paused
    if pygame.mixer.music.get_busy() and is_paused:
        pygame.mixer.music.unpause()
        is_paused = False
        status_label.config(text="AI speaking ▶️")
        speak_words()

def pause_audio():
    global is_paused
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        is_paused = True
        status_label.config(text="Paused ⏸️")

# ---------- Tkinter UI ----------
root = tk.Tk()
root.title("AI Reader")
root.geometry("1200x1200")

# Track current theme
current_theme_name = tk.StringVar(value="cozy")

# ---------- Background ----------
bg_label = tk.Label(root)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
bg_label.lower()

def set_background(image_path, theme_name):
    global bg_photo
    current_theme_name.set(theme_name)

    img = Image.open(image_path)
    img = img.resize((root.winfo_width(), root.winfo_height()), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(img)
    bg_label.config(image=bg_photo)

    theme = THEMES[theme_name]
    text_box.config(
        bg=theme["bg"],
        fg=theme["fg"],
        insertbackground=theme["fg"]
    )
    text_box.tag_config(
        "highlight",
        background=theme["highlight"],
        foreground=theme["fg"]
    )

# ---------- Widgets ----------
upload_btn = tk.Button(root, text="Upload File", command=upload_file)
upload_btn.pack(pady=10)

controls = tk.Frame(root)
controls.pack(pady=10)

tk.Button(controls, text="▶️ Start / Resume", command=start_audio).pack(side="left", padx=5)
tk.Button(controls, text="⏸️ Pause", command=pause_audio).pack(side="left", padx=5)

tk.Button(
    controls, text="Cozy",
    command=lambda: set_background("images/bruh.jpg", "cozy")
).pack(side="left", padx=5)

tk.Button(
    controls, text="Sunny",
    command=lambda: set_background("images/sunny.jpeg", "sunny")
).pack(side="left", padx=5)

tk.Button(
    controls, text="Rainy",
    command=lambda: set_background("images/rainy.jpeg", "rainy")
).pack(side="left", padx=5)

tk.Button(
    controls, text="Love",
    command=lambda: set_background("images/love.jpeg", "love")
).pack(side="left", padx=5)

tk.Button(
    controls, text="Sad",
    command=lambda: set_background("images/sad.jpeg", "sad")
).pack(side="left", padx=5)

status_label = tk.Label(root, text="No file selected")
status_label.pack()

text_box = tk.Text(root, wrap="word", height=5)
text_box.pack(padx=250, pady=30)

# ---------- Default Theme ----------
set_background("images/bruh.jpg", "cozy")

# ---------- Start ----------
root.mainloop()
