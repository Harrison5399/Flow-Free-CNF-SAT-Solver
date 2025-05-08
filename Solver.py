from BoardToCNF import BoardToCNF
from Board import Board
from datetime import datetime

from pysat.solvers import Glucose3, Minisat22
import pycosat
from flowcoSAT import solve

class Solver(BoardToCNF):

    def __init__(self, board: list[list[int]], model='pysat'):
        super().__init__(board)
        self.model = model

        start = datetime.now()

        self.addColorClauses()
        self.addDirectionClauses()

        end = datetime.now()
        # print('Time taken to add clauses:', end - start)
        self.clauseTime = end - start

        self.solution = []
        self.solutionTime = None

        self.solve()

        if self.solution == []: 
            self.solvedBoard = None
        else:
            self.solvedBoard = Board.fromSolver(self)

    
    def solve(self):
        if self.model == 'pysat':

            start = datetime.now()
            with Minisat22(bootstrap_with=self.cnf) as solver:
                if solver.solve():
                    model = solver.get_model()
                    # print("SATISFIABLE:", model)
                    self.solution = model
                    end = datetime.now()
                    # print('Time taken to solve:', end - start)
                    self.solutionTime = end - start
                else:
                    print("UNSATISFIABLE")

        elif self.model == 'pycosat':

            start = datetime.now()
            result = pycosat.solve(self.cnf)

            if result == "UNSAT":
                print("UNSATISFIABLE")
            else:
                # pycosat returns the solution directly as a list of integers
                # print("SATISFIABLE:", result)
                self.solution = result
                end = datetime.now()
                # print('Time taken to solve:', end - start)
                self.solutionTime = end - start

        elif self.model == 'andrew':
            
            start = datetime.now()
            solution = solve(self.cnf)
            # print('solver solution: ' + str(solution))
            end = datetime.now()
            
            self.solution = solution
            self.solutionTime = end - start

        else:
            pass