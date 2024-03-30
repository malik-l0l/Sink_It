"""
idea from : Top Gun

(Jet : You) VS (Ship : Computer)
"""

# import os
import random
from dialogues import *

# -----------------------------------------------------------------------

# These are values to create a circle radar.
SIZE = 17
a, b = 8, 8
r = 7
EPSILON = 2.1

# These values are the representations of objects in this game.

ocean_r = "~"  # ocean_representation.
ocean_b = "*"  # ocean_border.
ship = "S"  # ship representation.
missile = "X"  # missile representation.

# the 2D board
ocean = [[ocean_r for _ in range(SIZE)] for _ in range(SIZE)]

# options / nearby indexes of the ship.
opt = {
    "above-left": [],
    "above": [],
    "above-right": [],

    "left": [],
    "center": [],
    "right": [],

    "below-left": [],
    "below": [],
    "below-right": [],
}


# -----------------------------------------------------------------------

def print_ocean():
    """
    make radar shaped board
    """
    print(": RADAR :".center(SIZE + 17))
    for y in range(SIZE):
        for x in range(SIZE):
            if abs((x - a) ** 2 + (y - b) ** 2 - r ** 2) < EPSILON ** 2:
                ocean[y][x] = ocean_b
            elif abs((x - a) ** 2 + (y - b) ** 2 > r ** 2):
                ocean[y][x] = " "
    for row in ocean:
        print(" ".join(row))


def find_ship():
    """
    find ship
    :return: index of the ship's current position
    """
    for i in range(SIZE):
        for j in range(SIZE):
            if ocean[i][j] == ship:
                return i, j


def update_pos():
    """
    updates position of ship.
    :return: updated positions
    """

    i, j = find_ship()

    if i is None and j is None:
        print("oh! ship is off-radar.")
        print(f"\nCommander : {random.choice(lost_sight)}\n")
        print("~~``-- GAME OVER --``~~")
        quit()

    opt["above-left"] = [i - 1, j - 1]
    opt["above"] = [i - 1, j]
    opt["above-right"] = [i - 1, j + 1]

    opt["left"] = [i, j - 1]
    opt["center"] = [i, j]
    opt["right"] = [i, j + 1]

    opt["below-left"] = [i + 1, j - 1]
    opt["below"] = [i + 1, j]
    opt["below-right"] = [i + 1, j + 1]

    return opt


def move_ship():
    """
    move the ship from one place to another
    :return: ship's current position in 2D Array
    """
    x = random.choice(list(opt.values()))
    i, j = find_ship()
    ocean[i][j] = ocean_r
    ocean[x[0]][x[1]] = ship
    return x


def ask():
    """
    take user input (aim)
    :return: user's choice
    """

    print("options to aim:")
    for i in range(9):
        space = ""

        if i in [3, 4, 5]:
            space = "      "

        print(f"{i + 1}.{list(opt.keys())[i]}", end=f', {space}')
        if (i + 1) % 3 == 0:
            print("")
    print()

    while True:

        x = input("Take the shot :")

        if x in list(opt.keys()):
            return opt[x]
        elif x != "" and not x.isspace() and 1 <= int(x) <= 9:
            return opt[list(opt.keys())[int(x) - 1]]


def check_win(aimed, moved):
    """
    check if player wins
    :param aimed: the index where the player aimed
    :param moved: the index where the computer moved the ship before hit
    :return: 1 if ship busted or ship go off radar else 0
    """
    # check ship outside the radar.
    if abs((moved[0] - a) ** 2 + (moved[1] - b) ** 2 - r ** 2) < EPSILON ** 2:
        print(f"The ship got away!")
        print(f"\nCommander : {random.choice(lost_sight)}\n")
        print("~~``-- GAME OVER --``~~")
        return 1

    # check if aimed index == ship moved index
    elif aimed == moved:
        print("Well done!...")
        print(f"\nCommander : {random.choice(hit)}\n")
        print("~~``-- GAME OVER --``~~")
        return 1

    else:
        print(f"\nCommander : {random.choice(not_hit)}\n")
        return 0


def main():
    ocean[SIZE // 2][SIZE // 2] = ship
    print_ocean()

    print(f"\nCommander  : {random.choice(ship_spotted)}")
    print(f"Pilot(You) : {random.choice(response)}\n")
    while True:
        update_pos()
        aimed = ask()
        print("You shot  :", list(opt.keys())[list(opt.values()).index(aimed)], " :", aimed)
        moved = move_ship()
        ocean[aimed[0]][aimed[1]] = missile
        print("Ship moved:", list(opt.keys())[list(opt.values()).index(moved)], " :", moved)
        print_ocean()

        ocean[aimed[0]][aimed[1]] = ocean_r

        if check_win(aimed, moved):
            break
        # os.system("clear")


if __name__ == '__main__':
    main()
