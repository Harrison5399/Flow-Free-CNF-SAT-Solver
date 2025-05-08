### Flow Free SAT Solver

Run single board: main.solveBoard(pathToBoard, model='andrew / pysat / pycosat', display=True / False)

- pathToBoard: path to .csv of board
- model: which sat solver you'd like to use, 'andrew' is ours
- display: if you'd like to display the PYGame display of the board, True default
    
example, in main.py: solveBoard('Boards/6x6/board0.csv', model='andrew', display=True)



Bulk solve boards: main.bulkSolveBoards(paths, model, doDisplay = True / False)

  - used to bulk solve boards, like all 8x8 boards or something

example, in main.py: bulkSolveBoards(getBoardsInDirectory('Boards/8x8'), model='pysat', doDisplay=True)



Cycle solving a bunch of boards: main.demo()
  - will cycle solving all boards
