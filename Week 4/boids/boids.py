import pygame
import random
import math

# =========================
# CONFIG
# =========================

WIDTH = 1200
HEIGHT = 800

NUM_BOIDS = 100

VISION_RADIUS = 100
VISION_ANGLE = 120

SEPARATION_RADIUS = 25

SEPARATION_FORCE = 0.2
ALIGNMENT_STRENGTH = 0.05
COHESION_STRENGTH = 0.01

MAX_SPEED = 4
MAX_FORCE = 0.2

BG_COLOR = (20, 20, 20)
BOID_COLOR = (255, 255, 255)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boids Simulation")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)


# =========================
# BOID CLASS
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

        forward_mag = math.hypot(self.vx, self.vy)

        if forward_mag == 0:
            return True

        dot = dx * self.vx + dy * self.vy

        angle = math.degrees(
            math.acos(
                max(
                    -1,
                    min(
                        1,
                        dot / (dist * forward_mag + 1e-6)
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

            # ALIGNMENT
            align_x += other.vx
            align_y += other.vy

            # COHESION
            coh_x += other.x
            coh_y += other.y

            # SEPARATION
            if dist < SEPARATION_RADIUS:

                sep_x -= dx / dist
                sep_y -= dy / dist

        if count > 0:

            # Alignment
            align_x /= count
            align_y /= count

            align_x -= self.vx
            align_y -= self.vy

            # Cohesion
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

        # LIMIT FORCE
        force_mag = math.hypot(self.vx, self.vy)

        if force_mag > MAX_SPEED:

            self.vx = self.vx / force_mag * MAX_SPEED
            self.vy = self.vy / force_mag * MAX_SPEED

    def update(self):

        self.x += self.vx
        self.y += self.vy

        # WRAP SCREEN

        if self.x < 0:
            self.x = WIDTH

        elif self.x > WIDTH:
            self.x = 0

        if self.y < 0:
            self.y = HEIGHT

        elif self.y > HEIGHT:
            self.y = 0

    def draw(self, surface):

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
            surface,
            BOID_COLOR,
            [p1, p2, p3]
        )


# =========================
# INIT BOIDS
# =========================

boids = [Boid() for _ in range(NUM_BOIDS)]

# =========================
# MAIN LOOP
# =========================

running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False



    # ------------------
    # UPDATE
    # ------------------

    for boid in boids:
        boid.flock(boids)

    for boid in boids:
        boid.update()

    # ------------------
    # DRAW
    # ------------------

    screen.fill(BG_COLOR)

    for boid in boids:
        boid.draw(screen)

    text = font.render(
        f"Sep(Q/A): {SEPARATION_FORCE:.3f}   "
        f"Align(W/S): {ALIGNMENT_STRENGTH:.3f}   "
        f"Coh(E/D): {COHESION_STRENGTH:.4f}",
        True,
        (255, 255, 255)
    )

    screen.blit(text, (10, 10))

    pygame.display.flip()

pygame.quit()