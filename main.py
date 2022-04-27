import pygame

from pendulum import Pendulum


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Pendulum")

    clock = pygame.time.Clock()

    pendulum = Pendulum(400, 400, 5, 3)

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

        pygame.draw.aaline(
            screen,
            (255, 255, 255),
            (pendulum.x, pendulum.y),
            (pendulum.bob_x, pendulum.bob_y),
        )

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
