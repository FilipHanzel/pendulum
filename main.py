from collections import deque
from typing import Union

import pygame
import click

from pendulum import Pendulum
from double_pendulum import DoublePendulum


class DrawDoublePendulum:
    def __init__(self, surface, pendulum, trace):
        self.surface = surface
        self.pendulum = pendulum
        self.trace = trace

        self.trace_buffer_first_bob = deque()
        self.trace_buffer_second_bob = deque()

    def __call__(self):
        pendulum_position = (self.pendulum.x, self.pendulum.y)
        first_bob_position = (self.pendulum.first_bob.x, self.pendulum.first_bob.y)
        second_bob_position = (self.pendulum.second_bob.x, self.pendulum.second_bob.y)

        # Draw pendulum
        pygame.draw.aalines(
            surface=self.surface,
            color=(255, 255, 255),
            closed=False,
            points=(
                pendulum_position,
                first_bob_position,
                second_bob_position,
            ),
        )

        # Update trace buffers
        self.trace_buffer_first_bob.append(first_bob_position)
        self.trace_buffer_second_bob.append(second_bob_position)

        if len(self.trace_buffer_first_bob) > self.trace:
            self.trace_buffer_first_bob.popleft()
            self.trace_buffer_second_bob.popleft()

        # Draw trace buffers
        if len(self.trace_buffer_first_bob) > 1:
            pygame.draw.aalines(
                self.surface, (0, 255, 0), False, self.trace_buffer_first_bob
            )
            pygame.draw.aalines(
                self.surface, (255, 0, 0), False, self.trace_buffer_second_bob
            )


class DrawPendulum:
    def __init__(self, surface, pendulum, trace):
        self.surface = surface
        self.pendulum = pendulum
        self.trace = trace

        self.trace_buffer = deque()

    def __call__(self):
        pendulum_position = (self.pendulum.x, self.pendulum.y)
        bob_position = (self.pendulum.bob_x, self.pendulum.bob_y)

        # Draw pendulum
        pygame.draw.aaline(
            self.surface,
            (255, 255, 255),
            pendulum_position,
            bob_position,
        )

        # Update trace buffer
        self.trace_buffer.append(bob_position)

        if len(self.trace_buffer) > self.trace:
            self.trace_buffer.popleft()

        # Draw trace buffer
        if len(self.trace_buffer) > 1:
            pygame.draw.aalines(
                surface=self.surface,
                color=(0, 255, 0),
                closed=False,
                points=self.trace_buffer,
            )


def run(pendulum: Union[Pendulum, DoublePendulum], trace: int = 500):
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Pendulum")

    if isinstance(pendulum, DoublePendulum):
        draw = DrawDoublePendulum(screen, pendulum, trace)
    elif isinstance(pendulum, Pendulum):
        draw = DrawPendulum(screen, pendulum, trace)
    else:
        raise ValueError("pendulum must be an instance of Pendulum or DoublePendulum")

    clock = pygame.time.Clock()

    update_time = 1 / 60
    time_passed = 0
    end = False
    while not end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True

        time_passed += clock.tick() / 1000
        while time_passed > update_time:
            pendulum.update()
            time_passed -= update_time

        screen.fill((0, 0, 0))
        draw()
        pygame.display.flip()

    pygame.quit()


@click.group()
def cli():
    pass


@cli.command("pendulum")
def run_pendulum():
    run(
        Pendulum(
            x=400,
            y=400,
            arm_length=5,
            angle=3,
        ),
        trace=1000,
    )


@cli.command("double-pendulum")
def run_double_pendulum():
    run(
        DoublePendulum(
            x=400,
            y=200,
            first_arm_length=5,
            second_arm_length=5,
            first_angle=3.0,
            second_angle=3.0,
            first_mass=10,
            second_mass=10,
        ),
        trace=3000,
    )


if __name__ == "__main__":
    cli()
