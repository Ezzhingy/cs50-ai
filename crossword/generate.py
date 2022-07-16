import sys
import copy
import itertools
import math

from crossword import *

"""
time python3 generate.py data/structure2.txt data/words2.txt output.png
"""

class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        del_domain = copy.deepcopy(self.domains)
        for key, values in del_domain.items():
            for value in values:
                if len(value) != key.length:
                    self.domains[key].remove(value)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        del_domain_x = copy.deepcopy(self.domains[x])
        revised = False
        for value_x in del_domain_x:
            overlapping = self.crossword.overlaps[x, y]
            if overlapping != None:
                for value_y in self.domains[y]:
                    foo = False

                    if value_x[overlapping[0]] == value_y[overlapping[1]]:
                        foo = True
                        break # breaks most recent for loop
                            # continues downwards

                # no value_y == value_x, thus remove value_x
                if not foo:
                    self.domains[x].remove(value_x)

                # revision made
                revised = True
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs == None:
            all_arcs = []
            taken_arcs = []
            for variable in self.domains:
                taken_arcs.append(variable)
                neighbours = self.crossword.neighbors(variable)
                if neighbours != set():
                    for neighbour in neighbours:
                        if neighbour not in taken_arcs:
                                all_arcs.append((variable, neighbour))

            queue = all_arcs

        else:
            queue = arcs
        
        while len(queue) > 0:
            (x, y) = queue[0]
            queue.pop(0)

            if self.revise(x, y):

                if len(self.domains[x]) == 0:
                    return False
                x_neighbours = self.crossword.neighbors(x)
                if x_neighbours != set():    
                    for z in x_neighbours:
                        if z != y:
                            queue.append((z, x))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.domains:
            if var not in assignment:
                return False

        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        for variable, value in assignment.items():

            # confirm it is a distinct value
            for temp_var, temp_value in assignment.items():
                if value == temp_value and variable != temp_var:
                    return False

            #confirm value is of equal length to var length
            if len(value) != variable.length:
                return False

            variable_overlapping = self.crossword.neighbors(variable)
            if variable_overlapping != set():

                # for each overlapping var,
                for overlap_var in variable_overlapping:

                    # get the tile of overlap
                    overlap_tile = self.crossword.overlaps[variable, overlap_var]

                    # some variables may not have values yet; check those
                    if overlap_var in assignment:
                        
                        # check to see if the current var tile value == overlapping var tile value
                        if value[overlap_tile[0]] != assignment[overlap_var][overlap_tile[1]]:
                            return False
        
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # least-constraining values heuristic: return variables in order by number of choices that are ruled out for neighboring variables
        # try least-constraining values first
        
        neighbours = self.crossword.neighbors(var)
        few_great = {}
        for value in self.domains[var]:
            count = 0

            for neighbour in neighbours:
                if value in self.domains[neighbour]:
                    count += 1

            few_great[value] = count

        few_great = sorted(few_great, key=few_great.get)
        return few_great

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # MRV heuristic: select the variable that has the smallest domain
        # Degree heuristic: select the variable that is connected to the most nodes

        smallest_value = math.inf
        for variable in self.domains:
            if variable not in assignment:

                # MRV heuristic
                if len(self.domains[variable]) < smallest_value:
                    smallest_value = len(self.domains[variable])
                    smallest_var = variable

                # degree heuristic
                elif len(self.domains[variable]) == smallest_value:
                    neighbour1 = len(self.crossword.neighbors(variable))
                    neighbour2 = len(self.crossword.neighbors(smallest_var))
                    
                    if neighbour1 < neighbour2:
                        smallest_value = neighbour1
                        smallest_var = variable

        return smallest_var
    
    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.
        
        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        values = self.order_domain_values(var, assignment)
        for value in values:
            
            assignment[var] = value
            
            if self.consistent(assignment):

                # assuming that assignment[var] only takes in a string value
                result = self.backtrack(assignment)
                if result != None:
                    return result
            assignment.pop(var)

        return None


def main():


    # Check usage
    
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")


    # Parse command-line arguments
    structure = sys.argv[1]
    # structure = "data/structure0.txt"

    words = sys.argv[2]
    # words = "data/words0.txt"

    
    output = sys.argv[3] if len(sys.argv) == 4 else None
    

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
