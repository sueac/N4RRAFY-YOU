import tkinter as tk
import uuid
from tkinter import filedialog, messagebox
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import pygame
import os
import threading
from mutagen.mp3 import MP3

from test1 import QuoteExtraction
from Voices import VOICE_OPTIONS


# ---------- Setup ----------
load_dotenv()
client = ElevenLabs(api_key=os.getenv("API_KEY"))
pygame.mixer.init()

quotes = []
names = []
voice_map = {}
current_quote_index = 0

words = []
word_index = 0
word_delay_ms = 150
is_paused = False


# ---------- AUDIO THREAD ----------
def generate_audio(text, v_id):
    filename = f"audio_{uuid.uuid4().hex}.mp3"

    audio = client.text_to_speech.convert(
        text=text,
        voice_id=v_id,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

    with open(filename, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    return filename



# ---------- UI AUDIO PLAY ----------
def play_audio_ui(speaker, text, audio_file):
    global words, word_index, word_delay_ms

    text_box.delete("1.0", tk.END)
    words = text.split()
    word_index = 0

    mp3 = MP3(audio_file)
    duration = mp3.info.length
    word_delay_ms = int((duration / max(len(words), 1)) * 1000)

    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    status_label.config(text=f"{speaker} speaking 🎙️")
    speak_words()
    monitor_audio(audio_file)



def run_quote(speaker, text):
    v_id = voice_map.get(speaker, voice_map["Narrator"])

    def task():
        audio_file = generate_audio(text, v_id)
        root.after(0, lambda: play_audio_ui(speaker, text, audio_file))

    threading.Thread(target=task, daemon=True).start()
S


# ---------- SEQUENCE ----------
def monitor_audio():
    if pygame.mixer.music.get_busy():
        root.after(100, monitor_audio)
    else:
        next_quote()


def next_quote():
    global current_quote_index

    current_quote_index += 1

    if current_quote_index < len(quotes):
        speaker, quote = quotes[current_quote_index]
        run_quote(speaker, quote)
    else:
        status_label.config(text="Finished ✔️")


# ---------- TEXT HIGHLIGHT ----------
def speak_words():
    global word_index

    if is_paused or word_index >= len(words):
        return

    start = text_box.index(tk.END)
    text_box.insert(tk.END, words[word_index] + " ")
    end = text_box.index(tk.END)

    text_box.tag_add("highlight", start, end)
    text_box.tag_config("highlight", background="yellow")

    word_index += 1
    root.after(word_delay_ms, speak_words)


# ---------- FILE UPLOAD ----------
def upload_file():
    global quotes, names, current_quote_index

    file_path = filedialog.askopenfilename(
        filetypes=[("Text files", "*.txt")]
    )

    if not file_path:
        return

    quotes, names = QuoteExtraction(file_path)

    if not quotes:
        messagebox.showerror(
            "No Quotes Found",
            "No dialogue quotes were detected."
        )
        return

    if "Narrator" not in names:
        names.append("Narrator")

    current_quote_index = 0
    status_label.config(text="File loaded ✔️ Assign voices")
    open_voice_window()


# ---------- VOICE ASSIGNMENT ----------
def open_voice_window():
    window = tk.Toplevel(root)
    window.title("Assign Voices")
    window.geometry("400x500")

    dropdowns = {}

    for name in names:
        frame = tk.Frame(window)
        frame.pack(pady=5)

        tk.Label(frame, text=name, width=12).pack(side="left")
        var = tk.StringVar(value=list(VOICE_OPTIONS.keys())[0])
        tk.OptionMenu(frame, var, *VOICE_OPTIONS.keys()).pack(side="left")
        dropdowns[name] = var

    def confirm():
        for name, var in dropdowns.items():
            voice_map[name] = VOICE_OPTIONS[var.get()]
        window.destroy()
        start_reading()

    tk.Button(window, text="Start Reading", command=confirm).pack(pady=20)


# ---------- CONTROLS ----------
def start_reading():
    if not quotes:
        return

    speaker, quote = quotes[0]
    run_quote(speaker, quote)


def pause_audio():
    global is_paused
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        is_paused = True


def resume_audio():
    global is_paused
    if is_paused:
        pygame.mixer.music.unpause()
        is_paused = False
        speak_words()


# ---------- UI ----------
root = tk.Tk()
root.title("AI Multi-Voice Reader")
root.geometry("900x700")

tk.Button(root, text="Upload Book", command=upload_file).pack(pady=10)

controls = tk.Frame(root)
controls.pack()

tk.Button(controls, text="▶ Resume", command=resume_audio).pack(side="left", padx=5)
tk.Button(controls, text="⏸ Pause", command=pause_audio).pack(side="left", padx=5)

status_label = tk.Label(root, text="No file loaded")
status_label.pack(pady=5)

text_box = tk.Text(root, wrap="word", height=20)
text_box.pack(expand=True, fill="both", padx=10, pady=10)

root.mainloop()


