import tkinter as tk
from tkinter import filedialog
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import threading
import pygame
import os
from mutagen.mp3 import MP3


is_paused = False
audio_started = threading.Event()
word_delay_ms = 180
current_highlight = None

# ---------- Setup ----------
load_dotenv()
client = ElevenLabs(api_key=os.getenv("API_KEY"))


pygame.mixer.init()


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
    duration = mp3.info.length  # seconds


    word_delay_ms = int((duration / len(words)) * 1000)


    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()
    audio_started.set()




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






def speak_words():
    global word_index, current_highlight


    if is_paused:
        return  # ⛔ stop advancing text while paused


    if word_index >= len(words):
        status_label.config(text="AI finished speaking ✔️")
        return


    start = text_box.index(tk.END)
    text_box.insert(tk.END, words[word_index] + " ")
    end = text_box.index(tk.END)


    if current_highlight:
        text_box.tag_remove("highlight", current_highlight[0], current_highlight[1])


    text_box.tag_add("highlight", start, end)
    text_box.tag_config("highlight", background="yellow")


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


upload_btn = tk.Button(root, text="Upload File", command=upload_file)
upload_btn.pack(pady=10)


controls = tk.Frame(root)
controls.pack(pady=10)


start_btn = tk.Button(controls, text="▶️ Start / Resume", command=start_audio)
start_btn.pack(side="left", padx=5)


pause_btn = tk.Button(controls, text="⏸️ Pause", command=pause_audio)
pause_btn.pack(side="left", padx=5)


status_label = tk.Label(root, text="No file selected")
status_label.pack()


text_box = tk.Text(root, wrap="word", height=20)
text_box.pack(padx=10, pady=10, fill="both", expand=True)


words = []
word_index = 0


root.mainloop()
