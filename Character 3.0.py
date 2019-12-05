import math
import random
import os
import pygame

# Game Setup
# Initializes pygame
pygame.init()

# The Original screen width and height
originalWidth, originalHeight = 1366, 768

# The Desired screen width and height
screenWidth, screenHeight = pygame.display.Info().current_w, pygame.display.Info().current_h

# The Scales for the X and Y positions
scaleX, scaleY = screenWidth / originalWidth, screenHeight / originalHeight

# Sets up the window to display the game
win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("This is a character game")

# The clock of the game
clock = pygame.time.Clock()
framesPerSecond = 30  # How many frames are within a second

# The music that plays in the game
pygame.mixer_music.load("assets/music/music.mp3")
pygame.mixer_music.play(-1)  # Plays the music infinitely

# Font setup.
smallFont = pygame.font.Font(None, 60)
largeFont = pygame.font.Font(None, 115)

# Gameplay Setup

# The control scheme for player 1
p1Controls = [pygame.K_SPACE, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT]  # (Space, Jump, Left, Right)

# The control scheme for player 2
p2Controls = [pygame.K_f, pygame.K_w, pygame.K_a, pygame.K_d]  # (Space, Jump, Left, Right)

# Sprite Appearance Setup
# The variable used to scale sprites down to fit the screen
spriteScale = 0.5

# The optimal width and height of the player sprites
playerWidth, playerHeight = round(30 * scaleX), round(50 * scaleY)

# The optimal width and height of the bullet sprites
bulletWidth, bulletHeight = round(18 * scaleX), round(12 * scaleY)

# The optimal width and height of the projectile sprites
goblinWidth, goblinHeight = round(35 * scaleX), round(55 * scaleY)

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

# The color Black, for the text
BLACK = (0, 0, 0)

# Amount of health players  and enemies have.
playerHealth = 100
slimeHealth = 30
goblinHealth = 60

# Image Setup
# Loads the background's image into the window
bg = pygame.transform.scale(pygame.image.load('assets/sprites/bg.jpg').convert_alpha(), (screenWidth, screenHeight))

# Loads the first player's bullet into the window
p1Bullet = pygame.transform.scale(
    pygame.image.load('assets/sprites/players/projectiles/p1Projectile.png').convert_alpha(),
    (bulletWidth, bulletHeight))

# Loads the first player's bullet into the window
p2Bullet = pygame.transform.scale(
    pygame.image.load('assets/sprites/players/projectiles/p2Projectile.png').convert_alpha(),
    (bulletWidth, bulletHeight))

# The optimal platform width and height
platformWidth, platformHeight = round(127 * spriteScale * scaleX), round(96 * spriteScale * scaleY)

# The list containing all platform sprites
platformSprites = []

# The optimal ground width and height
groundWidth, groundHeight = round(128 * spriteScale * scaleX), round(175 * spriteScale * scaleY)

# The optimal width and height for the slime sprites
slimeWidth, slimeHeight = round(64 * spriteScale * scaleX), round(64 * spriteScale * scaleY)

# The list containing all of the ground's sprites
groundSprites = []

# The list containing all of the first player's sprites
# First list is the right walking sprites, second list is the left walking sprites
p1Sprites = []

# The list containing all of the second player's sprites
# First list is the right walking sprites, second list is the left walking sprites
p2Sprites = []

goblinSprites = []

slimeSprites = []

# Loads all of the floating platform sprites in the floating folder into the platforms list
for root, dirs, files in os.walk("assets/sprites/platforms/floating", topdown=False):
    # For each file in the list, put it at the end of the list
    # Name contains the file path
    for name in files:
        platformSprites.append(pygame.transform.scale(pygame.image.load(os.path.join(root, name)).convert_alpha(),
                                                      (platformWidth, platformHeight)))

# Loads all of the ground sprites in the ground folder into the platforms list
for root, dirs, files in os.walk("assets/sprites/platforms/ground", topdown=False):
    # For each file in the list, put it at the end of the list
    # Name contains the file path
    for name in files:
        groundSprites.append(pygame.transform.scale(pygame.image.load(os.path.join(root, name)).convert_alpha(),
                                                    (groundWidth, groundHeight)))

# Loads all of the first player's sprites in the p1 folder into the first player's list
for root, dirs, files in os.walk("assets/sprites/players/p1", topdown=False):
    # For each file in the list, put it at the end of the list
    # Name contains the file path
    for name in files:
        p1Sprites.append(
            pygame.transform.scale(pygame.image.load(os.path.join(root, name)).convert_alpha(),
                                   (playerWidth, playerHeight)))

# Loads all of the second player's in the p2 folder into the second player's list
for root, dirs, files in os.walk("assets/sprites/players/p2", topdown=False):
    # For each file in the list, put it at the end of the list
    # Name contains the file path
    for name in files:
        p2Sprites.append(
            pygame.transform.scale(pygame.image.load(os.path.join(root, name)).convert_alpha(),
                                   (playerWidth, playerHeight)))

# Loads all of the goblin's in the goblin folder into the goblin's sprite list
for root, dirs, files in os.walk("assets/sprites/enemies/goblin", topdown=False):
    # For each file in the list, put it at the end of the list
    # Name contains the file path
    for name in files:
        goblinSprites.append(
            pygame.transform.scale(pygame.image.load(os.path.join(root, name)).convert_alpha(),
                                   (goblinWidth, goblinHeight)))

# Loads all of the goblin's in the goblin folder into the goblin's sprite list
for root, dirs, files in os.walk("assets/sprites/enemies/slimes/red", topdown=False):
    # For each file in the list, put it at the end of the list
    # Name contains the file path
    for name in files:
        slimeSprites.append(
            pygame.transform.scale(pygame.image.load(os.path.join(root, name)).convert_alpha(),
                                   (slimeWidth, slimeHeight)))


# Class Setup
# The class all kinds of platforms use
class Platform(object):
    def __init__(self, x, y, width, height, sprites, length=0):
        self.x = round(x * scaleX)  # The X position of the platform
        self.y = round(y * scaleY)  # The Y position of the platform
        self.width = width  # The width of one of the platform sprites
        self.height = height  # The height of one of the platform sprites
        self.length = length  # The length of the platform
        self.sprites = [sprites[0], sprites[2]]  # The sprites the platform will use
        self.hitBox = pygame.rect.Rect(self.x, self.y, self.width, self.height)  # The hitbox of the platform
        self.color = GREEN  # The color of the hitBox

        # Inserts the middle part into the sprite list, determined by the length
        for i in range(length):
            self.sprites.insert(1, sprites[1])

    # Draws the sprites of the platform into the game
    def draw(self, game):

        # Draws the hitbox according to the parameters
        pygame.draw.rect(game, self.color, self.hitBox, 2)

        # Updates the hitbox based on the platfrom's position
        self.hitBox = pygame.rect.Rect(self.x, self.y, self.width * (self.length + 2), self.height)

        # Draws the platform's sprites onto the screen
        for i, sprite in enumerate(self.sprites):
            game.blit(sprite, (self.x + (i * self.width), self.y))


# The class all characters use
class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, sprites, width, height, vel, color, frameRate, *groups):
        super().__init__(*groups)

        # The character's position and size properties
        self.x = round(x * scaleX)  # The X position of the character
        self.y = round(y * scaleY)  # The Y position of the character
        self.width = width  # The width of the character's sprite
        self.height = height  # The height of the character's sprite

        # The character's movement properties
        self.gravity = round(4 * scaleY)  # How fast the characters will fall
        self.moveSpeed = 0  # The velocity of the character's horizontal movement
        self.fallSpeed = 0  # The velocity of the character's vertical movement
        self.isJump = False  # Determines if the character is able to jump
        self.vel = round(vel * scaleX)  # How fast the character can move
        self.facing = 1  # Which direction the character is facing. 1 is right, -1 is left

        # The character's appearance properties
        self.color = color  # The color of the hitBox
        self.hitBox = pygame.rect.Rect(self.x, self.y, self.width + 5, self.height + 5)  # The hitbox of the character
        self.sprites = sprites  # All of the character's sprites
        self.walkCount = 0  # The current sprite the character is one
        self.frameRate = frameRate  # How fast the animation cycles through the sprites.
        # Note: Must be divisible by the number of sprites for clean animations

    # Checks if the player's hitbox is within the other sprite's hitbox.
    # Moves the player depending on where they are
    def checkCollision(self, other):
        # Checks if the player's hitbox is within the other hitbox
        if self.hitBox.colliderect(other.hitBox) and other.color == GREEN:
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

        if self.hitBox.colliderect(other.hitBox) and other.color == CYAN:
            self.vel = 0

    # Draws the player's sprites and updates their position
    def draw(self, game):

        self.fallSpeed += self.gravity  # Increases the player's falling speed according to gravity's value

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
                game.blit(self.sprites[self.walkCount // self.frameRate], (self.x, self.y))
                self.walkCount += 1  # Increases the walk count

            # Otherwise, set the player to the neutral sprite
            else:
                # Replaces the current sprite with a sprite in the list
                game.blit(self.sprites[0], (self.x, self.y))

        # If it passes the first check, then checks if the player is facing left
        elif self.facing == -1:
            # Checks if the player is moving
            if self.moveSpeed < 0:
                # Replaces the current sprite with a flipped sprite in the list
                game.blit(pygame.transform.flip(self.sprites[self.walkCount // self.frameRate], True, False),
                          (self.x, self.y))
                self.walkCount += 1  # Increases the walk count

            # Otherwise, set the player to the neutral sprite
            else:
                # Replaces the current sprite with a flipped sprite in the list
                game.blit(pygame.transform.flip(self.sprites[0], True, False), (self.x, self.y))

        # Draws the player's hitbox
        pygame.draw.rect(game, self.color, self.hitBox, 2)

        # Updates the hitbox to match the player's position
        self.hitBox = pygame.rect.Rect(self.x, self.y, self.width + 5, self.height + 5)


# The class all players use
class Player(Character):
    def __init__(self, x, y, sprites, width, height, controls, pBullet, health,
                 name, score=0, *groups):
        super().__init__(x, y, sprites, width, height, 6, BLUE, 4, *groups)

        # The player's movement properties
        self.controls = controls

        # The player's shooting properties
        self.bullet = pBullet  # Which bullet sprite the player is using
        self.fireCount = 0  # How long each shot will take to come out
        self.fireRate = framesPerSecond * 0.5  # How often the player can shoot
        self.bulletSound = pygame.mixer.Sound("assets/sounds/shoot.wav")
        self.bulletSound.set_volume(0.25)

        self.health = health
        self.name = name
        self.score = 0

    def checkKeys(self, controlScheme):

        # If the fire count isn't equal to the fire rate, add to the fire count
        # Acts as a cooldown for the bullets
        if self.fireCount != self.fireRate:
            self.fireCount += 1
        # If the Space bar is pressed and there's less than 50 bullets in the list, then create a new bullet
        if controlScheme[self.controls[0]] and len(bullets) < 50 and self.fireCount == self.fireRate:
            self.bulletSound.play()
            # If the player is facing right, then fire the normal bullet
            if self.facing > 0:
                bullets.append(Projectile(round(self.x + self.width // 2 + 5), round(self.y + self.height // 2 + 5), self.bullet, bulletWidth, bulletHeight, self.facing))
            # If the player is facing left, then flip the bullet and then fire it
            if self.facing < 0:
                bullets.append(Projectile(round(self.x - self.width // 2 + 5), round(self.y + self.height // 2 + 5), pygame.transform.flip(self.bullet, True, False), bulletWidth, bulletHeight, self.facing))
            self.fireCount = 0  # Resets the cooldown

        # If the up arrow key is pressed and the player is not jumping, let them jump and set the player's fall speed
        if controlScheme[self.controls[1]] and not self.isJump and self.fallSpeed <= 4:
            self.isJump = True
            self.fallSpeed -= 50 * scaleY

        # If the left arrow key is pressed and the player is within the screen, move him and change his direction
        if controlScheme[self.controls[2]] and self.x > 0 + self.width // 2:
            self.moveSpeed -= self.vel
            self.facing = -1

        # If the right arrow key is pressed and the player is within the screen, move him and change his direction
        if controlScheme[self.controls[3]] and self.x < screenWidth - self.width * 1.5:
            self.moveSpeed += self.vel
            self.facing = 1


# The class all enemies use
class Enemy(Character):
    def __init__(self, x, y, sprites, width, height, vel, frameRate, health, *groups):
        super().__init__(x, y, sprites, width, height, vel, RED, frameRate, *groups)

        self.health = health

    # Checks if the player's hitbox is within the other sprite's hitbox.
    # Moves the player depending on where they are
    def checkCollision(self, other):
        super().checkCollision(other)

    def draw(self, game):
        # If the enemy reaches the edge of the screen, flip it
        if self.hitBox.x < 0 or self.hitBox.x > screenWidth:
            self.x -= self.width * self.facing // 2.5
            self.vel = -self.vel
            self.facing = -self.facing
        # Otherwise, keep it moving
        else:
            self.moveSpeed += self.vel

        # Continues the normal Character draw method
        super().draw(game)


class Slime(Enemy):
    def __init__(self, x, y, sprites, width, height, vel, frameRate, health, *groups):
        super().__init__(x, y, sprites, width, height, vel, frameRate, health, *groups)

        self.spawnSound = pygame.mixer.Sound("assets/sounds/slimeSpawn.wav")
        self.walkSound = pygame.mixer.Sound("assets/sounds/slimeWalk.wav")

        self.spawnSound.set_volume(0.25)
        self.spawnSound.play(0)

        self.walkSound.set_volume(0.25)
        self.walkSound.play(-1)
        self.walkSound.fadeout(500)

        self.health = health

    def spawn(self, players):
        nearestPlayer = players[0]

        for p in players:
            if math.hypot(self.hitBox.x - nearestPlayer.hitBox.x, self.hitBox.y - p.hitBox.y)\
                    < math.hypot(self.hitBox.x - nearestPlayer.hitBox.x, self.hitBox.y - nearestPlayer.hitBox.y):
                nearestPlayer = p

        if nearestPlayer.hitBox.x < self.hitBox.x:
            self.vel *= -1
        # self.moveSpeed = nearestPlayer.hitBox.x - self.hitBox.x
        # self.fallSpeed = nearestPlayer.hitBox.y - self.hitBox.y


# The class all projectiles use
class Projectile(object):
    def __init__(self, x, y, sprite, width, height, facing=1):
        self.vel = round(30 * facing * scaleX)  # The horizontal velocity of the projectile
        self.x = x  # The X position of the projectile
        self.y = y  # The Y position of the projectile
        self.width = width  # The width of the projectile
        self.height = height  # The height of the projectile
        self.sprite = sprite  # The sprite the projectile is using
        self.hitBox = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        self.color = CYAN

    # Draws the projectile's sprite
    def draw(self, game):
        # Draws the projectile's hitbox into the game
        pygame.draw.rect(game, GREEN, self.hitBox, 2)
        # Draws the projectile's sprite at it's position
        game.blit(self.sprite, (self.x, self.y))
        # Updates the hitbox's position based on the projectile
        self.hitBox = pygame.rect.Rect(self.x, self.y, self.width, self.height)


# Object Setups
# The Platforms

# Holds all of the platforms in the game
Platforms = []

# Holds the position and length of each platform
platformPosition = [[50, 550, 0], [800, 550, 1], [50, 350, 3], [300, 200, 2],
                    [400, 450, 2], [700, 150, 4], [950, 400, 3], [1200, 250, 1]]

# The Ground
ground = Platform(-20, 680, groundWidth, groundHeight, groundSprites, screenWidth // groundWidth)

# Creates a list of platforms based on given coordinates and lengths
for platform in platformPosition:
    Platforms.append(Platform(platform[0], platform[1], platformWidth, platformHeight, platformSprites, platform[2]))
Platforms.append(ground)

bullets1 = []  # Contains all bullets shot by player 1

bullets2 = []  # Contains all bullets shot by player 2

bullets = []

# Creates the characters for the players
player1 = Player(100, 200, p1Sprites, playerWidth, playerHeight, p1Controls,
                 p1Bullet, playerHealth, "Ricky")
player2 = Player(1000, 400, p2Sprites, playerWidth, playerHeight, p2Controls,
                 p2Bullet, playerHealth, "Bobby")

Players = [player1, player2]  # Contains all of the players in the game

goblin = Enemy(50, 200, goblinSprites, goblinWidth, goblinHeight, 4, 3,
               goblinHealth)  # Creates a goblin

slime = Slime(100, 200, slimeSprites, slimeWidth, slimeHeight, 2, 6,
              slimeHealth)

Enemies = [goblin, slime]  # Contains all of the enemies in the game
# A list of all the sprites in the game
all_sprites = pygame.sprite.Group()

# Position of text on screen
player1ScoreLocation = (0, 0)
player1HealthLocation = (0, 50)
player2ScoreLocation = (screenWidth - 410, 0)
player2HealthLocation = (screenWidth - 410, 50)

# Method Setup
# Redraws the window with the background and sprites
def redrawGameWindow():
    # Draws the background onto the window
    win.blit(bg, (0, 0))

    # Draws every platform in the Platforms list
    for p in Platforms:
        p.draw(win)

    # Draws every enemy in the Enemies list
    for e in Enemies:
        e.draw(win)

    # Draws every character in the Players list
    for pl in Players:
        pl.draw(win)

    # Draws every projectile in the bullets list
    for b in bullets:
        b.draw(win)

    # Draws text to screen
    win.blit(smallFont.render(f'{player1.name}\'s Health: {player1.health}', True, BLACK),
             player1HealthLocation)
    win.blit(smallFont.render(f'{player1.name}\'s Score: {player1.score}', True, BLACK),
             player1ScoreLocation)

    win.blit(smallFont.render(f'{player2.name}\'s Health: {player2.health}', True, BLACK),
             player2HealthLocation)
    win.blit(smallFont.render(f'{player2.name}\'s Score: {player2.score}', True, BLACK),
             player2ScoreLocation)

    # Updates the screen with all of the sprites
    pygame.display.update()


# The Game Loop
run = True  # Tracks whether or not the game is running

slimeSpawnCount = 0
slimeSpawnTime = framesPerSecond * 3

# The loop that runs the game
while run:

    if slimeSpawnCount != slimeSpawnTime:
        slimeSpawnCount += 1

    if slimeSpawnCount == slimeSpawnTime:
        Enemies.append(Slime(random.randint(0, screenWidth), 0, slimeSprites,
                             slimeWidth, slimeHeight, 2, 3, slimeHealth))
        # Enemies[len(Enemies) - 1].spawn(Players)
        slimeSpawnCount = 0

    # Redraws the game window
    redrawGameWindow()

    clock.tick(framesPerSecond)  # FPS keeps the loop running at the right speed

    keys = pygame.key.get_pressed()  # Keeps track of any and all keys that have been pressed


    for player in Players:
        for bullet in bullets:
            if player.hitBox.colliderect(bullet.hitBox):
                player.health -= 10
                bullets.pop(bullets.index(bullet))
                if player.health == 0:
                    player.x, player.y = random.randrange(0, screenWidth), random.randrange(0, screenHeight)
                    player.health = 100
                    if player.name == "ricky":
                        player2.score += 10
                    else:
                        player1.score += 10

        player.checkKeys(keys)


    for enemy in Enemies:
        for bullet in bullets:
            if enemy.hitBox.colliderect(bullet.hitBox):
                enemy.health -= 10
                bullets.pop(bullets.index(bullet))
                if enemy.health == 0:
                    Enemies.pop(Enemies.index(enemy))

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

        for enemy in Enemies:
            enemy.checkCollision(bullet)

    # Acts on each platform in the Platforms list
    for platform in Platforms:
        # Checks the collision for each player
        for player in Players:
            player.checkCollision(platform)
        # Checks the collision for each enemy
        for enemy in Enemies:
            enemy.checkCollision(platform)

    # If the Z key is pressed, quit the game
    if keys[pygame.K_z]:
        pygame.quit()

pygame.quit()
