from math import cos, sin
from collections import namedtuple


G = 9.8
TICK = 1 / 60


class Bob:
    __slots__ = ["x", "y", "arm_length", "angle", "velocity", "acceleration", "mass"]

    def __init__(self, x, y, arm_length, angle, velocity, acceleration, mass):
        self.x = x
        self.y = y
        self.arm_length = arm_length
        self.angle = angle
        self.velocity = velocity
        self.acceleration = acceleration
        self.mass = mass


class DoublePendulum:
    __slots__ = ["x", "y", "first_bob", "second_bob"]

    def __init__(
        self,
        x: int,
        y: int,
        first_arm_length: int,
        second_arm_length: int,
        first_angle: float,
        second_angle: float,
        first_mass: int,
        second_mass: int,
    ):
        self.x = x
        self.y = y
        self.first_bob = None
        self.first_bob = None

        self.first_bob = Bob(
            x=None,
            y=None,
            arm_length=first_arm_length,
            angle=first_angle,
            velocity=0,
            acceleration=0,
            mass=first_mass,
        )
        self.second_bob = Bob(
            x=None,
            y=None,
            arm_length=second_arm_length,
            angle=second_angle,
            velocity=0,
            acceleration=0,
            mass=second_mass,
        )

        self.update()

    def update(self):
        a = self.first_bob
        b = self.second_bob

        a.acceleration = (
            -G * (2 * a.mass + b.mass) * sin(a.angle)
            - b.mass * G * sin(a.angle - 2 * b.angle)
            - 2
            * sin(a.angle - b.angle)
            * b.mass
            * (
                b.velocity**2 * b.arm_length
                + a.velocity**2 * a.arm_length * cos(a.angle - b.angle)
            )
        ) / (
            a.arm_length
            * (2 * a.mass + b.mass - b.mass * cos(2 * a.angle - 2 * b.angle))
        )
        b.acceleration = (
            2
            * sin(a.angle - b.angle)
            * (
                a.velocity**2 * a.arm_length * (a.mass + b.mass)
                + G * (a.mass + b.mass) * cos(a.angle)
                + b.velocity**2 * b.arm_length * b.mass * cos(a.angle - b.angle)
            )
        ) / (
            b.arm_length
            * (2 * a.mass + b.mass - b.mass * cos(2 * a.angle - 2 * b.angle))
        )

        a.velocity += a.acceleration * TICK
        a.angle += a.velocity * TICK
        a.x = a.arm_length * 50 * sin(a.angle) + self.x
        a.y = a.arm_length * 50 * cos(a.angle) + self.y

        b.velocity += b.acceleration * TICK
        b.angle += b.velocity * TICK
        b.x = b.arm_length * 50 * sin(b.angle) + a.x
        b.y = b.arm_length * 50 * cos(b.angle) + a.y
