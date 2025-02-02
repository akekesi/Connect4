"""
Unit tests for the MCTS class.

Run:
$ python -m tests.test_mcts
"""

import unittest
from src.mcts.mcts import Node, MCTS
from src.connect4.connect4_mcts import Connect4


class TestNode(unittest.TestCase):
    """
    Unit tests for the Node class.
    """

    def setUp(self) -> None:
        """
        This method is called before each test. It initializes the MCTS instance.
        """
        self.game = Connect4()
        self.node = Node(state=Connect4())

    def tearDown(self) -> None:
        """
        This method is called after each test. It cleans up the MCTS instance.
        """
        del self.game
        del self.node

    def test_init(self):
        """
        Test the initialization of the Node class.
        """
        self.assertIsInstance(self.node, Node)
        self.assertIsInstance(self.node.state, Connect4)
        self.assertEqual(self.node.parent, None)
        self.assertEqual(self.node.children, [])
        self.assertEqual(self.node.visits, 0)

    def test_is_fully_expanded(self):
        """
        Test the is_fully_expanded method of the Node class.
        """
        self.assertFalse(self.node.is_fully_expanded())

    def test_best_child(self):
        """
        Test the best_child method of the Node class.
        """
        # TODO: Implement this test


class TestMCTS(unittest.TestCase):
    """
    Unit tests for the MCTS class.
    """

    def setUp(self) -> None:
        """
        This method is called before each test. It initializes the MCTS instance.
        """
        self.mcts = MCTS(
            game_constructor=Connect4,
            player_1="X",
            player_2="O",
        )

    def tearDown(self) -> None:
        """
        This method is called after each test. It cleans up the MCTS instance.
        """
        del self.mcts

    def test_init(self):
        """
        Test the initialization of the MCTS class.
        """
        self.assertIsInstance(self.mcts, MCTS)
        self.assertEqual(self.mcts.game_constructor, Connect4)
        self.assertEqual(self.mcts.player_1, "X")
        self.assertEqual(self.mcts.player_2, "O")
        self.assertEqual(self.mcts.iterations, 1000)
        
    def test_search(self):
        """
        Test the search method of the MCTS class.
        """
        root = Node(state=Connect4())
        self.assertIsInstance(self.mcts.search(root=root), Node)

    def test_get_changed_position(self):
        """
        Test the get_changed_position method of the MCTS class.
        """
        list1 = [
            ["X", "O", "X", "O", "X", " ", "X"],
            ["O", "X", "O", "X", "O", "X", "O"],
            ["X", "O", "X", "O", "X", "O", "X"],
            ["O", "X", "O", "X", "O", "X", "O"],
            ["X", "O", "X", "O", "X", "O", "X"],
            ["O", "X", "O", "X", "O", "X", "O"],
        ]
        list2 = [
            ["X", "O", "X", "O", "X", "O", "X"],
            ["O", "X", "O", "X", "O", "X", "O"],
            ["X", "O", "X", "O", "X", "O", "X"],
            ["O", "X", "O", "X", "O", "X", "O"],
            ["X", "O", "X", "O", "X", "O", "X"],
            ["O", "X", "O", "X", "O", "X", "O"],
        ]
        self.assertEqual(self.mcts.get_changed_position(list1=list1, list2=list2), (0, 5))

    def test_select(self):
        """
        Test the select method of the MCTS class.
        """
        root = Node(state=Connect4())
        self.assertIsInstance(self.mcts._select(node=root), Node)

    def test_expand(self):
        """
        Test the expand method of the MCTS class.
        """
        root = Node(state=Connect4())
        self.assertIsInstance(self.mcts._expand(node=root), Node)

    def test_simulate(self):
        """
        Test the simulate method of the MCTS class.
        """
        root = Node(state=Connect4())
        self.assertIsInstance(self.mcts._simulate(state=root.state), int)

    def test_backpropagate(self):
        """
        Test the backpropagate method of the MCTS class.
        """
        root = Node(state=Connect4())
        reward = 1
        self.assertIsNone(self.mcts._backpropagate(node=root, reward=reward))

    def test_get_next_state(self):
        """
        Test the get_next_state method of the MCTS class.
        """
        root = Node(state=Connect4())
        move = 3
        self.assertIsInstance(self.mcts._get_next_state(state=root.state, move=move), Connect4)

    def test_clone_state(self):
        """
        Test the clone_state method of the MCTS class.
        """
        root = Node(state=Connect4())
        self.assertIsInstance(self.mcts._clone_state(state=root.state), Connect4)

if __name__ == "__main__":
    unittest.main()
