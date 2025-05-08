from Board import Board
from BoardToCNF import BoardToCNF
from Solver import Solver
from PyGameBoard import PyGameBoard
from AStar import AStar

# b = Board.fromCSV('Boards/Bridges/6x6/board1.csv')
# print(str(b))


# b = [
#         [None, [0, 1], [0, 1]],
#         [[0, 1], 0, [0, 3]],
#         [None, [0, 1], None]
#     ]

# board = Board(b)
# print(str(board))
# print(board.flowingNeighbors(1,1))

# print(board.flowingNeighbors(1, 1))

# b = [
#         [0, 1, [1,0], [1,5]],
#         [None, None, 0, [1,1]],
#         [1, [1,0], [1,0], [1,3]],
#         [2, None, None, 2]
#     ]
# b = [
#         [0, 1, None, None],
#         [[0,2], [1,1], 0, None],
#         [1, [1,3], None, None],
#         [2, None, None, 2]
#     ]
# b = [
#         [0, 1, None, None],
#         [[0,2], [0,0], None, None],
#         [1, None, None, [2,5]],
#         [2, None, 0, 2]
#     ]


# board = Board(b)
# print(board)
# astar = AStar(board)
# print(astar.aloneEmptySpace(board))


board = Board.fromCSV('Boards/6x6/board1.csv')
print(board)
astar = AStar(board)
solvedBoard = astar.traverse()
pg = PyGameBoard(solvedBoard) 
pg.display()



# board = board.doMove([1,2,1,0])
# board = board.doMove([1,4,2,4])
# board = board.doMove([3,5,4,1])
# # board = board.doMove([3,3,4,5])
# board = board.doMove([3,3,3,1])
# board = board.doMove([4,3,3,2])
# board = board.doMove([4,4,3,0])
# board = board.doMove([4,5,3,3])




# board = Board.fromCSV('Boards/6x6/board1.csv')
# board = board.doMove([4,5,4,3])
# board = board.doMove([4,4,4,0])
# board = board.doMove([4,3,4,2])
# board = board.doMove([3,3,4,5])
# board = board.doMove([3,5,4,1])
# board = board.doMove([0,4,0,0])
# board = board.doMove([1,2,1,0])
# print(board)

# astar = AStar(board)
# print(astar.okayBoard(board))





# # # # print(board.flowingNeighbors(3,4))
# # # # print(board.traverseDot(3,4))

# # print(astar.heuristic(board))


# print(board.allPossibleMoves())

# print(board)
# print(board.allPossibleNeighbors(0, 5))
# board = board.doMove(board.allPossibleNeighbors(0, 5)[1])
# board = board.doMove([1,4,2,2])
# board = board.doMove([5,0,0,2])
# print(board)
# print(board.allPossibleMoves())

# board = board.doMove([4,1,0,1])
# board = board.doMove([3,1,4,4])
# print(board)
# print(board.allPossibleMoves())

# asolver = AStar(board)
# print(asolver.traverse())



# print(board.dots)
# print(board.allPossibleNeighbors(3, 2))
# print('\n\n')
