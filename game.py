import pygame
import math
import random
import time
import os
from pygame import mixer

pygame.init()
# INITIALIZE FONTS
scoreboard = pygame.font.SysFont("ARIAL", 40, True)
gameover = pygame.font.SysFont("ARIAL", 170, True)

# INITIALIZE SOUNDS
bgm = "ON"
mixer.init()
laser = pygame.mixer.Sound("laser_sound.wav")
explosion = pygame.mixer.Sound("explosion_sound.wav")
explosion.set_volume(1)
dialogue = ["alien_dialogue 1.wav", "alien_dialogue 2.wav", "alien_dialogue 3.wav", "alien_mocklaugh.wav"]
alien_speech = pygame.mixer.Sound(dialogue[0])
alien_speech.set_volume(1)
alien_hurt = pygame.mixer.Sound("alien_scream 1.wav")
alien_hurt.set_volume(1)
bg_music = pygame.mixer.Sound("space_invadersbgm.wav")
bg_music.set_volume(0.2)
game_over_bgm = pygame.mixer.Sound("GAME OVER.wav")
game_over_bgm.set_volume(1)
menu_bgm = pygame.mixer.Sound("menu_bgm.wav")
menu_bgm.set_volume(1)

# INITIALIZE PLAY SCREEN DIMENSIONS
width, height = 1000, 700
# INITIALIZE MAIN SCREEN DIMENSIONS
m_width = 1500
m_height = 700
# width, height = pg.size()
screen = pygame.display.set_mode((m_width, m_height))

# ASSET SIZES
spaceship_and_energy_visinity = 90
spaceship_and_alien_visinity = 90
bullet_and_alien_visinity = 110
ship_size = 100
ship_bullet_size = 60
ss_index = 1
alien_size = 70
a_index = 0
a_dialogue_index = 0

# LOAD ASSETS
bullet_variants = ["spaceship_bullet.png", "spaceship_bullet2.png", "spaceship_bullet3.png"]
ship_variants = ["spaceship1.png", "spaceship2.png", "spaceship3.png", "spaceship4.png", "spaceship5.png",
                 "spaceship6.png"]

alien_variant = ["alien1.png", "alien2.png", "alien3.png", "alienship1.png", "alienship2.png"]

space_bg = pygame.image.load("SPACE.png", "BACKGROUND")
space_ship = pygame.image.load("spaceship1.png", "SPACE SHIP")
old_variant = space_ship = pygame.transform.scale(space_ship, (ship_size, ship_size))
space_ship_bullets = pygame.image.load("spaceship_bullet3.png", "SPACE SHIP BULLETS")
space_ship_bullets = pygame.transform.scale(space_ship_bullets, (ship_bullet_size, ship_bullet_size))
alien = pygame.image.load("alien1.png", "alien")
alien = pygame.transform.scale(alien, (alien_size, alien_size))
energy = pygame.image.load("ENERGY.png", "ENERGY")
energy_size = 80
energy = pygame.transform.scale(energy, (energy_size, energy_size))

# INITIALIZING GAME CONDITIONS
game = False
menu = True
life = 1
game_pause = False
game_status = "PLAY"

# ASSET SPEED AND DATA
max_speed, max_bspeed = 10, 10
alien_direction = 1
alien_count = 5
ship_speed = 3
bullet_speed = 7
bullets_coordinates = []
alien_speed = 2
alien_coordinates = []
alien_speed_level = 12
ship_change = False
init_a_speed = 3

# INITIALIZING PLAYER SPACESHIP'S POSITION
player_x = width // 2 - 50
player_y = height - 100  # height - 500

# INITIALIZING ALIEN'S POSITION
alien_x = 0
alien_y = 0

# INITIALIZING PLAYER SCORE
score = 0
prev_score = 0

# COLOR CHANGER
color = [(148, 0, 211),(148, 0, 211), (75, 0, 130),(75, 0, 130), (0, 0, 255),(0, 0, 255), (0, 255, 0),(0, 255, 0), (255, 255, 0),(255, 255, 0), (255, 127, 0),(255, 127, 0),(255, 0, 0), (255, 0, 0)]
color_index = -1

# ENERGY COIN POSTION
e_timer = 200
e_plot = False
e_taken = False
e_x = 0
e_y = 0
old_speed = 0
old_b_speed = 0


def initialize():
    global game, menu, life, game_pause, game_status, alien_direction, alien_count, ship_speed, bullet_speed
    global bullets_coordinates
    global alien_speed, alien_coordinates, alien_speed_level, ship_change, player_y, player_x
    global alien_x, alien_y, score, prev_score, color_index, e_timer, e_plot, e_y, e_x, old_speed
    global old_b_speed, e_taken
    global spaceship_and_alien_visinity, spaceship_and_energy_visinity, bullet_and_alien_visinity
    global ship_size, ship_bullet_size, ss_index, a_index, a_dialogue_index, max_speed, max_bspeed
    # INITIALIZING GAME CONDITIONS
    life = 1
    game_pause = False
    game_status = "PLAY"
    # ASSET SPEED AND DATA
    alien_direction = 1
    alien_count = 5
    ship_speed = 3
    bullet_speed = 7
    max_speed = 10
    max_bspeed = 10
    bullets_coordinates = []
    alien_speed = 2
    alien_coordinates = []
    alien_speed_level = 8
    ship_change = False

    # INITIALIZING PLAYER SPACESHIP'S POSITION
    player_x = width // 2 - 50
    player_y = height - 100  # height - 500

    # INITIALIZING ALIEN'S POSITION
    alien_x = 0
    alien_y = 0

    # INITIALIZING PLAYER SCORE
    score = 0
    prev_score = 0

    # COLOR CHANGER
    color_index = -1

    # ENERGY COIN POSTION
    e_timer = 200
    e_plot = False
    e_taken = False
    e_x = 0
    e_y = 0
    old_speed = 0
    old_b_speed = 0

    # ASSET SIZES
    spaceship_and_energy_visinity = 90
    spaceship_and_alien_visinity = 90
    bullet_and_alien_visinity = 50
    ship_size = 100
    ship_bullet_size = 60
    ss_index = 1
    a_index = 0
    a_dialogue_index = 0


def deploy_energy_coin():
    global ship_speed, width, height, e_x, e_y, screen, e_plot, energy, e_timer
    global e_taken, old_b_speed, old_speed, ship_speed, bullet_speed
    if not e_taken and e_timer < 200:
        e_timer += 1
        if not e_plot:
            e_x = random.randrange(0, width - energy_size)
            e_y = random.randrange(400, height - energy_size)
            e_plot = True
        screen.blit(energy, (e_x, e_y))
    else:
        e_timer += 1
        e_x = e_y = 0
        if e_timer == 1000:

            e_plot = False
            e_timer = 0
            if e_taken:
                e_taken = False
                ship_speed = old_speed
                bullet_speed = old_b_speed
                old_speed = old_b_speed = 0
                

def level():
    global space_ship, space_ship, score, ss_index, life, a_index, alien, alien_size, prev_score, alien_speed_level
    global ship_change, ship_speed, bullet_speed, old_variant, max_speed, max_bspeed
    try:
        if score % 500 == 0 and ss_index <= len(ship_variants) and score != prev_score and not e_taken:

            if ss_index >= len(ship_variants):
                ss_index = 0
                ship_speed = 3
                bullet_speed = 7
                
            
            space_ship = pygame.image.load(ship_variants[ss_index], "SPACE SHIP")
            space_ship = pygame.transform.scale(space_ship, (ship_size, ship_size))
            old_variant = space_ship
            ss_index += 1
            life += 2
            ship_speed += 1
            bullet_speed += 1
            prev_score = score
            ship_change = True
        
        if bullet_speed == max_bspeed and not e_taken:
            max_bspeed += 5
        if ship_speed == max_speed and not e_taken: 
            max_speed += 5
        if bullet_speed == 30 and not e_taken:
            bullet_speed = 7
        if ship_speed == 30 and not e_taken:
            ship_speed = 3
            
    except IndexError:
        
        ss_index = 0
        space_ship = pygame.image.load(ship_variants[ss_index], "SPACE SHIP")
        space_ship = pygame.transform.scale(space_ship, (ship_size, ship_size))
        ship_speed = 3
        bullet_speed = 7       

             


                


def is_spaceship_and_energy_coin_collision():
    global player_x, player_y, e_x, e_y, screen, e_timer, life, energy, e_taken
    global old_b_speed, old_speed, ship_speed, bullet_speed
    global e_plot
    try:
        if math.sqrt(math.pow((player_x + (ship_size // 2)) - (e_x + (energy_size // 2)), 2) + math.pow(
                (player_y + (ship_size // 2)) - (e_y + (energy_size // 2)),
                2)) < spaceship_and_energy_visinity and not e_taken and e_plot:
            e_taken = True
            e_plot = False
            e_x = 0
            e_y = 0
            old_speed = ship_speed
            old_b_speed = bullet_speed
            ship_speed = max_speed
            bullet_speed = max_bspeed
    except IndexError:
      
        return False    




def show_character():


    char = alien
    char = pygame.transform.scale(char, (100, 100))
    screen.blit(char, (1040, 220))
    ship_data = pygame.font.SysFont("ARIAL", 40, True)
    t = ship_data.render("Alien Speed:" + str(alien_speed), True, (255, 255, 255))
    screen.blit(t, (1200, 250))
    
    char = space_ship
    char = pygame.transform.scale(char, (100, 100))
    screen.blit(char, (1040, 350))
    ship_data = pygame.font.SysFont("ARIAL", 40, True)
    t = ship_data.render("Speed:" + str(ship_speed), True, (255, 255, 255))
    screen.blit(t, (1200, 350))
    t = ship_data.render("Bullet Speed:" + str(bullet_speed), True, (255, 255, 255))
    screen.blit(t, (1200, 400))
   


def instructions():
    global game_pause, bgm, game_status, color, color_index
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), (1010, 10, 480, 680), 2)
    instruct = pygame.font.SysFont("arial", 30, True)
    display = "INSTRUCTIONS:"
    t = instruct.render(display, True, (255, 255, 255))
    screen.blit(t, (1020, 20))

    instruct = pygame.font.SysFont("arial", 20, True)
    display = "1.USE DIRECTION KEYS TO CONTROL SPACESHIP"
    t = instruct.render(display, True, (255, 255, 255))
    screen.blit(t, (1020, 60))

    display = "2.PRESS SPACE TO FIRE"
    t = instruct.render(display, True, (255, 255, 255))
    screen.blit(t, (1020, 90))

    display = "3.PRESS 'P' TO PAUSE OR PLAY "
    t = instruct.render(display, True, (255, 255, 255))
    screen.blit(t, (1020, 120))

    display = "4.PRESS 'M' TO STOP OR START BACKGROUND "
    t = instruct.render(display, True, (255, 255, 255))
    screen.blit(t, (1020, 150))
    display = "AND GAME MUSIC"
    t = instruct.render(display, True, (255, 255, 255))
    screen.blit(t, (1030, 180))
  

    
    global color, color_index
    try:
        
        instruct = pygame.font.SysFont("arial", 35, True)
        display = "SPACE INVADERS"
        t = instruct.render(display, True, color[color_index])
        screen.blit(t, (1020, 610))

        instruct = pygame.font.SysFont("arial", 20, True)
        display = "DEVELOPED BY AADITYA PRABU K"
        text = instruct.render(display, True, color[color_index])
        screen.blit(text, (1020, 650))
        color_index += 1

        
    except IndexError :
        color_index = 0
        instruct = pygame.font.SysFont("arial", 35, True)
        display = "SPACE INVADERS"
        t = instruct.render(display, True, color[color_index])
        screen.blit(t, (1020, 610))

        instruct = pygame.font.SysFont("arial", 20, True)
        display = "DEVELOPED BY AADITYA PRABU K"
        text = instruct.render(display, True, color[color_index])
        screen.blit(text, (1020, 650))


        

    instruct = pygame.font.SysFont("arial", 25, True)
    display = "BGM : " + bgm
    text = instruct.render(display, True, (255, 255, 255))
    screen.blit(text, (1020, 550))
    instruct = pygame.font.SysFont("arial", 25, True)
    display = "GAME STATUS : " + game_status
    text = instruct.render(display, True, (255, 255, 255))
    screen.blit(text, (1020, 520))


def show_score_and_life():
    global score, screen, life
    text = scoreboard.render("SCORE:" + str(score), True, (255, 255, 255))
    screen.blit(text, (10, 10))
    text = scoreboard.render("LIFE:" + str(life), True, (255, 255, 255))
    screen.blit(text, (10, 50))




def isspaceship_collision():
    global player_x, player_y, alien_coordinates, life, ship_speed, space_ship
    global score
    a = alien_coordinates
    try:
        for i in range(len(a)):
            if math.sqrt(math.pow((player_x + (ship_size // 2)) - (a[i][0] + (alien_size // 2)), 2) + math.pow(
                    (player_y + (ship_size // 2)) - (a[i][1] + (alien_size // 2)),
                    2)) < spaceship_and_alien_visinity and life <= 1 and not e_taken:

                bg_music.stop()
                explosion.play()
                instructions()
                show_character()
                canvas()
                bullet_pop()
                move_and_draw_spaceship()
                move_and_draw_aliens()
                show_score_and_life()
                pygame.display.update()
               
                for i in range(10):
                    if i % 2 == 0:
                        space_ship = pygame.image.load("spaceship_explosion.png")
                        space_ship = pygame.transform.scale(space_ship, (100, 100))
                        screen.blit(space_ship, (player_x, player_y))
                        time.sleep(0.3)

                    else:
                        space_ship = pygame.image.load("spaceship_exploded.png")
                        space_ship = pygame.transform.scale(space_ship, (100, 100))
                        screen.blit(space_ship, (player_x, player_y))
                        time.sleep(0.3)
   
                    pygame.display.flip()
                time.sleep(1)
                return True

            elif math.sqrt(math.pow((player_x + (ship_size // 2)) - (a[i][0] + (alien_size // 2)), 2) + math.pow(
                    (player_y + (ship_size // 2)) - (a[i][1] + (alien_size // 2)),
                    2)) < spaceship_and_alien_visinity and e_taken:

                score+=50
                alien_hurt.play()
                alien_coordinates.pop(i)

            elif math.sqrt(math.pow((player_x + (ship_size // 2)) - (a[i][0] + (alien_size // 2)), 2) + math.pow(
                    (player_y + (ship_size // 2)) - (a[i][1] + (alien_size // 2)),
                    2)) < spaceship_and_alien_visinity and life > 1:

                alien_hurt.play()
                alien_coordinates.pop(i)
                life -= 1

    except IndexError:
        return False


def isbullet_collision():
    global bullets_coordinates, alien_coordinates, score
    b = bullets_coordinates
    a = alien_coordinates
    try:
        for i in range(len(b)):
            for j in range(len(a)):
                if math.sqrt(
                        math.pow((b[i][0] + (ship_bullet_size // 2)) - (a[j][0] + (alien_size // 2)), 2) + math.pow(
                            b[i][1]+(ship_bullet_size // 2) - (a[j][1] + alien_size), 2)) < bullet_and_alien_visinity:
                    alien_hurt.play()
                    alien_coordinates.pop(j)
                    bullets_coordinates.pop(i)
                    score += 50
                    return True

        return False

    except IndexError:
      
        return False


def deploy_aliens():
    global alien_coordinates, alien_speed, a_dialogue_index, alien_speech, dialogue, a_index, alien_speed_level, alien
    global prev_score, score, ship_change,init_a_speed
        
    if ship_change:
        ship_change = False
        if a_index < len(alien_variant) :
            alien = pygame.image.load(alien_variant[a_index], "alien")
            alien = pygame.transform.scale(alien, (alien_size, alien_size))
            a_index += 1
            alien_speed_level += 1
        else:
            a_index = 0
            alien_speed_level = 8
            alien_speed_level = random.randrange(4, 9)

    if alien_speed < alien_speed_level:
            alien_speed += 1
    else:
        alien_speed = init_a_speed
        
    alien_speech.play()
    time.sleep(0.09)
    alien_speech.play()

    if a_dialogue_index == len(dialogue) - 1:
        a_dialogue_index = 0

    else:
        a_dialogue_index += 1

    music = dialogue[a_dialogue_index]
    alien_speech = pygame.mixer.Sound(music)


    for i in range(alien_count):
        x = int(random.randrange(0, 800))
        y = int(random.randrange(0, 200))
        alien_coordinates.append([x, y])


def move_and_draw_aliens():
    global alien_direction, alien_coordinates,alien_speed,init_a_speed

    if alien_coordinates:

        for i in range(len(alien_coordinates)):
            x, y = alien_coordinates[i]
            screen.blit(alien, [x, y])
            if x + alien_size >= width and alien_direction == 1:
                alien_direction = -1

                for j in range(0, len(alien_coordinates)):
                    alien_coordinates[j] = [alien_coordinates[j][0], alien_coordinates[j][1] + 100]

            elif x <= 0 and alien_direction == -1:
                alien_direction = 1

                for j in range(0, len(alien_coordinates)):
                    alien_coordinates[j] = [alien_coordinates[j][0], alien_coordinates[j][1] + 100]

            elif alien_coordinates[i][1] >= height:
 
                alien_direction = 1
                alien_coordinates = []
                deploy_aliens()
                return

            if alien_direction == 1:
                x = x + alien_speed
            elif alien_direction == -1:
                x = x - alien_speed

            alien_coordinates[i][0] = x
            
    else:
        deploy_aliens()
        


def canvas():
    # TO DRAW THE CANVAS SCREEN
    global screen
    # screen.fill((0,0,0))
    screen.blit(space_bg, (0, 0))


def move_and_draw_spaceship():
    # TO DRAW STUFFS
    global space_ship, old_speed, old_b_speed, ship_speed, bullet_speed, old_variant
    if e_taken:
        space_ship = pygame.image.load("ultimate_spaceship.png", "ULTIMATE SPACESHIP")
        space_ship = pygame.transform.scale(space_ship, (100, 100))
        spl_power = pygame.font.SysFont("ARIAL", 20, True)
        text = spl_power.render("HYPER ATTACK MODE INITIATED", True, (255, 255, 255))
        screen.blit(text, (1200, 460))
    else:
        space_ship = old_variant

    screen.blit(space_ship, (player_x, player_y))
    pygame.draw.circle(screen, (255, 255, 0), (player_x + ship_size // 2, player_y + ship_size // 2), 5)


def bullet_push(x, y):
    global bullets_coordinates
    bullets_coordinates.append([x, y])
    laser.set_volume(0.1)
    laser.play()


def bullet_pop():
    global bullets_coordinates, ship_bullet_size, space_ship_bullets
    i = 0
    if e_taken:
        space_ship_bullets = pygame.image.load("spaceship_bullet.png")
        space_ship_bullets = pygame.transform.scale(space_ship_bullets, (ship_bullet_size, ship_bullet_size))
    else:
        space_ship_bullets = pygame.image.load("spaceship_bullet3.png")
        space_ship_bullets = pygame.transform.scale(space_ship_bullets, (ship_bullet_size, ship_bullet_size))
    if bullets_coordinates:
        while i < len(bullets_coordinates):
            x, y = bullets_coordinates[i]
            y = y - bullet_speed
            screen.blit(space_ship_bullets, (x, y))

            if y > 0:
                bullets_coordinates[i] = [x, y]
                i += 1
            else:
                bullets_coordinates.pop(0)
                i -= 1

            if i < 0:
                i = 0


# canvas()

# INITIALIZE FRAMES AND FOLDERPATH
FOLDER_PATH = "BG FRAMES"
images = os.listdir(FOLDER_PATH)
frame = 0


def game_menu():
    global menu, game
    instruct = pygame.font.SysFont("ARIAL", 80, True)
    menumessage = " WELCOME TO SPACE INVADERS"
    text = instruct.render(menumessage, True, (255, 255, 255))
    screen.blit(text, (200, 60))
    text = instruct.render(menumessage, True, (0, 255, 255))
    screen.blit(text, (200, 54))
    instruct = pygame.font.SysFont("ARIAL", 40, True)
    menumessage = " PRESS 'S' TO SAVE THE WORLD FROM ALIENS "
    text = instruct.render(menumessage, True, (255, 255, 255))
    screen.blit(text, (330, 300))
    text = instruct.render(menumessage, True, (255, 0, 255))
    screen.blit(text, (330, 298))
    instruct = pygame.font.SysFont("ARIAL", 30, True)
    menumessage = " PRESS 'E' TO EXIT TO END THE WORLD "
    text = instruct.render(menumessage, True, (255, 255, 255))
    screen.blit(text, (460, 500))
    text = instruct.render(menumessage, True, (255, 255, 0))
    screen.blit(text, (460, 497))


def play_bg_animation():
    global screen, menu, frame, game
    menu_bg = pygame.image.load("BG FRAMES\\" + str(images[frame]), "BACKGROUND GIF")
    screen.blit(menu_bg, (0, 0))
    frame += 1
    if frame == len(images) - 1:
        frame = 0
    game_menu()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            menu = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_e:
                menu = False
            elif e.key == pygame.K_s:
                game = True

    pygame.display.update()


count_down = pygame.mixer.Sound("alien_countdown.wav")
if __name__ == "__main__":

    play_bg_animation()
    menu_bgm.play()
    while menu:  # set to false bg_music.play()

        play_bg_animation()
        bg_music.stop()
        if game:
            
            menu_bgm.stop()
            initialize()
            count_down.play()
            screen.fill((0, 0, 0))
            time.sleep(0.3)
            pygame.display.update()
            instructions()
            time.sleep(0.5)
            pygame.display.update()
            time.sleep(1)
            canvas()
            pygame.display.update()
            time.sleep(1.5)
            move_and_draw_spaceship()
            pygame.display.update()
            time.sleep(2.4)
            bg_music.play()

        while game:
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    game = False
                elif events.type == pygame.KEYDOWN:
                    if events.key == pygame.K_SPACE:
                        bullet_push(player_x + 19, player_y)

                    if events.key == pygame.K_m:
                        if bgm == "ON":
                            bg_music.stop()
                            bgm = "OFF"
                        else:
                            bg_music.play()
                            bgm = "ON"

                    if events.key == pygame.K_p:

                        game_pause = True
                        bg_music.stop()
                        bgm = "OFF"
                        game_status = "PAUSE"
                        instructions()
                        show_character()
                        canvas()
                        bullet_pop()
                        isbullet_collision()
                        move_and_draw_spaceship()
                        move_and_draw_aliens()
                        level()
                        show_score_and_life()
                        pygame.display.update()
                        while game_pause:
                            for pause_events in pygame.event.get():
                                if pause_events.type == pygame.KEYDOWN:
                                    if pause_events.key == pygame.K_p:
                                        game_pause = False
                                        bg_music.play()
                                        bgm = "ON"
                                        game_status = "PLAY"
                                        instructions()
                                        pygame.display.update()
                                if pause_events.type == pygame.QUIT:
                                    game_pause = False
                                    game = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= ship_speed
            elif keys[pygame.K_RIGHT] and player_x < width - ship_size:
                player_x += ship_speed
            elif keys[pygame.K_UP] and player_y > height // 2:
                player_y -= ship_speed
            elif keys[pygame.K_DOWN] and player_y < height - ship_size:
                player_y += ship_speed

            instructions()
            show_character()
            canvas()
            deploy_energy_coin()
            is_spaceship_and_energy_coin_collision()
            move_and_draw_spaceship()
            bullet_pop()
            isbullet_collision()
            move_and_draw_aliens()
            level()
            show_score_and_life()

            if isspaceship_collision():
                text = gameover.render("GAME OVER", True, (255, 255, 255))
                screen.blit(text, (90, height // 2 - 100))
                pygame.display.update()
                game = False
                bg_music.stop()
                game_over_bgm.play()
                time.sleep(7)
                menu_bgm.play()

           
            pygame.display.update()

    pygame.quit()
