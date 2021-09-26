import pygame
import os

# Importation des images, background et variables dimensions de l'écran

WIDTH, HEIGHT = 600, 700
red_sprite = pygame.image.load(os.path.join("assets", "red_sprite.png"))
green_sprite = pygame.image.load(os.path.join("assets", "green_sprite.png"))
blue_sprite = pygame.image.load(os.path.join("assets", "blue_sprite.png"))
yellow_sprite = pygame.image.load(os.path.join("assets", "yellow_sprite.png"))

red_laser = pygame.image.load(os.path.join("assets", "red_laser.png"))
green_laser = pygame.image.load(os.path.join("assets", "green_laser.png"))
blue_laser = pygame.image.load(os.path.join("assets", "blue_laser.png"))
yellow_laser = pygame.image.load(os.path.join("assets", "yellow_laser.png"))

BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background_lava.jpg")), (WIDTH, HEIGHT))
