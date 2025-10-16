import pygame
from game.game_engine import GameEngine

# Initialize pygame/Start application
pygame.init()
pygame.mixer.init()  # Initialize mixer for sounds

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Load sounds
PADDLE_HIT_SOUND = pygame.mixer.Sound("sounds/paddle_hit.wav")
WALL_BOUNCE_SOUND = pygame.mixer.Sound("sounds/wall_bounce.wav")
SCORE_SOUND = pygame.mixer.Sound("sounds/score.wav")

# Game loop
engine = GameEngine(WIDTH, HEIGHT, PADDLE_HIT_SOUND, WALL_BOUNCE_SOUND, SCORE_SOUND)

def main():
    running = True
    while running:
        SCREEN.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Check replay input if game over
            engine.handle_replay_input(event)

        engine.handle_input()
        engine.update()
        engine.render(SCREEN)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()



if __name__ == "__main__":
    main()
