import pygame

pygame.init()

# this to setup the window on pygame
win = pygame.display.set_mode((1600, 1000))

pygame.display.set_caption("This is a character game")
# this loads the background image
bg = pygame.image.load('bg.jpg')

bullet = pygame.image.load('B1.png')

#  game clock
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

RED = (255, 0, 0)
#  bottom left platform
PF1_1 = pygame.image.load('p0.png')
PF1_2 = pygame.image.load('p1.png')
#  right platform
PF2_1 = pygame.image.load('p0.png')
PF2_2 = pygame.image.load('p1.5.png')
PF2_3 = pygame.image.load('p1.png')
#  Big left platform
PF3_1 = pygame.image.load('p0.png')
PF3_2 = pygame.image.load('p1.5.png')
PF3_3 = pygame.image.load('p1.5.png')
PF3_4 = pygame.image.load('p1.5.png')
PF3_5 = pygame.image.load('p1.png')
# Top right platform
PF4_1 = pygame.image.load('p0.png')
PF4_2 = pygame.image.load('p1.5.png')
PF4_3 = pygame.image.load('p1.5.png')
PF4_4 = pygame.image.load('p1.png')

class Platform(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitBox = (self.x, self.y, width, height,)

    def draw(self, win):
        pygame.draw.rect(win, RED, self.hitBox, 2)
        self.hitBox = (self.x, self.y, 127, 96)


class part1(Platform):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.x = x
        self.y = y
        self.hitBox = (self.x, self.y, 500, 180)

    def draw(self, win):
        pygame.draw.rect(win, RED, self.hitBox, 2)


class part2(Platform):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.x = x
        self.y = y
        self.hitBox = (self.x, self.y, width, height)

    def draw(self, win):
        pygame.draw.rect(win, RED, self.hitBox, 2)


class part3(Platform):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.x = x
        self.y = y
        self.hitBox = (self.x, self.y, width, height)

    def draw(self, win):
        pygame.draw.rect(win, RED, self.hitBox, 2)


class part4(Platform):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.x = x
        self.y = y
        self.hitBox = (self.x, self.y, width, height)

    def draw(self, win):
        pygame.draw.rect(win, RED, self.hitBox, 2)


#  Instances
Pl1_1 = Platform(50, 800, 1000, 200)
pl1_2 = part1(177, 800, 1000, 200)

Pl2_1 = Platform(800, 500, 200, 200)
pl2_2 = part1(927, 500, 200, 200)
pl2_3 = part2(1054, 500, 200, 200)

pl3_1 = Platform(50, 245, 200, 200)
pl3_2 = part1(177, 245, 200, 200)
pl3_3 = part2(304, 245, 200, 200)
pl3_4 = part3(431, 245, 200, 200)
pl3_5 = part4(558, 245, 200, 200)

pl4_1 = Platform(1050, 100, 200, 200)
pl4_2 = part1(1177, 100, 200, 200)
pl4_3 = part2(1304, 100, 200, 200)
pl4_4 = part3(1431, 100, 200, 200)
# This loads the images for the Player
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'),
            pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'),
            pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'),
             pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),
             pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
char = pygame.image.load('standing.png')


#  class created for player one
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self, )
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 8
        self.left = False
        self.right = False
        self.walkCount = 0  # count sprite and what image were on
        self.jumpCount = 10
        self.standing = True
        self.isJump = False
        self.hitBox = (self.x + 17, self.y + 2, 31, 57)

    # use the images above to draw the character sprite
    def draw(self, win):
        if self.walkCount + 1 >= 28:
            self.walkCount = 0

        if not self.standing:
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        pygame.draw.rect(win, [255, 0, 0], self.hitBox, 2)
        self.hitBox = (self.x + 17, self.y + 14, 31, 50)


# this class is for the projectile that damages the other player
class ProJectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 15 * facing

    # this instance method draw as the projectile as a  circlar dot
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


# Sprite Load for Player2
player2_WL = [pygame.image.load('0.png'), pygame.image.load('1.png'), pygame.image.load('2.png'),
              pygame.image.load('3.png'), pygame.image.load('4.png'), pygame.image.load('5.png'),
              pygame.image.load('6.png'), pygame.image.load('7.png'), pygame.image.load('8.png')]
player2_WR = [pygame.image.load('9.png'), pygame.image.load('10.png'), pygame.image.load('11.png'),
              pygame.image.load('12.png'), pygame.image.load('13.png'), pygame.image.load('14.png'),
              pygame.image.load('15.png'), pygame.image.load('16.png'), pygame.image.load('17.png')]
player2_char = pygame.image.load('44.png')


# Class created for the first object which is player 2
class Player2(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 8
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.isJump = False
        self.hitBox = (self.x + 17, self.y + 2, 31, 57,)

    def draw(self, win):  # never draw in mainloop

        if self.walkCount + 1 >= 10:
            self.walkCount = 0

        if not self.standing:
            if self.left:
                win.blit(player2_WL[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(player2_WR[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

        else:
            if self.right:
                win.blit(player2_WR[0], (self.x, self.y))
            else:
                win.blit(player2_WL[0], (self.x, self.y))
        self.hitBox = (self.x + 0, self.y + 0, 31, 57)
        pygame.draw.rect(win, [255, 0, 0], self.hitBox, 2)


# This line redraws the window with the BG and sprites on the BG
def redrawgamewindow():
    win.blit(bg, (0, 0))  # to put pic as the background use win.blit(image var(tuple position)
    #  draws the rect of platform on window
    rect_Lvl1_1.draw(win)
    rect_Lvl1_2.draw(win)

    rect_Lvl2_1.draw(win)
    rect_Lvl2_2.draw(win)
    rect_Lvl2_3.draw(win)

    rect_Lvl3_1.draw(win)
    rect_Lvl3_2.draw(win)
    rect_Lvl3_3.draw(win)
    rect_Lvl3_4.draw(win)
    rect_Lvl3_5.draw(win)

    rect_Lvl4_1.draw(win)
    rect_Lvl4_2.draw(win)
    rect_Lvl4_3.draw(win)
    rect_Lvl4_4.draw(win)

    man.draw(win)
    man2.draw(win)
    #  draw the image of a Platform at a given location
    win.blit(PF1_1, (Pl1_1.x, Pl1_1.y))
    win.blit(PF1_2, (pl1_2.x, pl1_2.y))
    #  draws the image for the Platform at given location
    win.blit(PF2_1, (Pl2_1.x, Pl2_1.y))
    win.blit(PF2_2, (pl2_2.x, pl2_2.y))
    win.blit(PF2_3, (pl2_3.x, pl2_3.y))
    # draw the image of a platform at given location
    win.blit(PF3_1, (pl3_1.x, pl3_1.y))
    win.blit(PF3_2, (pl3_2.x, pl3_2.y))
    win.blit(PF3_3, (pl3_3.x, pl3_3.y))
    win.blit(PF3_4, (pl3_4.x, pl3_4.y))
    win.blit(PF3_5, (pl3_5.x, pl3_5.y))

    win.blit(PF4_1, (pl4_1.x, pl4_1.y))
    win.blit(PF4_2, (pl4_2.x, pl4_2.y))
    win.blit(PF4_3, (pl4_3.x, pl4_3.y))
    win.blit(PF4_4, (pl4_4.x, pl4_4.y))


    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()


#  instances
run = True
bullets = []
rect_Lvl1_1 = Platform(50, 800, 200, 200)
rect_Lvl1_2 = Platform(177, 800, 200, 200)

rect_Lvl2_1 = Platform(800, 500, 200, 200)
rect_Lvl2_2 = Platform(927, 500, 200, 200)
rect_Lvl2_3 = Platform(1054, 500, 200, 200)

rect_Lvl3_1 = Platform(50, 245, 200, 200)
rect_Lvl3_2 = Platform(177, 245, 200, 200)
rect_Lvl3_3 = Platform(304, 245, 200, 200)
rect_Lvl3_4 = Platform(431, 245, 200, 200)
rect_Lvl3_5 = Platform(558, 245, 200, 200)

rect_Lvl4_1 = Platform(1050, 100, 200, 200)
rect_Lvl4_2 = Platform(1177, 100, 200, 200)
rect_Lvl4_3 = Platform(1304, 100, 200, 200)
rect_Lvl4_4 = Platform(1431, 100, 200, 200)

man = Player(200, 887, 64, 64)  # (x, y, width,height)
man2 = Player2(800, 900, 45, 55)  # (x, y, width,height)

# main loop, This
while run:
    clock.tick(27)  # FPS keeps the loop running at the right speed
    for event in pygame.event.get():  # This to stop the game while you close window
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.x < 1600 and bullet.x > 0:
            # if 852 > bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys2 = pygame.key.get_pressed()
    if keys2[pygame.K_a] and man2.x > man.vel:
        man2.x -= man2.vel
        man2.left = True
        man2.right = False
        man2.standing = False
    elif keys2[pygame.K_d] and man2.x < 1600 - man.vel - man.width:
        man2.x += man.vel
        man2.right = True
        man2.left = False
        man2.standing = False
    else:
        man2.standing = True
    # Logic For baldy
    keys = pygame.key.get_pressed()
    # declare the variable keys and its function in the code
    if keys[pygame.K_SPACE]:
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 50:
            bullets.append(
                ProJectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (0, 0, 0), facing))

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False

    elif keys[pygame.K_RIGHT] and man.x < 1600 - man.vel - man.width:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0

    # This line disables movement in the y direction while spacebar is active
    if not man.isJump:
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.jumpCount = 10
            man.isJump = False

    redrawgamewindow()

pygame.quit()
