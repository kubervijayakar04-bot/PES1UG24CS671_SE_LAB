"""
Basket: the player-controlled catcher at the bottom of the screen.
"""

import pygame


class Basket:
    def __init__(self, x, y, width=90, height=24, speed=5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Normal and boosted movement speeds.
        self.normal_speed = speed
        self.boost_speed = speed * 2
        self.speed = self.normal_speed

        # Boost state.
        self.boosted_frames = 0

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2),
            int(self.y - self.height / 2),
            self.width,
            self.height,
        )

    def activate_boost(self, duration_frames=180):
        """
        Activate the temporary speed boost.

        At 60 FPS, 180 frames is about 3 seconds.
        """
        self.boosted_frames = duration_frames
        self.speed = self.boost_speed

    def update(self):
        """Update the temporary boost timer."""
        if self.boosted_frames > 0:
            self.boosted_frames -= 1

            if self.boosted_frames == 0:
                self.speed = self.normal_speed

    def is_boost_active(self):
        return self.boosted_frames > 0