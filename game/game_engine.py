import pygame
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height, paddle_sound, wall_sound, score_sound):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height,
                         paddle_sound, wall_sound, score_sound)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.game_over_font = pygame.font.SysFont("Arial", 60)

        self.game_over = False
        self.winner_text = ""
        self.winning_score = 5  # Default
        self.waiting_for_replay = False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if self.game_over:
            return  # Stop paddle movement after game over

        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        if self.game_over:
            return

        self.ball.move(self.player, self.ai)

        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.play_score_sound()
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.play_score_sound()
            self.ball.reset()

        self.ai.auto_track(self.ball, self.height)
        self.check_game_over()

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw scores
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

        # Draw game over / winner
        if self.game_over:
            text_surface = self.game_over_font.render(self.winner_text, True, WHITE)
            rect = text_surface.get_rect(center=(self.width//2, self.height//2 - 50))
            screen.blit(text_surface, rect)

        # Draw replay menu
        if self.waiting_for_replay:
            options = [
                "Press 3 for Best of 3",
                "Press 5 for Best of 5",
                "Press 7 for Best of 7",
                "Press ESC to Exit"
            ]
            for i, option in enumerate(options):
                option_surf = self.font.render(option, True, WHITE)
                screen.blit(option_surf, (self.width//2 - 120, self.height//2 + i*40))

    def check_game_over(self):
        if self.player_score >= self.winning_score:
            self.game_over = True
            self.winner_text = "Player Wins!"
            self.waiting_for_replay = True
        elif self.ai_score >= self.winning_score:
            self.game_over = True
            self.winner_text = "AI Wins!"
            self.waiting_for_replay = True

    def handle_replay_input(self, event):
        if not self.waiting_for_replay:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_3:
                self.winning_score = 3
                self.reset_game()
            elif event.key == pygame.K_5:
                self.winning_score = 5
                self.reset_game()
            elif event.key == pygame.K_7:
                self.winning_score = 7
                self.reset_game()
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    def reset_game(self):
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.player.y = self.height // 2 - self.paddle_height//2
        self.ai.y = self.height // 2 - self.paddle_height//2
        self.game_over = False
        self.waiting_for_replay = False
        self.winner_text = ""
