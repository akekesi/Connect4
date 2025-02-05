# TODO-?: How is the model trained whose turn is it?


import os
import torch
import random
from torch import nn
from torch import optim
import torch.nn.functional as F

from src.mcts.mcts import MCTS, Node
from src.utils.players import Players
from src.connect4.connect4_mcts import Connect4


PATH_MODEL_TRAINED = os.path.join(os.path.dirname(__file__), "connect4_nn.pth")
MAPPING_BOARD_TO_TENSOR = {
    Players.P1.value: 1,
    Players.P2.value: -1,
    Players.EMPTY.value: 0,
}


def board_to_tensor(board, mapping=MAPPING_BOARD_TO_TENSOR):
    board_array = [[mapping[cell] for cell in row] for row in board]
    board_tensor = torch.tensor(board_array, dtype=torch.float32)
    return board_tensor


class Connect4NN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 64, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1)
        self.fc1 = nn.Linear(128 * 6 * 7, 512)
        self.fc2 = nn.Linear(512, 7)  # Output layer for 7 possible moves

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = x.view(x.size(0), -1)  # Flatten
        x = F.relu(self.fc1(x))
        x = self.fc2(x)  # Raw scores for moves
        return x


class MCTSAgent:
    def __init__(self):
        self.mcts = MCTS(
            game_constructor=Connect4,
            player_1=Players.P1.value,
            player_2=Players.P2.value,
            iterations=1000,
        )
        self.training_data = []

    def get_best_move(self, game: Connect4): # TODO: Put get_best_move into MCTS class
        root = Node(game)
        board_best_move = self.mcts.search(root=root).state
        best_move = self.mcts.get_changed_position(
            list1=game.board,
            list2=board_best_move.board,
        )
        board_tensor = board_to_tensor(game.board)
        self.training_data.append((board_tensor, best_move[1]))

        return best_move

    def get_training_data(self):
        return self.training_data

    def play_game(self, turns=42):
        turn = 0
        game = Connect4()
        while not game.is_game_over():
            root = Node(game)
            board_best_move = self.mcts.search(root=root).state
            best_move = self.mcts.get_changed_position(
                list1=game.board,
                list2=board_best_move.board,
            )
            if turn == turns:
                return game
            turn += 1
            game.make_move(move=best_move[1])
        return None
 

def train_model(model, training_data, epochs=10, lr=0.001):
    optimizer = optim.Adam(model.parameters(), lr=lr)
    loss_function = nn.CrossEntropyLoss()

    for epoch in range(epochs):
        total_loss = 0
        for board_tensor, move in training_data:
            optimizer.zero_grad()

            # Forward pass
            output = model(board_tensor.clone().detach().unsqueeze(0).unsqueeze(0)) # TODO-?: Why unsqueeze(0) twice?

            # Convert move to tensor format
            move_target = torch.tensor([move], dtype=torch.long)

            # Compute loss
            # TODO-print:
            # print(f"{output = }")
            # print(f"{move = }")
            loss = loss_function(output, move_target)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print(f"Epoch {epoch + 1}/{epochs}, Loss: {total_loss:.4f}")


def self_play_and_train():
    model = Connect4NN()
    mcts_agent = MCTSAgent()

    # Simulate multiple games
    for _ in range(1000):  # TODO: check this!
        game = Connect4()
        turns = random.randint(0, 41)
        turns = 6 # play only 6 turns for testing
        # TODO-print:
        # print(f"{turns = }")
        game = mcts_agent.play_game(turns=turns)
        # game.board = [ # play always the same game for testing --> it works!
        #     [" ", " ", " ", " ", " ", " ", " "],
        #     [" ", " ", " ", " ", " ", " ", " "],
        #     [" ", " ", " ", " ", " ", " ", " "],
        #     [" ", " ", " ", " ", " ", " ", " "],
        #     [" ", " ", "O", "O", " ", " ", " "],
        #     [" ", "O", "X", "X", " ", "X", " "],
        # ]
        if game is None:
            continue
        # TODO-print:
        # game.display_board(turn=turns)
        mcts_agent.get_best_move(game=game)

    # Get training data
    training_data = mcts_agent.get_training_data()
    # TODO-print:
    print(f"{training_data = }")

    # Train the model
    train_model(model, training_data, epochs=20, lr=0.001)

    # Save trained model
    torch.save(model.state_dict(), PATH_MODEL_TRAINED)
    print("Model trained and saved!")


def load_trained_model():
    model = Connect4NN()
    model.load_state_dict(torch.load(PATH_MODEL_TRAINED))
    model.eval()
    return model


def test_model():
    """
    Test the trained model by selecting the best move for a given board state.
    """
    model = load_trained_model()

    game = Connect4()
    game.board = [
        [" ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " "],
        [" ", " ", "O", "O", " ", " ", " "],
        [" ", "O", "X", "X", " ", "X", " "],
    ]
    # TODO: board has to be set to a valid game state
    board_tensor = board_to_tensor(game.board).clone().detach().unsqueeze(0).unsqueeze(0) # TODO-?: Why unsqueeze(0) twice?

    best_move_scores = model(board_tensor)
    best_move = torch.argmax(best_move_scores).item()
    print("Selected move:", best_move)


if __name__ == "__main__":
    self_play_and_train()
    test_model()

"""
Output:
Epoch 1/20, Loss: 981.9482
Epoch 2/20, Loss: 237.0731
Epoch 3/20, Loss: 311.3291
Epoch 4/20, Loss: 386.4855
Epoch 5/20, Loss: 228.2634
Epoch 6/20, Loss: 221.9876
Epoch 7/20, Loss: 169.1801
Epoch 8/20, Loss: 132.8468
Epoch 9/20, Loss: 97.4664
Epoch 10/20, Loss: 52.3962
Epoch 11/20, Loss: 53.1575
Epoch 12/20, Loss: 26.9603
Epoch 13/20, Loss: 19.4877
Epoch 14/20, Loss: 49.7511
Epoch 15/20, Loss: 41.9704
Epoch 16/20, Loss: 12.0493
Epoch 17/20, Loss: 32.9875
Epoch 18/20, Loss: 9.5580
Epoch 19/20, Loss: 2.8325
Epoch 20/20, Loss: 52.3553
Model trained and saved!
Selected move: 6
"""
