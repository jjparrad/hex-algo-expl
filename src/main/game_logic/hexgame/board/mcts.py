import math
import random
from typing import Optional

class MCTSNode:
    def __init__(self, move: Optional[tuple[int, int]] = None, parent: Optional['MCTSNode'] = None, player_to_move: Optional[int] = None):
        self.move = move          # The move that led to this node
        self.parent = parent      # Parent node
        self.children = []        # Child nodes
        self.visits = 0           # Number of times this node was visited
        self.wins = 0             # Number of wins for this node
        self.player_to_move = player_to_move  # Player to move next

    def uct_value(self, exploration_weight: float = 1.41) -> float:
        if self.visits == 0:
            return float('inf')
        return (self.wins / self.visits) + exploration_weight * math.sqrt(math.log(self.parent.visits) / self.visits)


class HexMCTS:
    def __init__(self, board, simulations: int = 1000):
        self.board = board          # Current game state
        self.simulations = simulations

    def get_node_board(self, node: MCTSNode):
        """Reconstructs the board state for a given node"""
        board = self.board.clone()
        current_node = node
        moves = []
        players = []
        
        # Collect moves and players from node to root
        while current_node.parent is not None:
            moves.append(current_node.move)
            players.append(current_node.parent.player_to_move)
            current_node = current_node.parent
        
        # Apply moves in reverse order (from root to node)
        for move, player in zip(reversed(moves), reversed(players)):
            board.place_piece(player, move)
        return board

    def select(self, node: MCTSNode) -> MCTSNode:
        """Selects node using UCT until leaf node is reached"""
        while node.children:
            node = max(node.children, key=lambda child: child.uct_value())
        return node

    def expand(self, node: MCTSNode):
        """Expands node by creating all possible child states"""
        board = self.get_node_board(node)
        possible_moves = board.get_possible_moves()
        
        for move in possible_moves:
            child_player = 3 - node.player_to_move
            child = MCTSNode(
                move=move,
                parent=node,
                player_to_move=child_player
            )
            node.children.append(child)

    def simulate(self, node: MCTSNode) -> int:
        """Simulates random game from node's state and returns winner"""
        board = self.get_node_board(node)
        current_player = node.player_to_move
        
        while board.check_winner() is None:
            possible_moves = board.get_possible_moves()
            if not possible_moves:
                break  # No legal moves (shouldn't happen in Hex)
            move = random.choice(possible_moves)
            board.place_piece(current_player, move)
            current_player = 3 - current_player
        
        return board.check_winner()

    def backpropagate(self, node: MCTSNode, result: int, player: int):
        """Updates statistics along the path from node to root"""
        while node is not None:
            node.visits += 1
            if result == player:
                node.wins += 1
            node = node.parent

    def mcts(self, player: int) -> tuple[int, int]:
        """Performs MCTS search and returns best move"""
        root = MCTSNode(player_to_move=player)
        
        for _ in range(self.simulations):
            leaf = self.select(root)
            
            # Expand if not terminal state
            if leaf.visits == 0:
                winner = self.get_node_board(leaf).check_winner()
                if winner is not None:
                    self.backpropagate(leaf, winner, player)
                    continue
            
            if not leaf.children:
                self.expand(leaf)
            
            # Select node for simulation
            if leaf.children:
                selected = random.choice(leaf.children)
            else:
                selected = leaf  # Terminal node
                
            result = self.simulate(selected)
            self.backpropagate(selected, result, player)

        # Choose move with highest visit count
        best_move = max(root.children, key=lambda child: child.visits).move
        return best_move