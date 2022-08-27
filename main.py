from __future__ import annotations
from py.ball import Ball
import pygame
from time import time_ns
pygame.init()
screen = pygame.display.set_mode([1000, 1000])
b = [Ball() for _ in range(5000)]

while True:
    now = time_ns()
    # Quit the game when the window is closed. 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)


    # Fill the background with white
    screen.fill((0, 0, 0))

    # For every ball...
    for ball in b:
        # Move it
        ball.move(16) # TODO: prevent lost time with time module.
        # And draw it to the screen.
        pygame.draw.circle(screen, **ball.render())

    # Render
    pygame.display.flip()
    # print((time_ns() - now) / 1000000)