import sys, os
import pyttsx

engine = pyttsx.init()



def say(text):
    engine.say(text)
    engine.runAndWait()
