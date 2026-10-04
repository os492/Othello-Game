from components import initialise_board, legal_move, print_board

def flip_disks(colour, coordinate, board):
    if legal_move(colour, coordinate, board) == False: #Will only flip disks if the move is legal
        return False 

    if colour == "Dark ": 
        opponent = "Light"
    else:
        opponent = "Dark "
    row, col = coordinate 
    board[row][col] = colour  # Disk is placed on the board

    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),         (0, 1),
                  (1, -1),  (1, 0),  (1, 1)]

    for dx, dy in directions: # Loops once in each direction again as a disk placed might flip disks of the opposite colour in multiple directions
        temprow = row + dx
        tempcol = col + dy
        disks_to_flip = [] # Disks to flip are stored in an array

        # Collect opponent disks in each direction
        while 0 <= temprow < 8 and 0 <= tempcol < 8:
            current = board[temprow][tempcol]

            if current == opponent:
                disks_to_flip.append((temprow, tempcol))
            elif current == colour: # Once the users colour has been reached, we stop looking for disks in that direction
                for r, c in disks_to_flip:
                    board[r][c] = colour # The loop iterates through each item in the list, changing each position to the users colour
                break
            else:
                break  # If we hit "None " before finding a disk of the users colour then then we stop searching in this direction

            temprow = temprow + dx # We advance to the next square in the same direction
            tempcol = tempcol + dy
    return True  #Disks flipped successfully

def cli_coords_input():
    valid = False # valid must be True for the while loop to stop iterating
    while valid == False:
        try:
            userrow = int(input("Enter the row you would like to place your disk (0-7): "))
            usercol = int(input("Enter the column you would like to place your disk (0-7): "))
        except ValueError:
            print("Error: Enter an integer between 0 and 7.")
            continue  # Allows the user to retry and input again 
        if userrow<0 or userrow>7: # Checks if the row is outside of the domain
            print("Row input outside of the board domain")
        if usercol<0 or usercol>7: # Checks if the column is outside of the domain
            print("Column input outside of the board domain")
        else: # If there are no problems then the coordinate is valid
            valid = True
    coordinate = (userrow, usercol) # The tuple coordinate stores the column and row
    print(coordinate)
    return coordinate # Coordinate is returned

def any_legal_moves(current_player, board): # This subroutine iterates through each square on the board checking if the current player has at least 1 valid move
    for r in range(8):
        for c in range(8):
            if legal_move(current_player, (r,c), board=board) == True: # The current square is sent to the subroutine legal_move to check if it is valid
                return True # If a legal move is found, the subroutine immediatly stops and returns true
    return False # If no legal move is found, then the  subroutine returns false

def simple_game_loop():
    print("Welcome to Othello")
    board = initialise_board()
    current_player = "Dark " # Sets the first player to Dark
    other_player = "Light" # And the second player to Light
    move_counter = 60 # Move counter is initialised to 60

    while move_counter > 0: # Checks if the move_counter is above 0
        print_board(board) 
        if any_legal_moves(current_player, board) == False: # Calls the subroutine above checking if the current player has any legal moves
            print(current_player, "has no legal moves. Switching player.") # If the player has no legal moves, a message is output to the user letting them know
            current_player, other_player = other_player, current_player # The two players are switched
        
            if any_legal_moves(current_player, board) == False: # The subroutine will now check if the other player (now the current player) has any legal moves
                print("No legal moves for either player. Game Over.") # If neither player has any legal moves, then the game is over
                break
            continue
        print(current_player, "turn") # If either player has a legal move, then it is their turn
        coordinate = cli_coords_input() # The cli_coords_input will run asking the user to input the coordinates where the would like to place their disk
        if flip_disks(current_player, coordinate, board) == False: # The subroutine flip_disks will now check if any disks are flipped from these coordinates. If no disk is flipped then it will output an error message asking the user to try again.
            print("Illegal Move. Try again.")
            continue
        
        move_counter = move_counter - 1 # If the move is valid, the move_counter is reduced by one
        print("Current Move Counter is:", move_counter) # Prints the new move counter
        current_player, other_player = other_player, current_player # The players are switched
    end_game(board)

def end_game(board): 
    print("Game Over") 
    numDark = 0
    numLight = 0
    for row in board: # Once the game is over, we will iterate though each cell in the board keeping count of how many Light and Dark disks there are to determine the winner 
        for cell in row:
            if cell == "Dark ":
                numDark = numDark + 1 # If the current cell is Dark then we add one to the counter
            elif cell == "Light":
                numLight = numLight + 1 # If the current cell is Light then we add one to the counter 
    if numLight> numDark: # If Light has more disks then they win
        print("Light wins with ", numLight, "disks vs Dark with ", numDark, "disks")
        result = f"Light Wins: Light has {numLight} tiles and Dark has {numDark} tiles"
    elif numLight<numDark: # If Dark has more disks then they win
        print("Dark wins with ", numDark, "disks vs Light with ", numLight, "disks")
        result = f"Dark Wins: Dark has {numDark} tiles and Light has {numLight} tiles"
    else: # If they have the same amount of disks then it is a draw
        print("Draw: Both Light and Dark got",numLight," tiles")
        result = f"Draw: Both Light and Dark got {numLight} tiles"
    return numDark, numLight, result

if __name__ == "__main__":
    simple_game_loop()