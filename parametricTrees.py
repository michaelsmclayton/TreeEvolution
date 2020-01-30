import time
import turtle
import re
import numpy as np
import matplotlib.pyplot as plt

# Setup screen
screen = turtle.Screen()
screenSize = screen.screensize()
turtle.tracer(0) # have system draw instantly (pen.speed(0))

# Setup pen
global pen, penSize
penColour = 0
penSize = 5
initialPenSize = penSize
def makeNewPen(xOffset, yOffset, penSize):
    pen = turtle.Turtle()
    pen.hideturtle() # don't show the turtle
    pen.left(90) # point pen up instead of right
    pen.penup()
    pen.setpos(xOffset*screenSize[0], yOffset*screenSize[1])
    pen.pendown()
    pen.pensize(penSize)
    return pen
pen = makeNewPen(xOffset=0, yOffset=-.5, penSize=penSize)
pen.pencolor(penColour, penColour, penColour)

# Helper functions
def getArgs(string): # Define function to get arguments from string
    p = re.compile("[)]")
    indices = [m.start() for m in p.finditer(string)]
    return string[0:indices[0]+1]

# -----------------------
# Define production rules
# -----------------------
def X(*inputs):
    s = inputs[0] # # Get inputs (i.e. length)
    s *= RATE # Reduce length by rate
    if s > MIN:
        return \
            "F(%s)[+(%s)X(%s)][-(%s)X(%s)]X(%s)" % (s, ANGLE1, s, ANGLE2, s, s)
    else:
        return 'E'
productionRules = {
    'X': X
}

# -----------------------
# Perform iterative L-system
# -----------------------

def getLSystem(axiom, iterations=6):

    # Perform iterations
    for iteration in range(iterations):
        # Search through axiom
        new_axiom = ""
        for letter in range(len(axiom)):
            function, output = None, None
            # Get production rule (if it exists)
            try:
                rule = productionRules[axiom[letter]]
            except:
                new_axiom += axiom[letter]
                continue
            # Get function with parameters
            function = getArgs(axiom[letter:])
            # Run function
            if function != None:
                output = eval(function)
            new_axiom += output
        # Set new axiom
        axiom = new_axiom
    return axiom


# -----------------------
# Display L-system
# -----------------------

# Define pen functions
def F(length):
    pen.forward(length)
def plus(angle):
    pen.left(angle)
def minus(angle):
    pen.right(angle)
def E(x):
    pen.dot()
    leafPositions.append(pen.pos())

def drawAxiom(axiom):

    # Setup global store variables
    global leafPositions
    leafPositions, stack = [], []

    # Iterate over letters of axiom
    for letterIndex, letter in enumerate(axiom):

        # Get current pen size
        penSize = pen.pensize()

        # Get function to apply
        func = None
        if letter in ('F', 'E'):
            func = getArgs(axiom[letterIndex:])
        elif letter == '+':
            func = 'plus' + getArgs(axiom[letterIndex:])[1:]
        elif letter == '-' and axiom[letterIndex+1] == '(':
            func = 'minus' + getArgs(axiom[letterIndex:])[1:]
        elif letter == '[':
            stack.append((pen.heading(), pen.pos(), penSize))
            penSize = pen.pensize()*.6 # Update pen size
        elif letter == ']':
            heading, position, penSize = stack.pop()
            pen.penup()
            pen.goto(position)
            pen.setheading(heading)
            pen.pendown()

        # Apply function (if present)
        if func!=None:
            eval(func)

        # Update pen size
        pen.pensize(penSize)

    # Display final result
    turtle.update()

    # Return leaf positions
    return np.array(leafPositions)

# -----------------------
# Assess fitness
# -----------------------

def leafCoverFitnessFunction(leafPositions, leafWidth=4):
    if len(leafPositions)>0:
        xPositions = leafPositions[:,0]
        xSpace = np.arange(start=-screenSize[0]/2, stop=screenSize[0]/2, step=.1)
        xSpace = np.round(xSpace, decimals=1)
        leafCover = np.zeros(shape=xSpace.shape)
        for pos in xPositions:
            index = np.where(xSpace==np.round(pos, decimals=1))[0][0]
            for i in range(index-leafWidth, index+leafWidth):
                leafCover[i] = 1
        return np.sum(leafCover)
    else:
        return 0


champion = None
topfitness = 0
for i in range(100):

    # Reset screen
    screen.resetscreen()
    pen = makeNewPen(xOffset=0, yOffset=-.5, penSize=penSize)

    # Run example
    ANGLE1 = np.random.rand()*90
    ANGLE2 = np.random.rand()*90
    RATE = np.random.rand()
    MIN = np.random.rand()*30
    axiom = getLSystem(axiom = "X(100)")
    leafPositions = drawAxiom(axiom)

    # Get fitness
    fitness = leafCoverFitnessFunction(leafPositions)
    if fitness > topfitness:
        print(fitness)
        topfitness = fitness
        champion = [ANGLE1, ANGLE2, RATE, MIN, axiom]

    # time.sleep(0)

# Reset screen
screen.resetscreen()
pen = makeNewPen(xOffset=0, yOffset=-.5, penSize=penSize)

# Show winner
print('Winner found!')
ANGLE1, ANGLE2, RATE, MIN, axiom = champion
axiom = getLSystem(axiom = "X(100)")
leafPositions = drawAxiom(axiom)