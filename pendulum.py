from math import cos, sin


G = 9.8
TICK = 1 / 60


class Pendulum:
    __slots__ = (
        "x",
        "y",
        "bob_x",
        "bob_y",
        "bob_mass",
        "arm_length",
        "angle",
        "velocity",
        "acceleration",
    )

    def __init__(self, x: int, y: int, arm_length: int, angle: float):
        self.x = x
        self.y = y
        self.arm_length = arm_length
        self.angle = angle
        self.velocity = 0
        self.acceleration = 0
        self.bob_x = None
        self.bob_y = None

        self.update()

    def update(self):
        self.acceleration = -G / self.arm_length * sin(self.angle)
        self.velocity += self.acceleration * TICK
        self.angle += self.velocity * TICK

        self.bob_x = self.arm_length * 50 * sin(self.angle) + self.x
        self.bob_y = self.arm_length * 50 * cos(self.angle) + self.y
