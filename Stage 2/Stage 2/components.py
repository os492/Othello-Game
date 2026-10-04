def initialise_board(size=8):
    row = ["None "]*size #creates a row with 8 elements titled none
    board = []
    for x in range(size):
        board.append(row.copy()) #row.copy() means that we can modify 1 row without changing all of them in the board which will be important when we start adding the black and white counters 
    board[3][3] = "Light" 
    board[4][4] = "Light"
    board[3][4] = "Dark " 
    board[4][3] = "Dark "
    return board #board is returned to be taken as an argument for print_board
    
def print_board(board): 
    print("  0        1        2        3        4        5        6        7")
    for row in board: #each row in board is printed, giving the effect of an 8x8 board
        print(row)
    
def legal_move(colour, coordinate, board):
    if colour == "Dark ":
        opponent = "Light"
    else:
        opponent = "Dark "
    moves = [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7), #all legal coordinates in othello
             (1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7),
             (2,0), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7),
             (3,0), (3,1), (3,2), (3,3), (3,4), (3,5), (3,6), (3,7),
             (4,0), (4,1), (4,2), (4,3), (4,4), (4,5), (4,6), (4,7),    
             (5,0), (5,1), (5,2), (5,3), (5,4), (5,5), (5,6), (5,7),
             (6,0), (6,1), (6,2), (6,3), (6,4), (6,5), (6,6), (6,7),
             (7,0), (7,1), (7,2), (7,3), (7,4), (7,5), (7,6), (7,7)
             ]
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),         (0, 1),
                  (1, -1),  (1, 0),  (1, 1)]
    if coordinate not in moves: #if the coordinate is not part of the moves list then it must be outside the grid
        return False
    row, col = coordinate
    if board[row][col] != "None ":  #if the square has already been taken then it is an invalid move
        return False
    for dx, dy in directions: #will loop for all directions
        tempcol =  col + dy
        temprow = row + dx # dx and dy serve as the changes in direction
        found_opponent = False

        # Loops until opponent piece is found
        while 0 <= temprow < 8 and 0 <= tempcol < 8:
            current = board[temprow][tempcol] #will check the disk at this specific board position

            if current == "None ":
                break  # stop if we hit empty before our colour and we change the direction
            if current == opponent: #this means we have found the opponents disk in this direction
                found_opponent = True
            elif current == colour: # now we have found our own colour disk after the opponents disks meaning that it is a valid move
                if found_opponent == True:
                    return True  # so we return true if this is the case, meaning that the move is legal
                break # if we didn't find see a different coloured disk in one direction, then the move is not legal and therefore we break to repeat the loop in a different direction
            else:
                break #if we hit anything else, then we stop

            temprow += dx #this moves one more step in the same direction
            tempcol += dy

    return False # if none of the 8 directions produced a valid move, then the disk captures nothing, so it is an illegal placement of a disk according to the rules 
    
board = initialise_board()
print_board(board)
