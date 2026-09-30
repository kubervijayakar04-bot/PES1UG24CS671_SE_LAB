"""
GameEngine: owns the basket and all falling objects.

This version includes:
- Task 1: fixed collision handling
- Task 2: improved basket boundaries
- Task 3: controlled object spawning
- Task 4: temporary basket speed boost
"""

import random
import pygame

from game.basket import Basket
from game.falling_object import FallingObject
from game.collision import is_caught
from game.renderer import WIDTH, HEIGHT


# Task 3: controlled spawning
MIN_SPAWN_INTERVAL_FRAMES = 35
MAX_SPAWN_INTERVAL_FRAMES = 65
MAX_OBJECTS = 5
MIN_SPAWN_DISTANCE = 80

MAX_MISSES = 5


class GameEngine:
    def __init__(self):
        self.basket = Basket(x=WIDTH / 2, y=HEIGHT - 30)
        self.objects = []

        self.frames_until_spawn = 0
        self.last_spawn_x = None

        self.score = 0
        self.misses = 0
        self.game_over = False

    def _spawn_object(self):
        # Keep the complete falling object inside the screen width.
        min_x = 14
        max_x = WIDTH - 14

        x = random.randint(min_x, max_x)

        # Avoid repeatedly spawning near the previous object.
        if self.last_spawn_x is not None:
            attempts = 0

            while (
                abs(x - self.last_spawn_x) < MIN_SPAWN_DISTANCE
                and attempts < 10
            ):
                x = random.randint(min_x, max_x)
                attempts += 1

        self.objects.append(
            FallingObject(x=x, y=-14, speed=3)
        )

        self.last_spawn_x = x

    def handle_input(self, keys_pressed):
        if self.game_over:
            return

        # Task 2: smooth movement while the key is held.
        if keys_pressed[pygame.K_LEFT]:
            self.basket.x -= self.basket.speed

        if keys_pressed[pygame.K_RIGHT]:
            self.basket.x += self.basket.speed

        # Keep the entire basket inside the screen.
        self.basket.x = max(
            self.basket.width / 2,
            min(
                WIDTH - self.basket.width / 2,
                self.basket.x
            )
        )

    def handle_keydown(self, key):
        # Restart after game over.
        if self.game_over and key == pygame.K_r:
            self.__init__()
            return

        # Task 4: activate temporary speed boost with Space.
        if not self.game_over and key == pygame.K_SPACE:
            self.basket.activate_boost()

    def update(self):
        if self.game_over:
            return

        # Task 4: update the temporary boost timer.
        self.basket.update()

        # Task 3: varied spawn timing and maximum object limit.
        self.frames_until_spawn -= 1

        if (
            self.frames_until_spawn <= 0
            and len(self.objects) < MAX_OBJECTS
        ):
            self._spawn_object()

            self.frames_until_spawn = random.randint(
                MIN_SPAWN_INTERVAL_FRAMES,
                MAX_SPAWN_INTERVAL_FRAMES
            )

        # Update all falling objects.
        for obj in self.objects:
            obj.update()

        # Task 1: iterate over a copy so removing objects
        # does not cause another catchable object to be skipped.
        basket_rect = self.basket.get_rect()

        for obj in self.objects[:]:
            if is_caught(basket_rect, obj):
                self.score += 1
                self.objects.remove(obj)

        # Count missed objects.
        missed = [
            obj for obj in self.objects
            if obj.is_past_bottom(HEIGHT)
        ]

        if missed:
            self.objects = [
                obj for obj in self.objects
                if not obj.is_past_bottom(HEIGHT)
            ]

            self.misses += len(missed)

            if self.misses >= MAX_MISSES:
                self.game_over = True

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(
            surface,
            self.basket,
            self.objects
        )

        renderer.draw_text(
            surface,
            font,
            f"Score: {self.score}",
            (10, 10)
        )

        renderer.draw_text(
            surface,
            font,
            f"Misses: {self.misses}/{MAX_MISSES}",
            (10, 36)
        )

        # Task 4: clearly show when boost is active.
        if self.basket.is_boost_active():
            renderer.draw_text(
                surface,
                font,
                "BOOST ACTIVE!",
                (10, 62)
            )

        if self.game_over:
            renderer.draw_banner(
                surface,
                font,
                f"Game Over! Final score: {self.score}. Press R to restart."
            )