# Pygame-Pong

Simple Pygame Pong game

## Explained
How does the Block move when I press **W** or **s**?
```
def movement():
    global player_pos
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos -= 10
    if keys[pygame.K_s]:
        player_pos += 1
```

The funktion is going to check if the **W** Key is pressed
> ```if keys[pygame.K_w]:``` \n
then its going to move the player rectangle **UP** by subtracting 10 of the player's **Y Position** 
> ``` player_pos -= 10 ```
