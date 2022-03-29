import random
import copy
from sudoku import solve

EMPTY = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

DIFFICULTIES = {
    0: 47,
    1: 50,
    2: 53,
    3: 56
}


def generate_puzzle(difficulty):
    nonZeroSquares = []
    # Create a first row for the empty puzzle of randomly arranged numbers
    # (necessary for easily creating puzzle with solve function)
    start = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    random.shuffle(start)
    EMPTY[0] = start
    removed = 0
    # Fill in rest of puzzle with solve function
    solution = solve(EMPTY, False)
    puzzle = copy.deepcopy(solution)

    # Remove numbers until the puzzle is a certain difficulty
    while removed < DIFFICULTIES[difficulty]:
        # Select a square to remove a number from
        column = random.randint(0, 8)
        row = random.randint(0, 8)
        # Must be a square that is not empty and does not cause multiple solutions for the puzzle
        while puzzle[row][column] == 0 or (row, column) in nonZeroSquares:
            column = random.randint(0, 8)
            row = random.randint(0, 8)

        # Change the selected box to a 0
        changedBox = puzzle[row][column]
        puzzle[row][column] = 0

        # If there is more than one solution for the puzzle, add the number back and don't remove that number again
        if solve(puzzle, True) > 1:
            puzzle[row][column] = changedBox
            nonZeroSquares.append((row, column))
        else:
            removed += 1
    
    return puzzle, solution

def main():
    generate_puzzle(0)


if __name__ == "__main__":
    main()