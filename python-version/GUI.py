import pygame
import sys
# Initiate pygame
pygame.init()
pygame.font.init()

from generate import generate_puzzle


# Website for sudoku puzzles and queries corresponding to puzzle difficulties
SITE = "https://nine.websudoku.com/"
QUERIES = {
    "easy": "?level=1",
    "medium": "?level=2",
    "hard": "?level=3",
    "evil": "?level=4"
}

# Window constants
WIDTH = 525
HEIGHT = 600
BOXSIZE = 50
FIELDSIZE = 9
GAP = 4
SMALLGAP = 1
MARGIN = 25

# Style constants
WHITE = (255, 255, 255)
LIGHTGREY = (225, 225, 225)
RED = (245, 87, 87)
BLUE = (0, 0, 245)
BLACK = (0, 0, 0)
LARGEFONT = pygame.font.SysFont("Courier", 30)
BUTTONFONT = pygame.font.SysFont("Courier", 16)
SMALLFONT = pygame.font.SysFont("Courier", 13)
NUMBERFONT = pygame.font.SysFont("Helvetica", 30)
SMALLNUMBERFONT = pygame.font.SysFont("Helvetica", 14)

# Window and dictionary relating pygame keypresses to integers
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
NUMBERKEYS = {pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3, pygame.K_4: 4, pygame.K_5: 5, pygame.K_6: 6, pygame.K_7: 7, pygame.K_8: 8, pygame.K_9: 9}


def start_page():
    """
    Displays the introductory page where difficulty is chosen and returns hitboxes for difficulty buttons.
    """
    # Draw start page text
    textPlacementX = [WIDTH / 2, WIDTH / 2]
    textPlacementY = [HEIGHT / 2 - 200, HEIGHT - 150]
    phrases = ["Choose a Difficulty", "The puzzles used in this program are courtesy of websudoku.com"]
    fonts = [LARGEFONT, SMALLFONT]
    draw_text(textPlacementX, textPlacementY, phrases, fonts, WHITE)

    # Draw difficulty buttons
    buttonPlacementX = [WIDTH / 3 - 40, (WIDTH / 3) * 2 - 40, WIDTH / 3 - 40, (WIDTH / 3) * 2 - 40]
    buttonPlacementY = [HEIGHT / 2, HEIGHT / 2, (HEIGHT / 2) - 100, (HEIGHT / 2) - 100]
    buttonWidths = 75
    buttonHeights = 40
    phrases = ["Hard", "Evil", "Easy", "Medium"]
    buttons = draw_buttons(buttonPlacementX, buttonPlacementY, buttonWidths, buttonHeights, phrases, LIGHTGREY, BLACK)

    return buttons


def draw_buttons(widths, heights, boxwidth, boxheight, phrases, boxcolor, fontcolor):
    """
    Given information about a series of buttons to be built, draw those buttons and return their hitboxes.

    widths -- List of integer x-axis placements in the window (one for each button)\n
    heights -- List of integer y-axis placements in the window (one for each button)\n
    boxwidth -- Integer for the width of each button to be drawn\n
    boxheight -- Integer for the height of each button to be drawn\n
    phrases -- List of strings that are the text that will go into each button\n
    boxcolor -- RGB tuple of the background color for each button\n
    fontcolor -- RGB tuple of the foreground color for each button\n
    """
    buttons = []
    for i in range(len(phrases)):
        button = pygame.Rect(widths[i], heights[i], boxwidth, boxheight)
        text = BUTTONFONT.render(phrases[i], True, fontcolor)
        rect = text.get_rect()
        rect.center = button.center
        pygame.draw.rect(DISPLAY, boxcolor, button)
        DISPLAY.blit(text, rect)
        buttons.append(button)

    return buttons


def draw_text(widths, heights, phrases, fonttypes, fontcolor):
    """
    Given information about text boxes to be drawn, this draws the text into the window.

    widths -- List of integer x-axis placements in the window (one for each piece of text)\n
    heights -- List of integer y-axis placements in the window (one for each piece of text)\n
    phrases -- List of strings that are the text to be displayed\n
    fonttypes -- List of fonts (one for each piece of text)\n
    fontcolor -- RGB tuple of the foreground color of the text\n
    """
    for i in range(len(phrases)):
        text = fonttypes[i].render(phrases[i], True, fontcolor)
        textRect = text.get_rect()
        textRect.center = (widths[i], heights[i])
        DISPLAY.blit(text, textRect)





class Board:
    """
    Class for displaying the sudoku board and handling user input to the board.    
    """

    def __init__(self, puzzle, solved):
        """
        Puzzle and solved should be the original puzzle and that puzzle solved respectively.
        """
        self.puzzle = puzzle
        self.solved = solved
        self.selected = None
        # Permanents is a list of boxes whose values cannot be deleted
        self.permanents = []
        self.notes = dict()
        self.init_notes()
        self.update_permanents()

    def init_notes(self):
        for box_x in range(FIELDSIZE):
            for box_y in range(FIELDSIZE):
                self.notes[(box_x, box_y)] = []

    def update_permanents(self):
        """
        Add any boxes that are correctly filled in with the right number to the permanent list.
        """
        for box_x in range(FIELDSIZE):
            for box_y in range(FIELDSIZE):
                if self.puzzle[box_x][box_y] == self.solved[box_x][box_y]:
                    self.permanents.append((box_x, box_y))
        
    def draw_board(self):
        """
        Draw the sudoku grid with white squares for empty spaces/correct numbers and red squares for incorrect numbers.
        Draw number inside each box after the box is drawn.
        """
        for box_x in range(FIELDSIZE):
            for box_y in range(FIELDSIZE):
                left, top = get_box_placement(box_x, box_y)
                pygame.draw.rect(DISPLAY, WHITE, (left, top, BOXSIZE, BOXSIZE))

                # If the space is not empty
                if self.puzzle[box_x][box_y]:
                    self.notes[(box_x, box_y)] = []

                    # If the number in the space is not correct, background of box becomes red
                    if self.puzzle[box_x][box_y] != self.solved[box_x][box_y]:
                        pygame.draw.rect(DISPLAY, RED, (left, top, BOXSIZE, BOXSIZE))

                    # Draw number
                    number = NUMBERFONT.render(str(self.puzzle[box_x][box_y]), True, BLACK)
                    rect = number.get_rect()
                    rect.center = (left + BOXSIZE / 2, top + BOXSIZE / 2)
                    DISPLAY.blit(number, rect)
                
                else:
                    for note in self.notes[(box_x, box_y)]:
                        if note % 3 == 1:
                            width = 1.2 * (BOXSIZE / 5)
                        elif note % 3 == 2:
                            width = 2.5 * (BOXSIZE / 5)
                        else:
                            width = 3.8 * (BOXSIZE / 5)
                        if note in range(1, 4):
                            height = 1.2 * (BOXSIZE / 5)
                        elif note in range(4, 7):
                            height = 2.6 * (BOXSIZE / 5)
                        else:
                            height = 4 * (BOXSIZE / 5)
                        number = SMALLNUMBERFONT.render(str(note), True, BLACK)
                        rect = number.get_rect()
                        rect.center = (left + width, top + height)
                        DISPLAY.blit(number, rect)

                # Draw box outline
                if (box_x, box_y) == self.selected:
                    pygame.draw.rect(DISPLAY, BLUE, (left, top, BOXSIZE, BOXSIZE), 2)

    def select_square(self, mouse):
        """
        Given the position of the mouse when the user clicks, assign self.selected to the box in the grid that was clicked on.
        If the click was not inside any of the hitboxes for boxes in the grid, assign self.selected to None.
        """
        self.selected = None
        for box_x in range(FIELDSIZE):
            for box_y in range(FIELDSIZE):
                left, top = get_box_placement(box_x, box_y)
                box = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
                if box.collidepoint(mouse):
                    self.selected = (box_x, box_y)

    def draw_number(self, number, wrongGuesses):
        """
        Given an integer keyed in by the user and the integer amount of wrong guesses by the user, add the user's integer to a space in the puzzle if that space is selected and empty.
        If the number added does not correspond with the number in that space of the solved puzzle, add one to wrongGuesses.
        Return wrongGuesses as an integer.
        """
        # If a space has been selected (clicked on)
        if self.selected:

            # If the space is empty, add the number to the space in the puzzle
            if not self.puzzle[self.selected[0]][self.selected[1]]: 
                self.puzzle[self.selected[0]][self.selected[1]] = number

                # If the number is not correct according to the solved puzzle, add one to wrongGuesses
                if self.puzzle[self.selected[0]][self.selected[1]] != self.solved[self.selected[0]][self.selected[1]]:
                    wrongGuesses += 1

                # Update permanents list to include edited space if guess was correct
                self.update_permanents()

        return wrongGuesses

    def draw_notes(self, number):
        if self.selected:
            if not self.puzzle[self.selected[0]][self.selected[1]]:
                if number in self.notes[self.selected]:
                    self.notes[self.selected].remove(number)
                else:
                    self.notes[self.selected].append(number)

    def delete_number(self):
        """
        If a space in the grid is selected, delete the number inside that space if the space is not empty and is not in permanents. 
        """
        # If a space has been selected
        if self.selected:
            # If there is a number inside the space
            if self.puzzle[self.selected[0]][self.selected[1]]: 
                # If the space is not in permanents (number inside the space is not correct), delete the number inside the space
                if (self.selected[0], self.selected[1]) not in self.permanents:
                    self.puzzle[self.selected[0]][self.selected[1]] = 0

    def solve_puzzle(self):
        """
        Sets the puzzle being displayed equal to the solved version of the puzzle.
        """
        self.puzzle = self.solved





def get_box_placement(x, y):
    """
    Finds and returns the window coordinates for box (x, y) in the grid.
    """
    left = MARGIN + GAP
    for i in range(1, x + 1):
        if i % 3 == 0:
            left += BOXSIZE + GAP
        else:
            left += BOXSIZE + SMALLGAP
    
    top = MARGIN + GAP
    for i in range(1, y + 1):
        if i % 3 == 0:
            top += BOXSIZE + GAP
        else:
            top += BOXSIZE + SMALLGAP

    return left, top


def pg_events(board, buttons, difficulty, wrongGuesses):
    """
    Handles all user input events that occer during the sudoku game. Returns integer amount of wrongGuesses and string/None for difficulty.

    board -- Class of the sudoku grid being displayed\n
    buttons -- Hitboxes for all buttons in the GUI \n
    difficulty -- String of the difficulty of the game\n
    wrongGuesses -- Integer amount of wrong guesses made by the user\n
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the resest button is clicked
            if buttons[0].collidepoint(event.pos):
                # This will send user back to start page
                difficulty = None

            # If the solve button is clicked
            if buttons[1].collidepoint(event.pos):
                board.solve_puzzle()

            # Check if a box in the grid has been clicked on (selected)
            mouse = pygame.mouse.get_pos()
            board.select_square(mouse)

        if event.type == pygame.KEYDOWN:
            for key in NUMBERKEYS:
                # If the user keys in a number, use draw_number to add it to the puzzle if the correct conditions are met
                if event.key == key:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        board.draw_notes(NUMBERKEYS[key])
                    else:
                        wrongGuesses = board.draw_number(NUMBERKEYS[key], wrongGuesses)

            # If the user presses backspace, use delete_number to delete a number in a selected space if the right conditions are met
            if event.key == pygame.K_BACKSPACE:
                board.delete_number()

    return wrongGuesses, difficulty


def main():
    """
    Main function for controlling the sudoku GUI.
    """
    pygame.display.set_caption("Sudoku")
    difficulty = None
    wrongGuesses = 0

    while True:

        # If difficulty has not been chosen, show start page
        if difficulty is None:
            wrongGuesses = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            DISPLAY.fill(BLACK)

            # Check if any of the difficulty buttons have been clicked
            difficultyButtons = start_page()
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if difficultyButtons[0].collidepoint(mouse):
                    difficulty = 2
                elif difficultyButtons[1].collidepoint(mouse):
                    difficulty = 3
                elif difficultyButtons[2].collidepoint(mouse):
                    difficulty = 0
                elif difficultyButtons[3].collidepoint(mouse):
                    difficulty = 1

            if difficulty is not None:
                # Get puzzle of indicated difficulty and solve
                # puzzle = get_puzzle(SITE, QUERIES[difficulty])
                puzzle, solved = generate_puzzle(difficulty)
                # Initiate grid for puzzle
                board = Board(puzzle, solved)

        # If difficulty has been chosen, display GUI for the sudoku game
        else:
            DISPLAY.fill(WHITE)
            pygame.draw.rect(DISPLAY, BLACK, (MARGIN, MARGIN, GAP * 4 + SMALLGAP * 6 + (BOXSIZE * 9), GAP * 4 + SMALLGAP * 6 + (BOXSIZE * 9)))

            board.draw_board()

            buttons = draw_buttons([WIDTH - 130, WIDTH - 315], [HEIGHT - 70, HEIGHT - 70], 100, 40, ["Reset", "Solve"], BLACK, WHITE)
            draw_text([50, 50, 110], [HEIGHT - 60, HEIGHT - 40, HEIGHT - 50], ["Wrong", "guesses", f": {wrongGuesses}"], [SMALLFONT, SMALLFONT, BUTTONFONT], BLACK)

            wrongGuesses, difficulty = pg_events(board, buttons, difficulty, wrongGuesses)
            
        pygame.display.update()


if __name__ == "__main__":
    main()