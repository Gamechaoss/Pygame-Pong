# Example file showing a basic pygame "game loop"
import pygame
import time

# pygame setup
pygame.init()
height = 720
width = 1280

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
timer = 0

ball_x = 640
ball_y = 360
velocity_y = 10
velocity_x = 10

trail_x = 640
trail_y = 360
trail_velocity_y = 10
trail_velocity_x = 10

player_pos = 100


def movement():
    global player_pos
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos -= 10
    if keys[pygame.K_s]:
        player_pos += 10

def ball_movement():
    global ball_x, ball_y, velocity_y, velocity_x
    print("Velocity Y: ", velocity_y)
    print("Velocity X: ", velocity_x)
    
    ball_x += velocity_x
    ball_y += velocity_y
    if ball_y >= height:
        velocity_y -= 20
    elif ball_y <= 0:
        velocity_y += 20
    elif ball_x >= width:
        velocity_x -= 20
    elif ball_x <= 0:
        velocity_x += 20

def ball_collision():
    global ball_x, ball_y, velocity_y, velocity_x


    offset_top = player_pos
    offset_bottom = player_pos + 150
    offset_height = offset_bottom - offset_top  


    pygame.draw.rect(screen, "cyan", (100, offset_top, 10, offset_height))

    if (ball_x <= 110) and (offset_top <= ball_y <= offset_bottom):
        velocity_x += 20



def trail():
    global trail_x, trail_y, trail_velocity_y, trail_velocity_x
    trail_x += trail_velocity_x
    trail_y += trail_velocity_y
    if trail_y >= height:
        trail_velocity_y -= 20
    elif trail_y <= 0:
        trail_velocity_y += 20
    elif trail_x >= width:
        trail_velocity_x -= 20
    elif trail_x <= 0:
        trail_velocity_x += 20


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    screen.fill("black")
    ball_collision()
    # Ball
    pygame.draw.circle(screen, "white", (ball_x, ball_y),  30)
    #pygame.draw.circle(screen, "cyan", (trail_x, trail_y),  10)


    # Players 
    pygame.draw.rect(screen, "white", (100, player_pos, 10, 150))
    pygame.draw.rect(screen, "white", (1180, 100, 10, 150))

    movement()
    #trail()
    if timer <= 10:
        pass
    else:
        ball_movement()




    if velocity_x > 10:
        velocity_x = 10
    if velocity_y > 10:
        velocity_y = 10
    if velocity_x < -10:
        velocity_x = -10
    if velocity_y < -10:
        velocity_y = -10

    pygame.display.flip()
    timer += 1
    clock.tick(60)
pygame.quit()
