import copy
import random
from math import sqrt, log
from src.utils.players import Players


class TicTacToe:
    def __init__(self):
        self.board = [" "] * 9
        self.current_player = Players.P1.value

    def display_board(self) -> None:
        """
        Prints the board in a human-readable format.
        """
        print("\n")
        for i in range(3):
            print(" | ".join(self.board[i * 3:(i + 1) * 3]))
            if i < 2:
                print("-" * 9)
        print("\n")

    def is_valid_move(self, move: int) -> bool:
        """
        Checks if a move is valid (i.e., the chosen cell is empty).
        """
        return self.board[move] == " "

    def make_move(self, move: int) -> bool:
        """
        Executes a move and switches to the other player.
        """
        if self.is_valid_move(move):
            self.board[move] = self.current_player
            self.current_player = Players.P2.value if self.current_player == Players.P1.value else Players.P1.value
            return True
        return False

    def undo_move(self, move: int) -> None:
        """
        Reverts a move and switches back to the previous player.
        """
        self.board[move] = " "
        self.current_player = Players.P2.value if self.current_player == Players.P1.value else Players.P1.value

    def is_winner(self, player: str) -> bool:
        """
        Checks if the given player has a winning combination.
        """
        win_positions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        return any(all(self.board[pos] == player for pos in line) for line in win_positions)

    def is_draw(self) -> bool:
        """
        Determines if the board is full (resulting in a draw).
        """
        return all(cell != " " for cell in self.board)

    def get_valid_moves(self) -> list:
        """
        Returns a list of all valid (empty) cell indices.
        """
        return [i for i in range(9) if self.board[i] == " "]

    def is_game_over(self) -> bool:
        """
        Checks if the game has ended due to a win or a draw.
        """
        return self.is_winner(Players.P1.value) or self.is_winner(Players.P2.value) or self.is_draw()


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

    def best_child(self, exploration_weight: float = 1.4) -> "Node": # TODO: ??? why "Node" and not just Node ???
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
    def __init__(self, game_constructor, iterations: int = 1000) -> None:
        self.iterations = iterations
        self.game_constructor = game_constructor

    def search(self, root: Node) -> Node:
        """
        Repeats the MCTS process (selection, expansion, simulation, backpropagation) 
        for a given number of iterations.
        Returns the best child node after the iterations.
        """
        player1 = root.state.current_player
        player2 = Players.P2.value if player1 == Players.P1.value else Players.P1.value
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
        for node in root.children:
            node.state.display_board()
            print(f"{node.wins = }")
            print(f"{node.visits = }")
        return root.best_child(exploration_weight=0.0) # TODO-?: Is exploration_weight=0.0?
        # return root.best_child() # TODO-?: Is exploration_weight=1.4?

    # TODO-?: Which _selection is correct?
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

    # TODO-?: Which _selection is correct?
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
                node = node.best_child() # TODO-?: Is exploration_weight=1.4?
        return node

    def _expand(self, node: Node) -> Node: # TODO: Node or RuntimeError
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


if __name__ == "__main__":
    game = TicTacToe()
    mcts = MCTS(game_constructor=TicTacToe, iterations=1000)

    # initial state
    # game.board = [
    #     " ", "X", "X",
    #     "O", "O", " ",
    #     " ", " ", " "
    # ]
    # game.board = [
    #     "X", " ", "X",
    #     " ", " ", " ",
    #     "O", "O", " "
    # ]

    # _select flat can not solve this case
    # game.board = [
    #     " ", " ", " ",
    #     "O", "O", " ",
    #     "X", " ", " "
    # ]

    while not game.is_game_over():
        game.display_board()
        if game.current_player == Players.P1.value: # User will start the game
        # if game.current_player == Players.P2.value: # AI will start the game
            move = int(input("Your turn (0-8): "))
            while not game.is_valid_move(move=move):
                move = int(input("Invalid move. Try again."))
            game.make_move(move=move)
        else:
            print("AI is thinking...")
            root = Node(game)
            board_best_move = mcts.search(root=root).state
            list1 = game.board
            list2 = board_best_move.board
            best_move = [index for index, (element1, element2) in enumerate(zip(list1, list2)) if element1 != element2][0]
            game.make_move(move=best_move)

    game.display_board()
    if game.is_winner(player=Players.P1.value):
        print(f"{Players.P1.value} win!")
    elif game.is_winner(player=Players.P2.value):
        print(f"{Players.P2.value} wins!")
    else:
        print("It's a draw!")
