import pygame
import random
from pygame.locals import *
from sys import exit
import time

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
WIDTH = 1280
HEIGHT = 720
SCORE_MAX = 10
PROBABILITY = 93

size = (WIDTH, HEIGHT)
pygame.init()

#Initial Menu

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Inicial Menu")
option_play_font = pygame.font.Font('assets/PressStart2P.ttf',50)
option_play_text = option_play_font.render('Press Space to Start!',True,COLOR_WHITE)
option_play_text_rect = option_play_text.get_rect()
option_play_text_rect.center = (screen.get_width()/2,360)
screen.blit(option_play_text,option_play_text_rect)
pygame.display.flip()

# score text 1
score_font = pygame.font.Font('assets/PressStart2P.ttf', 110)
score_text = score_font.render('0', True, COLOR_WHITE, COLOR_BLACK)
score_text_rect = score_text.get_rect()
score_text_rect.center = (275, 90)

# score text 2
score_text2 = score_font.render('0', True, COLOR_WHITE, COLOR_BLACK)
score_text_rect2 = score_text2.get_rect()
score_text_rect2.center = (915, 90)

# draw middle bar
middle_bar = pygame.image.load("assets/middle_bar.png")
middle_bar_x = 640
middle_bar_y = 1
# align the middle bar to the center of the screen more accurately
middle_bar_center = ((screen.get_width() / 2) - middle_bar.get_width())

# victory text
result_font = pygame.font.Font('assets/PressStart2P.ttf', 100)
victory_text = result_font.render('VICTORY', True, COLOR_WHITE, COLOR_BLACK)
victory_text_rect = score_text.get_rect()
victory_text_rect.center = (550, 350)

# lose text
lose_text = result_font.render('DEFEAT', True, COLOR_WHITE, COLOR_BLACK)
lose_text_rect = score_text.get_rect()
lose_text_rect.center = (550, 350)

# sound effects
bounce_wall_sound_effect = pygame.mixer.Sound('assets/bounce_wall.wav')
bounce_table_sound_effect = pygame.mixer.Sound('assets/bounce_table.wav')
scoring_sound_effect = pygame.mixer.Sound('assets/score.wav')


class Player:
    def __int__(self, position_x, position_y, moving_down, moving_up, speed_y, score):
        self.position_x = position_x
        self.position_y = position_y
        self.moving_down = moving_down
        self.moving_up = moving_up
        self.speed_y = speed_y
        self.score = score


player_1_img = pygame.image.load("assets/player.png")
player_1 = Player()
player_1.position_x = 50
player_1.position_y = 300
player_1.moving_up = False
player_1.moving_down = False
player_1.speed_y = 12
player_1.score = 0

player_2_img = pygame.image.load("assets/player.png")
player_2 = Player()
player_2.position_x = 1230
player_2.position_y = 300
player_2.speed_y = 6
player_2.score = 0

# ball
ball = pygame.image.load("assets/ball.png")
ball_position_x = 640
ball_position_y = 360
ball_speed_x_default = 6
ball_speed_y_default = 6
ball_speed_x = ball_speed_x_default * random.choice([-1, 1])
ball_speed_y = ball_speed_y_default
ball_speed_extremity = 7
ball_speed_middle = 5

# game loop
game_clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                pygame.display.flip()
                pygame.display.set_caption("MyPong - PyGame Edition - 2023-12-12")
                game_loop = True

                while game_loop:
                    var_sleep = 0
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            exit()
                        if event.type == KEYDOWN:
                            if event.key == K_w:
                                player_1.moving_up = True
                            if event.key == K_s:
                                player_1.moving_down = True

                        if event.type == KEYUP:
                            if event.key == K_w:
                                player_1.moving_up = False
                            if event.key == K_s:
                                player_1.moving_down = False
                        elif event.type == KEYDOWN:
                            if event.key == K_ESCAPE:
                                pygame.display.quit()

                    # checking the victory condition
                    if player_1.score < SCORE_MAX and player_2.score < SCORE_MAX:
                        screen.fill(COLOR_BLACK)
                        # player 1 collides with upper wall
                        if player_1.position_y <= 0:
                            player_1.position_y = 0
                        # player 1 collides with lower wall
                        elif player_1.position_y >= 660:
                            player_1.position_y = 660
                        # player 2 collides with upper wall
                        if player_2.position_y <= 0:
                            player_2.position_y = 0
                        # player 2 collides with lower wall
                        elif player_2.position_y >= 660:
                            player_2.position_y = 660

                        # ball collision with the players
                        if ball_position_y <= player_2.position_y + 60 and ball_position_y + 12 >= player_2.position_y:
                            if ball_position_x + 12 >= player_2.position_x:
                                bounce_table_sound_effect.play()
                                ball_speed_y = ball_speed_extremity
                                ball_speed_x = ball_speed_extremity
                                l1 = player_2.position_y + 28
                                l2 = player_2.position_y + 32
                                if (ball_speed_y > 0 and ball_position_y + 11 < l1) or (ball_speed_y < 0 and ball_position_y > l2):
                                    ball_speed_y *= - 1
                                elif ball_position_y + 11 < l1:
                                    ball_speed_y = -1
                                elif ball_position_y > l2:
                                    ball_speed_y = ball_speed_y_default
                                else:
                                    ball_speed_y = 0
                                    ball_speed_x = ball_speed_middle

                                if ball_speed_x > 0:
                                    ball_speed_x *= -1

                        if ball_position_y <= player_1.position_y + 60 and ball_position_y + 12 >= player_1.position_y:
                            if ball_position_x <= player_1.position_x + 14:
                                bounce_table_sound_effect.play()
                                ball_speed_y = ball_speed_extremity
                                ball_speed_x = ball_speed_extremity
                                l1 = player_1.position_y + 28
                                l2 = player_1.position_y + 32
                                if (ball_speed_y > 0 and ball_position_y + 11 < l1) or (ball_speed_y < 0 and ball_position_y > l2):
                                    ball_speed_y *= - 1
                                elif ball_position_y + 11 < l1:
                                    ball_speed_y = -1
                                elif ball_position_y > l2:
                                    ball_speed_y = ball_speed_y_default
                                else:
                                    ball_speed_y = 0

                                if ball_speed_x < 0:
                                    ball_speed_x = ball_speed_middle
                                    ball_speed_x *= -1

                        # ball collision with the wall
                        if ball_position_y > 700 and ball_speed_y > 0:
                            ball_speed_y *= -1
                            bounce_wall_sound_effect.play()
                        elif ball_position_y <= 0 and ball_speed_y < 0:
                            ball_speed_y *= -1
                            bounce_wall_sound_effect.play()

                        # probability
                        prob = random.randint(1, 100)
                        if player_2.position_y > ball_position_y:
                            if prob <= PROBABILITY:
                                player_2.position_y -= player_2.speed_y
                        if player_2.position_y + 60 < ball_position_y + 12:
                            if prob <= PROBABILITY:
                                player_2.position_y += player_2.speed_y

                        # scoring points
                        if ball_position_x < 38:
                            direction_random = random.choice([-1, 1])
                            ball_speed_y = ball_speed_y_default * direction_random
                            ball_speed_x = ball_speed_x_default
                            if ball_speed_x > 0:
                                ball_speed_x *= -1
                            ball_position_x = 640
                            ball_position_y = random.randint(0, 720)
                            player_2.score += 1
                            scoring_sound_effect.play()
                            var_sleep = 1

                        elif ball_position_x > 1244:
                            direction_random = random.choice([-1, 1])
                            ball_speed_y = ball_speed_y_default * direction_random
                            ball_speed_x = ball_speed_x_default
                            if ball_speed_x < 0:
                                ball_speed_x *= -1
                            ball_position_x = 640
                            ball_position_y = random.randint(0, 720)
                            player_1.score += 1
                            PROBABILITY += 2
                            scoring_sound_effect.play()
                            var_sleep = 1
                        # player 1 movement
                        if player_1.moving_up:
                            player_1.position_y -= player_1.speed_y
                        if player_1.moving_down:
                            player_1.position_y += player_1.speed_y

                        # ball movement
                        ball_position_x = ball_position_x + ball_speed_x
                        ball_position_y = ball_position_y + ball_speed_y

                        # update score hud
                        score_text = score_font.render(str(player_1.score), True, COLOR_WHITE, COLOR_BLACK)
                        score_text2 = score_font.render(str(player_2.score), True, COLOR_WHITE, COLOR_BLACK)
                        screen.blit(ball, (ball_position_x, ball_position_y))
                        screen.blit(score_text, score_text_rect)
                        screen.blit(score_text2, score_text_rect2)
                        screen.blit(player_1_img, (player_1.position_x, player_1.position_y))
                        screen.blit(player_2_img, (player_2.position_x, player_2.position_y))
                        for cont in range(1, 20):
                            screen.blit(middle_bar, (middle_bar_center, middle_bar_y * cont))
                            middle_bar_y = 40
                    else:
                        # drawing victory
                        screen.fill(COLOR_BLACK)
                        screen.blit(score_text, score_text_rect)
                        screen.blit(score_text2, score_text_rect2)
                        if player_1.score>player_2.score:
                            screen.blit(victory_text, victory_text_rect)
                        else:
                            screen.blit(lose_text, lose_text_rect)
                    pygame.display.flip()
                    game_clock.tick(75)
                    if var_sleep == 1:
                        player_1.position_y = 300
                        player_2.position_y = 300
                        time.sleep(0.5)
