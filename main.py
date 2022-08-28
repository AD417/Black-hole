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
# The framerate of the application. This program can run rather quickly. 
FPS = 100

class App():
    """
    The "Black Hole" Game, based on the game I shamefully ripped off from 
    http://scholtek.com/blackhole/,
    Which itself is inspired by a game called Super Fill-Up. 
    """
    def __init__(self: App) -> App:
        pygame.init()

        # The time of the last tick, in nanoseconds. Starts at initialization.
        self._last_tick: int = time_ns()
        # The time of the last frame, in nanoseconds. Starts at initialization. 
        self._last_frame: int = time_ns()
        # The balls placed in the level.
        self.game_balls: list[Ball] = [Ball() for _ in range(5)]
        # The balls that the player places. 
        self.player_balls: list[Playerball] = []
        # The "surface" on which the game is played.
        self.screen: pygame.Surface = pygame.display.set_mode([1000, 1000])

        self.tickdata = []

    def gameloop(self: App) -> None:
        # Event handler and mouse state checking. 
        for event in pygame.event.get():
            # Quitting the game.
            if event.type == QUIT:
                pygame.quit()
                exit(0)
            # Mouse click - start creating a new black hole. 
            elif event.type == MOUSEBUTTONDOWN:
                self.player_balls += [Playerball(*pygame.mouse.get_pos())]
            # Mouse release - stop expanding the most recent black hole. 
            elif event.type == MOUSEBUTTONUP:
                self.player_balls[-1].onmouseup()

        # This frame -- the time difference between this frame and the last frame
        # Will be used for timing purposes. 
        this_tick: int = time_ns()

        ### TICK PROCESSING:

        # Dt: the amount of time between frames.
        # 1 000 000 ns = 1ms. Calculations will be done in ms.
        dt: float = (this_tick - self._last_tick) / 1e6
        # Game balls.
        for ball in self.game_balls:
            ball.tick(dt)
        # Player balls.
        for ball in self.player_balls:
            ball.tick(dt)
        
        self._last_tick = this_tick
        self.tickdata += [dt]
        if len(self.tickdata) == 5000:
            print("%.0f" % (1000 * 5000 / sum(self.tickdata)))
            self.tickdata = []

        ### FRAME PROCESSING: 

        # Do not continue if not enough time has passed between frames. 
        if this_tick - self._last_frame < 1e9 // FPS:
            return

        # Reset the screen. 
        self.screen.fill((0, 0, 0))
        # Game balls.
        for ball in self.game_balls:
            pygame.draw.circle(self.screen, **ball.render())
        # Player balls.
        for ball in self.player_balls:
            pygame.draw.circle(self.screen, **ball.render())

        # Render
        pygame.display.flip()
        self._last_frame = this_tick

game: App = App()
while True:
    game.gameloop()