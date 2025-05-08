from Board import Board
from BoardToCNF import BoardToCNF
from Solver import Solver
from PyGameBoard import PyGameBoard

import heapq
import math

class AStar():
    def __init__ (self, board: Board):
        self.board = board
        
        self.fringe = []
        # {Board: [row, col, color, direction]}
        #   such that you can reccursively undo the moves and get to original board
        self.lastMoveMap = {}
        self.visted = []


    def heuristic(self, board : Board):
        def manhattanDistance(x1, y1, x2, y2):
            return abs(x1 - x2) + abs(y1 - y2)
        
        # return 0
        # print('heuristic on board:')
        # print(board)

        dots = [i for _ in board.dots.values() for i in _]
        dotsToTravesedPath = {tuple(dot) : board.traverseDot(dot[0], dot[1], checked=[]) for dot in dots}

        for k, v in dotsToTravesedPath.items():
            if v == None:
                dotsToTravesedPath[k] = list(k)

        # print('dotsToTravesedPath', dotsToTravesedPath)

        emptySpaces = 1
        for row in range(board.rows):
            for col in range(board.cols):
                if board.board[row][col] == None:
                    emptySpaces += 1

        completePaths = 0
        sumDistanceFlowToOtherDot = 1
        sumDistanceFlowToOtherFlow = 1
        dotToDotDistances = []
        flowToDotDistances = []
        rawTotal = 1
        for dotPair in board.dots.values():
            # print('dotPair', dotPair)

            mainDot = dotPair[0]
            otherDot = dotPair[1]
            # completed path
            if dotsToTravesedPath[tuple(mainDot)] == otherDot or dotsToTravesedPath[tuple(otherDot)] == mainDot:
                completePaths += 1
                continue

            # for v, dot in enumerate(dotPair):
                # print('v, dot', v, dot)
            traversedPath = dotsToTravesedPath[tuple(mainDot)]
            otherDotTraveredPath = dotsToTravesedPath[tuple(otherDot)]

            # distance from end of flow of mainDot to otherDot
            flowToDotDistance = manhattanDistance(traversedPath[0], traversedPath[1], otherDot[0], otherDot[1])
            # print('distance flow to other dot', sumDistanceFlowToOtherDot)

            # distance from dot to other dot
            dotToDotDistance = manhattanDistance(mainDot[0], mainDot[1], otherDot[0], otherDot[1])
            # print('distance flow to other flow', sumDistanceFlowToOtherFlow)

            weight = 0.5
            rawTotal += (dotToDotDistance/flowToDotDistance) * dotToDotDistance
            # rawTotal += ((dotToDotDistance/flowToDotDistance)*weight) + ((1/(dotToDotDistance + flowToDotDistance))*(1-weight))




        # return 1 / ((board.rows * board.cols) - emptySpaces)

        # return emptySpaces + 1
        val = (math.log(rawTotal, (completePaths)+2)*25)# + (emptySpaces*5)
        print(val)
        return val


        # print('heurstic val', (completePaths + 1) / (sumDistanceFlowToOtherDot + sumDistanceFlowToOtherFlow + 1))
        # return (((completePaths*100) + 1) / ((((sumDistanceFlowToOtherFlow / sumDistanceFlowToOtherDot)) + 1) / emptySpaces)) + ((board.rows * board.cols) - emptySpaces)
        return ((completePaths*100) + 1) / (sumDistanceFlowToOtherDot + sumDistanceFlowToOtherFlow + 1)
    
    def doForcedMoves(self, board: Board):
        newBoard = Board(board.board.copy())
        for dotPair in board.dots.values():
            dot = dotPair[0]

            possibleNeighbors = board.allPossibleNeighbors(dot[0], dot[1])
            if len(possibleNeighbors) == 1:
                newBoard = newBoard.doMove(newBoard, possibleNeighbors[0])

        return newBoard


    '''
        given dot pair, checks if there is a path of empty spaces that will get you to the the opposite dot
    '''
    def dotHasFlowToOther(self, board:Board, dotPair):
        # print('\n')
        mainDot = dotPair[0]
        otherDot = dotPair[1]
        color = board.getColor(mainDot[0], mainDot[1])

        traversal = board.traverseDot(mainDot[0], mainDot[1], checked=[])
        
        otherTraversal = None
        try:
            otherTraversal = board.traverseDot(otherDot[0], otherDot[1], checked=[])
        except:
            pass

        # print('traversal', traversal)
        # print('otherTraversal', otherTraversal)
        if traversal == dotPair[1]:
            # print('traversed to other dot')
            return True

        # print('dotHasFlowToOther: ', dotPair)

        i = 0

        if traversal == None:
            return False

        checkEmpty = board.getNeighbors(traversal[0], traversal[1])
        # print('checkEmpty', checkEmpty)
        emptySpaces = []
        while i < len(checkEmpty):
            # if i == 0 and len(checkEmpty) == 0:
            #     return False
            
            # print(checkEmpty)
            checking = checkEmpty[i]
            if board.getDirection(checking[0], checking[1]) == None:
                emptySpaces.append(checking)

                for neighbor in board.getNeighbors(checking[0], checking[1]):
                   if neighbor not in checkEmpty:
                       checkEmpty.append(neighbor)
            
            i += 1

        # print(emptySpaces)

        # print('emptySpaces: ', emptySpaces)

        emptySpacesNeighbors = []
        for space in emptySpaces:
            for neighbor in board.getNeighbors(space[0], space[1]):
                if neighbor == dotPair[1]:
                    # print('found neighbor')
                    return True
                
        # print('false')
        return False
    

    '''
        checks for an empty space without empty spaces around it
            - true -> there exists some alone empty space
    '''
    def aloneEmptySpace(self, board: Board):
        vistedEmptySpaces = []

        for row in range(board.rows):
            for col in range(board.cols):
                if [row, col] in vistedEmptySpaces:
                    continue

                if board.getDirection(row, col) != None:
                    continue

                
                emptyCellZone = []
                searchSpace = [[row, col]]
                while len(searchSpace) != 0:
                    curr = searchSpace.pop(0)

                    for neighbor in board.getNeighbors(curr[0], curr[1]):
                        if board.getDirection(neighbor[0], neighbor[1]) == None and neighbor not in vistedEmptySpaces:
                            searchSpace.append(neighbor)
                            vistedEmptySpaces.append(neighbor)
                            emptyCellZone.append(neighbor)

                # print(emptyCellZone)

                hitDot = False
                perimeterDotColors = set()
                perimeterDirectionColors = set()
                for cell in emptyCellZone:
                    for neighbor in board.getNeighbors(cell[0], cell[1]):
                        if neighbor in emptyCellZone:
                            continue

                        direction = board.getDirection(neighbor[0], neighbor[1])
                        
                        if direction == -2:
                            perimeterDotColors.add(board.getColor(neighbor[0], neighbor[1]))
                            continue

                        if direction >= 0:
                            perimeterDirectionColors.add(board.getColor(neighbor[0], neighbor[1]))

                # print('emptyCellZone: ', emptyCellZone)
                # print('perimeterDotColors: ', perimeterDotColors)
                # print('perimeterDirectionColors: ', perimeterDirectionColors)

                if len(perimeterDotColors) == 0:
                    return True

                for i in perimeterDirectionColors:
                    if i not in perimeterDotColors:
                        return True

        
        return False
    
    def noZigZag(self, board: Board):
        
        visted = []
        for row in range(board.rows):
            for col in range(board.cols):
                color = board.getColor(row, col)
                if color == None:
                    continue
                
                if [row, col] in visted:
                    continue
                
                similarColorCount = 0
                for neighbor in board.getNeighbors(row, col):
                    if color == board.getColor(neighbor[0], neighbor[1]):
                        similarColorCount += 1
                
                if similarColorCount >= 3:
                    return False
                
        return True

                


    '''
        makes sure board being added to fringe doesn't do a move that cuts off another flow
    '''
    def okayBoard(self, board: Board):
        for dotPair in board.dots.values():
            if not self.dotHasFlowToOther(board, dotPair):
                # print('DOES NOT HAVE DOT FLOW', dotPair)
                return False
            
        if self.aloneEmptySpace(board):
            # print('HAS ALONE EMPTY SPACE')
            return False
        
        if not self.noZigZag(board):
            # print('HAS ZIG ZAG')
            return False

        return True

    def traverse(self):
        startBoard = self.doForcedMoves(self.board)
        startBoard = self.board
        if startBoard.isSolved():
            return current
        
        self.fringe = []
        self.lastMoveMap = {}
        self.doneMoves = []

        heapq.heappush(self.fringe, (self.heuristic(startBoard), startBoard))
        # self.fringe.append(startBoard)

        i = 0
        while self.fringe != []:
            _, current = heapq.heappop(self.fringe)
            # current = self.fringe.pop(0)
            if current.isSolved():
                return current
            
            # print(current)
            
            # for all points that should move
            # print('current board')
            # if i > 50:
            #     break
            # i+=1
            # print('current')
            print(current)

            # current = self.doForcedMoves(current)

            # print('all possible moves:')
            # print(current.allPossibleMoves())
            for cellMoving in current.allPossibleMoves():
                # for all moves that that cell can do
                for move in current.allPossibleNeighbors(cellMoving[0], cellMoving[1]):
                    newBoard = Board.doMove(current, move)
                    
                    # print('newBoard:')
                    # print(newBoard)
                    isOkay = self.okayBoard(newBoard)
                    notVisted = newBoard not in self.visted

                    if notVisted and isOkay:
                        # print('pushed!')
                        heapq.heappush(self.fringe, (self.heuristic(newBoard), newBoard))
                        self.visted.append(newBoard)
                    # self.fringe.append(newBoard)
                    else:
                        # print('not pushed', newBoard not in self.visted, isOkay)
                        pass

