"""Plot the training and validation losses and the accuracy."""


import os
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def plot_losses(path_losses_csv, n_samples):
    """Plot the training and validation losses."""
    df = pd.read_csv(path_losses_csv)
    plt.plot(df["epoch"], df["training_loss"], label="Training Loss")
    plt.plot(df["epoch"], df["validation_loss"], label="Validation Loss")
    plt.title(f"Training & Validation Loss ({n_samples} samples)")
    plt.ylabel("Loss")
    plt.xlabel("Epoch")
    plt.legend()
    plt.grid()
    path_losses_png = path_losses_csv.replace(".csv", ".png")
    plt.savefig(path_losses_png)
    plt.close()


def plot_accuracy(path_accuracies_csv):
    """Plot the accuracy."""
    df = pd.read_csv(path_accuracies_csv)
    plt.plot(df["n_sample"], df["accuracy"], marker="o", label="Accuracy")
    plt.title("Accuracy")
    plt.ylabel("Accuracy")
    plt.xlabel("Number of samples (80%-training, 20%-testing)")
    plt.xticks(df["n_sample"], rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.grid()
    path_losses_png = path_accuracies_csv.replace(".csv", ".png")
    plt.savefig(path_losses_png)
    plt.close()


if __name__ == "__main__":
    game = "connect4"
    turn = "t6"
    version  = "01"
    n_samples_list = [
        # 10,
        # 20,
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
        path_losses_csv = os.path.join(path_data_subdir, f"{game}_losses_{turn}_{n_samples}_{version}.csv")
        path_accuracy_csv = os.path.join(path_data_subdir, f"{game}_accuracy_{turn}_{n_samples}_{version}.csv")
        path_accuracies_csv = os.path.join(path_data_subdir, f"{game}_accuracies_{turn}_{version}.csv")

        # Create directories       
        os.makedirs(path_data_subdir, exist_ok=True)

        # Plot losses
        plot_losses(
            path_losses_csv=path_losses_csv,
            n_samples=n_samples,
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
