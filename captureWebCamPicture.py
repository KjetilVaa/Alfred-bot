import pygame, sys
from pygame.locals import *
import pygame.camera

pygame.init()
pygame.camera.init()

def takePicture():
    cam = pygame.camera.Camera("/dev/video0", (352, 288))
    cam.start()
    image = cam.get_image()
    pygame.image.save(image, "bilde.png")
    cam.stop()
    return "bilde.png"

