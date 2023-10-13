from random import random

validMoves = ["C", "M", "CC", "MM", "CM"]

right = ["C"] * 3 + ["M"] * 3
left = []
boat = "R"

def randInd():
    ind = []
    for i in range(11):
        ind.append(validMoves[int(random() * len(validMoves))])
    return ind

def moveBoat():
    global boat
    if boat == "R":
        boat = "L"
    else:
        boat = "R"


def checkEaten(fitness):
    if (right.count("C") > right.count("M") and right.count("M") > 0) or (
            left.count("C") > left.count("M") and left.count("M") > 0):
        fitness -= 5
        #print("Eaten - Fitness: " + str(fitness))
    return fitness


def play(move, fitness, double=False, skip_check=False):
    global boat
    global right
    global left

    #print(f"Move: {move}, Fitness: {fitness}")

    if len(move) == 1:
        if boat == "R" and move in right:
            right.remove(move)
            left.append(move)
            if not double:
                moveBoat()
                fitness += 1
        elif boat == "L" and move in left:
            left.remove(move)
            right.append(move)
            if not double:
                moveBoat()
                fitness += 1
        else:
            fitness -= 5  # Penalty for invalid move
    else:
        fitness = play(move[0], fitness, double=True, skip_check=True)  # capture returned fitness
        fitness = play(move[1], fitness, double=True, skip_check=True)  # capture returned fitness
        moveBoat()
        fitness += 1

    if not skip_check:
        fitness = checkEaten(fitness)

    return fitness



def testInd(ind):
    global right
    global left

    #print(ind)

    right = ["C"] * 3 + ["M"] * 3
    left = []

    #print(len(ind))
    fitness = 0
    for move in ind:
        fitness = play(move, fitness)
        #print(f"Move: {move}, Fitness: {fitness}")

    # Check for redundant moves, i.e. moving the boat back and forth
    for i in range(len(ind) - 1):
        if ind[i] == ind[i + 1]:
            fitness -= 10

    if len(left) != 6:
        fitness -= 3

    #print(f"Final Fitness: {fitness}")
    return fitness,




winner = ["CC", "C", "CC", "C", "MM", "MC", "MM", "C", "CC", "C", "CC"]

#ind = randInd()
#print(testInd(winner))
