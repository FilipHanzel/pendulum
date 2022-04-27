import pygame
import click
from typing import Union

from pendulum import Pendulum
from double_pendulum import DoublePendulum


def run(pendulum: Union[Pendulum, DoublePendulum]):
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Pendulum")

    clock = pygame.time.Clock()

    update_time = 1 / 60
    time_passed = 0
    end = False
    while not end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True

        screen.fill((0, 0, 0))

        time_passed += clock.tick() / 1000
        while time_passed > update_time:
            pendulum.update()
            time_passed -= update_time

        if isinstance(pendulum, DoublePendulum):
            pygame.draw.aalines(
                surface=screen,
                color=(255, 255, 255),
                closed=False,
                points=(
                    (pendulum.x, pendulum.y),
                    (pendulum.first_bob.x, pendulum.first_bob.y),
                    (pendulum.second_bob.x, pendulum.second_bob.y),
                ),
            )
        else:
            pygame.draw.aaline(
                screen,
                (255, 255, 255),
                (pendulum.x, pendulum.y),
                (pendulum.bob_x, pendulum.bob_y),
            )

        pygame.display.flip()

    pygame.quit()


@click.group()
def cli():
    pass


@cli.command("pendulum")
def run_pendulum():
    run(Pendulum(x=400, y=400, arm_length=5, angle=3))


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
        )
    )


if __name__ == "__main__":
    cli()
