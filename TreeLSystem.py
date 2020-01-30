import time
import turtle
import re
import numpy as np
import matplotlib.pyplot as plt

class TreeLSystem:
    '''Tree L-System'''

    # ------------------------------------------
    # Constructor
    def __init__(self, ANGLE1, ANGLE2, RATE, MIN, screenSize):
        self.ANGLE1 = ANGLE1
        self.ANGLE2 = ANGLE2
        self.RATE = RATE
        self.MIN = MIN
        self.leafPositions = None
        self.screenSize = screenSize
        self.pen = None
        self.productionRules

    # ------------------------------------------
    # Helper functions
    def getArgs(self, string): # Define function to get arguments from string
        p = re.compile("[)]")
        indices = [m.start() for m in p.finditer(string)]
        return string[0:indices[0]+1]

    def makeNewPen(self, screenSize, xOffset=0, yOffset=-.5, penSize=5, penColour=0):
        pen = turtle.Turtle()
        pen.hideturtle() # don't show the turtle
        pen.left(90) # point pen up instead of right
        pen.penup()
        pen.setpos(xOffset*screenSize[0], yOffset*screenSize[1])
        pen.pendown()
        pen.pensize(penSize)
        pen.pencolor(penColour, penColour, penColour)
        return pen

    # ------------------------------------------
    # Define production rules
    def X(self, *inputs):
        s = inputs[0] # # Get inputs (i.e. length)
        s *= self.RATE # Reduce length by rate
        if s > self.MIN:
            return \
                "F(%s)[+(%s)X(%s)][-(%s)X(%s)]X(%s)" % (s, self.ANGLE1, s, self.ANGLE2, s, s)
        else:
            return 'E'
    productionRules = {
        'X': X
    }


    # ------------------------------------------
    # Perform iterative L-system
    def getLSystem(self, axiom, iterations=6):
        # Perform iterations
        for iteration in range(iterations):
            # Search through axiom
            new_axiom = ""
            for letter in range(len(axiom)):
                function, output = None, None
                # Get production rule (if it exists)
                try:
                    rule = self.productionRules[axiom[letter]]
                except:
                    new_axiom += axiom[letter]
                    continue
                # Get function with parameters
                function = self.getArgs(axiom[letter:])
                # Run function
                if function != None:
                    output = eval('self.'+function)
                new_axiom += output
            # Set new axiom
            axiom = new_axiom
        return axiom


    # ------------------------------------------
    # Define turtle movement functions
    def F(self, length):
        self.pen.forward(length)
    def plus(self, angle):
        self.pen.left(angle)
    def minus(self, angle):
        self.pen.right(angle)
    def E(self, x):
        self.pen.dot()
        self.leafPositions.append(self.pen.pos())

    # ------------------------------------------
    # Draw function
    def drawAxiom(self, axiom):

        # Setup global store variables
        self.leafPositions, stack = [], []

        # Iterate over letters of axiom
        for letterIndex, letter in enumerate(axiom):

            # Get current pen size
            penSize = self.pen.pensize()

            # Get function to apply
            func = None
            if letter in ('F', 'E'):
                func = self.getArgs(axiom[letterIndex:])
            elif letter == '+':
                func = 'plus' + self.getArgs(axiom[letterIndex:])[1:]
            elif letter == '-' and axiom[letterIndex+1] == '(':
                func = 'minus' + self.getArgs(axiom[letterIndex:])[1:]
            elif letter == '[':
                stack.append((self.pen.heading(), self.pen.pos(), penSize))
                penSize = self.pen.pensize()*.6 # Update pen size
            elif letter == ']':
                heading, position, penSize = stack.pop()
                self.pen.penup()
                self.pen.goto(position)
                self.pen.setheading(heading)
                self.pen.pendown()

            # Apply function (if present)
            if func!=None:
                eval('self.'+func)

            # Update pen size
            self.pen.pensize(penSize)

        # Display final result
        turtle.update()

        # Return leaf positions
        return np.array(self.leafPositions)

    # ------------------------------------------
    # Assess fitness
    def leafCoverFitnessFunction(self, leafWidth=4):
        if len(self.leafPositions)>0:
            xPositions = self.leafPositions[:,0]
            xSpace = np.arange(start=-self.screenSize[0]/2, stop=self.screenSize[0]/2, step=.1)
            xSpace = np.round(xSpace, decimals=1)
            leafCover = np.zeros(shape=xSpace.shape)
            for pos in xPositions:
                index = np.where(xSpace==np.round(pos, decimals=1))[0][0]
                for i in range(index-leafWidth, index+leafWidth):
                    leafCover[i] = 1
            return np.sum(leafCover)
        else:
            return 0

    # ------------------------------------------
    # Run function
    def run(self):
        self.pen = self.makeNewPen(self.screenSize)
        axiom = self.getLSystem("X(100)")
        self.leafPositions = self.drawAxiom(axiom)
        fitness = self.leafCoverFitnessFunction()
        return {
            'parameters': [self.ANGLE1, self.ANGLE2, self.RATE, self.MIN],
            'fitness': fitness
        }
