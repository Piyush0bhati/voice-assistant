import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import time
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "f8c9d97dbc0b4824b71509123a26e628"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save("temp.mp3")

# Initialize Pygame mixer
    pygame.mixer.init()

# Load an MP3 file
    pygame.mixer.music.load("temp.mp3")

# Play the MP3 file
    pygame.mixer.music.play()

# Keep the program running while the music is playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # Check every second if the music is still playing

    pygame.mixer.music.unload()
    os.remove("temp.mp3")


def aiprocess(command):

    client = OpenAI(
      base_url="https://openrouter.ai/api/v1",
      api_key="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",
    )

    completion = client.chat.completions.create(
      extra_headers={
        "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
        "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
      },
      extra_body={},
      model="deepseek/deepseek-r1:free",
      messages=[
        {"role":"system", "content": "you are a virtual assistant named friday skilled in genral tests like alexa and google cloud"},
             {"role": "user", "content": command}
      ]
    )
    return(completion.choices[0].message)




# def aiprocess(command):
#     client = OpenAI(api_key="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"
#     )

#     completion = client.chat.completions.create(

#         model= "deepseek/deepseek-r1:free",
#         messages=[
#             {"role":"system", "content": "you are a virtual assistant named friday skilled in genral tests like alexa and google cloud"},
#             {"role": "user", "content": command}
#     ]
#     )
#     return (completion.choices[0].message)




def processcommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles:
                speak(article["title"])

    else:
        output = aiprocess(c)
        speak(output)
        
    

if __name__ == "__main__":
    speak("initializing friday...")
    while True:
        #  lister for the wake word billy
        # obtain audio from the microphone
        r = sr.Recognizer()
        print("recognizing...")


        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_sphinx(audio)
            if(word.lower() == "friday"):
                speak("yes peanut..")
                with sr.Microphone() as source:
                    print("friday activated.... ")
                    audio = r.listen(source)
                    command = r.recognize_sphinx(audio)

                    processcommand(command)

            
            print("Sphinx thinks you said " + r.recognize_sphinx(audio))
        except Exception as e:
            print(" sorry;{0}".format(e))
            


