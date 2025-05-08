import pygame
from Board import Board
from Solver import Solver
from datetime import datetime


class PyGameBoard:
    def __init__(self, board: Board):
        self.b = board
        if board is None:
            print('BOARD IS UNSATISFIABLE, CANNOT DISPLAY')
            return 
        
        self.board = board.board
        self.rows = board.rows
        self.cols = board.cols
        self.numColors = board.numColors

        self.COLORS = [
            (255, 0, 0),      # Red
            (0, 255, 0),      # Green
            (255, 255, 0),    # Yellow
            (0, 0, 255),      # Blue
            (255, 0, 255),    # Magenta
            (0, 255, 255),    # Cyan
            (128, 0, 0),      # Dark Red
            (0, 128, 0),      # Dark Green
            (128, 128, 0),    # Olive
            (0, 0, 128),      # Dark Blue
            (128, 0, 128),    # Purple
            (0, 128, 128),    # Teal
            (192, 192, 192),  # Gray
            (255, 165, 0),    # Orange
            (255, 192, 203),  # Pink
            (75, 0, 130),     # Indigo
            (255, 215, 0),    # Gold
            (0, 255, 127),    # Spring Green
            (70, 130, 180),   # Steel Blue
            (139, 69, 19),    # Saddle Brown
            (47, 79, 79),     # Dark Slate Gray
            (240, 230, 140),  # Khaki
            (173, 216, 230),  # Light Blue
        ]

    def draw_direction(self, screen, x, y, cell_size, direction, color):
        line_width = cell_size//5  # Thickness of the lines

        if direction == 0:  # Horizontal (─)
            pygame.draw.line(screen, color, (x, y + cell_size // 2), (x + cell_size, y + cell_size // 2), line_width)
        elif direction == 1:  # Vertical (│)
            pygame.draw.line(screen, color, (x + cell_size // 2, y), (x + cell_size // 2, y + cell_size), line_width)
        elif direction == 2:  # Bottom-left corner (└)
            # Line to the top edge
            pygame.draw.line(screen, color, (x + cell_size // 2, y + cell_size // 2), (x + cell_size // 2, y), line_width)
            # Line to the right edge
            pygame.draw.line(screen, color, (x + cell_size // 2, y + cell_size // 2), (x + cell_size, y + cell_size // 2), line_width)
        elif direction == 3:  # Bottom-right corner (┘)
            # Line to the top edge
            pygame.draw.line(screen, color, (x + cell_size // 2, y + cell_size // 2), (x + cell_size // 2, y), line_width)
            # Line to the left edge
            pygame.draw.line(screen, color, (x + cell_size // 2, y + cell_size // 2), (x, y + cell_size // 2), line_width)
        elif direction == 4:  # Top-left corner (┌)
            # Line to the bottom edge
            pygame.draw.line(screen, color, (x + cell_size // 2, y + cell_size // 2), (x + cell_size // 2, y + cell_size), line_width)
            # Line to the right edge
            pygame.draw.line(screen, color, (x + cell_size // 2, y + cell_size // 2), (x + cell_size, y + cell_size // 2), line_width)
        elif direction == 5:  # Top-right corner (┐)
            # Line to the bottom edge
            pygame.draw.line(screen, color, (x + cell_size // 2, y + cell_size // 2), (x + cell_size // 2, y + cell_size), line_width)
            # Line to the left edge
            pygame.draw.line(screen, color, (x + cell_size // 2, y + cell_size // 2), (x, y + cell_size // 2), line_width)

        elif direction == None:
            pygame.draw.circle(screen, color, (x + cell_size // 2, y + cell_size // 2), cell_size // 8)

    def draw_board(self, screen, cell_size=50):
        screen.fill((0, 0, 0)) 

        font = pygame.font.SysFont(None, 40)  # Font for directions
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * cell_size
                y = row * cell_size

                # Draw cell border
                pygame.draw.rect(screen, (255, 255, 255), (x, y, cell_size, cell_size), 1)

                cell = self.board[row][col]

                if cell is None:
                    # Empty cell
                    continue
                elif isinstance(cell, int):
                    # Starting dot (no direction)
                    color = self.COLORS[cell]
                    pygame.draw.circle(screen, color, (x + cell_size // 2, y + cell_size // 2), cell_size // 4)

                    # Draw small line connecting the dot to path
                    line_width = cell_size//5  # Thickness of the lines
                    for neighbor in self.b.getNeighbors(row, col):
                        # if neighbor does not have directions yet, dont do
                        if type(self.board[neighbor[0]][neighbor[1]]) != list:
                            continue

                        # left neighbor
                        if neighbor[0] == row and neighbor[1] == col-1:
                            # check for direction: 0, 2, 4
                            if [0, 2, 4].__contains__(self.board[neighbor[0]][neighbor[1]][1]):
                                pygame.draw.line(screen, color, (x + cell_size//2, y + cell_size//2), (x, y+cell_size//2), line_width)

                        # right neighbor
                        if neighbor[0] == row and neighbor[1] == col+1:
                            if [0, 3, 5].__contains__(self.board[neighbor[0]][neighbor[1]][1]):
                                pygame.draw.line(screen, color, (x + cell_size//2, y + cell_size//2), (x + cell_size, y+cell_size//2), line_width)

                        # up neighbor
                        if neighbor[0] == row-1 and neighbor[1] == col:
                            if [1, 4, 5].__contains__(self.board[neighbor[0]][neighbor[1]][1]):
                                pygame.draw.line(screen, color, (x + cell_size // 2, y + cell_size // 2), (x + cell_size // 2, y), line_width)

                        # down neighbor
                        if neighbor[0] == row+1 and neighbor[1] == col:
                            if [1, 2, 3].__contains__(self.board[neighbor[0]][neighbor[1]][1]):
                                pygame.draw.line(screen, color, (x + cell_size // 2, y + cell_size // 2), (x + cell_size // 2, y + cell_size), line_width)

                elif isinstance(cell, list) and len(cell) == 2:
                    # Cell with [color, direction]
                    color, direction = cell
                    if color == None and direction == None:
                        continue

                    color = 22 if color == None else color
                    color = self.COLORS[color]

                    self.draw_direction(screen, x, y, cell_size, direction, color)
                    pygame.draw.circle(screen, color, (x + cell_size // 2, y + cell_size // 2), cell_size//11)
                else:
                    continue




    def saveAsImage(self, screen, filename='board.png'):
        pygame.image.save(screen, filename)

    def display(self, imageFileName=None, title=None):
        if self.b is None:
            print('BOARD IS UNSATISFIABLE, CANNOT DISPLAY')
            return

        doSelfClose = True
        startTime = pygame.time.get_ticks()

        pygame.init()
        cell_size = 75
        screen = pygame.display.set_mode((self.cols * cell_size, self.rows * cell_size))
        self.draw_board(screen, cell_size)

        pygame.display.set_caption("Board Visualization" if title is None else title)

        # Ensure the window is focused
        # pygame.event.post(pygame.event.Event(pygame.ACTIVEEVENT, gain=1, state=6))

        if imageFileName is not None:
            self.saveAsImage(screen, imageFileName + '.png')

        running = True
        while running:
            currentTime = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if doSelfClose and (currentTime - startTime) >= 2000:
                    running = False

            pygame.display.flip()

        pygame.quit()


# Example usage
if __name__ == "__main__":
    b = Board.fromCSV('Boards/board5.csv')
    s = Solver(b.board)
    pygame_board = PyGameBoard(s.solvedBoard)
    pygame_board.display()