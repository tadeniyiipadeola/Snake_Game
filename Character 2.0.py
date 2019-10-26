import pygame
pygame.init()

# th is to setup the window on pygame
win = pygame.display.set_mode((500,480))
pygame.display.set_caption("This is a character game")

walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'),
            pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'),
            pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'),
             pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),
             pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]

bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()

class player(object):
    def __init__(self, x, y , width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not self.standing:
            if self.left:
                win.blit(walkLeft[self.walkCount // 10], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blits(walkRight[self.walkCount // 10], (self.x, self.y))
                self.walkCount -= 1

        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))


class projectile (object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self. color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(win):
        pygam.draw.circle(win, self.color, (self.x,self.y), self.radius)

def redrawgamewindow():
    win.blit(bg, (0, 0))
    man.draw(win)
    pygame.display.update()


run = True  # main loop, This
man = player(300, 410, 64, 64)
while run:
    clock.tick(27)

    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed() # declare the variable keys and its function in the code

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False

    elif keys[pygame.K_RIGHT] and man.x < 485 - man.vel - man.width:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0

# This line disables movement in the y direction while spacebar is active
    if not man.isJump:
        if keys[pygame.K_SPACE]:
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