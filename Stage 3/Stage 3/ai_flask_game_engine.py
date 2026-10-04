from flask import Flask, render_template, request, jsonify
from components import initialise_board, legal_move, print_board
from game_engine import flip_disks, any_legal_moves, end_game
import random

app = Flask(__name__)

# The first player is set, the board is initialised and the move_counter is reset to zero
current_player = "Dark "
board = initialise_board()
move_counter = 60

# Subroutine which gets all possible legal moves and stores them in an array for the AI
def get_legal_moves(player, board):
    moves = []
    for y in range(8):
        for x in range(8):
            if board[y][x] == "None " and legal_move(player, (y, x), board):
                moves.append((y, x))
    return moves

# The html Othello template is rendered 
@app.route("/")
def index():
    return render_template("index.html", game_board=board, current_player=current_player, move_counter=move_counter)

@app.route("/load_board", methods=["POST"])
def load_board(): # Updates the backend to match the saved game sent from the browser, so moves can be played after loading
    global board, move_counter, current_player # Makes these variables global so that their values can be changed across subroutines 
    data = request.json

    if data is None:
        return jsonify(status="fail", message="No data received. No saved game found."), 400
    
    required_keys = ["board", "move_counter", "current_player"]
    for key in required_keys:
        if key not in data:
            return jsonify(status="fail",message=f"Missing key: {key}. Cannot load game."), 400

    board = data["board"] # The backend game state is overwritten and updated to the saved board the user has saved, allowing them to carry on playing where they left off
    move_counter = data["move_counter"]
    current_player = data["current_player"]

    return jsonify(status="loaded") # Tells the frontend that the loading of the saved board has succeeded 

# Subroutine to check if board is full
def board_full(board):
    for row in board:
        if "None " in row: # If "None " is found in any row, then board is not full, and we return False
            return False
    return True     # If we finish the loop without finding "None ", the board is full and we return True

@app.route("/move")
def move():
    global board, current_player, move_counter # Makes these variables global so that their values can be changed across subroutines

    # x and y are requested from the URL and converts them into integers so that they can match the form (0-7) by subtracting 1
    y = int(request.args.get("y")) - 1
    x = int(request.args.get("x")) - 1
    coordinate = (y, x) # The coordinate variable stores x and y in a tuple
    
    # The board at the start of the turn is printed
    print_board(board)

    # If the cell has already been taken, the move is invalid and json returns an error message to the game log
    if board[y][x] != "None ":
        return jsonify(status="fail", message="Cell is not empty", board=board)

    # If the move is illegal, then the move is failed and json returns an error message to the game log
    if not legal_move(current_player, coordinate, board):
        return jsonify(status="fail", message="Not a legal move")

    # Move is performed if it is valid
    flip_disks(current_player, coordinate, board)
    move_counter = move_counter - 1

    # Checks if the game is over after my move
    if board_full(board) or (any_legal_moves("Dark ", board) == False and any_legal_moves("Light", board) == False):
        numDark, numLight, result = end_game(board)
        return jsonify(finished=True, message=result, board=board, scoreDark=numDark, scoreLight=numLight)

    # Switches to Light (AI)
    current_player = "Light"

    # Checks if the AI has any legal moves
    moves_array = get_legal_moves("Light", board)

    # If the AI has at least 1 legal move, the AI will pick a move at random from the array legal_moves, which stores all the possible legal moves the AI has
    if moves_array:
        ai_move = random.choice(moves_array)
        flip_disks("Light", ai_move, board)
        move_counter = move_counter - 1

    # Checks if the game is over after the AI move
    if board_full(board) or (any_legal_moves("Dark ", board) == False and any_legal_moves("Light", board) == False):
        numDark, numLight, result = end_game(board)
        return jsonify(finished=True, message=result, board=board, scoreDark=numDark, scoreLight=numLight)

    # Switches back to Dark (me)
    current_player = "Dark "

    return jsonify(status="success", board=board, player=current_player, movesLeft=move_counter) # Tells the frontend that the move is legal and has been applied to the board

# Flask is run
if __name__ == "__main__":
    app.run(debug=True)