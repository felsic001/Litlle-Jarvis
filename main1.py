import pyttsx3
import datetime
import requests
import speech_recognition as sr
import smtplib
from secret import senderemail, epwd, to
import pyautogui
import webbrowser as wb
from time import sleep
import wikipedia
import pywhatkit
from newsapi import NewsApiClient
import clipboard
import pyjokes
import time as tt
import psutil
from nltk.tokenize import word_tokenize

engine = pyttsx3.init()


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def getvoices(voice):
    voices = engine.getProperty('voices')
    # print(voices[2].id)
    if voice == 1:
        engine.setProperty('voice', voices[0].id)
        speak("Hello this is jarvis")
    if voice == 2:
        engine.setProperty('voice', voices[1].id)
        speak("Hello this is friday")


def time():
    Time = datetime.datetime.now().strftime("%I:%M:%S")  # hour= I,
    speak("The current time is: ")
    speak(Time)


def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    day = int(datetime.datetime.now().day)
    speak("The current date is")
    speak(day)
    speak(month)
    speak(year)


def greeting():
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        speak("Good morning sir!")
    elif hour >= 12 and hour < 18:
        speak("good afternoon sir!")
    elif hour >= 18 and hour < 24:
        speak("good evening sir!")
    else:
        speak("good night sir!")


def wishme():
    greeting()
    speak("Welcome sir!")
    # time()
    # date()
    speak("jarvis at your service, please tell me how can i help you!")


def takeCommandCMD():
    query = input("please tell me how can i help you?\n")
    return query


def takeCommandMic():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language="en-IN")
        print(query)
    except Exception as e:
        print(e)
        speak("Say that again Please....")
        return "None"
    return query


def sendEmail(receivermail, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(senderemail, epwd)
    server.sendmail(senderemail, receivermail, content)
    server.close()


def sendwhatsmsg(phone_no, message):
    Message = message
    wb.open('https://web.whatsapp.com/send?phone=' +phone_no+ '&text=' +Message)
    sleep(20)
    pyautogui.press('enter')


def searchgoogle():
    speak("What should I search sir?")
    search = takeCommandMic()
    wb.open('https://www.google.com/search?q='+search)


def news():
    newsapi = NewsApiClient(api_key='3eb266fc932d41349545299e9886741e')
    speak("on what topic do you want to hear the news sir?")
    newstopic = takeCommandMic()
    data = newsapi.get_top_headlines(q=newstopic,
                                     language='en',
                                     page_size=5)

    newsdata = data['articles']
    for x, y in enumerate(newsdata):
        print(f'{x}{y["description"]}')
        speak((f'{x}{y["description"]}'))

    speak("That's all for now I will update more in some time")


def text2speech():
    text = clipboard.paste()
    print(text)
    speak(text)


def screenshot():
    name_img = tt.time()
    name_img = f'C:\\Users\\Aditya\\PycharmProjects\\JarvisAI\\screenshot\\{name_img}.png'
    img = pyautogui.screenshot(name_img)
    img.show()


def cpu():
    usage = str(psutil.cpu_percent())
    speak('CPU is  at'+ usage)
    battery = psutil.sensors_battery()
    speak("Battery is at")
    speak(battery.percent)


if __name__ == "__main__":
    getvoices(1)
    wishme()
    wakeword = "jarvis"
    wakeword1 = "friday"
    while True:
        query = takeCommandMic().lower()
        query = word_tokenize(query)
        print(query)
        if wakeword or wakeword1 in query:
            if 'time' in query:
                time()
            elif 'date' in query:
                date()
            elif 'friday' in query:
                getvoices(2)
            elif 'email' in query:
                try:
                    speak('Please type the receiver email address Sir?')
                    receiveremail = takeCommandCMD()
                    speak('What should I say sir?')
                    content = takeCommandMic()
                    sendEmail(senderemail, content)
                    speak("Email has been sent sir")
                except Exception as e:
                    print(e)
                    speak("Unable to send the email")
            elif 'message' in query:
                user_name = {
                    'Aditya': '+919557072802',
                    'Jones': ''
                }
                try:
                    speak('To whom do you want to send the whatsapp message?')
                    name = takeCommandMic()
                    phone_no = user_name[name]
                    speak('What is the message sir?')
                    message = takeCommandMic()
                    sendwhatsmsg(phone_no, message)
                    speak("Message has been sent sir")
                except Exception as e:
                    print(e)
                    speak("Unable to send the message")

            elif 'wikipedia' in query:
                speak('what do you want to search?')
                query = takeCommandMic()
                result = wikipedia.summary(query, sentences = 2)
                print(result)
                speak(result)

            elif 'search' in query:
                searchgoogle()

            elif 'youtube' in query:
                speak("what should i search on youtube sir?")
                topic = takeCommandMic()
                pywhatkit.playonyt(topic)

            elif 'news' in query:
                news()

            elif 'read' in query:
                text2speech()

            elif 'joke' in query:
                speak(pyjokes.get_joke())

            elif 'screenshot' in query:
                screenshot()

            elif 'cpu' in query:
                cpu()


            elif 'offline' or 'bye' or 'sleep' in query:
                speak("goodbye sir, see you later")
                quit()







# wishme()
# while True:
#     voice = int(input("Press 1 for male voice \nPress 2 for female voice\n"))
#     # speak(audio)
#     getvoices(voice)
