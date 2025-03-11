# Pygame-Pong

Simple Pygame Pong game

## Explained

### How does the player rectangle move when I press **W** or **S**?
```
def movement():
    global player_pos
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos -= 10
    if keys[pygame.K_s]:
        player_pos += 1
```

The function checks if the **W** key is pressed
> ```if keys[pygame.K_w]:```

If it is pressed, it moves the player rectangle up by subtracting 10 from the player's y-position. 
> ``` player_pos -= 10 ```

### How do we position the ball?

The ball can move up, down, left, and right, so it has two coordinates—a y-coordinate and an x-coordinate. With that knowledge, we can move the ball to specific coordinates.

> [!NOTE]
> This example moves the ball to X = 100 and Y = 100 (where 30 is the radius of the circle):
> 
> ```pygame.draw.circle(screen, "white", (100, 100),  30)```

### How does the Ball move?
To simplify the code, we add velocity to the ball (which determines how fast it moves). The ball requires two velocities—a y-velocity and an x-velocity.
```
velocity_y = 10
velocity_x = 10
```

We add the velocity to the ball's position to move it:

```
ball_x += velocity_x
ball_y += velocity_y
```

> [!NOTE]
> This example shows how to create a ball with variables:
> 
> ```pygame.draw.circle(screen, "white", (ball_x, ball_y),  30)```

### How can we add the wall bouncing effect?

When we create the Pygame window, we select its height and width:

> screen = pygame.display.set_mode((1000, 1000))

> [!TIP]
> You can store the window's height and width in variables:
> 
> ```
> height = 1000
> width = 1000
>
> screen = pygame.display.set_mode((width, height))
> ```

Now we can check if the ball's position is off-screen:

> ```if ball_y >= height:```
> ```if ball_y >= Width:```

If the ball's position exceeds the screen's boundaries (for example, if the ball's y-position is higher than the screen's height), we adjust its velocity by subtracting 20 from the y-velocity so that it moves upward again.

Entire Ball movement code:
```
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
```

