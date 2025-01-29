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
    def __init__(self, game_constructor, player_1: str, player_2: str, iterations: int = 1000) -> None:
        self.iterations = iterations
        self.game_constructor = game_constructor
        self.player_1 = player_1
        self.player_2 = player_2

    def search(self, root: Node) -> Node:
        """
        Repeats the MCTS process (selection, expansion, simulation, backpropagation) 
        for a given number of iterations.
        Returns the best child node after the iterations.
        """
        for _ in range(self.iterations):
            node = self._select(node=root)
            # TODO-print:
            # node.state.display_board()
            # print(f"{node.state.player = }")
            reward = self._simulate(state=node.state)
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

    # traverses the tree from the root
    def _select(self, node: Node) -> Node:
        """
        Traverses the tree from the root, choosing the best child (based on UCT, UCB1), 
        until reaching an unexpanded node or a terminal state.
        """
        while not node.state.is_game_over():
            # TODO-print:
            # n_empty = len([x for row in node.state.board for x in row if x == " "])
            # if n_empty < 40:
            #     print(f"{n_empty = }")
            if not node.is_fully_expanded():
                return self._expand(node=node)
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
            state_new = self._get_next_state(state=node.state, move=move)
            if not any(child.state.board == state_new.board for child in node.children):
                node_child = Node(state=state_new, parent=node)
                node.children.append(node_child)
                return node_child

    def _simulate(self, state: Node) -> int:
        """
        Simulates a random playthrough from the current state until the game ends.
        Assigns a reward:
            +1 if ??? wins
            -1 if ??? wins
            0 for a draw.
        """
        state_cloned = self._clone_state(state=state)
        player_rewarded = self.player_1 if state_cloned.player == self.player_2 else self.player_2 # player wo made the last step to get current state

        # TODO-print:
        # print(f"{state_cloned.player = }")
        # print(f"{player_rewarded = }")
        while not state_cloned.is_game_over():
            move = random.choice(state_cloned.get_valid_moves())
            state_cloned.make_move(move=move)
        # TODO-print:
        # current_state.display_board()
        if state_cloned.is_winner(player=player_rewarded):
            return 1
        elif state_cloned.is_winner(player=state_cloned.player):
            return -1
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
        state_new = self._clone_state(state=state)
        state_new.make_move(move=move)
        return state_new

    def _clone_state(self, state: Node) -> Node:
        """
        Creates a deep copy of the game state 
        to ensure modifications do not affect the original.
        """
        state_new = self.game_constructor()
        state_new.board = copy.deepcopy(state.board)
        state_new.player = state.player
        return state_new
