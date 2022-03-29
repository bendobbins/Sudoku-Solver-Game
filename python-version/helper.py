class StackFrontier():
    """
    Class for implementing a frontier as a list that removes and returns the last element when prompted.
    """
    
    def __init__(self):
        self.frontier = []

    def add(self, node):
        """
        Add node to end of frontier.
        """
        self.frontier.append(node)

    def empty(self):
        """
        Return if frontier is empty.
        """
        return len(self.frontier) == 0

    def remove(self):
        """
        Remove and return last element in frontier.
        """
        # Don't need to check if frontier is empty because that is done in solve function of sudoku.py
        node = self.frontier[-1]
        self.frontier = self.frontier[:-1]
        return node