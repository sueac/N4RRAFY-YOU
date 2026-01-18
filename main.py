import tkinter as tk
import subprocess
import sys
import os

def launch_app():
    # Close main window
    root.destroy()

    # Launch app.py using same Python interpreter
    subprocess.Popen([sys.executable, "app.py"])

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
