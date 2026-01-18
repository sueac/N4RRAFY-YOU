import tkinter as tk
import subprocess
import sys
import os

VOICE_OPTIONS = {
    "Calm Male": "j9t3Yvh3vBwrHcn0bucs",
    "Warm Female": "s3gcxx3ITgo2NhnGkx27",
    "Storyteller": "cMrQcbcgpMlTZoEWG4zw",
    "Horror": "lwYLo90MsFbMuBdTlEPh"
}


def launch_app():
    selected_voice_name = voice_var.get()
    selected_voice_id = VOICE_OPTIONS[selected_voice_name]

    root.destroy()

    subprocess.Popen([
        sys.executable,
        "app.py",
        selected_voice_id
    ])


root = tk.Tk()
root.title("AI Narration App")
root.geometry("600x400")
root.configure(bg="#1e1e1e")

title = tk.Label(
    root,
    text="📖 AI Narration App",
    font=("Helvetica", 24, "bold"),
    fg="white",
    bg="#1e1e1e"
)
title.pack(pady=40)

subtitle = tk.Label(
    root,
    text="Upload a story and hear it come to life",
    font=("Helvetica", 14),
    fg="#cccccc",
    bg="#1e1e1e"
)
subtitle.pack(pady=10)

voice_var = tk.StringVar(value="Calm Male")

voice_label = tk.Label(
    root,
    text="Choose Narrator Voice:",
    font=("Helvetica", 12),
    fg="white",
    bg="#1e1e1e"
)
voice_label.pack(pady=(30, 5))

voice_menu = tk.OptionMenu(
    root,
    voice_var,
    *VOICE_OPTIONS.keys()
)
voice_menu.config(
    font=("Helvetica", 12),
    bg="#333333",
    fg="white",
    highlightthickness=0
)
voice_menu.pack()


start_btn = tk.Button(
    root,
    text="▶ Start Reading",
    font=("Helvetica", 14),
    bg="#4CAF50",
    fg="white",
    padx=20,
    pady=10,
    command=launch_app
)
start_btn.pack(pady=40)

footer = tk.Label(
    root,
    text="Powered by ElevenLabs",
    fg="#888888",
    bg="#1e1e1e"
)
footer.pack(side="bottom", pady=20)

root.mainloop()
