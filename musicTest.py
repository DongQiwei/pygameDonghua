import pygame
import sys
from pygame.locals import *
pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("bg_music.ogg")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play()

cat_sound = pygame.mixer.Sound()

