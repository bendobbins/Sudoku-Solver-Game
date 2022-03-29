import copy

from helper import StackFrontier

NUMBERS = [1, 2, 3, 4, 5, 6, 7, 8, 9]


def check_mini_grid(puzzle, space):
    """
    Takes a puzzle and a space in the grid, then returns all non-zero values in that space's 3x3 sudoku mini-grid.
    """
    minigrid = get_mini_grid(puzzle, space)
    takenNumbers = []
    # Find all non-zero numbers in mini-grid
    for row in minigrid:
        takenNumbers += check_row_or_column(row) 
    return takenNumbers


def get_mini_grid(puzzle, space):
    """
    Takes a puzzle grid and a space, then returns the sudoku 3x3 mini-grid for that space as a list of lists, where each nested list is a row in the mini-grid.
    """
    if space[0] <= 2:
        if space[1] <= 2:
            return [puzzle[0][:3], puzzle[1][:3], puzzle[2][:3]]
        elif space[1] >= 3 and space[1] <= 5:
            return [puzzle[0][3:6], puzzle[1][3:6], puzzle[2][3:6]]
        else:
            return [puzzle[0][6:], puzzle[1][6:], puzzle[2][6:]]

    elif space[0] >= 3 and space[0] <= 5:
        if space[1] <= 2:
            return [puzzle[3][:3], puzzle[4][:3], puzzle[5][:3]]
        elif space[1] >= 3 and space[1] <= 5:
            return [puzzle[3][3:6], puzzle[4][3:6], puzzle[5][3:6]]
        else:
            return [puzzle[3][6:], puzzle[4][6:], puzzle[5][6:]]

    else:
        if space[1] <= 2:
            return [puzzle[6][:3], puzzle[7][:3], puzzle[8][:3]]
        elif space[1] >= 3 and space[1] <= 5:
            return [puzzle[6][3:6], puzzle[7][3:6], puzzle[8][3:6]]
        else:
            return [puzzle[6][6:], puzzle[7][6:], puzzle[8][6:]]


def check_row_or_column(array):
    """
    Takes a list and returns a list of all non-zero values from it.
    """
    numberList = []
    for value in array:
        if value != 0:
            numberList.append(value)
    return numberList


def solve(puzzle, numEndings):
    """
    Takes a starting puzzle grid for a sudoku game and returns a solution grid using the backtracking algorithm.
    """
    counter = 0
    frontier = StackFrontier()
    # Get possible actions for the first empty space in the grid as well as coordinates for the space
    options = available(puzzle)

    for option in options[0]:
        # Add puzzle with possible change implemented to frontier
        frontier.add(change_state(copy.deepcopy(puzzle), options[1], option))

    while True:
        # No solution if no possible paths
        if frontier.empty():
            if not numEndings:
                raise Exception("No solution")
            return counter

        # Set puzzle equal to first state on stack
        puzzle = frontier.remove()

        # Get possible actions for next empty coordinate
        options = available(puzzle)

        # If there are actions, add them to the frontier
        # If there are no actions possible, no nodes are added to frontier, so when while loop repeats, algorithm backtracks to explore other paths
        if options[0]:
            for option in options[0]:
                child = change_state(copy.deepcopy(puzzle), options[1], option)
                frontier.add(child)

        # If there are no empty spaces, puzzle is solved
        if options[1] is None:
            if numEndings:
                counter += 1
            else:
                return puzzle


def change_state(puzzle, action, number):
    """
    Changes the value in puzzle at the coordinates of action to number.
    """
    puzzle[action[0]][action[1]] = number
    return puzzle


def available(puzzle):
    """
    Returns all possible numbers that can be placed in an empty space as well as the coordinates for the space.
    """
    # If no spaces empty return goal state
    if get_empty_space(puzzle) is None:
        return ([], None)
    
    space = get_empty_space(puzzle)
    column = []
    # Construct column that space of interest resides in
    for i in range(9):
        column.append(puzzle[i][space[1]]) 
    
    # Find all numbers that are not possible actions for the empty space by checking mini-grid, row and column
    taken = set(check_mini_grid(puzzle, space) + check_row_or_column(puzzle[space[0]]) + check_row_or_column(column))
    available = copy.deepcopy(NUMBERS)

    # Create list of numbers that can be placed in the empty space
    for num in taken:
        available.remove(num)

    return (available, space)


def get_empty_space(puzzle):
    """
    Returns the first empty space in a sudoku grid, or none if no spaces are empty.
    """
    rowCounter = 0
    for row in puzzle:
        for i in range(len(row)):
            if row[i] == 0:
                return (rowCounter, i)
        rowCounter += 1
    return None