EMPTY_SQUARE = "."
PLAYER_BLACK = "B"
PLAYER_WHITE = "W"
N = 4

def generate_board():
    """
    This will generate us an empty 4x4 board.
    """
    return [[EMPTY_SQUARE for _ in range(N)] for _ in range(N)] 

def print_board(board):
    """
    Prints the 4x4 board
    """
    for row in board:
        print(" ".join(row))
    print()

#Get orthoganal neigbhors

def orth_neighbors(r, c):
    """
    Inputs: The row (r) and column (c) of a square on the board. 
    Output: A list of all orthogonal neigbors (up, down, left, right).

    Example (on a 4x4 board):
    orth_neighbors(0, 0) -> [(0, 1), (1, 0)]
    orth_neighbors(1, 1) -> [(0, 1), (1, 0), (1, 2), (2, 1)]


    """
    orth_result = []
    if r > 0:
        orth_result.append((r-1, c)) # Up
    if r < N-1:
        orth_result.append((r+1, c)) # Down
    if c > 0:
        orth_result.append((r, c-1)) # Left
    if c < N-1:
        orth_result.append((r, c+1)) # Right
    return orth_result




def compute_control(board):
    """
    Input: The current 4x4 board
    Output: The control for the player 

    Rules for controlling:

    1. A square is controlled if there is already a marble on that square. 
    2. An empty square is controlled by a player if all of its orthogonal neighbors are controlled by the same player. 
    3. This process would be repeated until no new squares can be claimed. 
    """
    # Copies the board into 'control' (so the original board is not modified directly)
    control  = [[board[r][c] for c in range(N)] for r in range(N)] 

    status = True

    # Repeat until no futher chages are possible 
    while status:
        status = False
        for r in range(N):
            for c in range(N):
                # Get valyes of orthogonal neighbors
                if control[r][c] == EMPTY_SQUARE:
                    # If all non-empty neighbors are the same value, fill the square
                    neighbor_vals = [control[rr][cc] for rr, cc in orth_neighbors(r, c)]
                    if neighbor_vals and all(val == neighbor_vals[0] and val != EMPTY_SQUARE for val in neighbor_vals):
                        control[r][c] = neighbor_vals[0]
                        status = True # A change was made so continue looping
                    
    # Return the updated board with updated values
    return control




def player_move(board, player, r, c):
    """
    Inputs: The current 4x4 board, B or W player, row and column of index of the move 
    Output: The new board configuration after the player move and all autofills have been applied

    Steps: 

    1. Player places a marble on a chosen square. 
    2. Recompute the control of the board. 
    3. If this causes any empty squares to become controlled by the same player, automatically fill the squares with the player's marble. 
    4. Repeat the auto-fill process until no new squares have been filled. 
    5. Return the updated board configuration. 

    """
    # Convert the board rows into lists for mutation
    board = [list(row) for row in board]

    # Place the player's marble
    board[r][c] = player

    # Compute the initial control map for the board
    control = compute_control(board)
    board_filled = True

    # Repeat until no more squares can be filled
    while board_filled:
        board_filled = False
        for rr in range(N):
            for cc in range(N):
                # If a square is emptu but marked as controlled by player
                if board[rr][cc] == EMPTY_SQUARE and control[rr][cc] == player:
                    # Fill that square with player's piece
                    board[rr][cc] = player
                    board_filled = True
        
        # Recompute the control map
        control = compute_control(board)
    
    # Return the updated board configuration
    return board

def game_over(board):
    """
    Defines the condition if the game is over. 
    """
    return all(board[r][c] != EMPTY_SQUARE for r in range(N) for c in range(N))

def compute_score(board):
    """
    Compute the score of the board position. 

    Input: current 4x4 board
    Output: evaluation score

    Scoring rules:

    1. The score is the number of black marbles minus the number of white marbles.
    2. + values mean black is winning
    3. - values mean white is winning
    4. 0 values mean a draw

    """
    # Count the number of black and black marbles on the board
    black = sum(board[r][c] == PLAYER_BLACK for r in range(N) for c in range(N))
    # Count the number of black and white marbles on the board
    white = sum(board[r][c] == PLAYER_WHITE for r in range(N) for c in range(N))
    # Return the difference (positive if black has more, negative if white has more)
    return black - white

# We will set a global variable node_explored which will be used for the minimax and alpha beta pruning algorithm
nodes_explored = 0


def minimax(board, player, depth = 0, max_depth = 4): # Made sure to include depth parameters so that the algorithm doesn't recurse infinitely. 
    """
    Minimax search for the Og game. 

    This function will explore all the possible moves from the curremt board position and returns the best move with an achievable score. 
    Assume both players play optimally.

    How it works:

    1. If the board is full, return the evaluation score of the board otherwise, generate all possible moves for the next player. 
    2. If it's player Black's turn, choose the move that will maximize the score. 
    3. If it's player White's turn, choose the move that will minimize the score. 
    4. Keep track of how many nodes have been explored. 

    Inputs: the current 4x4 board and player black (B) or player white (w)
    Output: The player's chosen move as a tuple (row, column) and the best achievable score from it. 

    """

     # Keep track of how many nodes have been explored
    global nodes_explored
    nodes_explored += 1

    if game_over(board) or depth >= max_depth:
        return None, compute_score(board)
    
    best_move = None

    # If it's black's turn then maximize the player
    if player == PLAYER_BLACK:
        max_val = float("-inf") # lowest possible value
        for r in range(N):
            for c in range(N):
                if board[r][c] == EMPTY_SQUARE:
                    # Copy the board so original doesn't get modified
                    new_board = [list(row) for row in board]

                    # Simulate placing a piece for black
                    player_move(new_board, player, r, c)

                    # Recurse because it's whites turn
                    _, val = minimax(new_board, PLAYER_WHITE, depth+1, max_depth)

                    # Choose the best move that amximizes black's evaluation
                    if val > max_val:
                        max_val = val
                        best_move = (r, c)
        return best_move, max_val

    # If it's white's turn, then minimize the player
    else:
        min_val= float("inf") # start with highest possible value
        for r in range(N):
            for c in range(N): 
                if board[r][c] == EMPTY_SQUARE:
                    # Copy the board
                    new_board = [list(row) for row in board]
                     # Simulate placing a piece foer white
                    player_move(new_board, player, r, c)

                    # Recurse because it's blacks turn
                    _, val = minimax(new_board, PLAYER_BLACK, depth+1, max_depth)

                    # Choose the best move that minimizes white's evaluation
                    if val < min_val:
                        min_val = val
                        best_move = (r, c)
        return best_move, min_val

def alphabeta(board, player, alpha = float("-inf"), beta = float("inf"), depth = 0, max_depth = 4): #incorporated the alpha and beta parameters for alpha-beta pruning algorithm
    """
    Alphabeta search for the Og game. 

    Inputs: the current 4x4 board, player black (B) or player white (w), alpha (best value so far for maximizing player), and 
    beta (best value so far for minimizing player))
    Output: The player's chosen move as a tuple (row, column) and the best achievable score from it. 

    """

    #Keep track of how many nodes have been explored
    global nodes_explored 
    nodes_explored += 1
    if game_over(board) or depth >= max_depth:
        return None, compute_score(board)
    
    # Black's turn, maximize player 
    best_move = None
    if player == PLAYER_BLACK:
        max_val = float("-inf")
        for r in range(N):
            for c in range(N):
                if board[r][c] == EMPTY_SQUARE:

                    # Copy the board so original doesn't get modified
                    new_board = [list(row) for row in board]
                    new_board = player_move(new_board, player, r, c)

                    # Recurse because it's whites turn
                    _, val = alphabeta(new_board, PLAYER_WHITE, alpha, beta, depth+1, max_depth)  

                     # Choose the best move that minimizes black's evaluation      
                    if val > max_val:
                        max_val = val
                        best_move = (r, c)
                    
                    # Update alpha for pruning
                    alpha = max(alpha, val)

                    # Prune cutoff
                    if beta <= alpha:
                        break
        return best_move, max_val
    
    else:

        # White's turn: minimize player
        min_val = float("inf")
        for r in range(N):
            for c in range(N):
                if board[r][c] == EMPTY_SQUARE:

                    # Copy the board so original doesn't get modified
                    new_board = [list(row) for row in board]
                    new_board = player_move(new_board, player, r, c)

                    # Recurse because it's whites turn
                    _, val = alphabeta(new_board, PLAYER_BLACK, alpha, beta, depth+1, max_depth)

                    # Choose the best move that minimizes black's evaluation      
                    if val < min_val:
                        min_val = val
                        best_move = (r, c)

                    # Update beta for pruning
                    beta = min(beta, val)
                    if beta <= alpha:
                        break
        return best_move, min_val



# Generate new initial board 
board = generate_board()

# -----------------Minimax---------------------
nodes_explored = 0 # Reset node counter 

# First player's move (black)
move, value = minimax(board, PLAYER_BLACK)
print("minimax first player has value", value)
print("minimax examined", nodes_explored, "nodes")
print("next move: ", move)

# Apply chosen move if true
if move:
    board = player_move(board, PLAYER_BLACK, move[0], move[1])

# Second player's move (white)
move, value = minimax(board, PLAYER_WHITE)
print("minimax second player has value", value)
print("minimax examined", nodes_explored, "nodes")
print("next move: ", move)


print()

#----------------Alpha Beta Pruning-------------------
nodes_explored = 0 # reset node counter

# First player's move (black)
move, value = alphabeta(board, PLAYER_BLACK)
print("alpha-beta first player has value", value)
print("alpha-beta examined", nodes_explored, "nodes")
print("next move: ", move)

# Apply chosen move if true
if move:
    board = player_move(board, PLAYER_BLACK, move[0], move[1])

# Second player's move (white)
move, value = alphabeta(board, PLAYER_WHITE)
print("alpha-beta second player has value", value)
print("alpha-beta examined", nodes_explored, "nodes")
print("next move: ", move)