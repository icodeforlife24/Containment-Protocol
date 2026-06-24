import pygame
import random
import math

# ======================
# CONFIG
# ======================

WIDTH = 1200
HEIGHT = 800

NUM_BOIDS = 100

VISION_RADIUS = 80
VISION_ANGLE = 120

SEPARATION_RADIUS = 25

SEPARATION_FORCE = 0.08
ALIGNMENT_STRENGTH = 0.03
COHESION_STRENGTH = 0.01

OBSTACLE_FORCE = 0.25
OBSTACLE_MARGIN = 40

MAX_SPEED = 4

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boids with Obstacles")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)


# ======================
# OBSTACLE
# ======================

class Obstacle:

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, screen):

        pygame.draw.circle(
            screen,
            (220, 70, 70),
            (int(self.x), int(self.y)),
            self.radius
        )

        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (int(self.x), int(self.y)),
            self.radius,
            2
        )


# ======================
# BOID
# ======================

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

    def avoid_obstacles(self, obstacles):

        steer_x = 0
        steer_y = 0

        future_x = self.x + self.vx * 15
        future_y = self.y + self.vy * 15

        for obs in obstacles:

            dx = future_x - obs.x
            dy = future_y - obs.y

            dist = math.hypot(dx, dy)

            avoid_radius = obs.radius + OBSTACLE_MARGIN

            if 0 < dist < avoid_radius:

                strength = (avoid_radius - dist) / avoid_radius

                steer_x += (dx / dist) * strength
                steer_y += (dy / dist) * strength

        return steer_x, steer_y

    def flock(self, boids, obstacles):

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

        obs_x, obs_y = self.avoid_obstacles(obstacles)

        self.vx += sep_x * SEPARATION_FORCE
        self.vy += sep_y * SEPARATION_FORCE

        self.vx += align_x * ALIGNMENT_STRENGTH
        self.vy += align_y * ALIGNMENT_STRENGTH

        self.vx += coh_x * COHESION_STRENGTH
        self.vy += coh_y * COHESION_STRENGTH

        self.vx += obs_x * OBSTACLE_FORCE
        self.vy += obs_y * OBSTACLE_FORCE

        speed = math.hypot(self.vx, self.vy)

        if speed > MAX_SPEED:

            self.vx = self.vx / speed * MAX_SPEED
            self.vy = self.vy / speed * MAX_SPEED

    def update(self):

        self.x += self.vx
        self.y += self.vy

        if self.x < 0:
            self.x = WIDTH

        elif self.x > WIDTH:
            self.x = 0

        if self.y < 0:
            self.y = HEIGHT

        elif self.y > HEIGHT:
            self.y = 0

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


# ======================
# INIT
# ======================

boids = [Boid() for _ in range(NUM_BOIDS)]

obstacles = [
    Obstacle(400, 300, 50),
    Obstacle(800, 500, 70)
]

# ======================
# LOOP
# ======================

running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            mx, my = pygame.mouse.get_pos()

            obstacles.append(
                Obstacle(
                    mx,
                    my,
                    random.randint(30, 70)
                )
            )


    for boid in boids:
        boid.flock(boids, obstacles)

    for boid in boids:
        boid.update()

    screen.fill((20, 20, 20))

    for obs in obstacles:
        obs.draw(screen)

    for boid in boids:
        boid.draw(screen)

    txt = font.render(
        f"Sep(Q/A): {SEPARATION_FORCE:.3f}  "
        f"Align(W/S): {ALIGNMENT_STRENGTH:.3f}  "
        f"Coh(E/D): {COHESION_STRENGTH:.4f}",
        True,
        (255, 255, 255)
    )

    screen.blit(txt, (10, 10))

    pygame.display.flip()

pygame.quit()