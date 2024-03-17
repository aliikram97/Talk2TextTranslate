import os
import time
import datetime

import fpdf
import pyaudio
import wave
import tkinter as tk
from tkinter import filedialog
import threading
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS

class Talk2TextTranslate:
    def __init__(self):
        self.root = tk.Tk()
        self.height = self.root.winfo_screenheight()
        self.width = self.root.winfo_screenwidth()
        self.root.resizable = (self.height,self.width)
        self.button = tk.Button(text="🎤",font=("Arial","120","bold"),command=self.click_handler)
        self.button.pack()
        self.label_recording = tk.Label(text="00:00:00")
        self.label_recording.pack()
        self.recording = False
        self.recording_file_name = ""
        self.recording_file_name_load = ""
        self.latest = False
        self.browse_button = tk.Button(self.root, text="Browse Audio File", command=self.browse_file)
        self.browse_button.pack()
        # Dropdown menus for input and desired languages
        self.input_lang_var = tk.StringVar(self.root)
        self.output_lang_var = tk.StringVar(self.root)

        self.input_lang_label = tk.Label(self.root, text="Input Language:")
        self.input_lang_label.pack()
        self.input_lang_dropdown = tk.OptionMenu(self.root, self.input_lang_var, "english", "urdu-PK", "french","arabic","german","hindi")
        self.input_lang_dropdown.pack()

        self.output_lang_label = tk.Label(self.root, text="Desired Language:")
        self.output_lang_label.pack()
        self.output_lang_dropdown = tk.OptionMenu(self.root, self.output_lang_var, "english", "urdu-PK", "french","arabic","german","hindi","pashto")
        self.output_lang_dropdown.pack()

        self.translate_button = tk.Button(self.root, text="Translate", command=self.translate_text)
        self.translate_button.pack()


        self.root.mainloop()

    def click_handler(self):
        if self.recording:
            self.recording=False
            self.button.config(fg="black")
        else:
            self.recording=True
            self.button.config(fg="red")
            threading.Thread(target=self.record_audio).start()
    def record_audio(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16,channels=1,rate=44100,input=True,frames_per_buffer=1024)
        frames=[]
        start = time.time()
        while self.recording:
            data = stream.read(1024)
            frames.append(data)

            passed = time.time()-start
            seconds = passed % 60
            minutes = passed // 60
            hours = minutes // 60
            self.label_recording.config(text=f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")
        stream.stop_stream()
        stream.close()
        audio.terminate()
        # save the recorded input
        current_time = datetime.datetime.now()
        self.recording_file_name = f"recorded_input_{current_time.year}_{current_time.month}_{current_time.day}_{current_time.second}.wav"
        sound_file = wave.open(self.recording_file_name,"wb")
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b"".join(frames))
        sound_file.close()
    def language_selected(self):
        input_language = self.input_lang_var.get()
        desired_language = self.output_lang_var.get()
        if input_language == "english":
            input_lang = 'en'
        elif input_language == "urdu-PK":
            input_lang = 'ur-PK'
        elif input_language == "french":
            input_lang = 'fr'
        elif input_language == "arabic":
            input_lang = 'ar-SA'
        elif input_language == "german":
            input_lang = 'de-DE'
        elif input_language == "hindi":
            input_lang = 'hi-IN'

        if desired_language == "english":
            output_lang = 'en'
        elif desired_language == "urdu-PK":
            output_lang = 'ur'
        elif desired_language == "french":
            output_lang = 'fr'
        elif desired_language == "arabic":
            output_lang = 'ar'
        elif desired_language == "german":
            output_lang = 'de'
        elif desired_language == "hindi":
            output_lang = 'hi'
        print(input_lang,output_lang)
        return input_lang,output_lang
    def translate_text(self):
        input_lang,output_lang = self.language_selected()
        recognizer = sr.Recognizer()
        if self.latest:
            audio_file = self.recording_file_name
        else:
            audio_file = self.recording_file_name_load
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            query = recognizer.recognize_google(audio_data,language=input_lang)
        print(query)
        translated_query = GoogleTranslator(source='auto', target=output_lang).translate(query)
        print(translated_query)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        self.recording_file_name_load = file_path


Talk2TextTranslate()