
# zombie_information_simulator.py
import pygame, random, math
from collections import deque

WIDTH, HEIGHT = 1200, 800
NUM_BOIDS = 150

VISION_RADIUS = 80
VISION_ANGLE = 120
SEPARATION_RADIUS = 25

SEPARATION_FORCE = 0.09
ALIGNMENT_STRENGTH = 0.02
COHESION_STRENGTH = 0.01

ZOMBIE_DETECT_RADIUS = 180
INFO_RADIUS = 40
INFO_PROBABILITY = 0.5
INFO_COOLDOWN = 5.0

ESCAPE_FORCE = 0.80
CHASE_FORCE = 0.20

MAX_HUMAN_SPEED = 4
MAX_ZOMBIE_SPEED = 5

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Information Simulator")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

start_time = pygame.time.get_ticks()


class Boid:
    def __init__(self):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)

        ang = random.uniform(0, 2 * math.pi)
        self.vx = math.cos(ang)
        self.vy = math.sin(ang)

        self.infected = False
        self.informed = False
        self.info_timer = 0.0

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
            math.acos(max(-1, min(1, dot / (dist * speed + 1e-6))))
        )

        return angle < VISION_ANGLE / 2

    def detect_zombies(self, boids):
        if self.infected:
            return

        for other in boids:
            if not other.infected:
                continue

            d = math.hypot(other.x - self.x, other.y - self.y)

            if d < ZOMBIE_DETECT_RADIUS:
                self.informed = True
                self.info_timer = INFO_COOLDOWN
                return

    def share_information(self, boids):
        if self.infected or not self.informed:
            return

        for other in boids:
            if other is self:
                continue

            if other.infected:
                continue

            if other.informed:
                continue

            d = math.hypot(other.x - self.x, other.y - self.y)

            if d < INFO_RADIUS:
                if random.random() < INFO_PROBABILITY:
                    other.informed = True
                    other.info_timer = INFO_COOLDOWN

    def avoid_zombies(self, boids):
        sx = sy = 0

        for other in boids:
            if not other.infected:
                continue

            dx = self.x - other.x
            dy = self.y - other.y

            dist = math.hypot(dx, dy)

            if 0 < dist < ZOMBIE_DETECT_RADIUS:
                strength = (ZOMBIE_DETECT_RADIUS - dist) / ZOMBIE_DETECT_RADIUS
                sx += (dx / dist) * strength
                sy += (dy / dist) * strength

        return sx, sy

    def chase_humans(self, boids):
        nearest = None
        best = 1e18

        for other in boids:
            if other.infected:
                continue

            d = math.hypot(other.x - self.x, other.y - self.y)

            if d < best:
                best = d
                nearest = other

        if nearest:
            dx = nearest.x - self.x
            dy = nearest.y - self.y
            d = math.hypot(dx, dy)

            if d > 0:
                self.vx += dx / d * CHASE_FORCE
                self.vy += dy / d * CHASE_FORCE

    def infect(self, boids):
        if not self.infected:
            return

        for other in boids:
            if other.infected:
                continue

            d = math.hypot(other.x - self.x, other.y - self.y)

            if d < 10:
                other.infected = True
                other.informed = False

    def flock(self, boids):

        if self.infected:
            self.chase_humans(boids)
            return

        sep_x = sep_y = 0
        align_x = align_y = 0
        coh_x = coh_y = 0
        count = 0

        for other in boids:

            if other is self or other.infected:
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

            coh_x /= count
            coh_y /= count

            align_x -= self.vx
            align_y -= self.vy

            coh_x -= self.x
            coh_y -= self.y

            self.vx += align_x * ALIGNMENT_STRENGTH
            self.vy += align_y * ALIGNMENT_STRENGTH

            self.vx += coh_x * COHESION_STRENGTH
            self.vy += coh_y * COHESION_STRENGTH

        self.vx += sep_x * SEPARATION_FORCE
        self.vy += sep_y * SEPARATION_FORCE

        if self.informed:
            zx, zy = self.avoid_zombies(boids)
            self.vx += zx * ESCAPE_FORCE
            self.vy += zy * ESCAPE_FORCE

    def update(self, dt):

        if self.informed:
            self.info_timer -= dt
            if self.info_timer <= 0:
                self.informed = False

        max_speed = MAX_ZOMBIE_SPEED if self.infected else MAX_HUMAN_SPEED

        speed = math.hypot(self.vx, self.vy)

        if speed > max_speed:
            self.vx = self.vx / speed * max_speed
            self.vy = self.vy / speed * max_speed

        self.x += self.vx
        self.y += self.vy

        self.x %= WIDTH
        self.y %= HEIGHT

    def draw(self, surface):

        angle = math.atan2(self.vy, self.vx)
        size = 10 if self.infected else 8

        p1 = (self.x + math.cos(angle) * size,
              self.y + math.sin(angle) * size)

        p2 = (self.x + math.cos(angle + 2.5) * size,
              self.y + math.sin(angle + 2.5) * size)

        p3 = (self.x + math.cos(angle - 2.5) * size,
              self.y + math.sin(angle - 2.5) * size)

        if self.infected:
            color = (255, 60, 60)
        elif self.informed:
            color = (255, 255, 0)
        else:
            color = (255, 255, 255)

        pygame.draw.polygon(surface, color, [p1, p2, p3])


def count_groups(boids):
    humans = [b for b in boids if not b.infected]

    if not humans:
        return 0, 0

    visited = set()
    groups = []

    for i in range(len(humans)):
        if i in visited:
            continue

        q = deque([i])
        visited.add(i)
        size = 0

        while q:
            cur = q.popleft()
            size += 1

            for j in range(len(humans)):
                if j in visited:
                    continue

                d = math.hypot(
                    humans[cur].x - humans[j].x,
                    humans[cur].y - humans[j].y
                )

                if d < VISION_RADIUS:
                    visited.add(j)
                    q.append(j)

        groups.append(size)

    return len(groups), sum(groups) / len(groups)


boids = [Boid() for _ in range(NUM_BOIDS)]
boids[0].infected = True

collapse_time = None
max_informed = 0

running = True

while running:

    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for b in boids:
        b.detect_zombies(boids)

    for b in boids:
        b.share_information(boids)

    for b in boids:
        b.flock(boids)

    for b in boids:
        b.infect(boids)

    for b in boids:
        b.update(dt)

    humans = sum(not b.infected for b in boids)
    zombies = NUM_BOIDS - humans
    informed = sum(b.informed for b in boids if not b.infected)

    max_informed = max(max_informed, informed)

    survival_rate = humans / NUM_BOIDS * 100

    groups, avg_group_size = count_groups(boids)

    if humans == 0 and collapse_time is None:
        collapse_time = (pygame.time.get_ticks() - start_time) / 1000

    screen.fill((20, 20, 20))

    for b in boids:
        b.draw(screen)

    lines = [
        f"Humans: {humans}",
        f"Zombies: {zombies}",
        f"Survival Rate: {survival_rate:.1f}%",
        f"Groups: {groups}",
        f"Avg Group Size: {avg_group_size:.1f}",
        f"Informed (Yellow): {informed}",
        f"Max Informed: {max_informed}",
    ]

    if collapse_time is not None:
        lines.append(f"Collapse Time: {collapse_time:.2f}s")

    for i, txt in enumerate(lines):
        screen.blit(font.render(txt, True, (255,255,255)),
                    (10, 10 + i * 25))

    pygame.display.flip()

pygame.quit()
