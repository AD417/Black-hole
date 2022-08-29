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
        # If a ball is currently growing. 
        self.ball_is_growing: bool = False
        # The balls placed in the level.
        self.game_balls: list[Ball] = [Ball() for _ in range(5)]
        # The balls that the player places. 
        self.player_balls: list[Playerball] = []
        # The "surface" on which the game is played.
        self.screen: pygame.Surface = pygame.display.set_mode([1000, 1000])

        self.tickdata = []

    # This is the main game loop; keep it at the top of the class.
    def gameloop(self: App) -> None:
        # Event handler and mouse state checking. 
        for event in pygame.event.get():
            # Quitting the game.
            if event.type == QUIT:
                pygame.quit()
                exit(0)
            # Mouse click - start creating a new black hole. 
            elif event.type == MOUSEBUTTONDOWN:
                self.ball_is_growing = True
                self.player_balls += [Playerball(*pygame.mouse.get_pos())]
            # Mouse release - stop expanding the most recent black hole. 
            elif event.type == MOUSEBUTTONUP and self.ball_is_growing:
                self.ball_is_growing = False
                self.player_balls[-1].onmouseup()

        # This tick -- the time difference between this tick and the last tick
        # Will be used for timing purposes. 
        this_tick: int = time_ns()

        ### TICK PROCESSING:

        # Dt: the amount of time between frames.
        # 1 000 000 ns = 1ms. Calculations will be done in ms.
        dt: float = (this_tick - self._last_tick) / 1e6

        self.tick(dt)

        self._last_tick = this_tick

        ### FRAME PROCESSING: 

        # Do not continue if not enough time has passed between frames. 
        if this_tick - self._last_frame < 1e9 // FPS:
            return

        self.frame()

        self._last_frame = this_tick

    def frame(self: App) -> None:
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

    def tick(self: App, dt: float) -> None:
        """Process events that occur on every tick."""
        # Game balls.
        for i in range(len(self.game_balls)):
            ball = self.game_balls[i]
            ball.tick(dt)
            for other_ball in self.game_balls[i+1:]:
                if ball.collides_with(other_ball):
                    ball.process_collision_with(other_ball)
        # Player balls.
        for ball in self.player_balls:
            ball.tick(dt)
        # Check player collision with other balls.
        if self.ball_is_growing:
            active_ball = self.player_balls[-1]
            if active_ball.is_growing:
                for other_ball in self.game_balls:
                    # If the active ball hits another ball, then delete the active ball. 
                    if active_ball.collides_with(other_ball): 
                        self.player_balls.pop()
                        self.ball_is_growing = False
                        break
        
        # Debug tps shenanigans.
        self.tickdata += [dt]
        if len(self.tickdata) == 500:
            # If this value gets below 200, then we will have a problem with the framerate.
            # Value last time I checked: ~400tps. 
            print("%.0f" % (1000 * 500 / sum(self.tickdata)))
            self.tickdata = []

game: App = App()
while True:
    game.gameloop()