import pygame, sys
from pygame.locals import *
import pygame.camera
import random

pygame.init()
pygame.camera.init()


def takePicture():
    numPic = random.randint(0, 100000)
    cam = pygame.camera.Camera("/dev/video0", (150, 150))
    cam.start()
    image = cam.get_image()
    path = "bilde"+str(numPic)+".png"
    pygame.image.save(image, path)
    cam.stop()
    return path

