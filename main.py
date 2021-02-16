import pygame
import sys
import random

def draw_floor():
    screen.blit(floor_surface, (floor_xpos, 570))
    screen.blit(floor_surface, (floor_xpos+500, 570))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (700, random_pipe_pos-150))
    return top_pipe, bottom_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.top >= 0:
            screen.blit(pipe_surface, pipe)
        else:
            flipedpipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flipedpipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False

    if bird_rect.top <= 0 or bird_rect.bottom >= 570:
        death_sound.play()
        return False
    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement*3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state != 'game_over':
        if score <= 0: score_surface = font.render('0', True, (255, 255, 255))
        else: score_surface = font.render(str(score), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (250, 30))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        if score <= 0: score_surface = font.render('Score: 0', True, (255, 255, 255))
        else: score_surface = font.render(f'Score: {score}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (250, 30))
        screen.blit(score_surface, score_rect)

        high_score_surface = font.render(f'High Score: {high_score}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center = (250, 550))
        screen.blit(high_score_surface, high_score_rect)


pygame.init()
screen = pygame.display.set_mode((500, 720))
clock = pygame.time.Clock()

#Getting the high score
f = open('high.txt', 'r+')
high = f.readlines()
high = high[-1]
high_score = int(high)

# Game variables
gravity = 0.25
bird_movement = 0.0
floor_xpos = 0
game_active = False
score = -1
reset_score = False

# Font
font = pygame.font.Font('04B_19.ttf', 32)


# Surfaces
bg_surface = pygame.image.load('images/background-day.png').convert()
bg_surface = pygame.transform.scale(bg_surface, (500, 720))
night_surface = pygame.image.load('images/background-night.png').convert()
night_surface = pygame.transform.scale(night_surface, (500, 720))

floor_surface = pygame.image.load('images/base.png').convert()
floor_surface = pygame.transform.scale(floor_surface, (500, 150))

bird_downflap = pygame.image.load('images/bluebird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('images/bluebird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('images/bluebird-upflap.png').convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100, 300))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 100)

pipe_surface = pygame.image.load('images/pipe-green.png').convert()
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1000)

pipe_height = [350, 450, 250]

# Game over screen
game_over_surface = pygame.image.load('images/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (250, 360))

# Sounds
flap_sound = pygame.mixer.Sound('sounds/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sounds/sfx_die.wav')
hit_sound = pygame.mixer.Sound('sounds/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sounds/sfx_point.wav')

#takes whatever is beofre update() and updates it every loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if high_score == int(high[-1]): pass
            else:
                f.write('\n')
                f.write(str(high_score))
                f.close()
            pygame.quit()
            sys.exit()

        if event.type == pygame.FINGERUP:
            if event.key == pygame.FINGERUP and game_active:
                bird_movement = 0
                bird_movement -= 7
                flap_sound.play()
            if event.key == pygame.FINGERUP and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 360)
                bird_movement = 0

        if event.type == SPAWNPIPE and game_active:
            pipe_list.extend(create_pipe())
            if score >=0: score_sound.play()
            score += 1
            

        if event.type == BIRDFLAP:
            bird_index += 1
            if bird_index > 2: bird_index = 0
            bird_surface, bird_rect = bird_animation()
    
    screen.blit(bg_surface, (0, 0))

    if game_active:
        if reset_score:
            reset_score = False
            score = -1
        #bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)

        # Collisions
        game_active = check_collision(pipe_list)

        # pipes 
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        score_display('')
    else:
        screen.blit(game_over_surface, game_over_rect)
        if score > high_score: high_score = score
        score_display('game_over')
        pipe_list.clear()
        reset_score = True


    # Floor
    floor_xpos -= 1
    draw_floor()
    if floor_xpos <= -500:
        floor_xpos = 0

    pygame.display.update()
    clock.tick(120)

