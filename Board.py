import csv
import copy
import random


class Board:

    '''
        represents start board, not completed board,
           cnf solved completed board should construct fromSolver()

        board: 2D array of only ints representing starting dots
    '''
    def __init__(self, board:list[list[int]]):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0]) if board else 0

        # {color(int): [[dot1x, dot1y], [dot2x, dot2y]]}
        self.dots = {}
        for row in range(self.rows):
            for col in range(self.cols):
                if type(board[row][col]) == int:
                    if board[row][col] != -1:
                        if board[row][col] not in self.dots:
                            self.dots[board[row][col]] = []

                        self.dots[board[row][col]].append([row, col])

        self.numColors = len(set(color for row in board for color in row if type(color) == int))

    @classmethod
    def fromCSV(cls, csvFile:str):
        board = []
        with open(csvFile, 'r') as f:
            board = list(csv.reader(f, delimiter=','))
            f.close()
        
        # convert str->int, including if negative, else None (for empty cell)
        board = [[int(entry) if entry.lstrip('-').isdigit() else None for entry in row] for row in board]
        
        return cls(board)
    
    '''
        represents solved board, from solver.solution

        board: 2D array of int arrays of (color, dir), but starting dots are just a single int
    '''
    @classmethod
    def fromSolver(cls, solver):
        board = solver.board
        board = [[[None, None] if entry == None else entry for entry in row] for row in board]

        trueVars = [var for var in solver.solution if var > 0 and var is not None]

        for var in trueVars:
            try:
                colorCell = solver.IndexToColorCell(abs(var))
                board[colorCell.row][colorCell.col][0] = colorCell.color
            except KeyError:
                pass
            except TypeError:
                pass

            try:
                directionCell = solver.IndexToDirectionCell(abs(var))
                board[directionCell.row][directionCell.col][1] = directionCell.direction
            except KeyError:
                pass
            except TypeError:
                pass

        return cls(board)
    
    def isValidPoint(self, row, col):
        return 0 <= row and row < self.rows and 0 <= col and col < self.cols

    '''
        returns 2D array of neighbors: [[row, col], ...]
    '''
    def getNeighbors(self, row, col):
        neighbors = []

        neighbors.append([row+1, col])
        neighbors.append([row-1, col])
        neighbors.append([row, col+1])
        neighbors.append([row, col-1])

        return list(filter(lambda x: self.isValidPoint(x[0], x[1]), neighbors))
    
    def isDot(self, row, col):
        return self.board[row][col] != None and type(self.board[row][col]) == int and self.board[row][col] != -1

    def __str__(self):
        SQUARE = '■'
        RESET = '\033[0m'
        BRIDGE = '#'
        COLOR = {
            'Red': '\033[91m',
            'Green': '\033[92m',
            'Yellow': '\033[93m',
            'Blue': '\033[94m',
            'Magenta': '\033[95m',
            'Cyan': '\033[96m',
            'Bright Red': '\033[31m',
            'Bright Green': '\033[32m',
            'Bright Yellow': '\033[33m',
            'Bright Blue': '\033[34m',
            'Bright Magenta': '\033[35m',
            'Bright Cyan': '\033[36m',
            'Bright White': '\033[37m',
            'Gray': '\033[90m',
            'Orange': '\033[38;5;214m',  # Orange
            'Pink': '\033[38;5;213m',    # Pink
            'Purple': '\033[38;5;129m',  # Purple
            'Teal': '\033[38;5;37m',     # Teal
            'Bright Gray': '\033[37m',
            'White' : RESET
        }

        DIRECTIONS = [
                '\u2500',  # Horizontal line (─)        0
                '\u2502',  # Vertical line (│)          1
                '\u2514',  # Bottom-left corner (└)     2
                '\u2518',  # Bottom-right corner (┘)    3
                '\u250C',  # Top-left corner (┌)        4
                '\u2510',  # Top-right corner (┐)       5
        ]

        string = ''
        string += ('--'*self.rows)
        for row in self.board:
            string += '\n|'
            for i, v in enumerate(row):
                use_char = SQUARE
                entry = ''
                if type(v) == list:
                    entry = v[0]
                    if v[1] == None:
                        use_char = SQUARE
                    else:
                        use_char = DIRECTIONS[v[1]]
                else:
                    entry = v

                if entry == -1:
                    use_char = BRIDGE

                if entry != None:
                    string += COLOR[list(COLOR.keys())[entry]] + use_char + RESET + '|'
                else:
                    string += ' |'
            string += '\n' + ('--'*self.rows)

        return string
    
    def make_board(boardName, rows, cols):
        board = [[None for _ in range(cols)] for _ in range(rows)]
        
        for row in range(rows):
            print('new row')
            for col in range(cols):
                res = input(f"Enter value for cell ({row}, {col}): ")
                if res != '':
                    board[row][col] = res
                else:
                    board[row][col] = 'None'

        colors = set()
        for row in board:
            for cell in row:
                if cell != 'None':
                    colors.add(cell)
        # color = [i for i in range(len(colors))]
        color_map = {k: v for k, v in zip(colors, [i for i in range(len(colors))])}
        print(colors)
        print(color_map)
        for row in range(rows):
            for col in range(cols):
                if board[row][col] != 'None':
                    board[row][col] = color_map[board[row][col]]

        with open('Boards/' + boardName + '.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(board)

        return board
    
    '''
        returns the direction of the given cell, -2 if its a dot, -1 if its a bridge, None if empty
    '''
    def getDirection(self, row, col):
        if self.board[row][col] == None:
            return None

        if type(self.board[row][col]) == int:
            if self.board[row][col] == -1:
                return -1
            else:
                return -2

        return self.board[row][col][1]

    '''
        returns the color of the given cell, -1 if its a bridge, None if empty
    '''
    def getColor(self, row, col):
        if self.board[row][col] == None:
            return None

        if type(self.board[row][col]) == int:
            if self.board[row][col] == -1:
                return -1
            else:
                return self.board[row][col]

        return self.board[row][col][0]


    '''
        given point, returns list of neighbors that direction flow into the given point
    '''
    def flowingNeighbors(self, row, col):
        neighbors = self.getNeighbors(row, col)
        flowingNeighbors = []

        direction = self.getDirection(row, col)
        for neighbor in neighbors:
            # check if neighbor is same color as given
            if self.getColor(neighbor[0], neighbor[1]) != self.getColor(row, col):
                continue

            neighborDirection = self.getDirection(neighbor[0], neighbor[1])

            # check if neighbor is a bridge or empty
            if neighborDirection == None or neighborDirection == -1:
                continue

            # check if neighbor flows into current
            if neighborDirection == -2:
                flowingNeighbors.append(neighbor)

            # down
            if neighbor == [row+1, col]:
                if neighborDirection == 1 or neighborDirection == 2 or neighborDirection == 3:
                    flowingNeighbors.append(neighbor)

            # up
            elif neighbor == [row-1, col]:
                if neighborDirection == 1 or neighborDirection == 4 or neighborDirection == 5:
                    flowingNeighbors.append(neighbor)

            # right
            elif neighbor == [row, col+1]:
                if neighborDirection == 0 or neighborDirection == 3 or neighborDirection == 5:
                    flowingNeighbors.append(neighbor)

            # left
            elif neighbor == [row, col-1]:
                if neighborDirection == 0 or neighborDirection == 2 or neighborDirection == 4:
                    flowingNeighbors.append(neighbor)

            else:
                print('FLOWING NEIGHBORS ERROR: this should not happen')
                print('FLOWING NEIGHBORS ERROR: this should not happen')
                print('FLOWING NEIGHBORS ERROR: this should not happen')


        return flowingNeighbors


    '''
        returns True if the given dot has a valid flow from one to the other
    '''
    def validDotFlow(self, dotpos1, dotpos2, checked=[]):
        # print('checking dots:', dotpos1, dotpos2)
        flowingNeighbors = self.flowingNeighbors(dotpos1[0], dotpos1[1])
        
        checked.append(dotpos1)
        flowingNeighbors = list(filter(lambda x: x not in checked, flowingNeighbors))

        # check if both dots are the same color
        if dotpos1 == dotpos2:
            return True

        # if more than 1 flowing neighbor, return false
        if len(flowingNeighbors) != 1:
            return False
        
        return self.validDotFlow(flowingNeighbors[0], dotpos2, checked=checked)
        
    def isSolved(self):
        for row in self.board:
            for cell in row:
                if cell == None:
                    return False

        for dot in self.dots.values():
            # print(f'checking dot: {dot}')
            if not self.validDotFlow(dot[0], dot[1]):
                return False
        
        return True
    
    '''
        getNeighbors but has a key for the direction, value of None = not possible direction
        {'left': [row, col], 'right': [row, col], 'up': [row, col], 'down': [row, col]}
    '''
    def getNeighborsDict(self, row, col):
        neighbors = {
            'left': [row, col-1],
            'right': [row, col+1],
            'up': [row-1, col],
            'down': [row+1, col]
        }

        for key in neighbors.keys():
            if not self.isValidPoint(neighbors[key][0], neighbors[key][1]):
                neighbors[key] = None

        return neighbors
    
    '''
        given a point's direction, returns the neighbors that direction can flow
    '''
    def directionNeighbors(self, row, col, direction):
        neighbors = self.getNeighborsDict(row, col)
        # print('neighbors:', neighbors)

        DIRECTIONS = [
                        '\u2500',  # Horizontal line (─)        0
                        '\u2502',  # Vertical line (│)          1
                        '\u2514',  # Bottom-left corner (└)     2
                        '\u2518',  # Bottom-right corner (┘)    3
                        '\u250C',  # Top-left corner (┌)        4
                        '\u2510',  # Top-right corner (┐)       5
                    ]
        # check if direction is valid
        directionNeighbors = []
        # ─
        if direction == 0:
            directionNeighbors = [neighbors['left'], neighbors['right']]
        # │
        elif direction == 1:
            directionNeighbors = [neighbors['up'], neighbors['down']]
        # └
        elif direction == 2:
            directionNeighbors = [neighbors['up'], neighbors['right']]
        # ┘
        elif direction == 3:
            directionNeighbors = [neighbors['up'], neighbors['left']]
        # ┌
        elif direction == 4:
            directionNeighbors = [neighbors['down'], neighbors['right']]
        # ┐
        elif direction == 5:
            directionNeighbors = [neighbors['down'], neighbors['left']]
            
        return list(filter(lambda x: x != None, directionNeighbors))


    '''
        given a point, returns its valid moves that connect to it
            - returns all possible valid moves for a cell
    '''
    def allPossibleNeighbors(self, row, col):
        # possibleNeighbors = [[row+1, col], [row-1, col], [row, col+1], [row, col-1]]
        # possibleNeighbors = list(filter(lambda x: self.isValidPoint(x[0], x[1]) and not self.isDot(x[0], x[1]), possibleNeighbors))

        # [[row, col, color, direction], ...]
        allPossibleNeighbors = []        
        color = self.getColor(row, col)
        # print([row, col])

        # if path complete, return None
        # print('allPossibleNeighbors traversedDot ', self.traverseDot(row, col))
        # if self.traverseDot(row, col) == None:
        #     return None

        possibleNeighbors = self.getNeighbors(row, col)
        # dont want neighbors that are dots already, they cannot be overwritten
        possibleNeighbors = list(filter(lambda x: not self.isDot(x[0], x[1]), possibleNeighbors))
        # print(possibleNeighbors)
        possibleNeighbors = list(filter(lambda x: self.getDirection(x[0], x[1]) == None, possibleNeighbors))
        # print(possibleNeighbors)

        diagonal = False
        for possibleNeighbor in possibleNeighbors:
            for direction in range(6):
                # print(possibleNeighbor)
                if color == None:
                    print('doing allPossibleNeighbors() on empty cell, probably shouldnt do this, color == None')

                directionNeighbors = self.directionNeighbors(possibleNeighbor[0], possibleNeighbor[1], direction)

                # make sure direction has valid flows
                if len(directionNeighbors) != 2:
                    continue

                # make sure direction flows into the given point
                if not directionNeighbors.__contains__([row, col]):
                    continue

                # make sure [row, col]'s directionNeighbor
                if not self.isDot(row, col) and (not self.directionNeighbors(row, col, self.getDirection(row, col)).__contains__([possibleNeighbor[0], possibleNeighbor[1]])):
                    continue
               
                # make sure neighbor that isnt given point is not a dot
                directionNeighbors.remove([row, col])
                # print('row, col ', [row, col])
                # print('direction ', direction)
                # print('directionNeighbors ', directionNeighbors[0])
                # directionNeighbors is now a 2d array of possible point's direction neighbor that isnt [row, col]

                # print('directionNeighbors:', directionNeighbors)
                # print('row, col:', [row, col])
                if self.isDot(directionNeighbors[0][0], directionNeighbors[0][1]):
                    # unless its the same color then you should just play that
                    # TODO this may mess things up, if it does, replace with:
                    # make sure that it doesnt create a cycle and is actually the other dot
                    # possibleBoard = self.doMove([possibleNeighbor[0], possibleNeighbor[1], color, direction])
                    
                    if self.getColor(directionNeighbors[0][0], directionNeighbors[0][1]) != color:
                        continue
                    else:
                        # make sure its not two dots diagonal from eachother
                        if direction not in range(0, 2):
                            # print('here appending: ', [possibleNeighbor[0], possibleNeighbor[1], color, direction]) 
                            if diagonal == False:
                                allPossibleNeighbors.clear()
                            
                            diagonal = True

                            allPossibleNeighbors.append([possibleNeighbor[0], possibleNeighbor[1], color, direction])
                            

                            # continue
                        else:
                        # print([[possibleNeighbor[0], possibleNeighbor[1], color, direction]])
                            # print('returing', [[possibleNeighbor[0], possibleNeighbor[1], color, direction]])
                            return [[possibleNeighbor[0], possibleNeighbor[1], color, direction]]
                        # allPossibleNeighbors.append([possibleNeighbor[0], possibleNeighbor[1], color, direction])                        


                    continue

                # print('appending: ', [possibleNeighbor[0], possibleNeighbor[1], color, direction])
                if not diagonal:
                    allPossibleNeighbors.append([possibleNeighbor[0], possibleNeighbor[1], color, direction])

        # print(allPossibleNeighbors)
        return allPossibleNeighbors
    


    '''
        perfroms move on board:
        move: from allPossibleNeighbors()
            [row, col, color, direction]
        returns a new Board()
    '''
    @classmethod
    def doMove(cls, board, move):
        row, col, color, direction = move

        newBoard = copy.deepcopy(board.board)
        newBoard[row][col] = [color, direction]
        return cls(newBoard)

    '''
        given dot point, traverses to longest point on path
    '''
    def traverseDot(self, row, col, checked=[]):
        # print('traversing: ', row, col)
        neighbors = self.flowingNeighbors(row, col)
        # print('traverseDot ', row, col)
        # print('flowingNieghbors ', neighbors)
        # print(neighbors)
        # print(checked)

        # remove any already checked points from neighbors
        # and make sure flowNeighbors are same color:
        for neighbor in neighbors:
            if neighbor in checked:
                neighbors.remove(neighbor)

        if len(neighbors) > 1:
            # print('ERROR: traverseDot got a flowingNeighbors of > 1, some error in path')
            # print('ERROR: traverseDot got a flowingNeighbors of > 1, some error in path')
            # print('ERROR: traverseDot got a flowingNeighbors of > 1, some error in path')
            return None

        if len(neighbors) == 0:
            # print('len == 0')
            return [row, col]
        else:
            # print('appending')
            checked.append([row, col])
            return self.traverseDot(neighbors[0][0], neighbors[0][1], checked=checked)
        
                
    '''
        returns all points that that connect to just an empty cell, besides its parents
            - this is the classificaiton for a possible move
    '''
    def allPossibleMoves(self):
        # print('allPossibleMoves:')
        # print(self)

        allPossibleMoves = []
        # for dot in [i for _ in self.dots.values() for i in _]:
        for dotPair in self.dots.values():
            # print(dotPair)
            dot = dotPair[0]

            # print('traversing: ', dot)
            traversal = self.traverseDot(dot[0], dot[1], checked=[])
            # print('result, ', traversal)
            if traversal != None and traversal != dotPair[1]:
                allPossibleMoves.append(traversal)

        # print('allPossibleMoves: ', str(allPossibleMoves))
        return allPossibleMoves
    


    def __eq__(self, other):
        if not isinstance(other, Board):
            return False
        return self.board == other.board

    def __hash__(self):
        return hash(str(self.board))
    
    
    def __lt__(self, x):
        # return random.randint(0, 1)
        return True
