from Board import Board
from ColorCell import ColorCell
from DirectionCell import DirectionCell

class BoardToCNF(Board):

    def __init__(self, board: list[list[int]]):
        super().__init__(board)
        self.cnf = []
        # map of ColorCell to its index in the CNF
        self.colorCells = {}
        # map of DirectionCell to its index in the CNF
        self.directionCells = {}

        i = 1
        for row in range(self.rows):
            for col in range(self.cols):
                for color in range(self.numColors):
                    colorCell = ColorCell(row, col, color)
                    self.colorCells[colorCell] = i
                    i += 1

                for direction in range(6):
                    directionCell = DirectionCell(row, col, direction)
                    self.directionCells[directionCell] = i
                    i += 1

    def ColorCellToIndex(self, colorCell: ColorCell) -> int:
        return self.colorCells[colorCell]

    def IndexToColorCell(self, index: int) -> ColorCell:
        invertedColorCells = {v: k for k, v in self.colorCells.items()}
        return invertedColorCells[index]

    def DirectionCellToIndex(self, directionCell: DirectionCell) -> int:
        return self.directionCells[directionCell]

    def IndexToDirectionCell(self, index: int) -> DirectionCell:
        invertedDirectionCells = {v: k for k, v in self.directionCells.items()}
        return invertedDirectionCells[index]
    
    def addColorClauses(self):
        for row in range(self.rows):
            for col in range(self.cols):
                # SOME color
                self.cnf.append([self.ColorCellToIndex(ColorCell(row, col, color)) for color in range(self.numColors)])

                # AT MOST ONE color
                for color1 in range(self.numColors):
                    for color2 in range(color1 + 1, self.numColors):
                        self.cnf.append([-self.ColorCellToIndex(ColorCell(row, col, color1)), -self.ColorCellToIndex(ColorCell(row, col, color2))])

                if type(self.board[row][col]) == int:
                    # is dot
                    dotColor = self.board[row][col]
    
                    # every dot is assigned its color
                    self.cnf.append([self.ColorCellToIndex(ColorCell(row, col, dotColor))])

                    # every other color is false        
                    for color in range(self.numColors):
                        if color != dotColor: 
                            self.cnf.append([-self.ColorCellToIndex(ColorCell(row, col, color))])

                    neighborList = self.getNeighbors(row, col)
                    # SOME of dots neighbors have same color as dot
                    self.cnf.append([self.ColorCellToIndex(ColorCell(neighbor[0], neighbor[1], dotColor)) for neighbor in neighborList])

                    # AT MOST ONE of dots neighbors have same color as dot
                    for neighbor1 in range(len(neighborList)):
                        for neighbor2 in range(neighbor1+1, len(neighborList)):
                            neighbor1Cell = ColorCell(neighborList[neighbor1][0], neighborList[neighbor1][1], dotColor)
                            neighbor2Cell = ColorCell(neighborList[neighbor2][0], neighborList[neighbor2][1], dotColor)

                            self.cnf.append([-self.ColorCellToIndex(neighbor1Cell), -self.ColorCellToIndex(neighbor2Cell)])

        # print('Color clauses added:')
        # print(self.cnf)

    def addDirectionClauses(self):

        for row in range(self.rows):
            for col in range(self.cols):
                # print(self.board[row][col])
                # print(type(self.board[row][col]))
                # print(type(None))
                if self.board[row][col] == None:
                    # SOME direction
                    self.cnf.append([self.DirectionCellToIndex(DirectionCell(row, col, direction)) for direction in range(6)])

                    # # AT MOST ONE color
                    for direction1 in range(6):
                        for direction2 in range(direction1+1, 6):
                            self.cnf.append([-self.DirectionCellToIndex(DirectionCell(row, col, direction1)), -self.DirectionCellToIndex(DirectionCell(row, col, direction2))])
        
                    # direction has the same color on its corresponding neighbors
                    #   ex: direction ─ takes left and right neighbor
                    #       left and right neighbor color must be the same
                    DIRECTIONS = [
                    '\u2500',  # Horizontal line (─)
                    '\u2502',  # Vertical line (│)
                    '\u2514',  # Bottom-left corner (└)
                    '\u2518',  # Bottom-right corner (┘)
                    '\u250C',  # Top-left corner (┌)
                    '\u2510',  # Top-right corner (┐)
                    ]
                    left = [row, col-1]
                    right = [row, col+1]
                    up = [row-1, col]
                    down = [row+1, col]
                    for direction in range(6):
                        pos1 = None
                        pos2 = None
                        
                        match direction:
                            case 0: # ─
                                if self.isValidPoint(*left) and self.isValidPoint(*right):
                                    pos1 = left
                                    pos2 = right

                            case 1: # │
                                if self.isValidPoint(*up) and self.isValidPoint(*down):
                                    pos1 = up
                                    pos2 = down
                            
                            case 2: # └
                                if self.isValidPoint(*up) and self.isValidPoint(*right):
                                    pos1 = up
                                    pos2 = right
                            
                            case 3: # ┘
                                if self.isValidPoint(*up) and self.isValidPoint(*left):
                                    pos1 = up
                                    pos2 = left
                            
                            case 4: # ┌
                                if self.isValidPoint(*down) and self.isValidPoint(*right):
                                    pos1 = down
                                    pos2 = right
                            
                            case 5: # ┐
                                if self.isValidPoint(*down) and self.isValidPoint(*left):
                                    pos1 = down
                                    pos2 = left
                            
                        if pos1 == None and pos2 == None:
                            # not possible direction
                            self.cnf.append([-self.DirectionCellToIndex(DirectionCell(row, col, direction))])

                        else:
                            for color in range(self.numColors):

                                self.cnf.append([-self.DirectionCellToIndex(DirectionCell(row, col, direction)), -self.ColorCellToIndex(ColorCell(row, col, color)), self.ColorCellToIndex(ColorCell(*pos1, color))])
                                self.cnf.append([-self.DirectionCellToIndex(DirectionCell(row, col, direction)), self.ColorCellToIndex(ColorCell(row, col, color)), -self.ColorCellToIndex(ColorCell(*pos1, color))])
                                self.cnf.append([-self.DirectionCellToIndex(DirectionCell(row, col, direction)), -self.ColorCellToIndex(ColorCell(row, col, color)), self.ColorCellToIndex(ColorCell(*pos2, color))])
                                self.cnf.append([-self.DirectionCellToIndex(DirectionCell(row, col, direction)), self.ColorCellToIndex(ColorCell(row, col, color)), -self.ColorCellToIndex(ColorCell(*pos2, color))])

                                for neighbor in self.getNeighbors(row, col):
                                    if neighbor != pos1 and neighbor != pos2:
                                        self.cnf.append([-self.DirectionCellToIndex(DirectionCell(row, col, direction)), -self.ColorCellToIndex(ColorCell(row, col, color)), -self.ColorCellToIndex(ColorCell(*neighbor, color))])

        # print('Direction clauses added:')
        # print(self.cnf)


