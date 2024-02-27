import pygame, sys, math, random

##THIS IS A BAD IDEA, BUT I LOVE IT!
##THIS, is the gear! It's a Global variable! Why is it a Global? Because that's the best way
## I thought of handeling speed for the enemies and my spawn timer.
def pixel_collision(mask1, rect1, mask2, rect2):
    offset_x = rect2[0] - rect1[0]
    offset_y = rect2[1] - rect1[1]
    overlap = mask1.overlap(mask2, (offset_x, offset_y))
    if overlap:
        return True
    else:
        return False

def list_adder(list,newelement):
    list.append(newelement)

class Sprite:
    def __init__(self, image):
        self.image = image
        self.rectangle = image.get_rect()
        self.mask = pygame.mask.from_surface(image)

    def set_position(self, new_position):
        self.rectangle.center = new_position

    def draw(self, screen):
        screen.blit(self.image, self.rectangle)

    def is_colliding(self, other_sprite):
        return pixel_collision(self.mask, self.rectangle, other_sprite.mask, other_sprite.rectangle)


class Enemy:
    def __init__(self, image, width, height, gear):
        self.image = image
        self.mask = pygame.mask.from_surface(image)
        self.rectangle = image.get_rect()
        self.rectangle.center = (random.randint(0, width), random.randint(0, height))
        self.gear=gear
        self.speed=(random.randrange((-10*gear),(10*gear)),random.randrange((-10*gear),(10*gear)))

    def move(self):
        self.rectangle.move_ip(self.speed)

    def bounce(self,width,height):
        changeval=list(self.speed)
        if self.rectangle.left < 0  or self.rectangle.right > width:
            changeval[0]*=-1
            self.speed=tuple(changeval)
        if self.rectangle.top < 0 or self.rectangle.bottom > height:
            changeval[1]*=-1
            self.speed=tuple(changeval)

    def draw(self, screen):
        screen.blit(self.image, self.rectangle)


class PowerUp:
    def __init__(self, image, width, height):
        self.image = image
        self.mask = pygame.mask.from_surface(image)
        self.rectangle = image.get_rect()
        self.rectangle.center = (random.randint(0, width), random.randint(0, height))

    def draw(self, screen):
        screen.blit(self.image, self.rectangle)


def main():
    spawn_cooldown=0
    # Setup pygame
    pygame.init()
    gear=1
    Thetimer=pygame.time.Clock()
    starttime=pygame.time.get_ticks()
    # Get a font for printing the lives left on the screen.
    myfont = pygame.font.SysFont('monospace', 24)

    # Define the screen
    width, height = 600, 400
    size = width, height
    screen = pygame.display.set_mode((width, height))

    # Load image assets
    # Choose your own image
    enemy = pygame.image.load("GolfBall.png").convert_alpha()
    enemy_image = pygame.transform.smoothscale(enemy, (50, 50))

    enemy_sprites = []


    # This is the character you control. Choose your image.
    player = pygame.image.load("Wizard.gif").convert_alpha()
    player_image=pygame.transform.smoothscale(player,(60,50))
    player_sprite = Sprite(player_image)
    life = 3

    # This is the powerup image. Choose your image.
    powerup_image = pygame.image.load("knight.gif").convert_alpha()
    powerup_display=pygame.transform.smoothscale(powerup_image,(60,50))
    # Start with an empty list of powerups and add them as the game runs.
    powerups = []

    # Main part of the game
    is_playing = True
    # while loop
    while is_playing:  # while is_playing is True, repeat
        # Modify the loop to stop when life is <= to 0.
        # Check for events
        ##oh no. a userevent. Yeah This thing is, strange to be here.
        ##This odd bit of syntax we aren't supposed to know yet is part of the control of
        ##THE GEAR SYSTEM! Basically it needs to be, defined like this
        ##Just so I can set a timer on it using pygame later on.
        ##There, I will fully explain, the madness.
        gearshift=pygame.USEREVENT+1
        ##i hate having this code here... if only i could move it into a different function without breaking stuff...
        ##Anyways! This game is in an endless survival thing due to how I have my spawn code set up!
        ##So of course! We need to exploit the fact that there is a timer function in pygame to do just that!
        gametime=pygame.time.get_ticks()-starttime
        minutes=str(gametime//60000).zfill(2)
        seconds=str((gametime%60000)/1000).zfill(2)
        milliseconds=str(gametime%1000).zfill(3)
        finaltime="%s:%s:%s"%(minutes,seconds,milliseconds)
        ##Here's the timer for, gearshifts
        pygame.time.set_timer(gearshift,1000, 0) ##CHANGE THAT NUMBER ON THE END, GAME IS IMPOSSIBLE NOW
        for event in pygame.event.get():
            # Stop loop if click on window close button
            if event.type == gearshift:
                gear += 1
                print("Event happens")
            if event.type == pygame.QUIT:
                is_playing = False
        # Make the player follow the mouse
        pos = pygame.mouse.get_pos()
        player_sprite.set_position(pos)

        # Loop over the enemy sprites. If the player sprite is
        # colliding with an enemy, deduct from the life variable.
        # A player is likely to overlap an enemy for a few iterations
        # of the game loop - experiment to find a small value to deduct that
        # makes the game challenging but not frustrating.
        for enemy in enemy_sprites:

                if enemy.rectangle.colliderect(player_sprite.rectangle):
                    life -=.1
        # Loop over the powerups. If the player sprite is colliding, add
        # 1 to the life.
        # Make a list comprehension that removes powerups that are colliding with
        # the player sprite.
        for powerup in powerups:
            if powerup.rectangle.colliderect(player_sprite.rectangle):
                ##RNG Event to get a bonus screen clear, woooo!!!!
                if Moarrnglmao==40:
                    enemy_sprites=[]
                life+=1
        powerups=[powerup for powerup in powerups if not powerup.rectangle.colliderect(player_sprite.rectangle)]

        # Loop over the enemy_sprites. Each enemy should call move and bounce.
        for enemy in enemy_sprites:
            enemy.move()
            enemy.bounce(width,height)
        # Choose a random number. Use the random number to decide to add a new
        # powerup to the powerups list. Experiment to make them appear not too
        # often, so the game is challenging.
        Moarrnglmao=random.randint(0,100)
        if Moarrnglmao==100:
            powerups.append(PowerUp(powerup_display,width,height))
        if spawn_cooldown==0:

            enemy_sprites.append(Enemy(enemy_image, width, height, gear))
            spawn_cooldown=(100/gear)
            print(gear)
        else:
            spawn_cooldown-=1
        # Erase the screen with a background color
        screen.fill((0, 100, 50))  # fill the window with a color

        # Draw the characters
        for enemy_sprite in enemy_sprites:
            enemy_sprite.draw(screen)
        for powerup_sprite in powerups:
            powerup_sprite.draw(screen)

        player_sprite.draw(screen)

        # Write the life to the screen.
        text = "Life: " + str('%.1f' % life)
        life_banner = myfont.render(text, True, (255, 255, 0))
        screen.blit(life_banner, (20, 20))
        if life <=0:
            failtext="Game over! You survived for: "
            endtime=str(finaltime)
            screen.fill((255, 0, 0))
            ending_text_1=myfont.render(failtext, True, (71,255,144))
            ending_text_2=myfont.render(endtime,True,(218,165,32))
            screen.blit(ending_text_1,(50,100))
            screen.blit(ending_text_2,(50,150))
            is_playing=False


        # Bring all the changes to the screen into view
        pygame.display.update()
        # Pause for a few milliseconds
        pygame.time.wait(20)

    # Once the game loop is done, pause, close the window and quit.
    # Pause for a few seconds
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
