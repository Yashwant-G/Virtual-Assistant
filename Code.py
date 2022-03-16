import pyttsx3 
import speech_recognition as sr  
import datetime
import wikipedia 
import webbrowser
import os
import smtplib

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def greeting(name):
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        greet="morning "

    elif hour >= 12 and hour < 18:
        greet="afternoon "
    else:
        greet="evening "

    name="Hey, Good "+greet+name
    speak(name)
    speak("My name is Iris, your Personal Virtual Assistant. Please tell me how may I help you")

def takeCommand():
    # It takes microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nPlease speak now, I am Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"I listened this: {query}\n")

    except Exception as e:
        print("Could not understand, please say that again...")
        return "None"
    return query


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login("user's mailaddress", "user's password")
    server.sendmail("user's mailaddress", to, content)
    server.close()


if __name__ == "__main__":
    speak("Please say your name: ")
    name=takeCommand()
    greeting(name)
    while True:
        query = takeCommand().lower()
        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            speak("Opening Youtube")
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open("google.in")

        elif 'open stackoverflow' in query:
            speak("Opening Stack Overflow")
            webbrowser.open("stackoverflow.com")

        elif 'play music' in query:
            music_dir = 'path of music folder'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
            print(f"Sir, the time is {strTime}")

        elif 'open game' in query:
            gamePath = "gamename.exe file path here"
            os.startfile(gamePath)

        elif 'finish' in query:
            print("Okay, thanks for using me, bye")
            speak("Okay, thanks for using me, bye")
            break

        elif 'email to' in query:
            try:
                speak("Say the message you want to send")
                content = takeCommand()
                to = input("enter email address of the receiver")
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry, I was not able to send this email due to some error, please try again")
