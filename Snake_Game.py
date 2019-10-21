
import turtle
import time
import random

delay = 0.09

# Building the back ground screen 
UserGameDisplay = turtle.Screen()
UserGameDisplay.title("single player snake game")
UserGameDisplay.bgcolor("Blue")
UserGameDisplay.setup(width=800, height=800)
UserGameDisplay.tracer(0)

# constructing the snake head1
head1 = turtle.Turtle()
head1.speed(0)
head1.shape("turtle")
head1.color("yellow")
head1.penup() # turtle was meant for drawing make use the write the pen up so it does not draw
head1.goto(300,0)
head1.direction = "stop"


# constructing the snake head2
head2 = turtle.Turtle()
head2.speed(0)
head2.shape("triangle")
head2.color("red")
head2.penup() #turtle was meant for drawing make use the write the pen up so it does not draw
head2.goto(-300,0)
head2.direction = "stop"

#snake food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("purple")
food.penup()
food.goto(0,100)

Body_to_tail = []

#Functions
def Go_up():
    head1.direction = "up"

def Go_down():
    head1.direction = "down"

def Go_left():
    head1.direction = "left"

def Go_right():
    head1.direction = "right"

#Functions
def Go_up2():
    head2.direction = "up"

def Go_down2():
    head2.direction = "down"

def Go_left2():
    head2.direction = "left"

def Go_right2():
    head2.direction = "right"

#Functions
def move():
    if head1.direction == "up":
        y = head1.ycor()
        head1.sety(y + 20)

    if head1.direction == "down":
        y = head1.ycor()
        head1.sety(y - 20)

    if head1.direction == "left":
        x = head1.xcor()
        head1.setx(x - 20)

    if head1.direction == "right":
        x = head1.xcor()
        head1.setx(x + 20)

#Functions
def move():
    if head2.direction == "up":
        y = head2.ycor()
        head2.sety(y + 20)

    if head2.direction == "down":
        y = head2.ycor()
        head2.sety(y - 20)

    if head2.direction == "left":
        x = head2.xcor()
        head2.setx(x - 20)
        #turtle.tilt(120)

    if head2.direction == "right":
        x = head2.xcor()
        head2.setx(x + 20)


# Keyboard bindings
UserGameDisplay.listen()
UserGameDisplay.onkeypress(Go_up, "w")
UserGameDisplay.onkeypress(Go_down, "s")
UserGameDisplay.onkeypress(Go_left, "a")
UserGameDisplay.onkeypress(Go_right, "d")

# Keyboard bindings
UserGameDisplay.listen()
UserGameDisplay.onkeypress(Go_up2, "Up")
UserGameDisplay.onkeypress(Go_down2, "Down")
UserGameDisplay.onkeypress(Go_left2, "Left")
UserGameDisplay.onkeypress(Go_right2, "Right")


#Main game Loop 
while True:
    UserGameDisplay.update()

    # When head of snake touches fruit

    if head1.distance(food) < 20:
        #Move the food to a random spot
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x,y)

        # Add a Body to the snake
        new_body = turtle.Turtle()
        new_body.speed(0)
        new_body.shape("square")
        new_body.colr("grey")
        new_body.penup()
        body.append(new_body)

    move()

    time.sleep(delay)


UserGameDisplay.mainloop()


