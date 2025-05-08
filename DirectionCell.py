class DirectionCell():
    def __init__(self, row, col, direction):
        self.row = row
        self.col = col
        self.direction = direction

    def __hash__(self):
        return hash((self.row, self.col, self.direction))
    
    def __eq__(self, value):
        return self.row == value.row and self.col == value.col and self.direction == value.direction