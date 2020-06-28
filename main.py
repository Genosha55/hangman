import pygame
import os

# set display
pygame.init()
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")

# load images
images = []
for i in range(6):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)

# game variables
hangman_status = 4

# colors
WHITE = (255,255,255)

# setup game loop
FPS = 60
clock = pygame.time.Clock()
run = True

while run:
    clock.tick(FPS) # set the clock to tick at this speed

    win.fill(WHITE)
    win.blit(images[hangman_status],(150,100))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            print(pos)

pygame.quit()