import pygame
import time
import sys
import random

# ───────────────────────────────────────────────────────────────────────────────
pygame.init()
pygame.font.init()

# Bildschirm
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock  = pygame.time.Clock()

# Schrift
font = pygame.font.Font(None, 74)

# Sounds
collision_sound   = pygame.mixer.Sound("paddelcol.mp3")
compgoal_sound    = pygame.mixer.Sound("cgoal.mp3")
playergoal_sound  = pygame.mixer.Sound("pgoal.mp3")

# Spiel‑Status
running     = True
game_state  = "home"
start_timer = 0

# Ball‑Parameter
radius       = 20
direction    = [0, 1]
angle        = [0, 1, 2]
ball_x       = WIDTH  / 2
ball_y       = HEIGHT / 2
velocity_x   = 0
velocity_y   = 0.1
initial_speed= 8

# Paddle‑Parameter
player_pos        = 100
computer_pos_x    = WIDTH - 100
computer_pos_y    = 100
computer_timer    = 0
ball_target_y     = ball_y
ball_c_offset     = 0

# Score
player_goal   = 0
computer_goal = 0

# Zusatz: für Trainings‑Szenarien (optional)
second_left_paddle_y  = 0
second_right_paddle_y = 0

# Beschleunigung nach Kollision
acceleration2 = 1.05
# ───────────────────────────────────────────────────────────────────────────────

def movement():
    global player_pos
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos -= 10
    if keys[pygame.K_s]:
        player_pos += 10
    # Grenzen prüfen
    player_pos = max(0, min(HEIGHT - 150, player_pos))

def ball_movement():
    global ball_x, ball_y, velocity_x, velocity_y
    global player_goal, computer_goal
    global second_left_paddle_y, second_right_paddle_y
    global start_timer

    # Ball verschieben
    ball_x += velocity_x
    ball_y += velocity_y

    # Obere/untere Wand
    if ball_y <= 0 + radius or ball_y >= HEIGHT - radius:
        velocity_y *= -1

    # Punkt für Spieler (rechts vorbeigegangen)
    if ball_x >= WIDTH - radius:
        playergoal_sound.play()
        player_goal += 1

        # Paddle‑Position sichern (optionaler Use‑Case)
        second_left_paddle_y  = player_pos
        second_right_paddle_y = computer_pos_y

        # Ball in Mitte zurücksetzen
        ball_x = WIDTH  / 2
        ball_y = HEIGHT / 2
        start_timer = 0

        # Zufalls­richtung und -winkel
        dir = random.choice(direction)
        ang = random.choice(angle)
        if dir == 0:
            if ang == 0:
                velocity_y, velocity_x = -1.4, 0.7
            elif ang == 1:
                velocity_y, velocity_x = -0.7, 0.7
            else:
                velocity_y, velocity_x = -0.7, 1.4
        else:
            if ang == 0:
                velocity_y, velocity_x =  1.4, 0.7
            elif ang == 1:
                velocity_y, velocity_x =  0.7, 0.7
            else:
                velocity_y, velocity_x =  0.7, 1.4

        velocity_x *= -1  # Ball nun nach links

    # Punkt für Computer (links vorbeigegangen)
    if ball_x <= 0 + radius:
        compgoal_sound.play()
        computer_goal += 1

        second_left_paddle_y  = player_pos
        second_right_paddle_y = computer_pos_y

        ball_x = WIDTH  / 2
        ball_y = HEIGHT / 2
        start_timer = 0

        dir = random.choice(direction)
        ang = random.choice(angle)
        if dir == 0:
            if ang == 0:
                velocity_y, velocity_x = -1.4, 0.7
            elif ang == 1:
                velocity_y, velocity_x = -0.7, 0.7
            else:
                velocity_y, velocity_x = -0.7, 1.4
        else:
            if ang == 0:
                velocity_y, velocity_x =  1.4, 0.7
            elif ang == 1:
                velocity_y, velocity_x =  0.7, 0.7
            else:
                velocity_y, velocity_x =  0.7, 1.4
        # velocity_x bleibt positiv → Ball geht nach rechts

def ball_collision():
    global velocity_x, velocity_y

    ball_rect   = pygame.Rect(ball_x - radius, ball_y - radius, radius*2, radius*2)
    player_rect = pygame.Rect(100, player_pos, 10, 150)
    comp_rect   = pygame.Rect(computer_pos_x, computer_pos_y, 10, 150)

    # Kollision links
    if ball_rect.colliderect(player_rect) and velocity_x < 0:
        collision_sound.play()
        velocity_x = abs(velocity_x) * acceleration2
        velocity_y *= acceleration2
        if velocity_y <= 0:
            velocity_y = round(random.uniform(5, 7), 3)
        else:
            velocity_y = round(random.uniform(-7, -5), 3)
        velocity_y *= acceleration2 / 1.4

    # Kollision rechts
    elif ball_rect.colliderect(comp_rect) and velocity_x > 0:
        collision_sound.play()
        if velocity_y <= 0:
            velocity_y = round(random.uniform(5, 7), 3)
        else:
            velocity_y = round(random.uniform(-7, -5), 3)

        # X‑Geschwindigkeit gestaffelt erhöhen
        if abs(velocity_x) <= 10:
            velocity_x = -abs(velocity_x) * 1.05
            velocity_y *= acceleration2 / 1.2
        elif abs(velocity_x) <= 15:
            velocity_x = -abs(velocity_x) * 1.03
            velocity_y *= acceleration2 / 1.2
        elif abs(velocity_x) <= 20:
            velocity_x = -abs(velocity_x) * 1.02
            velocity_y *= acceleration2 / 1.18
        else:
            velocity_x = -abs(velocity_x) * 1.02
            velocity_y *= acceleration2 / 1.2

def computer_movement():
    global computer_pos_y, computer_timer, ball_target_y, ball_y, ball_c_offset

    randomskip = random.randint(0, 3)
    ball_c_offset = computer_pos_y - ball_target_y

    # Ab und zu „Nachrichten verpassen“
    if randomskip == 2:
        pass

    # Zielposition alle 10 Frames neu setzen
    if computer_timer >= 10:
        ball_target_y = ball_y - 50
        computer_timer = 0

    # Nach oben oder unten bewegen
    if computer_pos_y < ball_target_y:
        if abs(ball_c_offset) >= 100:
            computer_pos_y += 10
        elif abs(ball_c_offset) >= 20:
            computer_pos_y += 9
        else:
            computer_pos_y += 3
    elif computer_pos_y > ball_target_y:
        if abs(ball_c_offset) >= 100:
            computer_pos_y -= 10
        elif abs(ball_c_offset) >= 20:
            computer_pos_y -= 9
        else:
            computer_pos_y -= 3

    computer_timer += 1

def goal_detection():
    global game_state
    if computer_goal >= 10 or player_goal >= 10:
        game_state = "game_over"

def start():
    global velocity_x, velocity_y, start_timer
    if start_timer == 0:
        velocity_x = -initial_speed
        velocity_y = 0
    start_timer += 1
    # (optional) weitere Beschleunigung
    velocity_x *= 1
    velocity_y *= 1

# ───────────────────────────────────────────────────────────────────────────────
# Haupt­schleife
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_state == "home" and event.key == pygame.K_SPACE:
                # Spielstart
                game_state     = "playing"
                computer_goal  = 0
                player_goal    = 0
                ball_x, ball_y = WIDTH/2, HEIGHT/2
                player_pos     = 100
                computer_pos_y = 100
                start_timer    = 0

            elif game_state == "game_over" and event.key == pygame.K_SPACE:
                # Neustart nach Game Over
                game_state     = "playing"
                computer_goal  = 0
                player_goal    = 0
                ball_x, ball_y = WIDTH/2, HEIGHT/2
                player_pos     = 100
                computer_pos_y = 100
                start_timer    = 0

    screen.fill("black")

    if game_state == "home":
        text1 = font.render("Pong!", True, "white")
        text2 = font.render("Drücke SPACE zum Starten", True, "white")
        screen.blit(text1, (WIDTH/2 - text1.get_width()/2, HEIGHT/2 - 50))
        screen.blit(text2, (WIDTH/2 - text2.get_width()/2, HEIGHT/2 + 10))

    elif game_state == "playing":
        # Kollision und Zeichnen
        ball_collision()
        pygame.draw.circle(screen, "white", (int(ball_x), int(ball_y)), radius)
        pygame.draw.rect(screen, "cyan", (100, player_pos, 10, 150))
        pygame.draw.rect(screen, "red",  (computer_pos_x, computer_pos_y, 10, 150))
        for i in range(10):
            pygame.draw.rect(screen, "white", (WIDTH/2, 100 + 100*i, 10, 30))

        movement()

        if start_timer < 20:
            start()
        else:
            ball_movement()

        computer_movement()
        goal_detection()

        # Score anzeigen
        score_text = font.render(f"{computer_goal} | {player_goal}", True, "white")
        screen.blit(score_text, (WIDTH/2 - score_text.get_width()/2, 20))

    else:  # game_over
        if computer_goal >= 10:
            msg = "Computer gewinnt!"
        else:
            msg = "Spieler gewinnt!"
        text1 = font.render(msg, True, "white")
        text2 = font.render("Drücke SPACE zum Neustart", True, "white")
        screen.blit(text1, (WIDTH/2 - text1.get_width()/2, HEIGHT/2 - 50))
        screen.blit(text2, (WIDTH/2 - text2.get_width()/2, HEIGHT/2 + 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()