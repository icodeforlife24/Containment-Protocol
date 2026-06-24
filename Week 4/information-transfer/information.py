import pygame
import random
import math

# =========================
# CONFIG
# =========================

WIDTH = 1200
HEIGHT = 800

NUM_BOIDS = 200

VISION_RADIUS = 80
VISION_ANGLE = 120

SEPARATION_RADIUS = 25
COMM_RADIUS = 20

SEPARATION_FORCE = 0.1
ALIGNMENT_STRENGTH = 0.03
COHESION_STRENGTH = 0.01

MAX_SPEED = 2

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boids - Information Spread")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)


# =========================
# BOID
# =========================

class Boid:

    def __init__(self):

        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)

        angle = random.uniform(0, 2 * math.pi)

        self.vx = math.cos(angle)
        self.vy = math.sin(angle)

        self.informed = False

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

    def flock(self, boids):

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

            self.vx += align_x * ALIGNMENT_STRENGTH
            self.vy += align_y * ALIGNMENT_STRENGTH

            self.vx += coh_x * COHESION_STRENGTH
            self.vy += coh_y * COHESION_STRENGTH

        self.vx += sep_x * SEPARATION_FORCE
        self.vy += sep_y * SEPARATION_FORCE

        speed = math.hypot(self.vx, self.vy)

        if speed > MAX_SPEED:

            self.vx = self.vx / speed * MAX_SPEED
            self.vy = self.vy / speed * MAX_SPEED

    def spread_information(self, boids):

        if not self.informed:
            return

        for other in boids:

            if other is self:
                continue

            if other.informed:
                continue

            dx = other.x - self.x
            dy = other.y - self.y

            dist = math.hypot(dx, dy)

            if dist < COMM_RADIUS:

                other.informed = True

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

        color = (
            (0, 255, 0)
            if self.informed
            else (255, 255, 255)
        )

        pygame.draw.polygon(
            screen,
            color,
            [p1, p2, p3]
        )


# =========================
# CREATE BOIDS
# =========================

boids = [Boid() for _ in range(NUM_BOIDS)]

# Initial informed agent
boids[0].informed = True


# =========================
# MAIN LOOP
# =========================

running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_q]:
        SEPARATION_FORCE += 0.001

    if keys[pygame.K_a]:
        SEPARATION_FORCE = max(
            0,
            SEPARATION_FORCE - 0.001
        )

    if keys[pygame.K_w]:
        ALIGNMENT_STRENGTH += 0.001

    if keys[pygame.K_s]:
        ALIGNMENT_STRENGTH = max(
            0,
            ALIGNMENT_STRENGTH - 0.001
        )

    if keys[pygame.K_e]:
        COHESION_STRENGTH += 0.0001

    if keys[pygame.K_d]:
        COHESION_STRENGTH = max(
            0,
            COHESION_STRENGTH - 0.0001
        )

    # Flocking

    for boid in boids:
        boid.flock(boids)

    # Information Spread

    for boid in boids:
        boid.spread_information(boids)

    # Movement

    for boid in boids:
        boid.update()

    # Draw

    screen.fill((20, 20, 20))

    for boid in boids:
        boid.draw(screen)

    informed_count = sum(
        boid.informed
        for boid in boids
    )

    txt = font.render(
        f"Informed: {informed_count}/{NUM_BOIDS}",
        True,
        (255, 255, 255)
    )

    screen.blit(txt, (10, 10))

    pygame.display.flip()

pygame.quit()