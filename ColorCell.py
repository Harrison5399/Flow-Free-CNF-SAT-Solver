class ColorCell():

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color 

    def __hash__(self):
        return hash((self.row, self.col, self.color))
    
    def __eq__(self, value):
        return self.row == value.row and self.col == value.col and self.color == value.color