import tkinter as tk
import pyttsx3
import speech_recognition as sr
from datetime import datetime, date
import openai

# Set your OpenAI API key
openai.api_key = "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"

# Voice engine setup
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Speech input
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = recognizer.listen(source, timeout=5)
            query = recognizer.recognize_google(audio)
            entry.insert(0, query)
            send_message()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Please try again.")
        except sr.RequestError:
            speak("Network error. Please check your internet connection.")
        except sr.WaitTimeoutError:
            speak("No voice detected. Try again.")

# Bot response logic
def get_bot_response(user_input):
    user_input = user_input.lower()

    if user_input in ['hi', 'hello', 'hey']:
        return "Hello there! How can I help you?"
    elif "your name" in user_input:
        return "I'm ChatBot, your assistant!"
    elif "how are you" in user_input:
        return "I'm doing well, thanks for asking!"
    elif "time" in user_input:
        return f"The current time is {datetime.now().strftime('%H:%M:%S')}"
    elif "date" in user_input:
        return f"Today's date is {date.today()}"
    elif "help" in user_input:
        return "You can ask me about the date, time, math questions, or just chat!"
    elif any(op in user_input for op in ['+', '-', '*', '/', '**']):
        try:
            result = eval(user_input)
            return f"The answer is {result}"
        except:
            return "Sorry, I couldn't compute that."
    elif user_input == "bye":
        return "Goodbye! Have a great day!"
    else:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_input}]
            )
            return response['choices'][0]['message']['content'].strip()
        except Exception as e:
            return "I'm having trouble reaching AI right now."

# Send message logic
def send_message(event=None):
    user_input = entry.get()
    if user_input.strip() == "":
        return
    entry.delete(0, tk.END)

    user_msg = f"👤 You: {user_input}\n"
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, user_msg)

    response = get_bot_response(user_input)
    bot_msg = f"🤖 Bot: {response}\n\n"
    chat_log.insert(tk.END, bot_msg)
    chat_log.config(state=tk.DISABLED)
    chat_log.yview(tk.END)

    chat_history.append(user_msg)
    chat_history.append(bot_msg)
    with open("chat_history.txt", "w") as f:
        f.writelines(chat_history)

    speak(response)

    if user_input.lower() == "bye":
        window.after(1500, window.quit)

# Theme toggle
def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    if dark_mode:
        window.config(bg="#2e2e2e")
        chat_log.config(bg="#1e1e1e", fg="white", insertbackground="white")
        entry.config(bg="#1e1e1e", fg="white", insertbackground="white")
        send_button.config(bg="#444", fg="white")
        voice_button.config(bg="#444", fg="white")
        theme_button.config(text="☀️ Light Mode", bg="#444", fg="white")
    else:
        window.config(bg="SystemButtonFace")
        chat_log.config(bg="white", fg="black", insertbackground="black")
        entry.config(bg="white", fg="black", insertbackground="black")
        send_button.config(bg="SystemButtonFace", fg="black")
        voice_button.config(bg="SystemButtonFace", fg="black")
        theme_button.config(text="🌙 Dark Mode", bg="SystemButtonFace", fg="black")

# GUI Setup
window = tk.Tk()
window.title("🎙️ Voice ChatBot")
window.geometry("500x600")
dark_mode = False
chat_history = []

chat_log = tk.Text(window, font=("Arial", 12), state=tk.DISABLED, wrap=tk.WORD)
chat_log.pack(padx=10, pady=(10, 0), fill=tk.BOTH, expand=True)

bottom_frame = tk.Frame(window)
bottom_frame.pack(fill=tk.X, padx=10, pady=10)

entry = tk.Entry(bottom_frame, font=("Arial", 12))
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
entry.bind("<Return>", send_message)

send_button = tk.Button(bottom_frame, text="Send", font=("Arial", 12), command=send_message)
send_button.pack(side=tk.LEFT, padx=5)

voice_button = tk.Button(bottom_frame, text="🎤 Voice", font=("Arial", 12), command=listen)
voice_button.pack(side=tk.LEFT)

theme_button = tk.Button(window, text="🌙 Dark Mode", font=("Arial", 10), command=toggle_theme)
theme_button.pack(pady=(0, 5))

window.mainloop()
