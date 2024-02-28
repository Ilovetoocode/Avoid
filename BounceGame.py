import pygame, sys, math, random, string
##So this used to be the function from last time...
##BUT OH MY GOODNESS, IS IT SO MUCH BETTER NOW!!
##Managed to somehow make it all one line, nowehere near as messy
##AND It's actually able to strip data! Yes!
#Also it always pops the first element, because that data ends up causing bugs later on.
#You will see why.
def make_list_from_file(file):
    with open(file, 'r', encoding='utf8') as file:
        items = file.read().lower().splitlines()
        items.pop(0)
        return items
def file_writer(text_to_print):
    with open('High_scores!.txt', 'w') as result_file:
        result_file.write("Scores!\n")
        result_file.write(text_to_print+"\n")
def highscore_table_creator(scoreinput,tableinput):
    possible_new_high=scoreinput.split(":")
    confirmed_highs=[highscore for highscore in tableinput]
    itempoint=0
    endstring=""
    for score in confirmed_highs:
        broken_score=str(score).split(":")
        inner_loop_pointer=0
        Newhigh=False
        for scorepart in possible_new_high:
             if scorepart<broken_score[inner_loop_pointer]:
                 break
             elif scorepart==broken_score[inner_loop_pointer]:
                 inner_loop_pointer+=1
             else:
                 Newhigh=True
                 break
        if Newhigh==True:
            tableinput[itempoint]=scoreinput
            break
        itempoint+=1
    for item in tableinput:
        endstring=endstring+item+"\n"

    file_writer(endstring)




def pixel_collision(mask1, rect1, mask2, rect2):
    offset_x = rect2[0] - rect1[0]
    offset_y = rect2[1] - rect1[1]
    overlap = mask1.overlap(mask2, (offset_x, offset_y))
    if overlap:
        return True
    else:
        return False


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
        self.rectangle.center = (random.randrange(0, width), random.randint(0, height))
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
    pygame.init()
    spawn_cooldown = 0
    gear=1

    Thetimer=pygame.time.Clock()
    starttime=pygame.time.get_ticks()

    myfont = pygame.font.SysFont('monospace', 24)
    width, height = 600, 400
    size = width, height
    screen = pygame.display.set_mode((width, height))

    enemy = pygame.image.load("GolfBall.png").convert_alpha()
    enemy_image = pygame.transform.smoothscale(enemy, (50, 50))

    enemy_sprites = []

    player = pygame.image.load("Derg.jpg").convert_alpha()
    player_image=pygame.transform.smoothscale(player,(60,50))
    player_sprite = Sprite(player_image)
    life = 3

    powerup_image = pygame.image.load("knight.gif").convert_alpha()
    powerup_display=pygame.transform.smoothscale(powerup_image,(60,50))

    bomb_image=pygame.image.load("Bomb.png").convert_alpha()
    bomb_display=pygame.transform.smoothscale(bomb_image,(60,50))

    powerups = []
    bombs=[]

    gearshift = pygame.USEREVENT + 1
    pygame.time.set_timer(gearshift, 10000, 0)

    is_playing = True
    while is_playing:
        gametime=pygame.time.get_ticks()-starttime
        minutes=str(gametime//60000).zfill(2)
        seconds=str((gametime%60000)//1000).zfill(2)
        milliseconds=str(gametime%1000).zfill(3)
        finaltime="%s:%s:%s"%(minutes,seconds,milliseconds)

        for event in pygame.event.get():
            if event.type == gearshift:
                gear += 1
                bombs=[]
                bombs.append(PowerUp(bomb_display, width, height))

            if event.type == pygame.QUIT:
                is_playing = False

        pos = pygame.mouse.get_pos()
        player_sprite.set_position(pos)

        for enemy in enemy_sprites:
                if enemy.rectangle.colliderect(player_sprite.rectangle):
                    life -=.1
        for powerup in powerups:
            if powerup.rectangle.colliderect(player_sprite.rectangle):
                if Moarrnglmao==40:
                    enemy_sprites=[]
                life+=1

        powerups=[powerup for powerup in powerups if not powerup.rectangle.colliderect(player_sprite.rectangle)]
        for bomb in bombs:
            if bomb.rectangle.colliderect(player_sprite.rectangle):
                enemy_sprites=[]
        bombs = [bomb for bomb in bombs if not bomb.rectangle.colliderect(player_sprite.rectangle)]
        for enemy in enemy_sprites:
            enemy.move()
            enemy.bounce(width,height)
        Moarrnglmao=random.randint(0,100)
        if Moarrnglmao==100:
            powerups.append(PowerUp(powerup_display,width,height))
        if spawn_cooldown<=0:

            enemy_sprites.append(Enemy(enemy_image, width, height, gear))
            spawn_cooldown=100/gear
        else:
            spawn_cooldown-=1
        screen.fill((0, 100, 50))
        for enemy_sprite in enemy_sprites:
            enemy_sprite.draw(screen)
        for powerup_sprite in powerups:
            powerup_sprite.draw(screen)
        for bomb_sprite in bombs:
            bomb_sprite.draw(screen)
        player_sprite.draw(screen)

        text = "Life: " + str('%.1f' % life)
        life_banner = myfont.render(text, True, (255, 255, 0))
        screen.blit(life_banner, (20, 20))
        if life <=0:
            highscore_table_creator(finaltime,make_list_from_file("High_scores!.txt"))
            failtext="Game over!"
            endtime="You survived for: " + str(finaltime)
            endgear="And got through: "+str(gear)+" Gearshifts!"
            screen.fill((255, 0, 0))
            ending_text_1=myfont.render(failtext, True, (71,255,144))
            ending_text_2=myfont.render(endtime,True,(71,255,144))
            ending_text_3=myfont.render(endgear, True, (71,255,144))
            screen.blit(ending_text_1,(150,60))
            screen.blit(ending_text_2,(80,100))
            screen.blit(ending_text_3, (50,150))
            is_playing=False


        pygame.display.update()
        # Pause for a few milliseconds
        pygame.time.wait(20)

    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
