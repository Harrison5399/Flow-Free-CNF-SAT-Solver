from Board import Board
from BoardToCNF import BoardToCNF
from Solver import Solver
from PyGameBoard import PyGameBoard
import threading


def solveBoard(pathToBoard, doDisplay=True, model='pysat', imageFileName=None):
    print('Solving board:', pathToBoard)
    # select unsolved board from Boards/
    b = Board.fromCSV(pathToBoard)
    # print(b) # __str__ representation of board

    if doDisplay:
        display = PyGameBoard(b)
        display.display(imageFileName=imageFileName, title=f'{pathToBoard} - Unsolved')


    # make solver and solve the board
    s = Solver(b.board, model=model)
    
    # print(s.solvedBoard) # s.solvedBoard is Board() object with directions

    # pygame represenation of board

    print('Time taken to generate clauses:', s.clauseTime)
    print('Time taken to solve:', s.solutionTime)

    if doDisplay:
        display = PyGameBoard(s.solvedBoard)
        display.display(imageFileName=imageFileName, title=f'{pathToBoard} - Solved')

    return s.clauseTime, s.solutionTime

def bulkSolveBoards(paths, doDisplay=True, model='pysat'):
    averageClauseTime = 0
    averageSolveTime = 0

    for path in paths:
        # if int(path.split('/')[-1].strip('board').strip('.csv')) <= 9:
        #     continue

        clauseTime, solutionTime = solveBoard(path, doDisplay, model)
        if clauseTime is None or solutionTime is None:
            print('Board could not be solved.')
            continue

        averageClauseTime += clauseTime.total_seconds()
        averageSolveTime += solutionTime.total_seconds()
    
    averageClauseTime /= len(paths)
    averageSolveTime /= len(paths)

    print('\n\n')
    print('Average time to generate clauses:', averageClauseTime, 'seconds')
    print('Average time to solve:', averageSolveTime, 'seconds')

    return averageClauseTime, averageSolveTime

def getBoardsInDirectory(directory):
    import os
    fileNames = os.listdir(directory)
    paths = []
    for fileName in fileNames:
        if fileName.endswith('.csv'):
            paths.append(os.path.join(directory, fileName))
    return paths

# bulkSolveBoards(getBoardsInDirectory('Boards/14x14/'))
# solveBoard('Boards/6x6/board1.csv', True, 'andrew')


# for poster images
def allPossibleDirectionsBoard():
    for direction in range(6):

        b = Board.fromCSV('Boards/6x6/board2.csv')
        for row in range(b.rows):
            for col in range(b.cols):
                if b.board[row][col] == None:
                    b.board[row][col] = [22, direction]

        display = PyGameBoard(b)
        display.display(imageFileName='poster_images/allDirections_' + str(direction))

# for poster images
def allPossibleColorsBoard():
    for color in range(4):

        b = Board.fromCSV('Boards/6x6/board2.csv')
        for row in range(b.rows):
            for col in range(b.cols):
                if b.board[row][col] == None:
                    b.board[row][col] = [color, None]

        display = PyGameBoard(b)
        display.display(imageFileName='poster_images/allColors_' + str(color))


# solveBoard('Boards/10x10/board9.csv', True, 'andrew')

# allPossibleDirectionsBoard()
# allPossibleColorsBoard()

# boards that andrew's model can solve
solvable = {
    '6x6': [0,1,4,5,6,7,8,10,11,12,15,16,17,18],
    '7x7': [0,1,3,4,5,7,8,11,12,14,15,16,17,19],
    '8x8': [1,2,3,4,7,23,24,25,28,29],
    '9x9': [7,10,11,15,16,21,23,24,26,29],
    '10x10': [4,6,19,35,42],
    '12x12': [2,14]
}

def solvablePaths(solvable):
    solvablePaths = []
    for size in solvable:
        for boardNum in solvable[size]:
            solvablePaths.append('Boards/' + size + '/board' + str(boardNum) + '.csv')
    return solvablePaths


def getAllTimes():
    # models = ['pysat', 'pycosat', 'andrew']
    models = ['andrew']
    # boardSizes = ['6x6', '7x7', '8x8', '9x9', '10x10', '12x12']
    boardSizes = ['6x6', '7x7', '8x8', '9x9', '10x10']

    times = {k:[None, None] for k in boardSizes}
    times = {k:times.copy() for k in models}

    for model in models:
        for size in boardSizes:
            boardPaths = getBoardsInDirectory('Boards/' + size + '/')

            # filter boardPaths to only include solvable boards
            # boardPaths = [
            #     board for board in boardPaths
            #     if int(board.split('/')[-1].strip('board').strip('.csv')) in solvable[size]
            # ]

            print('Solving boards of size', size, 'with model', model)
            averageClauseTime, averageSolveTime = bulkSolveBoards(boardPaths, doDisplay=False, model=model)
            averageClauseTime *= 1000 # convert to milliseconds
            averageSolveTime *= 1000
            
            times[model][size] = [averageClauseTime, averageSolveTime]
        print('\n\n')
    
    for model in times:
        print('-'*20)
        print(f'Model: {model}')
        for size in times[model]:
            print(f'Size: {size} \t Average Clause Time: {times[model][size][0]:.6f} \t Average Solve Time: {times[model][size][1]:.6f}')


def demo():
    allBoards = (
        getBoardsInDirectory('Boards/6x6/') +
        getBoardsInDirectory('Boards/7x7/') +
        getBoardsInDirectory('Boards/8x8/') +
        getBoardsInDirectory('Boards/9x9/') +
        getBoardsInDirectory('Boards/10x10/') 
        # getBoardsInDirectory('Boards/12x12/') +
        # getBoardsInDirectory('Boards/14x14/')
    )

    bulkSolveBoards(allBoards, model='andrew')


# bulkSolveBoards(getBoardsInDirectory('Boards/14x14/'), doDisplay=True, model='andrew')
# while 1:        
    # bulkSolveBoards(solvablePaths(solvable), doDisplay=True, model='andrew')

demo()

# getAllTimes()


