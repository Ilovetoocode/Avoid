import pygame, sys, math, random

##So this used to be the function from last time...
##BUT OH MY GOODNESS, IS IT SO MUCH BETTER NOW!!
##Managed to somehow make it all one line, nowehere near as messy
##AND It's actually able to strip data! Yes!
# Also it always pops the first element, because that data ends up causing bugs later on.
# You will see why.
def make_list_from_file(file):
    with open(file, 'r', encoding='utf8') as file:
        items = file.read().lower().strip().splitlines()
        items.pop(0)
        return items

# The file writer from the last program... and right below it...
def file_writer(text_to_print):
    with open('High_scores!.txt', 'w') as result_file:
        result_file.write("Scores!\n")
        result_file.write(text_to_print + "\n")

# This beast. This is an over-engineered function to say the least, so many moving parts!
# Don't worry, I'll break this down step by step.
def highscore_table_creator(scoreinput, tableinput):
    # This starting point turns an input score into a list with 3 elements.
    #After this, it takes in the inputted table of scores
    # And stores that in a container of its own.
    # It finally instantiates a variable for index pointing, and
    # A place to store the end result of the function as a string instead of a large list.
    possible_new_high = scoreinput.split(":")
    confirmed_highs = [highscore for highscore in tableinput]
    itempoint = 0
    endstring = ""
    for score in confirmed_highs:
        #This part might have been able to be done in list ccomprehension
        #However IDK how powerful it is, and also seeing this might
        # Be better at understanding the trouble I had implimenting this one feauture.
        # It starts out fine each loop, just instantiating for the loop
        # A new list of the current list item from the confirmed_highs list from earlier.
        # After that it instantiates two needed items that help control the inner loop.
        broken_score = str(score).split(":")
        inner_loop_pointer = 0
        Newhigh = False
        for scorepart in possible_new_high:
            #Speaking of: here's the inner loop.
            # This part is where I nearly had a mental block.
            # This thing needed so many iterations just to make sure
            # The final part of the code didn't break and corrupt the high scores file.
            # What it does is go through the broken up parts of the player's score, comparing them
            # To the broken up elements created in the outer loop.
            # From here, one of three things happen:
            if scorepart < broken_score[inner_loop_pointer]:
                # 1: The code reaches a part of the score that is clearly
                # lower than the current high score that's being looped through.
                # In this case, the loop is broken out of back into the one for the high scores
                # With nothing extra being sent.
                break
            elif scorepart == broken_score[inner_loop_pointer]:
                # 2: The current values of the scores are the exact same.
                # In this case, the code stays inside of this loop,
                # checking the next element of the score that's being compared against.
                inner_loop_pointer += 1
            else:
                # And 3: An element of the score is higher than the one from the original table that's
                # Being compared against. In which case, the code is broken out of after setting
                # A variable instantiated earlier to True, the Newhigh variable.
                Newhigh = True
                break
        # This code checks if Newhigh has been set to true at any point within the larger loop.
        # What it does is insert into the tableinput list the new score at an index set to a
        # pointer variable designed specifically to track how many items have been looked through
        # In the larger list. Afterward, it pops out the final entry on the scoreboard, keeping it at a constant
        # 5 scores, unless someone adds in a new score manually, making that into the new max size of the high score file.
        # Finally, it tells the large loop to break, if it didn't, it would
        # Turn all the scores lower than yours into your score,
        # Rather than just the one.
        if Newhigh == True:
            tableinput.insert(itempoint, scoreinput)
            tableinput.pop(-1)
            break
        # This is the indexing variable for the large loop
        itempoint += 1
    # After the large loop is finished, either exhausting
    # All of the table values without being able to find a score lower than the one of
    # The current player's, or being broken out of due to the player getting a high score,
    # The endstring value defined earlier is fed in the tableinput
    # list, each item being put on a new line.
    for item in tableinput:
        endstring = endstring + item + "\n"
    # Finally, the ending string created is sent into the file writer.
    file_writer(endstring)


def pixel_collision(mask1, rect1, mask2, rect2):
    offset_x = rect2[0] - rect1[0]
    offset_y = rect2[1] - rect1[1]
    overlap = mask1.overlap(mask2, (offset_x, offset_y))
    if overlap:
        return True
    else:
        return False
# This function just simply takes in two numbers.
# An input number for the function, and the base the input will be working on
# This function exists as a mitigation effort to make a later part of this code readable.
def log_int(inputnum,inputbase):
    outputnum=int(math.log(inputnum,inputbase))
    return outputnum
class Sprite:
    def __init__(self, image):
        self.image = image
        self.rectangle = image.get_rect()
        self.mask = pygame.mask.from_surface(image)


    def draw(self, screen):
        screen.blit(self.image, self.rectangle)

    def is_colliding(self, other_sprite):
        return pixel_collision(self.mask, self.rectangle, other_sprite.mask, other_sprite.rectangle)

class Player(Sprite):
    def set_position(self, new_position):
        self.rectangle.center = new_position
class Enemy:
    # The enemy class has added variables now.
    # First off, there's of course the initial position, randomly selected on the grip
    # Via two random inputs bounded into the range given in as parameters for the object.
    # And then there's speed. Speed isn't simple. It was for a while...
    # But then the gear system got put in and had to be balanced out a little for the game to be fun.
    # And now it's a mess.
    def __init__(self, image, width, height, gear):
        self.image = image
        self.mask = pygame.mask.from_surface(image)
        self.rectangle = image.get_rect()
        self.rectangle.center = (random.randrange(0, width), random.randint(0, height))
        # This takes in from the parameters a certain gear.
        # This makes sure the gear functionalities of the game works.
        # The gear is a system made for difficulty in the simplest way possible.
        # The higher the number, the faster the enemies.
        # Simple, right? Well....
        self.gear = gear
        # This base speed is set as 100 times the gear, which finally brings us....
        self.basespeed=100*gear
        # To this. My worst code ever. What it does is set two random ranges for the X and Y
        # Cooridinates to pick from. That's the simple part, the issue comes in
        # When the balancing changes are sent in. For these, it grabs self.basevalue,
        # is told whatever the output of something done inside must be converted into an int
        # It then takes this base value and does a logarithmic equation to it.
        # Finally, for the negative values, it is multiplied by negative one, rather than
        # Attempting to pass a negative number into the log function.
        # The log to int handeling is of course sent to the function set above,
        # Though this only slightly fixes up the core issue of the number of parameters within.
        self.speed = (
            random.randrange((log_int(self.basespeed, 2) * -1), log_int(self.basespeed, 2)), random.randrange((log_int(
                self.basespeed, 2) * -1), log_int(self.basespeed * gear, 2)))
    #A simple move function, all it does
    # Is use the speed the object has to move around on the board.
    def move(self):
        self.rectangle.move_ip(self.speed)
    # Slightly broken.
    # Detects the edge of the screen on all sides, making sure
    # things stay inside.
    # Code is broken due to sometimes causing enemies to get stuck forever
    # If they somehow spawn inside a wall.
    def bounce(self, width, height):
        changeval = list(self.speed)
        if self.rectangle.left < 0 or self.rectangle.right > width:
            changeval[0] *= -1
            self.speed = tuple(changeval)
        if self.rectangle.top < 0 or self.rectangle.bottom > height:
            changeval[1] *= -1
            self.speed = tuple(changeval)

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
    pygame.init()
    spawn_cooldown = 0
    # The gear is defined for the entire program
    gear = 1
    # The timer for scoring is initialized here
    Thetimer = pygame.time.Clock()
    starttime = pygame.time.get_ticks()

    myfont = pygame.font.SysFont('monospace', 24)
    width, height = 600, 400
    size = width, height
    screen = pygame.display.set_mode((width, height))

    enemy = pygame.image.load("Spikeball.png").convert_alpha()
    enemy_image = pygame.transform.smoothscale(enemy, (50, 50))

    enemy_sprites = []

    player = pygame.image.load("Derg.jpg").convert_alpha()
    player_image = pygame.transform.smoothscale(player, (60, 50))
    player_sprite = Player(player_image)
    life = 3

    powerup_image = pygame.image.load("Water.jpeg").convert_alpha()
    powerup_display = pygame.transform.smoothscale(powerup_image, (60, 50))

    bomb_image = pygame.image.load("Bomb.png").convert_alpha()
    bomb_display = pygame.transform.smoothscale(bomb_image, (60, 50))

    powerups = []
    # This new list is for a new form of powerup.
    # It will be explained shortly
    bombs = []
    #The gear timer is initialized, alongside the event that
    # Is triggered to make sure it happens
    gearshift = pygame.USEREVENT + 1
    pygame.time.set_timer(gearshift, 10000, 0)

    is_playing = True
    while is_playing:
        # Up here, parameters are initialized in order to
        # Store the game time for the final score.
        gametime = pygame.time.get_ticks() - starttime
        minutes = str(gametime // 60000).zfill(2)
        seconds = str((gametime % 60000) // 1000).zfill(2)
        milliseconds = str(gametime % 1000).zfill(3)
        finaltime = "%s:%s:%s" % (minutes, seconds, milliseconds)

        for event in pygame.event.get():
            # This gets the event that is called
            # Every 10 seconds, telling the game to
            # Add one to the gear variable
            # And then spawn a new bomb to the bomb list
            if event.type == gearshift:
                gear += 1
                bombs.append(PowerUp(bomb_display, width, height))

            if event.type == pygame.QUIT:
                is_playing = False

        pos = pygame.mouse.get_pos()
        player_sprite.set_position(pos)

        for enemy in enemy_sprites:
            if enemy.rectangle.colliderect(player_sprite.rectangle):
                life -= .1
        # RNG function in the powerup grab.
        # Gives random chance to clear the screen of enemies.
        # They always give lives though
        for powerup in powerups:
            if powerup.rectangle.colliderect(player_sprite.rectangle):
                if Moarrnglmao == 40:
                    enemy_sprites = []
                life += 1
        # Removing powerups picked up
        powerups = [powerup for powerup in powerups if not powerup.rectangle.colliderect(player_sprite.rectangle)]
        #This is why bombs are given out so rarely, they act as a
        # Garaenteed way to clear out all enemies, rather than depending on an RNG chance.
        for bomb in bombs:
            if bomb.rectangle.colliderect(player_sprite.rectangle):
                enemy_sprites = []
        # Bombs are also removed from the list as they are used
        bombs = [bomb for bomb in bombs if not bomb.rectangle.colliderect(player_sprite.rectangle)]
        for enemy in enemy_sprites:
            enemy.move()
            enemy.bounce(width, height)
        Moarrnglmao = random.randint(0, 100)
        if Moarrnglmao == 100:
            powerups.append(PowerUp(powerup_display, width, height))
        # This part handles enemy spawning, taking in a base value of 100
        # And dividing it by the gear value. This makes the game more hectic
        # Since enemies spawn faster as the game goes on.
        if spawn_cooldown <= 0:

            enemy_sprites.append(Enemy(enemy_image, width, height, gear))
            spawn_cooldown = 100 / gear
        else:
            spawn_cooldown -= 1

        screen.fill((0, 100, 50))
        for enemy_sprite in enemy_sprites:
            enemy_sprite.draw(screen)
        for powerup_sprite in powerups:
            powerup_sprite.draw(screen)
        for bomb_sprite in bombs:
            bomb_sprite.draw(screen)
        player_sprite.draw(screen)
        #Finally, after the player dies, this code is run to display the game over screen
        # It grabs the time stored and shows it to the player
        # It also grabs the gear to give an idea of how many times the game
        # Got harder before they died. It also runs the table creator before making the ending screen,
        # Since hitting it also triggers the is_playing value to be false at the end.
        text = "Life: " + str('%.1f' % life)
        life_banner = myfont.render(text, True, (255, 255, 0))
        screen.blit(life_banner, (20, 20))
        if life <= 0:
            highscore_table_creator(finaltime, make_list_from_file("High_scores!.txt"))
            failtext = "Game over!"
            endtime = "You survived for: " + str(finaltime)
            endgear = "And got through: " + str(gear) + " Gearshifts!"
            screen.fill((255, 0, 0))
            ending_text_1 = myfont.render(failtext, True, (71, 255, 144))
            ending_text_2 = myfont.render(endtime, True, (71, 255, 144))
            ending_text_3 = myfont.render(endgear, True, (71, 255, 144))
            screen.blit(ending_text_1, (150, 60))
            screen.blit(ending_text_2, (80, 100))
            screen.blit(ending_text_3, (50, 150))
            is_playing = False

        pygame.display.update()
        # Pause for a few milliseconds
        pygame.time.wait(20)

    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
