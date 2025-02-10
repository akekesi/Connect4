# TODO-?: How is the model trained whose turn is it?


import os
import torch
import pandas as pd
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

from src.utils.players import Players
from src.nn.plots import plot_losses, plot_accuracy


ROWS = 6
COLS = 7
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
    """Neural network for Connect4."""

    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 64, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1)
        self.dropout = nn.Dropout(0.3)  # Dropout to prevent overfitting
        self.fc1 = nn.Linear(128 * 6 * COLS, 512)
        self.fc2 = nn.Linear(512, COLS)  # Output layer for COLS possible moves

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = x.view(x.size(0), -1)  # Flatten
        x = F.relu(self.fc1(x))
        x = self.dropout(x)  # Dropout applied here
        x = self.fc2(x)  # Raw scores for moves
        return x


def train_model(
        model,
        data_train,
        data_test,
        path_model_trained,
        path_losses_csv,
        epochs=20,
        lr=0.001,
    ):
    epochs_list = list(range(epochs))
    losses_training = []
    losses_validation = []
    optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=1e-4)
    loss_function = nn.CrossEntropyLoss()

    for epoch in epochs_list:
        # Training phase
        model.train()
        total_loss_training = 0
        for board_tensor, best_move in data_train:
            optimizer.zero_grad()

            # Forward pass
            output = model(board_tensor.clone().detach().unsqueeze(0).unsqueeze(0)) # TODO-?: Why unsqueeze(0) twice?

            # Convert move to tensor format
            move_target = torch.tensor([best_move], dtype=torch.long)

            # Compute loss
            loss_training = loss_function(output, move_target)
            loss_training.backward()
            optimizer.step()

            total_loss_training += loss_training.item()

        # Validation phase
        model.eval()
        total_loss_validation = 0
        with torch.no_grad():
            for board_tensor, best_move in data_test:
                # Forward pass
                output = model(board_tensor.clone().detach().unsqueeze(0).unsqueeze(0))

                # Convert move to tensor format
                move_target = torch.tensor([best_move], dtype=torch.long)

                # Compute loss
                loss = loss_function(output, move_target)
                total_loss_validation += loss.item()

        losses_training.append(total_loss_training)
        losses_validation.append(total_loss_validation)

        print(f"Epoch {epoch + 1}/{epochs}, Training Loss: {total_loss_training:.4f}, Validation Loss: {total_loss_validation:.4f}")

    # Save trained model
    torch.save(model.state_dict(), path_model_trained)

    # Create a DataFrame
    df = pd.DataFrame({
        "epoch": epochs_list,
        "training_loss": losses_training,
        "validation_loss": losses_validation,
    })

    # Save as CSV
    df.to_csv(path_losses_csv, index=False)


def load_trained_model(
        model,
        path_model_trained
    ):
    model.load_state_dict(torch.load(path_model_trained))
    model.eval()
    return model


def test_model(
        model,
        data_test,
        path_accuracy_csv,
    ) -> None:
    moves_correct = 0
    moves_total = 0
    for board_tensor, best_move in data_test:
        best_move_scores = model(board_tensor.clone().detach().unsqueeze(0).unsqueeze(0))
        best_move_model = torch.argmax(best_move_scores).item()

        if best_move_model == best_move:
            moves_correct += 1
        moves_total += 1

    # Calculate accuracy
    accuracy = moves_correct / moves_total if moves_total > 0 else 0
    print(f"Accuracy of the model: {accuracy * 100:.2f}%")
    df = pd.DataFrame({
        "moves_correct": [moves_correct],
        "moves_total": [moves_total],
        "accuracy": [accuracy],
    })

    # Save as CSV
    df.to_csv(path_accuracy_csv, index=False)


if __name__ == "__main__":

    # Versions:
    # 01
    # - Dropout (0.3)
    # - L2 Regularization (Weight Decay 1e-4)
    # 02
    # - delete this verison

    game = "connect4"
    turn = "t6"
    version  = "02"
    n_samples_list = [
        10,
        20,
        # 50,
        # 100,
        # 200,
        # 500,
        # 1_000,
        # 2_000,
        # 5_000,
        # 10_000,
    ]
    accuracies = []
    for n_samples in n_samples_list:
        # Paths
        path_data_dir = os.path.join(os.path.dirname(__file__), "data")
        path_data_subdir = os.path.join(path_data_dir, f"{turn}_{version}")
        path_model_trained = os.path.join(path_data_subdir, f"{game}_model_{turn}_{n_samples}_{version}.pth")
        path_losses_csv = os.path.join(path_data_subdir, f"{game}_losses_{turn}_{n_samples}_{version}.csv")
        path_accuracy_csv = os.path.join(path_data_subdir, f"{game}_accuracy_{turn}_{n_samples}_{version}.csv")
        path_accuracies_csv = os.path.join(path_data_subdir, f"{game}_accuracies_{turn}_{version}.csv")
        path_data_train = os.path.join(path_data_dir, "boards", f"{game}_boards_{turn}_{n_samples}_train.csv")
        path_data_test = os.path.join(path_data_dir, "boards", f"{game}_boards_{turn}_{n_samples}_test.csv")

        # Create directories
        os.makedirs(path_data_subdir, exist_ok=True)

        # Prepare data
        df_train = pd.read_csv(path_data_train)
        df_test = pd.read_csv(path_data_test)

        df_train_boards = df_train.iloc[:, :-1]
        df_test_boards = df_test.iloc[:, :-1]

        df_train_best_moves = df_train.iloc[:, -1]
        df_test_best_moves = df_test.iloc[:, -1]

        data_train = [(board_to_tensor([data[::-1][i:i+COLS][::-1] for i in range(0, len(data), COLS)]), best_move) for data, best_move in zip(df_train_boards.values, df_train_best_moves.values)]
        data_test = [(board_to_tensor([data[::-1][i:i+COLS][::-1] for i in range(0, len(data), COLS)]), best_move) for data, best_move in zip(df_test_boards.values, df_test_best_moves.values)]

        # Train model
        train_model(
            model=Connect4NN(),
            data_train=data_train,
            data_test=data_test,
            path_model_trained=path_model_trained,
            path_losses_csv=path_losses_csv,
            epochs=20,
            lr=0.001,
        )

        # Plot losses
        plot_losses(path_losses_csv, n_samples)

        # Test model
        model = load_trained_model(
            model=Connect4NN(),
            path_model_trained=path_model_trained
        )
        test_model(
            model=model,
            data_test=data_test,
            path_accuracy_csv=path_accuracy_csv,
        )

        # Get accuracy
        df_accuracy = pd.read_csv(path_accuracy_csv)
        accuracies.append(df_accuracy["accuracy"].values[0])

    # Save accuracies and n_samples as CSV
    df = pd.DataFrame({
        "n_sample": n_samples_list,
        "accuracy": accuracies
    })
    df.to_csv(path_accuracies_csv, index=False)

    # Plot accuracy
    plot_accuracy(path_accuracies_csv=path_accuracies_csv)
