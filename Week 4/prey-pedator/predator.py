import pygame
import random
import math

# =========================
# CONFIG
# =========================

WIDTH = 1200
HEIGHT = 800

NUM_PREY = 100
NUM_PREDATORS = 3

VISION_RADIUS = 80
VISION_ANGLE = 120

SEPARATION_RADIUS = 25

SEPARATION_FORCE = 0.05
ALIGNMENT_STRENGTH = 0.03
COHESION_STRENGTH = 0.03

PREDATOR_AVOID_RADIUS = 150
PREDATOR_AVOID_FORCE = 2

MAX_PREY_SPEED = 4
MAX_PREDATOR_SPEED = 6

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Predator-Prey Boids")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)


# =========================
# PREY BOID
# =========================

class Boid:

    def __init__(self):

        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)

        angle = random.uniform(0, 2 * math.pi)

        self.vx = math.cos(angle)
        self.vy = math.sin(angle)

    def in_vision(self, other):

        dx = other.x - self.x
        dy = other.y - self.y

        dist = math.hypot(dx, dy)

        if dist > VISION_RADIUS:
            return False

        speed = math.hypot(self.vx, self.vy)

        if speed == 0:
            return True

        dot = dx * self.vx + dy * self.vy

        angle = math.degrees(
            math.acos(
                max(
                    -1,
                    min(
                        1,
                        dot / (dist * speed + 1e-6)
                    )
                )
            )
        )

        return angle < VISION_ANGLE / 2

    def avoid_predators(self, predators):

        steer_x = 0
        steer_y = 0

        for predator in predators:

            dx = self.x - predator.x
            dy = self.y - predator.y

            dist = math.hypot(dx, dy)

            if 0 < dist < PREDATOR_AVOID_RADIUS:

                strength = (
                    PREDATOR_AVOID_RADIUS - dist
                ) / PREDATOR_AVOID_RADIUS

                steer_x += (dx / dist) * strength
                steer_y += (dy / dist) * strength

        return steer_x, steer_y

    def flock(self, boids, predators):

        sep_x = 0
        sep_y = 0

        align_x = 0
        align_y = 0

        coh_x = 0
        coh_y = 0

        count = 0

        for other in boids:

            if other is self:
                continue

            if not self.in_vision(other):
                continue

            dx = other.x - self.x
            dy = other.y - self.y

            dist = math.hypot(dx, dy)

            if dist < 1:
                continue

            count += 1

            align_x += other.vx
            align_y += other.vy

            coh_x += other.x
            coh_y += other.y

            if dist < SEPARATION_RADIUS:

                sep_x -= dx / dist
                sep_y -= dy / dist

        if count > 0:

            align_x /= count
            align_y /= count

            align_x -= self.vx
            align_y -= self.vy

            coh_x /= count
            coh_y /= count

            coh_x -= self.x
            coh_y -= self.y

        pred_x, pred_y = self.avoid_predators(predators)

        self.vx += sep_x * SEPARATION_FORCE
        self.vy += sep_y * SEPARATION_FORCE

        self.vx += align_x * ALIGNMENT_STRENGTH
        self.vy += align_y * ALIGNMENT_STRENGTH

        self.vx += coh_x * COHESION_STRENGTH
        self.vy += coh_y * COHESION_STRENGTH

        self.vx += pred_x * PREDATOR_AVOID_FORCE
        self.vy += pred_y * PREDATOR_AVOID_FORCE

        speed = math.hypot(self.vx, self.vy)

        if speed > MAX_PREY_SPEED:

            self.vx = self.vx / speed * MAX_PREY_SPEED
            self.vy = self.vy / speed * MAX_PREY_SPEED

    def update(self):

        self.x += self.vx
        self.y += self.vy

        self.x %= WIDTH
        self.y %= HEIGHT

    def draw(self, screen):

        angle = math.atan2(self.vy, self.vx)

        size = 8

        p1 = (
            self.x + math.cos(angle) * size,
            self.y + math.sin(angle) * size
        )

        p2 = (
            self.x + math.cos(angle + 2.5) * size,
            self.y + math.sin(angle + 2.5) * size
        )

        p3 = (
            self.x + math.cos(angle - 2.5) * size,
            self.y + math.sin(angle - 2.5) * size
        )

        pygame.draw.polygon(
            screen,
            (255, 255, 255),
            [p1, p2, p3]
        )


# =========================
# PREDATOR
# =========================

class Predator:

    def __init__(self):

        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)

        angle = random.uniform(0, 2 * math.pi)

        self.vx = math.cos(angle) * 2
        self.vy = math.sin(angle) * 2

    def chase(self, prey_list):

        nearest = None
        nearest_dist = float('inf')

        for prey in prey_list:

            dx = prey.x - self.x
            dy = prey.y - self.y

            dist = math.hypot(dx, dy)

            if dist < nearest_dist:

                nearest_dist = dist
                nearest = prey

        if nearest:

            dx = nearest.x - self.x
            dy = nearest.y - self.y

            dist = math.hypot(dx, dy)

            if dist > 0:

                self.vx += (dx / dist) * 0.15
                self.vy += (dy / dist) * 0.15

        speed = math.hypot(self.vx, self.vy)

        if speed > MAX_PREDATOR_SPEED:

            self.vx = self.vx / speed * MAX_PREDATOR_SPEED
            self.vy = self.vy / speed * MAX_PREDATOR_SPEED

    def update(self):

        self.x += self.vx
        self.y += self.vy

        self.x %= WIDTH
        self.y %= HEIGHT

    def draw(self, screen):

        angle = math.atan2(self.vy, self.vx)

        size = 12

        p1 = (
            self.x + math.cos(angle) * size,
            self.y + math.sin(angle) * size
        )

        p2 = (
            self.x + math.cos(angle + 2.5) * size,
            self.y + math.sin(angle + 2.5) * size
        )

        p3 = (
            self.x + math.cos(angle - 2.5) * size,
            self.y + math.sin(angle - 2.5) * size
        )

        pygame.draw.polygon(
            screen,
            (50, 120, 255),  # BLUE
            [p1, p2, p3]
        )


# =========================
# CREATE AGENTS
# =========================

prey = [
    Boid()
    for _ in range(NUM_PREY)
]

predators = [
    Predator()
    for _ in range(NUM_PREDATORS)
]


# =========================
# MAIN LOOP
# =========================

running = True

while running:

    clock.tick(60)


    # Update prey

    for boid in prey:
        boid.flock(prey, predators)

    for boid in prey:
        boid.update()

    # Update predators

    for predator in predators:
        predator.chase(prey)
        predator.update()

    # Draw

    screen.fill((20, 20, 20))

    for boid in prey:
        boid.draw(screen)

    for predator in predators:
        predator.draw(screen)

    text = font.render(
        f"Prey:{NUM_PREY}  Predators:{NUM_PREDATORS}  FPS:{int(clock.get_fps())}",
        True,
        (255, 255, 255)
    )

    screen.blit(text, (10, 10))

    pygame.display.flip()

pygame.quit()