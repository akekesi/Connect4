import copy
import random
from math import sqrt, log


class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0

    def is_fully_expanded(self) -> bool:
        """
        Returns True if all valid moves from this state have been expanded as child nodes.
        """
        return len(self.children) == len(self.state.get_valid_moves())

    def best_child(self, exploration_weight: float = 1.4) -> "Node": # TODO-?: Why "Node" and not just Node?
        """
        Selects the child node with the best balance of exploration and exploitation, 
        using the UCT/UCB1 formula.
        """
        return max(
            self.children,
            key=lambda child: (child.wins / child.visits) +
                              exploration_weight * sqrt(log(self.visits) / child.visits)
        )


class MCTS:
    def __init__(self, game_constructor, player1: str, player2: str, iterations: int = 1000) -> None:
        self.iterations = iterations
        self.game_constructor = game_constructor
        self.player1 = player1
        self.player2 = player2

    def search(self, root: Node) -> Node:
        """
        Repeats the MCTS process (selection, expansion, simulation, backpropagation) 
        for a given number of iterations.
        Returns the best child node after the iterations.
        """
        player1 = root.state.current_player
        player2 = self.player2 if player1 == self.player1 else self.player1
        for _ in range(self.iterations):
            node = self._select(node=root)
            # TODO-print:
            # print(f"{player1 = }")
            # node.state.display_board()
            # print(f"{node.state.current_player = }")
            reward = self._simulate(state=node.state, player1=player1, player2=player2)
            # TODO-print:
            # print(f"{reward = }")
            self._backpropagate(node=node, reward=reward)
        # TODO-print:
        # for node in root.children:
        #     node.state.display_board()
        #     print(f"{node.wins = }")
        #     print(f"{node.visits = }")
        return root.best_child(exploration_weight=0.0)

    def get_changed_position(self, list1, list2) -> tuple[int, int]:
        pos_y = [index for index, (element1, element2) in enumerate(zip(list1, list2)) if element1 != element2][0]
        pos_x = [index for index, (element1, element2) in enumerate(zip(list1[pos_y], list2[pos_y])) if element1 != element2][0]
        return (pos_y, pos_x)

    # TODO-?: Which _select is correct?
    # traverses the tree from the root
    # def _select(self, node: Node) -> Node:
    #     """
    #     Traverses the tree from the root, choosing the best child (based on UCT, UCB1), 
    #     until reaching an unexpanded node or a terminal state.
    #     """
    #     while not node.state.is_game_over():
    #         if not node.is_fully_expanded():
    #             return self._expand(node=node)
    #         else:
    #             node = node.best_child()
    #     return node

    # TODO-?: Which _select is correct?
    # traverses the children of the root (not the tree)
    def _select(self, node: Node) -> Node:
        """
        Traverses the children of the root, choosing the best child (based on UCT, UCB1), 
        until reaching an unexpanded node or a terminal state.
        """
        if not node.state.is_game_over():
            if not node.is_fully_expanded():
                node = self._expand(node=node)
            else:
                node = node.best_child()
        return node

    def _expand(self, node: Node) -> Node:
        """
        Expands a node by generating a new child node for an unvisited move.
        Creates a new game state for the selected move.
        """
        moves = node.state.get_valid_moves()
        for move in moves:
            new_state = self._get_next_state(state=node.state, move=move)
            if not any(child.state.board == new_state.board for child in node.children):
                child_node = Node(state=new_state, parent=node)
                node.children.append(child_node)
                return child_node

    def _simulate(self, state: Node, player1: str, player2: str) -> int:
        """
        Simulates a random playthrough from the current state until the game ends.
        Assigns a reward:
            +1 if ??? wins
            -1 if ??? wins
            0 for a draw.
        """
        current_state = self._clone_state(state=state)
        # TODO-print:
        # print(f"{state.current_player = }")
        while not current_state.is_game_over():
            # TODO-print:
            # current_state.display_board()
            # print(f"{current_state.current_player = }")
            move = random.choice(current_state.get_valid_moves())
            current_state.make_move(move=move)
        # TODO-print:
        # current_state.display_board()
        if current_state.is_winner(player=player1):
            return 1
            # return 1 + len([tile for tile in current_state.board if tile == " "])
        elif current_state.is_winner(player=player2):
            return -1
            # return -1 - len([tile for tile in current_state.board if tile == " "])
        else:
            return 0

    def _backpropagate(self, node: Node, reward: int) -> None:
        """
        Updates the wins and visits of the node and its ancestors, 
        alternating the reward (+1 for one player, -1 for the other).
        """
        while node is not None:
            node.visits += 1
            node.wins += reward
            reward = -reward
            node = node.parent

    def _get_next_state(self, state: Node, move: int) -> Node:
        """
        Creates a copy of the current state and 
        applies a move to generate a new state.
        """
        new_state = self._clone_state(state=state)
        new_state.make_move(move=move)
        return new_state

    def _clone_state(self, state: Node) -> Node:
        """
        Creates a deep copy of the game state 
        to ensure modifications do not affect the original.
        """
        new_state = self.game_constructor()
        new_state.board = copy.deepcopy(state.board)
        new_state.current_player = state.current_player
        return new_state
