import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import sys
import time
import urllib.request
import json
import socket
import subprocess
import pyautogui
import pygetwindow as gw
import requests
from openai import OpenAI

from openai import OpenAI

import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)
# 🧠 GPT BRAIN IMPORTS
try:
    from transformers import pipeline
    generator = pipeline("text-generation", model="microsoft/DialoGPT-medium")
except:
    generator = None

def send_to_unity(message):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(message.encode(), ("127.0.0.1", 5005))
        sock.close()
    except:
        pass

def send_emotion_to_unity(emotion):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(emotion.encode(), ("127.0.0.1", 5005))
        sock.close()
    except:
        pass

def speak(text):
    """LADKI KI AWAZ - FIXED"""
    print(f"Aira: {text}")
    if any(word in text.lower() for word in ['hi', 'hey', 'hello', 'hii']):
        send_to_unity("wave")
    new_engine = pyttsx3.init()
    new_engine.setProperty('rate', 170)
    new_engine.setProperty('volume', 1.0)
    
    # LADKI KI AWAZ
    voices = new_engine.getProperty('voices')
    if len(voices) > 1:
        new_engine.setProperty('voice', voices[1].id)  # Female voice
    else:
        new_engine.setProperty('voice', voices[0].id)  # Default
    
    new_engine.say(text)
    new_engine.runAndWait()
    new_engine.stop()


def wish_me():
    """Function to greet the user based on time of day"""
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning, Sir.")
    elif 12 <= hour < 18:
        speak("Good Afternoon, Sir.")
    else:
        speak("Good Evening, Sir.")
    speak("I am Aira. How can I help you today?")

def take_command():
    """Function to listen to microphone and return text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 300
        try:
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        except:
            return "None"

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query.lower()
    except:
        return "None"

def get_weather(query="Kolkata"):
    """Get weather information - uses free API (no key needed)"""
    try:
        # Extract city name from query
        city = "Kolkata"  # Default to West Bengal
        
        # Check for city in query
        if 'in' in query:
            parts = query.split('in')
            if len(parts) > 1:
                city = parts[-1].strip()
        elif 'at' in query:
            parts = query.split('at')
            if len(parts) > 1:
                city = parts[-1].strip()
        
        # Clean city name (remove special characters)
        city = city.replace("'", "").replace('"', "").replace(' ', '_')
        
        url = f"https://wttr.in/{city}?format=j1"
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        temp = data['current_condition'][0]['temp_C']
        weather = data['current_condition'][0]['weatherDesc'][0]['value']
        return f"The weather in {city.replace('_', ' ')} is {weather} with temperature {temp}°C."
    except:
        return "I couldn't get the weather information right now. Please check your internet connection."

def open_whatsapp():
    """Open WhatsApp - with your correct path"""
    speak("Opening WhatsApp")
    
    # Try different WhatsApp paths
    whatsapp_paths = [
        r"C:\Users\navab\OneDrive\Desktop\WhatsApp - Shortcut.lnk",
        r"C:\Users\navab\AppData\Local\WhatsApp\WhatsApp.exe",
        r"C:\Program Files\WhatsApp\WhatsApp.exe",
        r"C:\Program Files (x86)\WhatsApp\WhatsApp.exe"
    ]
    
    for path in whatsapp_paths:
        try:
            if os.path.exists(path):
                os.startfile(path)
                speak("WhatsApp opened successfully")
                return
        except:
            continue
    
    # If no path works, open WhatsApp Web
    speak("Opening WhatsApp Web instead")
    webbrowser.open("https://web.whatsapp.com")

def open_wps_office():
    """Open WPS Office - with correct path"""
    speak("Opening WPS Office")
    wps_path = r"C:\Users\navab\AppData\Local\Kingsoft\WPS Office\ksolaunch.exe"
    try:
        if os.path.exists(wps_path):
            os.startfile(wps_path)
            speak("WPS Office opened successfully")
            return
    except:
        pass
    try:
        subprocess.Popen("wps")
        speak("WPS Office opened")
    except:
        speak("WPS Office not found. Please check if it's installed.")

def write_to_notepad(text):
    """Write text to Notepad using keyboard automation"""
    try:
        os.system("notepad.exe")
        time.sleep(2)
        pyautogui.write(text, interval=0.1)
        speak("I've written the text in Notepad")
    except Exception as e:
        speak(f"Could not write to Notepad: {e}")
        speak("Please paste the text manually")

def open_app(app_name, app_path):
    """Open any app on your laptop"""
    speak(f"Opening {app_name}")
    try:
        os.startfile(app_path)
        time.sleep(2)
        speak(f"{app_name} opened successfully")
        return True
    except:
        try:
            subprocess.Popen(app_path)
            time.sleep(2)
            speak(f"{app_name} opened successfully")
            return True
        except:
            speak(f"{app_name} not found. Trying to open...")
            subprocess.Popen(app_path)
    return False

def open_website(url):
    """Open a website"""
    speak(f"Opening {url}")
    webbrowser.open(url)

# ==================== FREE AI INTEGRATION ====================

def get_ai_response(query):
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Aira, a smart, friendly "
                        "female desktop AI assistant. "
                        "Talk naturally like a human. "
                        "Keep answers conversational and clear."
                    )
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            temperature=0.7
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        print("AI Error:", e)
        return "Sorry Sir, my AI brain is temporarily unavailable."
# ==================== EMOTIONAL INTELLIGENCE ====================

def detect_emotion(query):
    """Detect emotion from user's words"""
    emotions = {
        'sad': ['sad', 'depressed', 'unhappy', 'down', 'cry', 'tears', 'lonely', 'heartbroken', 'grief', 'sorrow'],
        'happy': ['happy', 'joy', 'excited', 'great', 'wonderful', 'amazing', 'fantastic', 'awesome', 'good', 'smile'],
        'angry': ['angry', 'mad', 'furious', 'upset', 'annoyed', 'frustrated', 'rage', 'hate', 'pissed'],
        'stressed': ['stressed', 'tired', 'exhausted', 'overwhelmed', 'burnout', 'pressure', 'anxious', 'worried'],
        'lonely': ['lonely', 'alone', 'no one', 'isolation', 'missing', 'miss you'],
        'love': ['love', 'like', 'affection', 'care', 'heart', 'romantic'],
        'thankful': ['thank', 'thanks', 'grateful', 'appreciate', 'blessed'],
        'confused': ['confused', 'don\'t understand', 'lost', 'unclear', 'puzzled'],
        'excited': ['excited', 'thrilled', 'eager', 'enthusiastic', 'looking forward'],
        'worried': ['worried', 'concerned', 'nervous', 'scared', 'afraid', 'fear']
    }
    
    detected = []
    for emotion, keywords in emotions.items():
        for keyword in keywords:
            if keyword in query:
                detected.append(emotion)
                break
    
    return detected if detected else None

def respond_to_emotion(emotion, query):
    """Respond appropriately to detected emotion"""
    responses = {
        'sad': [
            "I'm so sorry you're feeling sad, Sir. I'm here for you.",
            "It's okay to feel sad sometimes. Do you want to talk about it?",
            "I'm here to listen if you need someone to talk to.",
            "Would you like me to play some calming music for you?",
            "Remember, this feeling will pass. You're stronger than you think."
        ],
        'happy': [
            "That's wonderful! I'm so happy for you, Sir!",
            "Your happiness makes me happy too!",
            "That's amazing! Tell me more about it!",
            "I love seeing you smile, Sir!",
            "Let's celebrate this moment together!"
        ],
        'angry': [
            "I understand you're angry, Sir. Take a deep breath.",
            "It's okay to feel angry. Do you want to vent?",
            "I'm here to listen if you need to talk about it.",
            "Would you like me to help you find a solution?",
            "Let's take a moment to calm down together."
        ],
        'stressed': [
            "I understand you're stressed, Sir. Let's take a break.",
            "Would you like me to play some relaxing music?",
            "Remember to take care of yourself, Sir.",
            "I can help you organize your tasks if you want.",
            "Take a deep breath. You're doing great."
        ],
        'lonely': [
            "I'm here for you, Sir. You're not alone.",
            "I'm always here to talk to you whenever you need.",
            "Would you like to chat about something?",
            "I care about you, Sir. You matter to me.",
            "Let's have a conversation to cheer you up."
        ],
        'love': [
            "That's beautiful! Love is wonderful.",
            "I'm happy you're experiencing love, Sir.",
            "Love makes life beautiful.",
            "I'm here to support you in your relationships.",
            "That's wonderful to hear!"
        ],
        'thankful': [
            "You're welcome, Sir! I'm always happy to help.",
            "Thank you for your kind words!",
            "I'm here whenever you need me, Sir.",
            "It's my pleasure to assist you.",
            "Your happiness is my priority."
        ],
        'confused': [
            "I understand you're confused, Sir. Let me help you.",
            "What would you like me to explain?",
            "I'm here to help you understand.",
            "Don't worry, we'll figure it out together.",
            "Let me break it down for you."
        ],
        'excited': [
            "I can feel your excitement, Sir! That's amazing!",
            "I'm excited for you too!",
            "Tell me more about what's exciting you!",
            "Your enthusiasm is contagious!",
            "Let's make the most of this moment!"
        ],
        'worried': [
            "I understand you're worried, Sir. Let's talk about it.",
            "What's on your mind?",
            "I'm here to help you work through it.",
            "Don't worry, we'll find a solution together.",
            "You're not alone in this."
        ]
    }
    
    if emotion in responses:
        import random
        emotion_map = {
            'happy': 'happy',
            'excited': 'happy',
            'thankful': 'joy',
            'sad': 'sad',
            'lonely': 'sad',
            'angry': 'angry',
            'stressed': 'sad',
            'worried': 'sad',
            'confused': 'happy',
            'love': 'joy'
        }
        if emotion in emotion_map:
            send_emotion_to_unity(emotion_map[emotion])
        return random.choice(responses[emotion])
    return None

# ==================== APP PATHS ====================

apps = {
    'chrome': 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    'firefox': 'C:\\Program Files\\Mozilla Firefox\\firefox.exe',
    'edge': 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
    'browser': 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    'internet': 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    'after effects': r"C:\Program Files\Adobe\Adobe After Effects 2025\Support Files\AfterFX.exe",
    'aftereffects': r"C:\Program Files\Adobe\Adobe After Effects 2025\Support Files\AfterFX.exe",
    'after effects 2025': r"C:\Program Files\Adobe\Adobe After Effects 2025\Support Files\AfterFX.exe",
    'illustrator': r"C:\Program Files\Adobe\Adobe Illustrator 2025\Support Files\Contents\Windows\Illustrator.exe",
    'illustrator 2025': r"C:\Program Files\Adobe\Adobe Illustrator 2025\Support Files\Contents\Windows\Illustrator.exe",
    'photoshop': r"C:\Program Files\Adobe\Adobe Photoshop 2025\Photoshop.exe",
    'photoshop 2025': r"C:\Program Files\Adobe\Adobe Photoshop 2025\Photoshop.exe",
    'premiere pro': r"C:\Program Files\Adobe\Adobe Premiere Pro 2025\Adobe Premiere Pro.exe",
    'premierepro': r"C:\Program Files\Adobe\Adobe Premiere Pro 2025\Adobe Premiere Pro.exe",
    'premiere pro 2025': r"C:\Program Files\Adobe\Adobe Premiere Pro 2025\Adobe Premiere Pro.exe",
    'premiere rush': r"C:\Program Files\Adobe\Adobe Premiere Rush 2.0\Adobe Premiere Rush.exe",
    'premiererush': r"C:\Program Files\Adobe\Adobe Premiere Rush 2.0\Adobe Premiere Rush.exe",
    'adobe express': r"C:\Users\navab\OneDrive\Desktop\Adobe Express - Shortcut.lnk",
    'adobe xd': r"C:\Users\navab\OneDrive\Desktop\Adobe XD - Shortcut.lnk",
    'vroid studio': r"C:\Users\navab\OneDrive\Desktop\VRoidStudio 2.11.0.lnk",
    'vroid': r"C:\Users\navab\OneDrive\Desktop\VRoidStudio 2.11.0.lnk",
    'capcut': r"C:\Users\navab\OneDrive\Desktop\CapCut.lnk",
    'cap cut': r"C:\Users\navab\OneDrive\Desktop\CapCut.lnk",
    'notepad': 'notepad.exe',
    'calculator': 'calc.exe',
    'word': 'C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE',
    'excel': 'C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE',
    'powerpoint': 'C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE',
    'vscode': 'C:\\Users\\navab\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe',
    'visual studio': 'C:\\Users\\navab\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe',
    'cmd': 'cmd.exe',
    'terminal': 'wt.exe',
    'whatsapp': r"C:\Users\navab\OneDrive\Desktop\WhatsApp - Shortcut.lnk",
    'WizTree': r"C:\Program Files\WizTree\WizTree64.exe",
    'ShareX': r"C:\Program Files\ShareX\ShareX.exe",
    'slack': 'C:\\Users\\navab\\AppData\\Local\\slack\\slack.exe',
    'zoom': 'C:\\Users\\navab\\AppData\\Local\\Zoom\\bin\\Zoom.exe',
    'teams': 'C:\\Users\\navab\\AppData\\Local\\Microsoft\\Teams\\Current\\Teams.exe',
    'spotify': 'C:\\Users\\navab\\AppData\\Roaming\\Spotify\\Spotify.exe',
    'steam': 'C:\\Program Files (x86)\\Steam\\steam.exe',
    'xbox': r"C:\Users\navab\OneDrive\Desktop\Xbox - Shortcut.lnk",
    'photos': r"C:\Users\navab\OneDrive\Desktop\Photos - Shortcut.lnk",
    'epic games': r"C:\Program Files\Epic Games\Launcher\Portal\Binaries\Win64\EpicGamesLauncher.exe",
    'epicgames': r"C:\Program Files\Epic Games\Launcher\Portal\Binaries\Win64\EpicGamesLauncher.exe",
    'epic games launcher': r"C:\Program Files\Epic Games\Launcher\Portal\Binaries\Win64\EpicGamesLauncher.exe",
    'Rise of the Tomb Raider': r"C:\Games\Rise of the Tomb Raider\ROTTR.exe",
    'google drive': r"C:\Program Files\Google\Drive File Stream\122.0.1.0\GoogleDriveFS.exe",
    'drive': r"C:\Program Files\Google\Drive File Stream\122.0.1.0\GoogleDriveFS.exe",
    'copilot': r"C:\Users\navab\OneDrive\Desktop\Copilot - Shortcut.lnk",
    'wps': r"C:\Users\navab\AppData\Local\Kingsoft\WPS Office\ksolaunch.exe",
    'wps office': r"C:\Users\navab\AppData\Local\Kingsoft\WPS Office\ksolaunch.exe",
    'microsoft store': r"C:\Users\navab\OneDrive\Desktop\Microsoft Store - Shortcut.lnk",
    'microsoftstore': r"C:\Users\navab\OneDrive\Desktop\Microsoft Store - Shortcut.lnk",
    'store': r"C:\Users\navab\OneDrive\Desktop\Microsoft Store - Shortcut.lnk",
    'free download manager': r"C:\Users\navab\OneDrive\Desktop\Free Download Manager.lnk",
    'fmd': r"C:\Users\navab\OneDrive\Desktop\Free Download Manager.lnk",
    'hotspot shield': r"C:\Users\Public\Desktop\Hotspot Shield.lnk",
    'hotspotshield': r"C:\Users\Public\Desktop\Hotspot Shield.lnk",
    'weatherbot': r"C:\Users\navab\OneDrive\Desktop\WeatherBot",
    'weather bot': r"C:\Users\navab\OneDrive\Desktop\WeatherBot",
    'youtube': 'https://www.youtube.com',
    'google': 'https://www.google.com',
    'facebook': 'https://www.facebook.com',
    'instagram': 'https://www.instagram.com',
    'twitter': 'https://www.twitter.com',
    'linkedin': 'https://www.linkedin.com',
    'github': 'https://www.github.com',
    'stackoverflow': 'https://stackoverflow.com',
    'gmail': 'https://mail.google.com',
    'netflix': 'https://www.netflix.com',
    'amazon': 'https://www.amazon.com',
    'playstore': 'https://play.google.com',
    'app store': 'https://www.apple.com/app-store/',
}

if __name__ == "__main__":
    # Test voice first - UPDATED GREETING
    print("Testing voice...")
    speak("Hey Abhinav ASR I am Aira")
    time.sleep(1)
    
    
    # Now greet the user
    wish_me()
    
    # TTS RESET TEST
    speak("yeah tell me what you want Sir")
    time.sleep(1)
    
    while True:

        query = take_command()
        # Wave when user greets
        if any(word in query for word in ['hi', 'hey', 'hello', 'hii', 'listen']):
            send_to_unity("wave")
        
        if any(wake in query.lower() for wake in ['listen', 'hey aira', 'aira']):
            speak("Llama ON!")
            msg = take_command()
            try:
                import requests
                requests.post("http://localhost:4891/v1/chat/completions", 
                            json={"model": "Llama-3.2-3B-Instruct", "messages": [{"role": "user", "content": msg}]})
                speak("Llama replied!")
            except:
                pass
            continue
        
        # normal commands (time, wifi, etc)...


        # Logic for executing tasks
        if 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")
        
        elif 'open youtube' in query:
            if 'search' in query:
                search_query = query.replace("open youtube and search for ", "").replace("search for ", "")
                speak(f"Searching for {search_query} on YouTube")
                webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
            else:
                speak("Yes sir, opening YouTube")
                webbrowser.open("youtube.com")
        
        elif 'open google' in query:
            if 'search' in query:
                search_query = query.replace("open google and search for ", "").replace("search for ", "")
                speak(f"Searching for {search_query} on Google")
                webbrowser.open(f"https://www.google.com/search?q={search_query}")
            else:
                speak("Yes sir, opening Google")
                webbrowser.open("google.com")
        
        elif 'open chrome' in query:
            if 'search' in query:
                search_query = query.replace("open chrome and search for ", "").replace("search for ", "")
                speak(f"Searching for {search_query} on Chrome")
                webbrowser.open(f"https://www.google.com/search?q={search_query}")
            else:
                speak("Yes sir, opening Chrome")
                webbrowser.open("chrome.com")
        
        elif 'open firefox' in query:
            speak("Yes sir, opening Firefox")
            webbrowser.open("firefox.com")
        
        elif 'open edge' in query:
            speak("Yes sir, opening Edge")
            webbrowser.open("edge.com")
        
        elif 'open stackoverflow' in query:
            speak("Yes sir, opening Stack Overflow")
            webbrowser.open("stackoverflow.com")
        
        elif 'open whatsapp' in query:
            open_whatsapp()
        
        elif 'open wps' in query or 'open wps office' in query:
            open_wps_office()
        
        elif 'open notepad' in query:
            if 'write' in query:
                text_to_write = query.replace("write in notepad ", "").replace("write ", "").replace("write this ", "")
                if text_to_write:
                    write_to_notepad(text_to_write)
                else:
                    speak("Please tell me what to write")
                    os.system("notepad.exe")
            else:
                open_app('notepad', 'notepad.exe')
        
        elif 'open calculator' in query:
            open_app('calculator', 'calc.exe')
        
        elif 'open word' in query:
            open_app('word', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE')
        
        elif 'open excel' in query:
            open_app('excel', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE')
        
        elif 'open powerpoint' in query:
            open_app('powerpoint', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE')
        
        elif 'open vscode' in query or 'open visual studio' in query:
            open_app('vscode', 'C:\\Users\\navab\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe')
        
        elif 'open spotify' in query:
            open_app('spotify', 'C:\\Users\\navab\\AppData\\Roaming\\Spotify\\Spotify.exe')
        
        elif 'open zoom' in query:
            open_app('zoom', 'C:\\Users\\navab\\AppData\\Local\\Zoom\\bin\\Zoom.exe')
        
        elif 'open teams' in query:
            open_app('teams', 'C:\\Users\\navab\\AppData\\Local\\Microsoft\\Teams\\Current\\Teams.exe')
        
        elif 'open slack' in query:
            open_app('slack', 'C:\\Users\\navab\\AppData\\Local\\slack\\slack.exe')
        
        elif 'open browser' in query or 'open internet' in query:
            open_app('browser', 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe')
        
        elif 'open facebook' in query:
            open_website('https://www.facebook.com')
        
        elif 'open instagram' in query:
            open_website('https://www.instagram.com')
        
        elif 'open twitter' in query:
            open_website('https://www.twitter.com')
        
        elif 'open linkedin' in query:
            open_website('https://www.linkedin.com')
        
        elif 'open github' in query:
            open_website('https://www.github.com')
        
        elif 'open gmail' in query:
            open_website('https://mail.google.com')
        
        elif 'open netflix' in query:
            open_website('https://www.netflix.com')
        
        elif 'open amazon' in query:
            open_website('https://www.amazon.com')
        
        elif 'open playstore' in query:
            open_website('https://play.google.com')
        
        elif 'open app store' in query:
            open_website('https://www.apple.com/app-store/')
        
        elif 'open after effects' in query or 'open aftereffects' in query:
            open_app('After Effects', r"C:\Program Files\Adobe\Adobe After Effects 2025\Support Files\AfterFX.exe")
        
        elif 'open illustrator' in query:
            open_app('Illustrator', r"C:\Program Files\Adobe\Adobe Illustrator 2025\Support Files\Contents\Windows\Illustrator.exe")
        
        elif 'open photoshop' in query:
            open_app('Photoshop', r"C:\Program Files\Adobe\Adobe Photoshop 2025\Photoshop.exe")
        
        elif 'open premiere pro' in query or 'open premierepro' in query:
            open_app('Premiere Pro', r"C:\Program Files\Adobe\Adobe Premiere Pro 2025\Adobe Premiere Pro.exe")
        
        elif 'open premiere rush' in query or 'open premiererush' in query:
            open_app('Premiere Rush', r"C:\Program Files\Adobe\Adobe Premiere Rush 2.0\Adobe Premiere Rush.exe")
        
        elif 'open adobe express' in query:
            open_app('Adobe Express', r"C:\Users\navab\OneDrive\Desktop\Adobe Express - Shortcut.lnk")
        
        elif 'open adobe xd' in query:
            open_app('Adobe XD', r"C:\Users\navab\OneDrive\Desktop\Adobe XD - Shortcut.lnk")
        
        elif 'open vroid studio' in query or 'open vroid' in query:
            open_app('VRoid Studio', r"C:\Users\navab\OneDrive\Desktop\VRoidStudio 2.11.0.lnk")
        
        elif 'open capcut' in query or 'open cap cut' in query:
            open_app('CapCut', r"C:\Users\navab\OneDrive\Desktop\CapCut.lnk")
        
        elif 'open steam' in query:
            open_app('Steam', r"C:\Program Files (x86)\Steam\steam.exe")
        
        elif 'open epic games' in query or 'open epicgames' in query:
            open_app('Epic Games', r"C:\Program Files\Epic Games\Launcher\Portal\Binaries\Win64\EpicGamesLauncher.exe")
        
        elif 'open google drive' in query or 'open drive' in query:
            open_app('Google Drive', r"C:\Program Files\Google\Drive File Stream\122.0.1.0\GoogleDriveFS.exe")
        
        elif 'open copilot' in query:
            open_app('Copilot', r"C:\Users\navab\OneDrive\Desktop\Copilot - Shortcut.lnk")
        
        elif 'open photos' in query:
            open_app('Photos', r"C:\Users\navab\OneDrive\Desktop\Photos - Shortcut.lnk")
        
        elif 'open xbox' in query:
            open_app('Xbox', r"C:\Users\navab\OneDrive\Desktop\Xbox - Shortcut.lnk")

        elif 'open anti gravity' in query:
            open_app('Antigravity', r"C:\Users\navab\AppData\Local\Programs\Antigravity\Antigravity.exe")

        elif 'open ranch simulator' in query:
            open_app('Ranch_Simulator', r"C:\Games\Ranch Simulator\Ranch_Simulator.exe")
        
        elif 'open microsoft store' in query or 'open microsoftstore' in query or 'open store' in query:
            open_app('Microsoft Store', r"C:\Users\navab\OneDrive\Desktop\Microsoft Store - Shortcut.lnk")
        
        elif 'open free download manager' in query or 'open fmd' in query:
            open_app('Free Download Manager', r"C:\Users\navab\OneDrive\Desktop\Free Download Manager.lnk")
        
        elif 'open hotspot shield' in query or 'open hotspotshield' in query:
            open_app('Hotspot Shield', r"C:\Users\Public\Desktop\Hotspot Shield.lnk")
        
        elif 'open weatherbot' in query or 'open weather bot' in query:
            open_app('WeatherBot', r"C:\Users\navab\OneDrive\Desktop\WeatherBot")
        
        elif 'weather' in query:
            speak("Let me check the weather for you")
            weather_info = get_weather(query)
            speak(weather_info)
        
        # 🔥 ZERO INSTALL VOLUME - pyautogui!
        elif 'volume up' in query or 'volume increase' in query:
            pyautogui.press('volumeup')
            pyautogui.press('volumeup')  # Double press = +20%
            speak("Volume UP Sir!")
        
        elif 'volume down' in query or 'volume decrease' in query:
            pyautogui.press('volumedown')
            pyautogui.press('volumedown')  # Double = -20%
            speak("Volume DOWN Sir!")
        
        elif 'volume max' in query or 'max volume' in query:
            for _ in range(10):  # Max volume
                pyautogui.press('volumeup')
            speak("Volume MAXIMUM Sir!")
        
        elif 'mute' in query or 'silence' in query:
            pyautogui.press('volumemute')
            speak("Audio MUTED!")
        
        elif 'unmute' in query or 'sound on' in query:
            pyautogui.press('volumemute')
            speak("Sound UNMUTED!")
        
        # 🔥 SAFE SHUTDOWN
        elif 'shutdown' in query:
            speak("DANGER! Say CONFIRM TWICE to shutdown!")
            confirm1 = take_command()
            if 'confirm' in confirm1:
                confirm2 = take_command()
                if 'confirm' in confirm2:
                    speak("Shutting down NOW!")
                    os.system("shutdown /s /t 5")
                else:
                    speak("Second confirm needed - CANCELLED!")
            else:
                speak("Shutdown cancelled Sir!")

        # 📸 AIRA SCREENSHOT FOLDER!
        elif 'take screenshot' in query or 'screenshot' in query:
            # YOUR EXACT FOLDER
            aira_folder = r"C:\Users\navab\OneDrive\Desktop\Aira Screenshot"
            
            # Folder banao if not exists
            if not os.path.exists(aira_folder):
                os.makedirs(aira_folder)
            
            filename = f"Screenshot_{int(time.time())}.png"
            full_path = os.path.join(aira_folder, filename)
            
            speak("Screenshot saved to Aira Screenshot folder!")
            time.sleep(2)
            
            screenshot = pyautogui.screenshot()
            screenshot.save(full_path)
            speak(f"Saved: {filename} in Aira Screenshot!Check it ")
        
        elif 'screenshot now' in query:
            aira_folder = r"C:\Users\navab\OneDrive\Desktop\Aira Screenshot"
            filename = f"Instant_{int(time.time())}.png"
            full_path = os.path.join(aira_folder, filename)
            
            speak("Instant screenshot!")
            screenshot = pyautogui.screenshot()
            screenshot.save(full_path)
            speak("Saved in Aira Screenshot folder!")

         # 🎵 ULTIMATE MUSIC CONTROLLER - ENGLISH!
        elif 'play song' in query or 'play music' in query:
            speak("Spotify or YouTube?")
            platform = take_command()
            
            if 'spotify' in platform or 'spot' in platform:
                speak("Which song Sir?")
                song_name = take_command()
                
                # Open Spotify App
                os.startfile(r"C:\Users\navab\OneDrive\Desktop\Spotify - Shortcut.lnk")
                time.sleep(3)
                
                # Search in Spotify App (Ctrl+K)
                pyautogui.hotkey('ctrl', 'k')
                time.sleep(0.5)
                pyautogui.write(song_name)
                pyautogui.press('enter')
                
                speak(f"{song_name} searched in Spotify app!")
                
            elif 'youtube' in platform or 'tube' in platform:
                speak("Which song on YouTube?")
                song_name = take_command()
                search_url = f"https://www.youtube.com/results?search_query={song_name}"
                webbrowser.open(search_url)
                speak(f"{song_name} ready on YouTube!")
            
            else:
                speak("Opening Spotify!")
                os.startfile(r"C:\Users\navab\OneDrive\Desktop\Spotify - Shortcut.lnk")
        
        # 🎵 SONG CONTROLS
        elif 'next song' in query or 'next track' in query:
            pyautogui.press('nexttrack')
            speak("Next song playing!")
        
        elif 'previous song' in query or 'previous track' in query:
            pyautogui.press('prevtrack')
            speak("Previous song!")
        
        elif 'pause' in query or 'pause song' in query:
            pyautogui.press('playpause')
            speak("Music paused!")
        
        elif 'resume' in query or 'play now' in query:
            pyautogui.press('playpause')
            speak("Music resumed!")
        
        elif 'previous song' in query or 'previous track' in query or 'prev' in query:
            pyautogui.press('prevtrack')
            speak("Ok Sir previous Song!")
        
        elif 'pause' in query or 'pause song' in query or 'pause music' in query:
            pyautogui.press('playpause')
            speak("Paused")
        
        elif 'play' in query or 'resume' in query or 'continue' in query:
            pyautogui.press('playpause')
            speak("Played Sir")

        # 📶 WIFI CONTROL - ALL VARIATIONS!
        elif any(word in query for word in ['wifi off', 'wi-fi off', 'wifi disable', 'disable wifi', 'turn wifi off']):
            speak("Turning WiFi OFF in 3 seconds! Say STOP!")
            time.sleep(1)
            confirm = take_command()
            if 'stop' not in confirm:
                os.system('netsh interface set interface "Wi-Fi" admin=disable')
                speak("WiFi disabled Sir!")
            else:
                speak("WiFi kept ON!")
        
        elif any(word in query for word in ['wifi on', 'wi-fi on', 'wifi enable', 'enable wifi', 'turn wifi on']):
            os.system('netsh interface set interface "Wi-Fi" admin=enable')
            speak("WiFi enabled!")
        
        elif 'wifi status' in query or 'wi-fi status' in query:
            result = os.popen('netsh interface show interface "Wi-Fi"').read()
            if 'Connected' in result:
                speak("WiFi connected!")
            else:
                speak("WiFi disconnected or OFF!")

        # ✂️ COPY FROM-TO - PRO!
        elif 'copy from' in query or 'copy this part' in query:
            speak("What is the full text Sir?")
            full_text = take_command()
            
            speak("Copy from which word?")
            start_word = take_command()
            
            speak("To which word?")
            end_word = take_command()
            
            try:
                # Find positions
                start_pos = full_text.lower().find(start_word.lower())
                end_pos = full_text.lower().find(end_word.lower(), start_pos) + len(end_word)
                
                if start_pos != -1 and end_pos != -1:
                    copied_text = full_text[start_pos:end_pos]
                    import pyperclip
                    pyperclip.copy(copied_text)
                    speak(f"Copied: {copied_text}")
                    speak("Ready to paste with Ctrl+V!")
                else:
                    speak("Words not found!")
            except:
                speak("Copy failed! Try again.")
        
        elif 'paste' in query:
            pyautogui.hotkey('ctrl', 'v')
            speak("Pasted!")


        elif 'who are you' in query or 'what are you' in query:
            speak("I am Aira, a virtual assistant created by Python.")
        
        elif 'stop' in query or 'exit' in query or 'quit' in query:
            speak("Minimizing to system tray, Sir.")
            import pygetwindow as gw
            import time
            
            # Find the Aira window
            try:
                aira_windows = gw.getWindowsWithTitle('aira.py')
                
                if aira_windows:
                    aira_window = aira_windows[0]
                    aira_window.minimize()
                    print("Aira window minimized successfully!")
                else:
                    import ctypes
                    ctypes.windll.user32.ShowWindow(ctypes.windll.user32.GetForegroundWindow(), 6)
            except Exception as e:
                print(f"Error: {e}")
                import ctypes
                ctypes.windll.user32.ShowWindow(ctypes.windll.user32.GetForegroundWindow(), 6)
            
            speak("I'm in standby mode. Say 'Wake up Aira' to bring me back.")
            time.sleep(1)
        
        elif 'wake up' in query or 'hey aira' in query or 'open aira' in query:
            speak("I'm back, Sir! How can I help you?")
            import pygetwindow as gw
            import time
            
            # Find the Aira window
            try:
                # Get all windows with 'aira' in title
                aira_windows = gw.getWindowsWithTitle('aira.py')
                
                if aira_windows:
                    # Get the first window
                    aira_window = aira_windows[0]
                    
                    # Restore the window
                    aira_window.restore()
                    
                    # Bring window to foreground
                    aira_window.activate()
                    
                    print("Aira window restored successfully!")
                else:
                    # Fallback to ctypes if window not found
                    import ctypes
                    hwnd = ctypes.windll.user32.GetForegroundWindow()
                    ctypes.windll.user32.ShowWindow(hwnd, 9)
                    ctypes.windll.user32.SetForegroundWindow(hwnd)
                    print("Using fallback method...")
            except Exception as e:
                print(f"Error: {e}")
                # Fallback to ctypes
                import ctypes
                hwnd = ctypes.windll.user32.GetForegroundWindow()
                ctypes.windll.user32.ShowWindow(hwnd, 9)
                ctypes.windll.user32.SetForegroundWindow(hwnd)
            
            time.sleep(1)
        
        # ==================== EMOTIONAL INTELLIGENCE ====================
        # Check for emotions first
        else:
            emotion = detect_emotion(query)
            if emotion:
                response = respond_to_emotion(emotion[0], query)
                if response:
                    speak(response)
                    continue
            
            # If no specific command matched, use free AI for general questions
            speak("Let me think about that...")
            chatgpt_response = get_ai_response(query)
            speak(chatgpt_response)
