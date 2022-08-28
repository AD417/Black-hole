from __future__ import annotations
from py.ball import Ball
from py.player import Playerball
import pygame
from pygame import (
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    QUIT
)
from time import time_ns

from py.player import Playerball
pygame.init()
screen = pygame.display.set_mode([1000, 1000])
balls: list[Ball | Playerball] = [Ball() for _ in range(5)]

while True:
    now = time_ns()
    # Quit the game when the window is closed. 
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit(0)
        elif event.type == MOUSEBUTTONDOWN:
            balls += [Playerball(*pygame.mouse.get_pos())]
        elif event.type == MOUSEBUTTONUP:
            balls[-1].onmouseup()


    # Fill the background with white
    screen.fill((0, 0, 0))

    # For every ball...
    for ball in balls:
        # Move it
        ball.tick(16) # TODO: prevent lost time with time module.
        # And draw it to the screen.
        pygame.draw.circle(screen, **ball.render())

    # Render
    pygame.display.flip()
    # print((time_ns() - now) / 1000000)