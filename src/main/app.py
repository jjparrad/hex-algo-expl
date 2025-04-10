# app.py
# Imports
from flask import Flask, render_template, request, jsonify # Flask imports
from game_logic.hexgame.board.hexboard import HexBoard # Hex imports
from game_logic.hexgame.board.mcts import *
from game_logic.awalegame.board.awaleboard import AwaleBoard # Awale imports


# Global variables
app = Flask(__name__, template_folder='game_ui/templates', static_folder='game_ui/static')
board_hex = None
board_awale = None
current_player = 1
size = 5
size_px = size
depth_hex = 4

depth_awale = 6

# Player vs IA variables
player = 1
IA = 2

# IA vs IA variables
IA1 = 1
IA2 = 2
current_IA = 2

# --------------------------------- Home pages --------------------------------- #
@app.route('/') # Home page
def index():
    return render_template('home.html')


@app.route('/home_hex') # Hex options page
def home_hex():
    return render_template('home_hex.html')


@app.route('/home_awale') # Awale options page
def home_awale():
    return render_template('home_awale.html')




# --------------------------------- Hex pages --------------------------------- #
@app.route('/game_hex', methods=['POST']) # Hex player vs player page
def game_hex():
    global board_hex, current_player, size_px, size
    size = int(request.form['size'])
    size_px = 120 + (44 * size)  # update the size_px used in the play.html
    board_hex = HexBoard(size)  # Create a new game board
    board_hex.display_board()  # Display the game board in the console
    current_player = 1  # Set player 1 as the starting player
    return render_template('game_hex.html', size=size, size_px=size_px, current_player=current_player)


@app.route('/game_hexia', methods=['POST']) # Hex player vs IA page
def game_hexia():
    global board_hex, current_player, size_px, size, player, IA
    player = int(request.form['player'])
    IA = 1 if player == 2 else 2
    #print(player)
    #print(IA)   
    size = int(request.form['size'])
    size_px = 120 + (44 * size)  # update the size_px used in the play.html
    board_hex = HexBoard(size)  # Create a new game board
    board_hex.display_board()  # Display the game board in the console
    
    return render_template('game_hexia.html', size=size, size_px=size_px)


@app.route('/game_hexiaia', methods=['POST']) # Hex IA vs IA page
def game_hexiaia():
    global board_hex, size_px, size
    size = int(request.form['size'])
    size_px = 120 + (44 * size)  # update the size_px used in the play.html
    board_hex = HexBoard(size)  # Create a new game board
    board_hex.display_board()  # Display the game board in the console
    return render_template('game_hexiaia.html', size=size, size_px=size_px)

@app.route('/game_mcts_hexia', methods=['POST']) # Hex player vs IA page
def game_mcts_hexia():
    global board_hex, current_player, size_px, size, player, IA
    player = int(request.form['player'])
    IA = 1 if player == 2 else 2
    size = int(request.form['size'])
    size_px = 120 + (44 * size)  # update the size_px used in the play.html
    board_hex = HexBoard(size)  # Create a new game board
    board_hex.display_board()  # Display the game board in the console
    
    return render_template('game_mcts_hexia.html', size=size, size_px=size_px)


@app.route('/game_mcts_hexiaia', methods=['POST']) # Hex IA vs IA page
def game_mcts_hexiaia():
    global board_hex, size_px, size
    size = int(request.form['size'])
    size_px = 120 + (44 * size)  # update the size_px used in the play.html
    board_hex = HexBoard(size)  # Create a new game board
    board_hex.display_board()  # Display the game board in the console
    return render_template('game_mcts_hexiaia.html', size=size, size_px=size_px)


@app.route('/hex_place_piece', methods=['POST']) # Player place a piece on the board
def hex_place_piece():
    global board_hex, current_player
    
    data = request.get_json()
    hexid = data['hexid']
    current_player = data['current_player']
    
    # Remove the "hex" prefix and split into row and column
    row, col = map(int, hexid[3:].split('-'))
    # change the current player
    try:
        if board_hex is not None:
            board_hex.place_piece(current_player, (row, col)) # Try to place the piece
            
            
            # check if the current player won
            winner = board_hex.check_winner()
            if winner:
                short_path = board_hex.shortest_path(current_player)
                print(f"Shortest path for player {current_player}: {short_path}")
                hexid = [f"hex{i[0]}-{i[1]}" for i in short_path]
                return jsonify({'winner': current_player, 'game_over': True, 'current_player': current_player,'hexid':hexid})
            current_player = 1 if current_player == 2 else 2

    except Exception as e:
        # Handle the exception here
        error_message = str(e)  # Get the error message
        board_hex.display_board() # Display the game board in the console
        print("error: ", error_message)
        return jsonify({'error': "An error has occured"}), 400
    return jsonify({'result': 'Success', 'current_player': current_player})


@app.route('/players_hexia', methods=['POST']) # Return player's and IA's values
def players_hexia():
    global player, IA
    return jsonify({'result': 'Success','player': player,'IA':IA})


@app.route('/first_move_IA_hex',methods=['POST']) #Return IA's first move if player=2
def first_move_IA_hex():
    global board_hex, IA 
    move = board_hex.get_best_move(depth_hex,IA)
    board_hex.place_piece(IA, move)
    iamove = "hex" + str(move[0]) + "-" + str(move[1])
    return jsonify({'result': 'Success','iamove':iamove})

@app.route('/hexiaia_place_piece', methods=['POST']) # IA place a unique piece on the board
def hexiaia_place_piece():
    print("MINMAX")
    global board_hex, current_IA

    data = request.get_json()
    current_IA = data['current_IA']

    try:
        if board_hex is not None:

            move_IA = board_hex.get_best_move(depth_hex,current_IA)
            board_hex.place_piece(current_IA, move_IA) # Try to place the piece
            iamove = "hex" + str(move_IA[0]) + "-" + str(move_IA[1])
            
            # check if current_IA won
            winner = board_hex.check_winner()
            if winner:
                short_path = board_hex.shortest_path(current_IA)
                print(f"Shortest path for player {current_IA}: {short_path}")
                hexid = [f"hex{i[0]}-{i[1]}" for i in short_path]
                return jsonify({'winner': current_IA, 'game_over': True,'hexid':hexid,'iamove':iamove})
            
    except Exception as e:
        # Handle the exception here
        error_message = str(e)  # Get the error message
        board_hex.display_board()
        print("error: ", error_message)
        return jsonify({'error': "An error has occured"}), 400
        
    return jsonify({'result': 'Success','iamove': iamove,'game_over': False})

@app.route('/hexiaia_mcts_place_piece', methods=['POST']) # IA place a unique piece on the board
def hexiaia_mcts_place_piece():
    print("MCTS")
    global board_hex, current_IA

    data = request.get_json()
    current_IA = data['current_IA']

    print("data")
    print(data)
    print("current_IA")
    print(current_IA)

    try:
        if board_hex is not None:
            
            mcts = HexMCTS(board_hex, simulations=5000)  # Initialiser MCTS avec le plateau
            
            move_IA = mcts.mcts(current_IA)  # Obtenir le meilleur coup avec MCTS
            print("ici",move_IA)
            board_hex.place_piece(current_IA, move_IA) # Try to place the piece
            
            iamove = "hex" + str(move_IA[0]) + "-" + str(move_IA[1])
            
            # check if current_IA won
            winner = board_hex.check_winner()
            if winner:
                short_path = board_hex.shortest_path(current_IA)
                print(f"Shortest path for player {current_IA}: {short_path}")
                hexid = [f"hex{i[0]}-{i[1]}" for i in short_path]
                return jsonify({'winner': current_IA, 'game_over': True,'hexid':hexid,'iamove':iamove})
            
    except Exception as e:
        # Handle the exception here
        error_message = str(e)  # Get the error message
        board_hex.display_board()
        print("error: ", error_message)
        return jsonify({'error': "An error has occured"}), 400
        
    return jsonify({'result': 'Success','iamove': iamove,'game_over': False})


@app.route('/hexiaia_random',methods=['POST']) #Return random move for IA
def hexiaia_random():
    global board_hex, current_IA 
    data = request.get_json()
    current_IA = data['current_IA']
    move = board_hex.random_move()   
    board_hex.place_piece(current_IA, move)
    iamove = "hex" + str(move[0]) + "-" + str(move[1])
    return jsonify({'result': 'Success','iamove':iamove})


@app.route('/hex_undo_move', methods=['POST']) # Undo last move on the board
def hex_undo_move():
    global board_hex
    
    data = request.get_json()
    hexid = data['hexid']
    
    # Remove the "hex" prefix and split into row and column
    row, col = map(int, hexid[3:].split('-'))

    # Remove the hex in board
    try:
        if board_hex is not None:
            board_hex.undo_move((row,col))

    except Exception as e:
        # Handle the exception here
        error_message = str(e)  # Get the error message
        board_hex.display_board()

        print("error: ", error_message)
        return jsonify({'error': "An error has occured"}), 400

    return jsonify({'result': 'Success'})


# --------------------------------- Awale pages --------------------------------- #
@app.route('/game_awale', methods=['POST']) # Hex play page
def game_awale():
    global board_awale, current_player
    board_awale = AwaleBoard()  # Create a new game board
    board_awale.display_board()  # Display the game board in the console
    current_player = 1  # Set player 1 as the starting player
    return render_template('game_awale.html',current_player=current_player)


@app.route('/game_awaleia', methods=['POST']) # Hex play page
def game_awaleia():
    global board_awale, current_player, player, IA
    board_awale = AwaleBoard()  # Create a new game board
    board_awale.display_board()  # Display the game board in the console
    player = int(request.form['player'])
    IA = 1 if player == 2 else 2
    current_player = 1  # Set player 1 as the starting player
    return render_template('game_awale_ia.html',current_player=current_player)


@app.route('/game_awaleiaia', methods=['POST']) # Hex play page
def game_awaleiaia():
    global board_awale
    board_awale = AwaleBoard()  # Create a new game board
    board_awale.display_board()  # Display the game board in the console
    current_player = 1  # Set player 1 as the starting player
    return render_template('game_awale_iaia.html',current_player=current_player)



@app.route('/players_awaleia', methods=['POST']) # Return player's and IA's values
def players_awaleia():
    global player, IA
    return jsonify({'result': 'Success','player': player,'IA':IA})

@app.route('/first_move_IA_awale',methods=['POST']) #Return IA's first move if player=2
def first_move_IA_awale():
    global board_awale, IA 
    move = board_awale.get_best_move(depth_awale,IA)
    board_awale.make_move(move, IA)
    iamove = move
    values = board_awale.get_board()
    scores = board_awale.get_scores()
    return jsonify({'result': 'Success','values':values,'score_1':scores[0],'score_2':scores[1]})


@app.route('/awaleia_place_piece', methods=['POST']) # IA place a unique piece on the board
def awaleia_place_piece():
    
    global board_awale, current_IA
    data = request.get_json()
    current_IA = data['current_IA']

    try:
        if board_awale is not None:
            
            values = board_awale.get_board()
            scores = board_awale.get_scores()
            print(scores)
            move_IA = board_awale.get_best_move(depth_awale,current_IA)
            winner = board_awale.check_winner()
            
            # check if current_IA won
            if winner == 1 or winner == 2:
                return jsonify({'winner': current_player, 'game_over': True, 'current_player': current_player,'values':values,'score_1':scores[0],'score_2':scores[1]})
            
            
            board_awale.make_move(move_IA,current_IA) # Try to place the piece
            iamove = move_IA
            values = board_awale.get_board()
            scores = board_awale.get_scores()
        
    
    except Exception as e:
        #print("OUI!!")
        # Handle the exception here
        error_message = str(e)  # Get the error message
        board_awale.display_board()
        values = board_awale.get_board()
        scores = board_awale.get_scores()
        print("error: ", error_message)
        return jsonify({'error': "An error has occured"}), 400
    #print("iamove",iamove)
    return jsonify({'result': 'Success','game_over': False,'iamove':iamove,'values':values,'score_1':scores[0],'score_2':scores[1]})


@app.route('/awale_place_piece', methods=['POST']) # player place a piece on the board
def awale_place_piece():
    global board_awale, current_player
    
    data = request.get_json()
    pitid = data['pitid']
    current_player = data['current_player']
    id = int(pitid)
    
    if board_awale is not None:
        try:
            board_awale.make_move(id, current_player) # Try to place the piece
            scores = board_awale.get_scores()
            board_awale.display_board() # Display the game board in the console
            values = board_awale.get_board()
            #print("values",values)
            winner = board_awale.check_winner()
            print("Gagnant joueur",winner)
            if winner:

                return jsonify({'winner': winner, 'game_over': True, 'current_player': current_player,'values':values,'pitid':pitid,'score_1':scores[0],'score_2':scores[1]})
            current_player = 1 if current_player == 2 else 2
        except Exception as e:
            # Handle the exception here
            error_message = str(e)  # Get the error message
            board_awale.display_board() # Display the game board in the console
            print("error: ", error_message)
            return jsonify({'error': "An error has occured"}), 400
    return jsonify({'result': 'Success', 'game_over': False,'current_player': current_player,'values':values,'score_1':scores[0],'score_2':scores[1],'pitid':pitid})




@app.route('/undo_move_awale', methods=['POST']) # Place last board into the board
def undo_move_awale():
    global board_awale
    
    data = request.get_json()
    values = data['values']
    score_1 = int(data['score_1'])
    score_2 = int(data['score_2'])

    try:
        if board_awale is not None:
            board_awale.undo_move(values,score_1,score_2)

    except Exception as e:
        # Handle the exception here
        error_message = str(e)  # Get the error message
        print("error: ", error_message)
        return jsonify({'error': "An error has occured"}), 400

    return jsonify({'result': 'Success'})




# --------------------------------- Run the app --------------------------------- #
if __name__ == '__main__':
    app.run(debug=False)
