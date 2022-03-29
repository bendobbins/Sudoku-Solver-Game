from bs4 import BeautifulSoup as bs
import requests


def get_puzzle(site, level):
    """
    Given the websudoku URL and a query for puzzle difficulty, return a list of lists where each list is a row of one random puzzle
    of corresponding difficulty.
    """
    # Get HTML for website, find rows of table with puzzle values
    website = requests.get(site + level).text
    siteHTML = bs(website, 'lxml')
    puzzleTable = siteHTML.find("table", {'id': "puzzle_grid"})
    rows = puzzleTable.find_all('tr')

    puzzle = []
    for row in rows:
        # Get each box of given row
        values = row.find_all('td')
        newRow = []

        for value in values:
            # If box is not empty, the value will be in the value attribute of an input inside the td
            try:
                number = value.find("input").attrs['value']
                newRow.append(int(number))
            # If value does not exist for a td, the box is empty
            except KeyError:
                newRow.append(0)
        puzzle.append(newRow)

    return puzzle