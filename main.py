import pygame
import sys

screen = pygame.display.set_mode((300, 300))

bg_color = (255, 255, 255)

pygame.display.set_caption('Pokemon Card Game')

screen.fill(bg_color)

pygame.display.flip()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            pygame.quit()
            sys.exit()