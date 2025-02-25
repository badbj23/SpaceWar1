import os
import random
import turtle
import time

turtle.fd(0)
turtle.speed(0)
turtle.bgcolor("black")
turtle.title("Space War")
turtle.bgpic("/home/f2sol_admin/Desktop/giphy.gif")
turtle.ht()
turtle.setundobuffer(1)
turtle.tracer(0)

class Sprite(turtle.Turtle):
    def __init__(self, spriteshape, color, startx, starty):
        turtle.Turtle.__init__(self, shape = spriteshape)
        self.speed(0)
        self.penup()
        self.fd(0)
        self.color(color)
        self.goto(startx, starty)
        self.speed = 1


    def move(self):
        self.fd(self.speed)

        if self.xcor() > 290:
            self.setx(290)
            self.rt(60)

        if self.xcor() < -290:
            self.setx(-290)
            self.rt(60)

        if self.ycor() > 290:
            self.sety(290)
            self.rt(60)

        if self.ycor() < -290:
            self.sety(-290)
            self.rt(60)


    #location of game pieces
    def collision(self, other):
        if (self.xcor() >= (other.xcor() -20)) and \
           (self.xcor() <= (other.xcor() + 20)) and \
           (self.ycor() >= (other.ycor() - 20)) and \
           (self.ycor() <= (other.ycor() + 20)):
            return True
        else:
            return False



class Player(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.6, stretch_len=1.1, outline=None)
        self.speed = 3
        self.lives = 3

    def mk_left(self):
        self.lt(45)

    def mk_right(self):
        self.rt(45)

    def accelerate(self):
        self.speed += 1

    def decelerate(self):
        self.speed -= 1



class Opponent(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 5
        self.setheading(random.randint(0,360))



class Ally(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 7
        self.setheading(random.randint(0,360))

    def move(self):
        self.fd(self.speed)

        if self.xcor() > 290:
            self.setx(290)
            self.lt(60)

        if self.xcor() < -290:
            self.setx(-290)
            self.lt(60)

        if self.ycor() > 290:
            self.sety(290)
            self.lt(60)

        if self.ycor() < -290:
            self.sety(-290)
            self.lt(60)




class Ammo(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.3, stretch_len=0.5, outline=None)
        self.speed = 15
        self.status = "active"
        self.goto(-1000, 1000)


    def fire(self):
        if self.status == "active":
            #os.system("aplay /home/f2sol_admin/Desktop/cas-missile-launching-with-some-reverb-66630.mp3&")
            self.goto(player.xcor(), player.ycor())
            self.setheading(player.heading())

            self.status = "shoot"

    def move(self):

        if self.status == "active":
            self.goto(-1000, 1000)

        if self.status == "shoot":
            self.fd(self.speed)


        if self.xcor() < -290 or self.xcor() > 290 or \
            self.ycor() > 290 or self.ycor() < -290:
            self.goto(-1000, 1000)
            self.status = "active"


class Particles(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.1, stretch_len=0.1, outline=None)
        self.goto(-1000, -1000)
        self.frame = 0


    def explode(self, startx, starty):
        self.goto(startx, starty)
        self.setheading(random.randint(0,360))
        self.frame = 1

    def move(self):
        if self.frame > 0:
            self.fd(10)
            self.frame += 1

        if self.frame < 20:
            self.frame = 0
            self.goto(-1000, 1000)


class Game():
    def __init__(self):
        self.level = 1
        self.score = 0
        self.state = "live"
        self.pen = turtle.Turtle()
        self.lives = 3

    def border(self):
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300, 300)
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()
        self.pen.pendown()

    def status(self):
        self.pen.undo()
        msg = "Game Score: %s" %(self.score)
        self.pen.penup()
        self.pen.goto(-300, 310)
        self.pen.write(msg, align="left", font=("Arial", 20, "bold"))



game = Game()

game.border()
game.status()

player = Player("triangle", "green", 0, 0)
#opp = Opponent("circle", "red", -100, 0)
ammo = Ammo("triangle", "blue", 0, 0)
#ally = Ally("square", "purple", 0, 0)

opps =[]
for i in range(20):
    opps.append(Opponent("circle", "red", -100, 0))

allies =[]
for i in range(20):
    allies.append(Ally("square", "purple", -220, 0))

#Keyboard bindings
turtle.onkey(player.mk_left, "Left")
turtle.onkey(player.mk_right, "Right")
turtle.onkey(player.accelerate, "Up")
turtle.onkey(player.decelerate, "Down")
turtle.onkey(ammo.fire, "space")
turtle.listen()










while True:
    turtle.update()
    time.sleep(0.02)
    player.move()
    ammo.move()



    for opp in opps:
        opp.move()

        if player.collision(opp):
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            opp.goto(x, y)
            game.score -= 50
            game.status()

        # check if shot hits
        if ammo.collision(opp):
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            opp.goto(x, y)
            ammo.status = "active"
            game.score += 100
            game.status()
            for particle in Particles:
                particle.explode(Ammo.xcor(), Ammo.ycor())


    for ally in allies:
        ally.move()

        # check if shot hits ally
        if ammo.collision(ally):
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            ally.goto(x, y)
            ammo.status = "active"
            game.score -= 100
            game.status()











#delay = raw_input("Press enter to continue")