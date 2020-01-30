import turtle
import numpy as np
from TreeLSystem import TreeLSystem

# Setup screen
screen = turtle.Screen()
screenSize = screen.screensize()
turtle.tracer(0) # have system draw instantly (pen.speed(0))

# Initialise population
populationSize = 100
ANGLE1 = np.random.rand(populationSize)*90
ANGLE2 = np.random.rand(populationSize)*90
RATE = np.random.rand(populationSize)
MIN = np.random.rand(populationSize)*30

# Initialise fitness stores
maxFitness = 0
champion = None

# Iterate through organisms
for p in range(populationSize):

    # Reset screen
    screen.reset()

    # Get new organism parameters
    angle1 = ANGLE1[p]
    angle2 = ANGLE2[p]
    rate = RATE[p]
    minimum = MIN[p]

    # Make new tree
    lSystem = TreeLSystem(angle1, angle2, rate, minimum, screenSize)
    result = lSystem.run()

    # Assess fitness
    print(result['fitness'])
    if result['fitness']>maxFitness:
        maxFitness = result['fitness']
        champion = result['parameters']

# Show final winner
lSystem = TreeLSystem(champion[0], champion[1], champion[2], champion[3], screenSize)
screen.reset()
result = lSystem.run()