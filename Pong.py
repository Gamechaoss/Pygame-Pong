# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
pygame.init()
height = 720
width = 1280

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
on_start = True
velocity_y = 10
velocity_x = 10
player_pos = 100

ball_x = 640
ball_y = 360

def movement():
    global player_pos
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos -= 10
    if keys[pygame.K_s]:
        player_pos += 10

def ball_movement():
    global ball_x, ball_y, on_start, velocity_y, velocity_x
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

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    screen.fill("black")

    # Ball
    pygame.draw.circle(screen, "white", (ball_x, ball_y),  30)


    # Players
    pygame.draw.rect(screen, "white", (100, player_pos, 10, 150))
    pygame.draw.rect(screen, "white", (1180, 100, 10, 150))

    movement()
    ball_movement()


    pygame.display.flip()
    clock.tick(60)
    on_start = False
pygame.quit()