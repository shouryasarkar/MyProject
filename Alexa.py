# Lets build Alexa together, ok Habla? :*

import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import os, cv2

# Regular expression support
import re

# Mainly for platform (OS) info
import platform

# Get the OS the script is running on;
# useful for syscalls or platform
# specific commands
__OS__ = platform.system()

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def take_command():
    command = ''
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                # print(command)
    except Exception as e:
        print(e)
    return command


def talk(text):
    engine.say(text)
    engine.runAndWait()

def run_alexa():
    command = take_command()
    print(command)

    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)
        
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
    
    """ Random interactions """
    elif 'joke' in command:
        talk(pyjokes.get_joke())
        
    elif 'are you single' in command:
        talk('I am in a relationship with wifi')
        
    elif 'what is my name' in command:
        talk('Your name is Shourya Sarkar')
    
    elif 'how is your day going' in command:
        talk('Excellent,and yours??')
    
    # Run Wikipedia query
    elif 'who is' in command or 'what is' in command:
        query = re.compile('who|what is').sub('', command).strip()
        info = wikipedia.summary(query, 1)
        print(info)
        talk(info)
        
    elif "shut down" in command:
      
        if "pc" in command or "computer" in commmand:
            talk("Powering off your computer")
            if  __OS__ == 'Windows':
                # Assuming user is administrator;
                # no checks for failure
                os.system("shutdown /s /t 1")
            elif __OS__ == 'Linux':
                # POSIX shutdown does not have second-level
                # granularity, hence falling back to sleep
                process_code = os.system("sleep 1 && shutdown now")
                if process_code == 1:
                    print("Shutdown unsuccessful; insufficient permissions")
                    talk("You do not have sufficient permissions to shut down the computer")

        else:
            talk("I can only shutdown your computer as of now.")
            
    elif "selfie" in command:
        vid = cv2.VideoCapture(0)
        while (True):
            ret, frame = vid.read()
            if ret:
                name = 'Habla_selfie.jpg'
                print('Creating... ' + name)
                cv2.imwrite(name, frame)
                break
            else:
                break
        vid.release()
        cv2.destroyAllWindows()
        
    elif "open" in command and "camera" in command:
        vid = cv2.VideoCapture(0)
        while (True):
            ret, frame = vid.read()
            if ret:
                cv2.imshow('camera', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
        vid.release()
        cv2.destroyAllWindows()

while True:
    run_alexa()
