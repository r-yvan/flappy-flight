"""
Flappy Flight - Flappy Bird Game
A fully procedurally-generated Flappy Bird clone using Pygame.
All graphics are drawn with Pygame primitives — no external assets needed.
"""

import pygame
import random
import sys
import math

# Import config
try:
    from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_TITLE
except ImportError:
    SCREEN_WIDTH = 400
    SCREEN_HEIGHT = 600
    FPS = 60
    GAME_TITLE = "Flappy Flight - Flappy Bird"


# ─── Color Palette ───
class Colors:
    # Sky gradient
    SKY_TOP = (25, 25, 80)
    SKY_BOTTOM = (15, 15, 50)

    # Cyber theme
    NEON_GREEN = (0, 255, 128)
    NEON_BLUE = (0, 200, 255)
    NEON_PINK = (255, 0, 200)
    NEON_PURPLE = (180, 0, 255)
    DARK_BG = (10, 10, 30)

    # Pipe colors
    PIPE_BODY = (0, 180, 100)
    PIPE_BORDER = (0, 255, 140)
    PIPE_DARK = (0, 120, 70)

    # Bird colors
    BIRD_BODY = (0, 255, 200)
    BIRD_WING = (0, 200, 255)
    BIRD_EYE = (255, 255, 255)
    BIRD_PUPIL = (10, 10, 30)
    BIRD_BEAK = (255, 200, 0)

    # UI
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    SCORE_COLOR = (0, 255, 200)
    GAME_OVER_COLOR = (255, 50, 100)

    # Ground
    GROUND_TOP = (0, 100, 60)
    GROUND_BOTTOM = (0, 60, 40)
    GROUND_LINE = (0, 200, 120)

    # Particles
    PARTICLE_COLORS = [(0, 255, 128), (0, 200, 255), (255, 0, 200), (180, 0, 255)]


# ─── Particle System ───
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-5, -1)
        self.life = random.randint(15, 40)
        self.max_life = self.life
        self.size = random.randint(2, 5)
        self.color = random.choice(Colors.PARTICLE_COLORS)

    def update(self):
        self.x += self.vx
        self.vy += 0.15
        self.y += self.vy
        self.life -= 1

    def draw(self, surface):
        alpha = self.life / self.max_life
        r = max(0, int(self.color[0] * alpha))
        g = max(0, int(self.color[1] * alpha))
        b = max(0, int(self.color[2] * alpha))
        size = max(1, int(self.size * alpha))
        pygame.draw.circle(surface, (r, g, b), (int(self.x), int(self.y)), size)

    def is_dead(self):
        return self.life <= 0


# ─── Star Background ───
class Star:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT - 100)
        self.brightness = random.randint(50, 200)
        self.speed = random.uniform(0.1, 0.5)
        self.twinkle_speed = random.uniform(0.02, 0.08)
        self.twinkle_offset = random.uniform(0, math.pi * 2)

    def update(self, frame):
        self.x -= self.speed
        if self.x < 0:
            self.x = SCREEN_WIDTH
            self.y = random.randint(0, SCREEN_HEIGHT - 100)
        brightness = self.brightness + int(40 * math.sin(frame * self.twinkle_speed + self.twinkle_offset))
        brightness = max(30, min(255, brightness))
        return brightness

    def draw(self, surface, frame):
        b = self.update(frame)
        pygame.draw.circle(surface, (b, b, min(255, b + 20)), (int(self.x), int(self.y)), 1)


# ─── Bird ───
class Bird:
    def __init__(self):
        self.x = 80
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.gravity = 0.5
        self.jump_strength = -8
        self.size = 18
        self.angle = 0
        self.wing_frame = 0
        self.trail = []

    def jump(self):
        self.velocity = self.jump_strength

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

        # Angle based on velocity
        target_angle = max(-30, min(60, -self.velocity * 4))
        self.angle += (target_angle - self.angle) * 0.15

        # Wing animation
        self.wing_frame = (self.wing_frame + 0.3) % (math.pi * 2)

        # Trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > 12:
            self.trail.pop(0)

    def draw(self, surface):
        # Draw trail
        for i, (tx, ty) in enumerate(self.trail):
            alpha = i / len(self.trail) if self.trail else 0
            size = max(1, int(4 * alpha))
            color = (
                int(0 * alpha),
                int(255 * alpha),
                int(200 * alpha)
            )
            pygame.draw.circle(surface, color, (int(tx), int(ty)), size)

        # Body glow
        glow_surf = pygame.Surface((self.size * 4, self.size * 4), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (0, 255, 200, 30), (self.size * 2, self.size * 2), self.size * 2)
        surface.blit(glow_surf, (int(self.x - self.size * 2), int(self.y - self.size * 2)))

        # Main body
        pygame.draw.circle(surface, Colors.BIRD_BODY, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(surface, Colors.NEON_GREEN, (int(self.x), int(self.y)), self.size, 2)

        # Wing
        wing_offset = int(math.sin(self.wing_frame) * 6)
        wing_points = [
            (int(self.x - 5), int(self.y)),
            (int(self.x - 18), int(self.y + wing_offset - 4)),
            (int(self.x - 8), int(self.y + 5)),
        ]
        pygame.draw.polygon(surface, Colors.BIRD_WING, wing_points)
        pygame.draw.polygon(surface, Colors.NEON_BLUE, wing_points, 1)

        # Eye
        eye_x = int(self.x + 7)
        eye_y = int(self.y - 5)
        pygame.draw.circle(surface, Colors.BIRD_EYE, (eye_x, eye_y), 5)
        pygame.draw.circle(surface, Colors.BIRD_PUPIL, (eye_x + 2, eye_y), 3)
        # Eye shine
        pygame.draw.circle(surface, Colors.WHITE, (eye_x + 3, eye_y - 2), 1)

        # Beak
        beak_points = [
            (int(self.x + 15), int(self.y + 2)),
            (int(self.x + 25), int(self.y)),
            (int(self.x + 15), int(self.y + 6)),
        ]
        pygame.draw.polygon(surface, Colors.BIRD_BEAK, beak_points)

    def get_rect(self):
        return pygame.Rect(self.x - self.size + 4, self.y - self.size + 4,
                           self.size * 2 - 8, self.size * 2 - 8)


# ─── Pipe ───
class Pipe:
    WIDTH = 52
    GAP = 160

    def __init__(self, x):
        self.x = x
        self.gap_y = random.randint(120, SCREEN_HEIGHT - 200)
        self.speed = 3
        self.scored = False
        self.glow_intensity = 0

    def update(self):
        self.x -= self.speed
        self.glow_intensity = (self.glow_intensity + 0.05) % (math.pi * 2)

    def draw(self, surface):
        glow = int(20 * math.sin(self.glow_intensity))

        # Top pipe
        top_rect = pygame.Rect(self.x, 0, self.WIDTH, self.gap_y - self.GAP // 2)
        self._draw_pipe_segment(surface, top_rect, glow)

        # Bottom pipe
        bottom_y = self.gap_y + self.GAP // 2
        bottom_rect = pygame.Rect(self.x, bottom_y, self.WIDTH, SCREEN_HEIGHT - bottom_y)
        self._draw_pipe_segment(surface, bottom_rect, glow)

        # Pipe caps
        cap_height = 20
        cap_width = self.WIDTH + 8

        # Top pipe cap
        top_cap = pygame.Rect(self.x - 4, self.gap_y - self.GAP // 2 - cap_height,
                              cap_width, cap_height)
        self._draw_cap(surface, top_cap, glow)

        # Bottom pipe cap
        bottom_cap = pygame.Rect(self.x - 4, bottom_y, cap_width, cap_height)
        self._draw_cap(surface, bottom_cap, glow)

    def _draw_pipe_segment(self, surface, rect, glow):
        # Main body
        pygame.draw.rect(surface, Colors.PIPE_BODY, rect)

        # Gradient effect (vertical lines)
        for i in range(0, rect.width, 4):
            shade = max(0, min(255, Colors.PIPE_BODY[1] - 30 + i))
            color = (0, shade, int(shade * 0.6))
            line_rect = pygame.Rect(rect.x + i, rect.y, 2, rect.height)
            pygame.draw.rect(surface, color, line_rect)

        # Border glow
        border_color = (
            max(0, min(255, Colors.PIPE_BORDER[0] + glow)),
            max(0, min(255, Colors.PIPE_BORDER[1] + glow)),
            max(0, min(255, Colors.PIPE_BORDER[2] + glow)),
        )
        pygame.draw.rect(surface, border_color, rect, 2)

    def _draw_cap(self, surface, rect, glow):
        pygame.draw.rect(surface, Colors.PIPE_BODY, rect)
        border_color = (
            max(0, min(255, Colors.PIPE_BORDER[0] + glow)),
            max(0, min(255, Colors.PIPE_BORDER[1] + glow)),
            max(0, min(255, Colors.PIPE_BORDER[2] + glow)),
        )
        pygame.draw.rect(surface, border_color, rect, 2)
        # Highlight line
        highlight_rect = pygame.Rect(rect.x + 4, rect.y + 3, rect.width - 8, 3)
        pygame.draw.rect(surface, (0, 255, 160), highlight_rect)

    def is_offscreen(self):
        return self.x + self.WIDTH < 0

    def get_rects(self):
        top = pygame.Rect(self.x, 0, self.WIDTH, self.gap_y - self.GAP // 2)
        bottom_y = self.gap_y + self.GAP // 2
        bottom = pygame.Rect(self.x, bottom_y, self.WIDTH, SCREEN_HEIGHT - bottom_y)
        return [top, bottom]


# ─── Ground ───
class Ground:
    HEIGHT = 60

    def __init__(self):
        self.scroll = 0
        self.speed = 3

    def update(self):
        self.scroll = (self.scroll + self.speed) % 40

    def draw(self, surface):
        y = SCREEN_HEIGHT - self.HEIGHT

        # Ground body
        ground_rect = pygame.Rect(0, y, SCREEN_WIDTH, self.HEIGHT)
        pygame.draw.rect(surface, Colors.GROUND_BOTTOM, ground_rect)

        # Top strip
        pygame.draw.rect(surface, Colors.GROUND_TOP, (0, y, SCREEN_WIDTH, 10))

        # Scrolling grid pattern
        for i in range(-40 + int(-self.scroll), SCREEN_WIDTH + 40, 40):
            pygame.draw.line(surface, Colors.GROUND_LINE,
                             (i, y + 10), (i + 20, y + self.HEIGHT), 1)
            pygame.draw.line(surface, Colors.GROUND_LINE,
                             (i + 20, y + 10), (i, y + self.HEIGHT), 1)

        # Neon border line
        pygame.draw.line(surface, Colors.NEON_GREEN, (0, y), (SCREEN_WIDTH, y), 2)


# ─── Game Class ───
class FlappyBirdGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(GAME_TITLE)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        # Font
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 40)
        self.font_small = pygame.font.Font(None, 28)

        # Game state
        self.state = "menu"  # menu, playing, game_over
        self.score = 0
        self.high_score = 0
        self.frame = 0

        # Game objects
        self.bird = Bird()
        self.pipes = []
        self.ground = Ground()
        self.particles = []
        self.stars = [Star() for _ in range(60)]

        # Pipe spawn timer
        self.pipe_timer = 0
        self.pipe_interval = 90  # frames between pipes

    def reset(self):
        """Reset game state for new round."""
        self.bird = Bird()
        self.pipes = []
        self.particles = []
        self.score = 0
        self.pipe_timer = 0
        self.state = "playing"

    def handle_events(self):
        """Process input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

                if self.state == "menu":
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.reset()

                elif self.state == "playing":
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        self.bird.jump()
                        # Jump particles
                        for _ in range(5):
                            self.particles.append(Particle(self.bird.x, self.bird.y + 10))

                elif self.state == "game_over":
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.reset()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == "menu":
                    self.reset()
                elif self.state == "playing":
                    self.bird.jump()
                    for _ in range(5):
                        self.particles.append(Particle(self.bird.x, self.bird.y + 10))
                elif self.state == "game_over":
                    self.reset()

        return True

    def update(self):
        """Update game logic."""
        self.frame += 1
        self.ground.update()

        if self.state != "playing":
            return

        # Update bird
        self.bird.update()

        # Spawn pipes
        self.pipe_timer += 1
        if self.pipe_timer >= self.pipe_interval:
            self.pipes.append(Pipe(SCREEN_WIDTH + 20))
            self.pipe_timer = 0

        # Update pipes
        for pipe in self.pipes:
            pipe.update()

            # Score check
            if not pipe.scored and pipe.x + Pipe.WIDTH < self.bird.x:
                pipe.scored = True
                self.score += 1
                # Score particles
                for _ in range(10):
                    self.particles.append(
                        Particle(self.bird.x + 30, self.bird.y))

        # Remove offscreen pipes
        self.pipes = [p for p in self.pipes if not p.is_offscreen()]

        # Update particles
        for particle in self.particles:
            particle.update()
        self.particles = [p for p in self.particles if not p.is_dead()]

        # Collision detection
        bird_rect = self.bird.get_rect()

        # Ground collision
        if self.bird.y + self.bird.size >= SCREEN_HEIGHT - Ground.HEIGHT:
            self.game_over()
            return

        # Ceiling collision
        if self.bird.y - self.bird.size <= 0:
            self.bird.y = self.bird.size
            self.bird.velocity = 0

        # Pipe collision
        for pipe in self.pipes:
            for pipe_rect in pipe.get_rects():
                if bird_rect.colliderect(pipe_rect):
                    self.game_over()
                    return

    def game_over(self):
        """Handle game over."""
        self.state = "game_over"
        if self.score > self.high_score:
            self.high_score = self.score
        # Explosion particles
        for _ in range(30):
            self.particles.append(Particle(self.bird.x, self.bird.y))

    def draw_background(self):
        """Draw the cyber-themed scrolling background."""
        # Gradient sky
        for y in range(SCREEN_HEIGHT - Ground.HEIGHT):
            ratio = y / (SCREEN_HEIGHT - Ground.HEIGHT)
            r = int(Colors.SKY_TOP[0] + (Colors.SKY_BOTTOM[0] - Colors.SKY_TOP[0]) * ratio)
            g = int(Colors.SKY_TOP[1] + (Colors.SKY_BOTTOM[1] - Colors.SKY_TOP[1]) * ratio)
            b = int(Colors.SKY_TOP[2] + (Colors.SKY_BOTTOM[2] - Colors.SKY_TOP[2]) * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        # Stars
        for star in self.stars:
            star.draw(self.screen, self.frame)

        # Scrolling grid lines (Matrix effect)
        grid_offset = (self.frame * 2) % 40
        for x in range(0, SCREEN_WIDTH + 40, 40):
            adjusted_x = x - grid_offset
            color = (0, 30, 20)
            pygame.draw.line(self.screen, color,
                             (adjusted_x, 0), (adjusted_x, SCREEN_HEIGHT - Ground.HEIGHT))

    def draw_score(self):
        """Draw the current score."""
        # Score shadow
        score_text = self.font_large.render(str(self.score), True, (0, 100, 80))
        text_rect = score_text.get_rect(centerx=SCREEN_WIDTH // 2 + 2, y=52)
        self.screen.blit(score_text, text_rect)

        # Score main
        score_text = self.font_large.render(str(self.score), True, Colors.SCORE_COLOR)
        text_rect = score_text.get_rect(centerx=SCREEN_WIDTH // 2, y=50)
        self.screen.blit(score_text, text_rect)

    def draw_menu(self):
        """Draw the main menu."""
        # Title with glow effect
        glow = int(20 * math.sin(self.frame * 0.05))
        title_color = (0, max(0, min(255, 255 + glow)), max(0, min(255, 200 + glow)))

        title = self.font_large.render("Flappy Flight", True, title_color)
        title_rect = title.get_rect(centerx=SCREEN_WIDTH // 2, y=140)
        self.screen.blit(title, title_rect)

        # Subtitle
        sub = self.font_small.render("A Cybersecurity Simulation", True, Colors.NEON_BLUE)
        sub_rect = sub.get_rect(centerx=SCREEN_WIDTH // 2, y=200)
        self.screen.blit(sub, sub_rect)

        # Animated "Press SPACE" text
        alpha = int(128 + 127 * math.sin(self.frame * 0.08))
        start_color = (0, alpha, int(alpha * 0.8))
        start_text = self.font_medium.render("Press SPACE to Play", True, start_color)
        start_rect = start_text.get_rect(centerx=SCREEN_WIDTH // 2, y=350)
        self.screen.blit(start_text, start_rect)

        # High score
        if self.high_score > 0:
            hs = self.font_small.render(f"Best: {self.high_score}", True, Colors.NEON_PURPLE)
            hs_rect = hs.get_rect(centerx=SCREEN_WIDTH // 2, y=420)
            self.screen.blit(hs, hs_rect)

        # Controls hint
        hint = self.font_small.render("SPACE / Click to Flap", True, (100, 100, 120))
        hint_rect = hint.get_rect(centerx=SCREEN_WIDTH // 2, y=480)
        self.screen.blit(hint, hint_rect)

        # Floating bird on menu
        menu_bird_y = 280 + int(15 * math.sin(self.frame * 0.04))
        # Simple bird preview
        pygame.draw.circle(self.screen, Colors.BIRD_BODY,
                           (SCREEN_WIDTH // 2, menu_bird_y), 20)
        pygame.draw.circle(self.screen, Colors.NEON_GREEN,
                           (SCREEN_WIDTH // 2, menu_bird_y), 20, 2)
        # Eye
        pygame.draw.circle(self.screen, Colors.BIRD_EYE,
                           (SCREEN_WIDTH // 2 + 8, menu_bird_y - 5), 5)
        pygame.draw.circle(self.screen, Colors.BIRD_PUPIL,
                           (SCREEN_WIDTH // 2 + 10, menu_bird_y - 5), 3)

    def draw_game_over(self):
        """Draw the game over screen."""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        self.screen.blit(overlay, (0, 0))

        # Game Over text
        glow = int(20 * math.sin(self.frame * 0.1))
        go_color = (max(0, min(255, 255 + glow)), 50, 100)
        go_text = self.font_large.render("GAME OVER", True, go_color)
        go_rect = go_text.get_rect(centerx=SCREEN_WIDTH // 2, y=180)
        self.screen.blit(go_text, go_rect)

        # Score display
        score_label = self.font_medium.render(f"Score: {self.score}", True, Colors.NEON_GREEN)
        score_rect = score_label.get_rect(centerx=SCREEN_WIDTH // 2, y=270)
        self.screen.blit(score_label, score_rect)

        # High score
        hs_label = self.font_medium.render(f"Best: {self.high_score}", True, Colors.NEON_PURPLE)
        hs_rect = hs_label.get_rect(centerx=SCREEN_WIDTH // 2, y=320)
        self.screen.blit(hs_label, hs_rect)

        # New high score!
        if self.score == self.high_score and self.score > 0:
            new_hs = self.font_small.render("★ NEW HIGH SCORE! ★", True, Colors.BIRD_BEAK)
            new_rect = new_hs.get_rect(centerx=SCREEN_WIDTH // 2, y=370)
            self.screen.blit(new_hs, new_rect)

        # Restart hint
        alpha = int(128 + 127 * math.sin(self.frame * 0.08))
        restart_color = (0, alpha, int(alpha * 0.8))
        restart = self.font_small.render("Press SPACE to Restart", True, restart_color)
        restart_rect = restart.get_rect(centerx=SCREEN_WIDTH // 2, y=430)
        self.screen.blit(restart, restart_rect)

    def render(self):
        """Draw everything."""
        self.draw_background()

        # Draw pipes
        for pipe in self.pipes:
            pipe.draw(self.screen)

        # Draw ground
        self.ground.draw(self.screen)

        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)

        if self.state == "menu":
            self.draw_menu()
        elif self.state == "playing":
            self.bird.draw(self.screen)
            self.draw_score()
        elif self.state == "game_over":
            self.bird.draw(self.screen)
            self.draw_score()
            self.draw_game_over()

        pygame.display.flip()

    def run(self):
        """Main game loop."""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

        pygame.quit()


def start_game():
    """Entry point to start the Flappy Bird game."""
    game = FlappyBirdGame()
    game.run()


if __name__ == "__main__":
    start_game()
