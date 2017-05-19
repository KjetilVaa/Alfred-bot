import sys, os
import pyttsx

engine = pyttsx.init()


def say(text):
    print("kjorer")
    engine.say(text)
    engine.runAndWait()
