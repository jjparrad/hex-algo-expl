import math
import random
from typing import Tuple

class MCTSNode:
    def __init__(self,state=None, move=None, parent=None):
        self.state = state
        self.move = move  # Le coup joué pour atteindre ce nœud
        self.parent = parent  # Référence au parent
        self.children = []  # Liste des enfants
        self.visits = 0  # Nombre de visites
        self.wins = 0  # Nombre de victoires

    def uct_value(self, exploration_weight=1.41):
        if self.visits == 0:
            return float('inf')  # Encourager l'exploration des nœuds non visités
        return (self.wins / self.visits) + exploration_weight * math.sqrt(math.log(self.parent.visits) / self.visits)

    def is_terminal(self):
        """Retourne True si l'état du jeu à ce nœud est terminal."""
        return self.state.is_game_over()

class HexMCTS:
    def __init__(self, board, simulations=1000):
        self.board = board
        self.simulations = simulations
    
    def select(self, node):
        """ Sélectionne le meilleur nœud basé sur UCT """
        while node.children:
            node = max(node.children, key=lambda child: child.uct_value())
        return node

    def expand(self, node, player):
        """ Ajoute des enfants non explorés au nœud """
        possible_moves = self.board.get_possible_moves()
        for move in possible_moves:
            child = MCTSNode(move, parent=node)
            node.children.append(child)
    
    def simulate(self, node, player):
        """ Joue une partie aléatoire à partir du nœud actuel et retourne le gagnant """
        temp_board = self.board.clone()
        
        #temp_board.place_piece(player, node.move)
        current_player = player  # Alterne entre les joueurs


        while temp_board.check_winner() is None:
            
            move = random.choice(temp_board.get_possible_moves())
            temp_board.place_piece(current_player, move)
            current_player = 3 - current_player

        return temp_board.check_winner()

    def backpropagate(self, node, result, player):
        """ Met à jour les statistiques en remontant dans l'arbre """
        while node is not None:
            node.visits += 1
            if result == player:
                node.wins += 1
            node = node.parent
    
    def mcts(self, player):
        """ Effectue les simulations et retourne le meilleur mouvement """
        root = MCTSNode()
        for i in range(self.simulations):

            leaf = self.select(root)
            if leaf.visits > 0:
                self.expand(leaf, player)
                leaf = random.choice(leaf.children)
               
            
            result = self.simulate(leaf, player)
            self.backpropagate(leaf, result, player)

        maxi = 0.0
        best_child = root.children[0]

        for child in root.children:
            current = child.wins / child.visits
            #print(child.move,child.wins,child.visits,"score",current*100)
            if (current >= maxi):
                maxi = current
                best_child = child
            
        

        print("choix final",best_child.move, maxi)
        return best_child.move