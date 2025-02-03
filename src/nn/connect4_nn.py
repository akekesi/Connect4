import os
import torch
from torch import nn
from torch import optim
import torch.nn.functional as F

from src.mcts.mcts import MCTS
from src.utils.players import Players
from src.connect4.connect4_mcts import Connect4


PATH_MODEL_TRAINED = os.path.join(os.path.dirname(__file__), "connect4_nn.pth")


def board_to_tensor(board):
    mapping = {
        Players.P1.value: 1,
        Players.P2.value: -1,
        Players.EMPTY.value: 0,
    }
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
    def __init__(self, model):
        self.model = model
        self.training_data = []  # Store board states and chosen moves

    def select_move(self, board_state):
        board_tensor = board_state.clone().detach().unsqueeze(0).unsqueeze(0)

        # Simulate MCTS
        # TODO: replace with real MCTS logic
        move_scores = self.model(board_tensor)
        move = torch.argmax(move_scores).item()

        # Store training data (state, chosen move)
        self.training_data.append((board_tensor, move))

        return move

    def get_training_data(self):
        return self.training_data


def train_model(model, training_data, epochs=10, lr=0.001):
    optimizer = optim.Adam(model.parameters(), lr=lr)
    loss_function = nn.CrossEntropyLoss()

    for epoch in range(epochs):
        total_loss = 0
        for board_tensor, move in training_data:
            optimizer.zero_grad()

            # Forward pass
            output = model(board_tensor)

            # Convert move to tensor format
            move_target = torch.tensor([move], dtype=torch.long)

            # Compute loss
            loss = loss_function(output, move_target)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print(f"Epoch {epoch + 1}/{epochs}, Loss: {total_loss:.4f}")


def self_play_and_train():
    model = Connect4NN()
    agent = MCTSAgent(model)

    # Simulate multiple games
    for _ in range(1000):  # Play 1000 self-play games
        board_state = torch.randn(6, 7)  # TODO: Replace with a real board state
        agent.select_move(board_state)

    # Get training data
    training_data = agent.get_training_data()

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


# Example usage
def test_model():
    model = Connect4NN() # Just for testing without trained model
    # model = load_trained_model()  # Load trained model
    agent = MCTSAgent(model)

    # TODO: Replace with an actual game board state
    example_board = torch.randn(6, 7)  # Simulates a valid game board
    best_move = agent.select_move(example_board)
    print("Selected move:", best_move)


if __name__ == "__main__":
    game = Connect4()
    mcts = MCTS(
        game_constructor=Connect4,
        player_1=Players.P1.value,
        player_2=Players.P2.value,
        iterations=1000,
    )

    # self_play_and_train()

    # test_model()

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
