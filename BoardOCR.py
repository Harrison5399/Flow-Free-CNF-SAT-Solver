import cv2
import numpy as np
import csv
import os

from Board import Board
from Solver import Solver

def imageToBoardArr(imagePath, rows, cols):

    # Load the image
    image = cv2.imread(imagePath)

    # crop out ad, top buttons, and 1px side margin
    image = image[600:2000, 1:-1, :]

    # do contrast 
    alpha = 0.05 # Simple contrast control
    beta = 50    # Simple brightness control 
    contrasted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

    shape = contrasted.shape

    def findHorziontal(image, searchTop=True):
        lookingFor = np.array([beta, beta, beta], dtype=np.uint8)
        shape = image.shape
        foundHeight = None
        searchRange = None

        if searchTop:
            searchRange = range(shape[0])
        else:
            searchRange = range(shape[0]-1, -1, -1)

        for height in searchRange:
            strip = contrasted[height, 10:shape[1]-10, :]
            avg = np.mean(strip, axis=0).astype(np.uint8)

            # print('avg: ' + str(avg))
            if not np.allclose(avg, lookingFor, atol=3) and np.ptp(avg) > 1:
                # print('found line at: ' + str(height) + '\tavg: ' + str(avg))
                foundHeight = height
                break

        return foundHeight

    topLine = findHorziontal(contrasted)
    contrasted = contrasted[topLine:shape[0], :, :]
    image = image[topLine:shape[0], :, :]
    # print('topLine: ' + str(topLine))

    bottomLine = findHorziontal(contrasted, searchTop=False)
    contrasted = contrasted[0:bottomLine, :, :]
    image = image[0:bottomLine, :, :]
    # print('bottomLine: ' + str(bottomLine))

    rowCellSize = contrasted.shape[0] // rows
    colCellSize = contrasted.shape[1] // cols
    rowLocations = []
    colLocations = []

    i = rowCellSize // 2
    for row in range(rows):
        cv2.line(contrasted, (0, i), (contrasted.shape[1], i), (0, 0, 255), 1)
        rowLocations.append(i)
        # print('row: ' + str(row) + '\t' + str(i))
        i += rowCellSize



    i = colCellSize // 2
    for col in range(cols):
        cv2.line(contrasted, (i, 0), (i, contrasted.shape[0]), (0, 0, 255), 1)
        colLocations.append(i)
        i += colCellSize

    cellLocations = []

    for rowLoc in rowLocations:
        for colLoc in colLocations:
            cellLocations.append((rowLoc, colLoc))

    board = [[None for _ in range(cols)] for _ in range(rows)]


    i = 0
    duplicateColors = 0
    colorSet = []
    for row in range(rows):
        for col in range(cols):
            cellVal = image[cellLocations[i][0], cellLocations[i][1], :]

            # check if the cell is empty
            if np.allclose(cellVal, [0, 0, 0], atol=50):
                board[row][col] = None
            else:
                # allow for some tolerance in the color for some reason some colors not consistent in the same image?
                found = False
                for color in colorSet:
                    if np.allclose(color, tuple(cellVal), atol=10):
                        found = True
                        cellVal = color
                        break
                
                if not found:
                    colorSet.append(tuple(cellVal))
                    print('row: ' + str(row) + '\tcol: ' + str(col) + '\tcellVal: ' + str(cellVal))
                else:
                    print('row: ' + str(row) + '\tcol: ' + str(col) + '\tduplicate color: ' + str(cellVal))
                    duplicateColors += 1

                board[row][col] = colorSet.index(tuple(cellVal))
                # print('row: ' + str(row) + '\tcol: ' + str(col) + '\tcellVal: ' + str(cellVal))
                

            i += 1
    if duplicateColors != len(colorSet):
        print('ERROR, MISSING SOME COLORS')
        print('duplicateColors: ' + str(duplicateColors) + '\tcolorSet: ' + str(len(colorSet)))
    
    print(list(map(lambda x: list(map(lambda y: int(y), x)), colorSet)))
    # print('colorSet: ' + str(colorSet))
    print('saving')
    cv2.imwrite('Boards/contrasted.png', contrasted)
    cv2.imwrite('Boards/image.png', image)
    return board



def saveBoardToCSV(board, filename, rows, cols):
    with open('Boards/' + str(rows) + 'x' + str(cols) + '/' + filename + '.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for row in board:
            writer.writerow(row)



def bulkImages():
    fileNames = os.listdir('Boards/Images/')
    print(fileNames)
    rows = 12
    cols = 12

    i = 10
    for fileName in fileNames:
        boardArr = imageToBoardArr('Boards/Images/' + fileName, rows, cols)
        saveBoardToCSV(boardArr, 'board' + str(i), rows , cols)

        b = Board(boardArr)

        print('saving board, ' + str(i) + ' : ' + fileName)
        print(b)
        print('\n\nwaiting...')
        input()

        i += 1




bulkImages()

# boardArr = imageToBoardArr('Boards/12x12/IMG_9083.png', 12, 12)
# saveBoardToCSV(boardArr, 'board1', 12, 12)
# b = Board(boardArr)
# print(b)
# s = Solver(b.board)
# s.solve()
# solvedBoard = Board.fromSolver(s)
# print(solvedBoard)

