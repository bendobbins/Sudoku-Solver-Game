#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <set>

using namespace std;

int * readCSVrow(string row);
int ** get_puzzle();
vector<int> check_minigrid(vector<int> space, int **puzzle);
vector<int> get_taken_minigrid(int horistart, int vertistart, int **puzzle);
vector<int> check_row_or_column(vector<int> space, int **puzzle);
vector<int> get_empty_space(int **puzzle);
vector< vector<int> > available(int **puzzle);
int ** puzzle_maker(int **puzzle, int state, vector<int> action);
int ** solve(int **puzzle);
void make_answer(int **puzzle);


int * readCSVrow(string row) {
    // Initialize pointer to array of ints, allocate memory for array
    int *p = new int[9];
    if (!p) {
        cout << "Memory allocation error\n";
        exit(2);
    }
    
    int counter = 0;
    // Read each numeric value in from one row of csv file, convert value to int and add to array
    for (int i=0; i<row.length(); i++) {
        if (row[i] != ' ' && row[i] != ',' && row[i] != '\n') {
            p[counter] = row[i] - '0';
            counter++;
        }
    }

    return p;
}


int ** get_puzzle() {
    // Initialize pointer to array of 9 pointers, allocate memory for array
    int **puzzle = new int*[9];
    if (!puzzle) {
        cout << "Memory allocation error\n";
        exit(2);
    }

    // Read csv file
    ifstream myfile;
    myfile.open("puzzle.csv");
    if (myfile.fail()) {
        cout << "Puzzle file could not be opened\n";
        exit(1);
    }

    string row;
    int counter = 0;
    // Pass each row of file to readCSVrow until file ends
    while (!myfile.eof()) {
        getline(myfile, row);

        if (myfile.bad() || myfile.fail()) {
            cout << "Problem reading puzzle line\n";
            exit(1);
        }

        // Add pointer to array of csv row integers to array of pointers
        int *p = readCSVrow(row);
        puzzle[counter] = p;
        counter++;
    }

    myfile.close();
    return puzzle;
}


vector<int> check_minigrid(vector<int> space, int **puzzle) {
    vector<int> taken;
    taken.reserve(9);

    // Find the section of the puzzle that contains the minigrid for the space in question, then pass to get_taken_minigrid
    if (space[0] <= 2) {
        if (space[1] <= 2) {
            taken = get_taken_minigrid(0, 0, puzzle);
        }
        else if (space[1] >= 3 && space[1] <= 5) {
            taken = get_taken_minigrid(0, 3, puzzle);
        }
        else {
            taken = get_taken_minigrid(0, 6, puzzle);
        }
    }

    else if (space[0] >= 3 && space[0] <= 5) {
        if (space[1] <= 2) {
            taken = get_taken_minigrid(3, 0, puzzle);
        }
        else if (space[1] >= 3 && space[1] <= 5) {
            taken = get_taken_minigrid(3, 3, puzzle);
        }
        else {
            taken = get_taken_minigrid(3, 6, puzzle);
        }
    }

    else {
        if (space[1] <= 2) {
            taken = get_taken_minigrid(6, 0, puzzle);
        }
        else if (space[1] >= 3 && space[1] <= 5) {
            taken = get_taken_minigrid(6, 3, puzzle);
        }
        else {
            taken = get_taken_minigrid(6, 6, puzzle);
        }
    }

    // Return numbers that are in the space's minigrid
    return taken;
}


vector<int> get_taken_minigrid(int horistart, int vertistart, int **puzzle) {
    vector<int> taken;
    taken.reserve(9);

    // Border of minigrid vertically and horizontally will be 3 spaces away from the start
    int horiend = horistart + 3;
    int vertiend = vertistart + 3;
    for (int i=horistart; i<horiend; i++) {
        for (int j=vertistart; j<vertiend; j++) {
            // Add numbers of all not empty spaces in minigrid to vector
            if (puzzle[i][j] != 0) {
                taken.push_back(puzzle[i][j]);
            }
        }
    }
    return taken;
}


vector<int> check_row_or_column(vector<int> space, int **puzzle) {
    vector<int> taken;
    taken.reserve(18);

    for (int i=0; i<9; i++) {
        // Add all numbers from non-empty spaces in the same row as the argument space to the taken vector
        if (puzzle[space[0]][i] != 0) {
            taken.push_back(puzzle[space[0]][i]);
        }
        // Add all numbers from non-empty spaces in the same column as the argument space to the taken vector
        if (puzzle[i][space[1]] != 0) {
            taken.push_back(puzzle[i][space[1]]);
        }
    }
    return taken;
}


vector<int> get_empty_space(int **puzzle) {
    vector<int> space;
    space.reserve(2);

    for (int i=0; i<9; i++) {
        for (int j=0; j<9; j++) {
            // Return the first empty space (space that == 0) from the puzzle, if there is one
            if (puzzle[i][j] == 0) {
                space.push_back(i);
                space.push_back(j);
                return space;
            }
        }
    }
    return space;
}


vector< vector<int> > available(int **puzzle) {
    vector<int> available;
    available.reserve(9);
    vector<int> space = get_empty_space(puzzle);

    // If there is an empty space
    if (space.size() != 0) {
        // Find all possible values that cannot go in the space by checking its row, column and minigrid
        vector<int> taken_grid = check_minigrid(space, puzzle);
        vector<int> taken_column_row = check_row_or_column(space, puzzle);

        // Iterate over taken values in minigrid and row/column, adding them to a set so that values are unique
        set<int> taken_unique;
        vector<int>::iterator itr1 = taken_column_row.begin();
        vector<int>::iterator itr2 = taken_grid.begin();
        while (itr1 != taken_column_row.end()) {
            taken_unique.insert(*itr1);
            itr1++;
        }
        while (itr2 != taken_grid.end()) {
            taken_unique.insert(*itr2);
            itr2++;
        }

        // For numbers 1-9, check if they can be found in the set, and add them to available if not
        for (int i=1; i<10; i++) {
            if (find(taken_unique.begin(), taken_unique.end(), i) == taken_unique.end()) {
                available.push_back(i);
            }
        }
    }

    // Return a vector that stores a space and all available numbers that can go in that space
    vector< vector<int> > avail_and_space;
    avail_and_space.reserve(2);
    avail_and_space.push_back(available);
    avail_and_space.push_back(space);
    return avail_and_space;
}


int ** puzzle_maker(int **puzzle, int state, vector<int> action) {
    // Create new pointer initialized to an array of pointers (in essence, a new puzzle)
    int **newpuzzle = new int*[9];
    if (!newpuzzle) {
        cout << "Memory allocation error\n";
        exit(2);
    }

    for (int i=0; i<9; i++) {
        // Create pointer initialized to array of ints (new row for the puzzle)
        int *newrow = new int[9];
        if (!newrow) {
            cout << "Memory allocation error\n";
            exit(2);
        }

        for (int j=0; j<9; j++) {
            // When the first empty space in the puzzle is reached, add the available number to that spot
            if (i == action[0] && j == action[1]) {
                newrow[j] = state;
            }
            // Otherwise, fill up the puzzle with all the same values as the last one so the only difference is the one change on the first empty space
            else {
                newrow[j] = puzzle[i][j];
            }
        }
        newpuzzle[i] = newrow;
    }

    return newpuzzle;
}


int ** solve(int **puzzle) {
    // Vector for holding all possible puzzles (acts like a stack frontier would in the python implementation)
    vector<int **> puzzles;

    vector< vector<int> > avail = available(puzzle);
    for (int i=0; i<avail[0].size(); i++) {
        // Add puzzles to the stack exloring each possible number that can occupy the first empty space
        puzzles.push_back(puzzle_maker(puzzle, avail[0][i], avail[1]));
    }

    // Deallocate memory for initial puzzle
    for (int i=0; i<9; i++) {
        delete[] puzzle[i];
    }
    delete[] puzzle;

    while (true) {
        // Check if there are no possible puzzles left to explore
        if (puzzles.size() == 0) {
            cout << "No solution\n";
            exit(3);
        }

        // Take the last added puzzle from the stack and pop it out to explore
        int **nextpuzzle = puzzles.back();
        puzzles.pop_back();
        vector< vector<int> > avail = available(nextpuzzle);

        // If there is no empty space in the puzzle (goal state)
        if (avail[1].size() == 0) {
            // Go through puzzles vector and deallocate memory for every puzzle, then return solution
            for (int i=0; i<puzzles.size(); i++) {
                for (int j=0; j<9; j++) {
                    delete[] puzzles[i][j];
                }
                delete[] puzzles[i];
            }
            return nextpuzzle;
        }

        // Add more puzzles to stack, again exploring each possible number that can occupy the first empty space
        for (int i=0; i<avail[0].size(); i++) {
            puzzles.push_back(puzzle_maker(nextpuzzle, avail[0][i], avail[1]));
        }

        // Deallocate memory for puzzle state that was just explored
        for (int i=0; i<9; i++) {
            delete[] nextpuzzle[i];
        }
        delete[] nextpuzzle;
    }
}


void make_answer(int **puzzle) {
    ofstream myfile;
    myfile.open("answer.csv");

    for (int i=0; i<9; i++) {
        for (int j=0; j<9; j++) {
            // Add row of puzzle
            myfile << puzzle[i][j];
            if (j != 8) {
                myfile << ", ";
            }
        }
        if (i != 8) {
            myfile << '\n';
        }
    }
    myfile.close();
}


int main() {
    int **puzzle = get_puzzle();
    int **solved = solve(puzzle);
    make_answer(solved);

    // Deallocate memory for solution puzzle, which is last puzzle with memory that still needs to be freed
    for (int i=0; i<9; i++) {
        delete[] solved[i];
    }
    delete[] solved;
    return 0;
}