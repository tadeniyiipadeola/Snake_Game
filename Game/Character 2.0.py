import os
import pygame

# Game Setup
# Initializes pygame
pygame.init()

# The Desired screen width and height
screenWidth = pygame.display.Info().current_w
screenHeight = pygame.display.Info().current_h

# Sets up the window to display the game
win = pygame.display.set_mode((screenWidth, screenHeight), pygame.FULLSCREEN)
pygame.display.set_caption("This is a character game")

# The clock of the game
clock = pygame.time.Clock()

# Gameplay Setup
# How fast characters will fall
gravity = 4

# The control scheme for player 1
p1Controls = [pygame.K_SPACE, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT]  # (Space, Jump, Left, Right)

# The control scheme for player 2
p2Controls = [pygame.K_f, pygame.K_w, pygame.K_a, pygame.K_d]  # (Space, Jump, Left, Right)

# Sprite Appearance Setupd
# The variable used to scale sprites down to fit the screen
spriteScale = 0.5

# The color Red, for Enemies
RED = (255, 0, 0)

# The color Green, for Power Ups
YELLOW = (255, 255, 0)

# The color Green, for Platforms
GREEN = (0, 255, 0)

# The color Cyan, for the Projectiles
CYAN = (0, 255, 255)

# The color Blue, for Players
BLUE = (0, 0, 255)

# Image Setup
# Loads the background's image into the window
bg = pygame.transform.scale(pygame.image.load('sprites/bg.jpg').convert_alpha(), (screenWidth, screenHeight))

# Loads the first player's bullet into the window
p1Bullet = pygame.transform.scale(pygame.image.load('sprites/players/projectiles/p1Projectile.png').convert_alpha(),
                                  (18, 12))

# Loads the first player's bullet into the window
p2Bullet = pygame.transform.scale(pygame.image.load('sprites/players/projectiles/p2Projectile.png').convert_alpha(),
                                  (18, 12))

# The optimal platform width and height
platformWidth = round(127 * spriteScale)
platformHeight = round(96 * spriteScale)

# The list containing all platform sprites
platformSprites = []

# The optimal ground width and height
groundWidth = round(128 * spriteScale)
groundHeight = round(175 * spriteScale)

# The list containing all of the ground's sprites
groundSprites = []

# The list containing all of the first player's sprites
# First list is the right walking sprites, second list is the left walking sprites
p1Sprites = [[], []]

# The list containing all of the second player's sprites
# First list is the right walking sprites, second list is the left walking sprites
p2Sprites = [[], []]

# Loads all of the images in the floating folder into the list
for root, dirs, files in os.walk("sprites/platforms/floating", topdown=False):
    # For each file in the list, put it at the end of the list
    # Name contains the file path
    for name in files:
        platformSprites.append(pygame.transform.scale(pygame.image.load(os.path.join(root, name)).convert_alpha(),
                                                      (platformWidth, platformHeight)))

# Loads all of the images in the ground folder into the list
for root, dirs, files in os.walk("sprites/platforms/ground", topdown=False):
    # For each file in the list, put it at the end of the list
    # Name contains the file path
    for name in files:
        groundSprites.append(pygame.transform.scale(pygame.image.load(os.path.join(root, name)).convert_alpha(),
                                                    (groundWidth, groundHeight)))

# Loads all of the images in the right folder into the first player's list
for root, dirs, files in os.walk("sprites/players/p1/right", topdown=False):
    # For each file in the list, put it at the end of the list
    # Name contains the file path
    for name in files:
        p1Sprites[0].append(
            pygame.transform.scale(pygame.image.load(os.path.join(root, name)).convert_alpha(), (30, 50)))

# Loads all of the images in the left folder into the first player's list
for root, dirs, files in os.walk("sprites/players/p1/left", topdown=False):
    # For each file in the list, put it at the end of the list
    # Name contains the file path
    for name in files:
        p1Sprites[1].append(
            pygame.transform.scale(pygame.image.load(os.path.join(root, name)).convert_alpha(), (30, 50)))

# Loads all of the images in the right folder into the second player's list
for root, dirs, files in os.walk("sprites/players/p2/right", topdown=False):
    # For each file in the list, put it at the end of the list
    # Name contains the file path
    for name in files:
        p2Sprites[0].append(
            pygame.transform.scale(pygame.image.load(os.path.join(root, name)).convert_alpha(), (30, 50)))

# Loads all of the images in the left folder into the second player's list
for root, dirs, files in os.walk("sprites/players/p2/left", topdown=False):
    # For each file in the list, put it at the end of the list
    # Name contains the file path
    for name in files:
        p2Sprites[1].append(
            pygame.transform.scale(pygame.image.load(os.path.join(root, name)).convert_alpha(), (30, 50)))


# Class Setup
# The class all kinds of platforms use
class Platform(object):
    def __init__(self, x, y, width, height, sprites, length=0):
        self.x = x  # The X position of the platform
        self.y = y  # The Y position of the platform
        self.width = width  # The width of one of the platform sprites
        self.height = height  # The height of one of the platform sprites
        self.length = length  # The length of the platform
        self.sprites = [sprites[0], sprites[2]]  # The sprites the platform will use
        self.hitBox = pygame.rect.Rect(self.x, self.y, self.width, self.height)  # The hitbox of the platform

        # Inserts the middle part into the sprite list, determined by the length
        for i in range(length):
            self.sprites.insert(1, sprites[1])

    # Draws the sprites of the platform into the game
    def draw(self, game):

        # Draws the hitbox according to the parameters
        pygame.draw.rect(game, RED, self.hitBox, 2)

        # Updates the hitbox based on the platfrom's position
        self.hitBox = pygame.rect.Rect(self.x, self.y, self.width * (self.length + 2), self.height)

        # Draws the platform's sprites onto the screen
        for i, sprite in enumerate(self.sprites):
            game.blit(sprite, (self.x + (i * self.width), self.y))


# The class all players use
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, sprites, width, height, controls, pBullet, *groups):
        super().__init__(*groups)

        # The player's position and size properties
        self.x = x  # The X position of the player
        self.y = y  # The Y position of the player
        self.width = width  # The width of the player's sprite
        self.height = height  # The height of the player's sprite

        # The player's movement properties
        self.controls = controls
        self.moveSpeed = 0  # The velocity of the player's horizontal movement
        self.fallSpeed = 0  # The velocity of the player's vertical movement
        self.vel = 6  # How fast the player can move
        self.facing = 1  # Which direction the player is facing. 1 is right, -1 is left
        self.walkCount = 0  # The current sprite the player is one
        self.isJump = False  # Tracks whether or not the player is jumping

        # The player's appearance properties
        self.hitBox = pygame.rect.Rect(self.x, self.y, self.width + 5, self.height + 5)  # The hitbox of the player
        self.sprites = sprites  # All of the player's sprites
        self.frameRate = 3

        # The player's shooting properties
        self.bullet = pBullet
        self.fireCount = 0  # How long each shot will take to come out
        self.fireRate = 5

    def checkKeys(self, controlScheme):

        # If the Space bar is pressed and there's less than 50 bullets in the list, then create a new bullet
        if controlScheme[self.controls[0]] and len(bullets) < 50:
            self.fireCount += 1
            if self.fireCount >= self.fireRate:
                if self.facing > 0:
                    bullets.append(
                        Projectile(round(self.x + self.width // 2 + 5), round(self.y + self.height // 2 + 5),
                                   self.bullet, self.facing))
                if self.facing < 0:
                    bullets.append(
                        Projectile(round(self.x + self.width // 2 + 5), round(self.y + self.height // 2 + 5),
                                   pygame.transform.flip(self.bullet, True, False), self.facing))
                self.fireCount = 0

        # If the up arrow key is pressed and the player is not jumping, let them jump and set the player's fall speed
        if controlScheme[self.controls[1]] and not self.isJump and self.fallSpeed <= 4:
            self.isJump = True
            self.fallSpeed -= 50

        # If the left arrow key is pressed and the player is within the screen, move him and change his direction
        if controlScheme[self.controls[2]] and self.x > 0 + self.width // 2:
            self.moveSpeed -= self.vel
            self.facing = -1

        # If the right arrow key is pressed and the player is within the screen, move him and change his direction
        if controlScheme[self.controls[3]] and self.x < screenWidth - self.width * 1.5:
            self.moveSpeed += self.vel
            self.facing = 1

    # Checks if the player's hitbox is within the other sprite's hitbox.
    # Moves the player depending on where they are
    def checkCollision(self, other):
        # Checks if the player's hitbox is within the other hitbox
        if self.hitBox.colliderect(other.hitBox):
            # If the player is higher than the other hitbox and is falling, then stop them
            # Y position increases as the window goes down
            # // 2 is there to prevent it from interfering with other checks
            if self.y <= other.hitBox.y and self.fallSpeed >= 0:
                self.y = other.hitBox.y - self.height  # Sets the player's Y position to just above the platform
                self.fallSpeed = 0  # Makes the player not fall any more
                self.isJump = False  # Allows the player to jump again

            # If the player is on the right side of the platform, then stop them
            if self.x > other.hitBox.x + other.hitBox.width:
                self.moveSpeed = 0  # Stops the player from moving any more into it
                self.x = other.hitBox.x + other.hitBox.width  # Sets the player's X position to the right of the hitbox
            # If the player passes the check above, and is on the left side of the platform, then stop them
            elif self.x > other.hitBox.x + other.hitBox.width:
                self.moveSpeed = 0  # Stops the player from moving any more into it
                self.x = other.hitBox.x - self.width  # Sets the player's X position to the left of the hitbox
    # Draws the player's sprites and updates their position
    def draw(self, game):

        self.fallSpeed += gravity  # Increases the player's falling speed according to gravity's value

        # If the fall speed is lower than 1 or -1, then set it to 0
        if -1 < self.fallSpeed < 1:
            self.fallSpeed = 0  # Sets the fall speed to 0

        # Otherwise, decrease it
        else:
            self.fallSpeed = self.fallSpeed * 0.95  # Shrinks the fall speed slightly

        # If the fall speed is greater than 35, then set it to 35
        # Creates a cap for the fall speed in order to prevent the player from going through platforms
        if self.fallSpeed > 50:
            self.fallSpeed = 50

        # Updates the player's Y position based of the fall speed
        self.y += self.fallSpeed

        # If the movement speed is lower than 1 or -1, then set it to 0
        if -1 < self.moveSpeed < 1:
            self.moveSpeed = 0
        # Otherwise, decrease it
        else:
            self.moveSpeed = self.moveSpeed * 0.6  # Shrinks the move speed in order to cap it

        # Updates the player's X position based on the movement speed
        self.x += self.moveSpeed

        # Resets the walk count to 0 if it's greater than the amount of sprites times the frame rate
        # Multiplied so it only changes every n frames, determined by the player's frame rate
        if self.walkCount >= len(self.sprites * self.frameRate):
            self.walkCount = 0

        # Checks if the player is facing right
        if self.facing == 1:
            # Checks if the player is moving
            if self.moveSpeed > 0:
                # Replaces the current sprite with a sprite in the list
                game.blit(self.sprites[0][self.walkCount // self.frameRate], (self.x, self.y))
                self.walkCount += 1  # Increases the walk count

            # Otherwise, set the player to the neutral sprite
            else:
                # Replaces the current sprite with a sprite in the list
                game.blit(self.sprites[0][0], (self.x, self.y))

        # If it passes the first check, then checks if the player is facing left
        elif self.facing == -1:
            # Checks if the player is moving
            if self.moveSpeed < 0:
                # Replaces the current sprite with a sprite in the list
                game.blit(self.sprites[1][self.walkCount // self.frameRate], (self.x, self.y))
                self.walkCount += 1  # Increases the walk count

            # Otherwise, set the player to the neutral sprite
            else:
                # Replaces the current sprite with a sprite in the list
                game.blit(self.sprites[1][0], (self.x, self.y))

        # Draws the player's hitbox
        pygame.draw.rect(game, BLUE, self.hitBox, 2)

        # Updates the hitbox to match the player's position
        self.hitBox = pygame.rect.Rect(self.x, self.y, self.width + 5, self.height + 5)


# The class all projectiles use
class Projectile(object):
    def __init__(self, x, y, sprite, facing=1):
        self.vel = 30 * facing  # The horizontal velocity of the projectile
        self.x = x  # The X position of the projectile
        self.y = y  # The Y position of the projectile
        self.sprite = sprite  # The sprite the projectile is using
        self.hitBox = pygame.rect.Rect(self.x, self.y, 16, 12)

    # Draws the projectile's sprite
    def draw(self, game):

        # Draws the projectile's hitbox into the game
        pygame.draw.rect(game, GREEN, self.hitBox, 2)
        # Draws the projectile's sprite at it's position
        game.blit(self.sprite, (self.x, self.y))
        # Updates the hitbox's position based on the projectile
        self.hitBox = pygame.rect.Rect(self.x, self.y, 16, 12)


# Object Setups
# The Platforms

# Holds all of the platforms in the game
Platforms = []

# Holds the position and length of each platform
platformPosition = [[50, 550, 0], [800, 550, 1], [50, 350, 3], [300, 200, 2],
                    [400, 450, 2], [700, 150, 4], [950, 400, 3], [1200, 250, 1]]

# The Ground
ground = Platform(-20, screenHeight - 85, groundWidth, groundHeight, groundSprites, screenWidth // groundWidth)

# Creates a list of platforms based on given coordinates and lengths
for platform in platformPosition:
    Platforms.append(Platform(platform[0], platform[1], platformWidth, platformHeight, platformSprites, platform[2]))
Platforms.append(ground)

bullets = []  # Contains all of the projectiles on the screen

player1 = Player(50, 200, p1Sprites, 30, 50, p1Controls, p1Bullet)  # Creates the first player's character
player2 = Player(100, 200, p2Sprites, 30, 50, p2Controls, p2Bullet)  # Creates the second player's character

Players = [player1, player2]  # Contains all of the players in the game

# A list of all the sprites in the game
all_sprites = pygame.sprite.Group()


# Method Setup
# Redraws the window with the background and sprites
def redrawGameWindow():
    # Draws the background onto the window
    win.blit(bg, (0, 0))

    # Draws every platform in the Platforms list
    for p in Platforms:
        p.draw(win)

    # Draws every character in the Players list
    for pl in Players:
        pl.draw(win)

    # Draws every projectile in the bullets list
    for b in bullets:
        b.draw(win)

    # Updates the screen with all of the sprites
    pygame.display.update()


# The Game Loop
run = True  # Tracks whether or not the game is running

# The loop that runs the game
while run:

    # Redraws the game window
    redrawGameWindow()

    clock.tick(30)  # FPS keeps the loop running at the right speed

    keys = pygame.key.get_pressed()  # Keeps track of any and all keys that have been pressed

    # Allows each player to check if any of their keys are being pressed
    for player in Players:
        player.checkKeys(keys)

    # Keeps track of every event that occurs in the game
    for event in pygame.event.get():
        # If the loop receives a quit event, then set run to false, ending the game
        if event.type == pygame.QUIT:
            run = False

    # Acts on each projectile in the bullets list
    for bullet in bullets:
        # If the projectile is in the screen, then move it
        if 0 < bullet.x < screenWidth:
            bullet.x += bullet.vel

        # Otherwise, erase it from the game
        else:
            bullets.pop(bullets.index(bullet))

    # Acts on each platform in the Platforms list
    for platform in Platforms:
        # Checks the collision for each player
        for player in Players:
            player.checkCollision(platform)

    # If the Z key is pressed, quit the game
    if keys[pygame.K_z]:
        pygame.quit()

pygame.quit()
