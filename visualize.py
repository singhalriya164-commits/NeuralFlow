"""
Visualization Module
====================
Generates publication-quality, aesthetically pleasing comparative charts
for technical analysis, whitepapers, and enterprise benchmarking.
All charts are saved as PNG files with 300 DPI resolution.
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for headless execution
import matplotlib.pyplot as plt
import seaborn as sns


# Set styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
matplotlib.rcParams['font.sans-serif'] = 'DejaVu Sans'
matplotlib.rcParams['axes.edgecolor'] = '#CCCCCC'
matplotlib.rcParams['axes.linewidth'] = 0.8

PALETTE = {
    "Vanilla RNN": "#E74C3C",     # Red / Coral
    "Bidirectional RNN": "#9B59B6", # Purple
    "LSTM": "#2980B9",            # Blue
    "GRU": "#27AE60"              # Emerald Green
}


def safe_savefig(fig, output_path: str, dpi: int = 300, **kwargs):
    """Safely saves a plot figure, handling locked file exceptions gracefully."""
    try:
        fig.savefig(output_path, dpi=dpi, **kwargs)
        print(f"[Saved] {output_path}")
    except OSError as e:
        print(f"[Warning] Could not overwrite {output_path} directly ({e}). Trying alternative path...")
        alt_path = output_path.replace(".png", "_new.png")
        try:
            fig.savefig(alt_path, dpi=dpi, **kwargs)
            print(f"[Saved Alternative] {alt_path}")
        except Exception as e2:
            print(f"[Notice] Skipped file write for {output_path}: {e2}")
    finally:
        plt.close(fig)


def plot_accuracy_comparison(results: dict, output_path: str = "accuracy_comparison.png"):
    """Bar chart comparing Test Accuracy across all 4 models."""
    fig, ax = plt.subplots(figsize=(8, 5))
    models = list(results.keys())
    accs = [results[m]["accuracy"] for m in models]
    colors = [PALETTE[m] for m in models]

    bars = ax.bar(models, accs, color=colors, width=0.55, edgecolor='#333333', linewidth=1.2)
    ax.set_title("Test Accuracy Comparison Across Recurrent Architectures", fontsize=13, fontweight='bold', pad=15)
    ax.set_ylabel("Test Accuracy (%)", fontsize=11, fontweight='bold')
    ax.set_ylim(0, 105)

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=11, fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[Saved] {output_path}")


def plot_f1_comparison(results: dict, output_path: str = "f1_comparison.png"):
    """Grouped bar chart comparing Macro vs Weighted F1 scores."""
    fig, ax = plt.subplots(figsize=(9, 5))
    models = list(results.keys())
    macro_f1 = [results[m]["f1_macro"] for m in models]
    weighted_f1 = [results[m]["f1_weighted"] for m in models]

    x = np.arange(len(models))
    width = 0.32

    rects1 = ax.bar(x - width/2, macro_f1, width, label='Macro F1-score', color='#3498DB', edgecolor='#2C3E50')
    rects2 = ax.bar(x + width/2, weighted_f1, width, label='Weighted F1-score', color='#1ABC9C', edgecolor='#16A085')

    ax.set_title("F1-Score Comparison (Macro vs Weighted)", fontsize=13, fontweight='bold', pad=15)
    ax.set_ylabel("F1-Score (%)", fontsize=11, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=10, fontweight='bold')
    ax.set_ylim(0, 105)
    ax.legend(loc='lower right', frameon=True)

    for bar in rects1:
        h = bar.get_height()
        ax.annotate(f'{h:.1f}%', xy=(bar.get_x() + bar.get_width()/2, h),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9)
    for bar in rects2:
        h = bar.get_height()
        ax.annotate(f'{h:.1f}%', xy=(bar.get_x() + bar.get_width()/2, h),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[Saved] {output_path}")


def plot_parameter_count_comparison(param_counts: dict, output_path: str = "parameters_comparison.png"):
    """Horizontal bar chart comparing Trainable Parameters."""
    fig, ax = plt.subplots(figsize=(9, 4.5))
    models = list(param_counts.keys())
    totals = [param_counts[m]["total_parameters"] for m in models]
    recurrents = [param_counts[m]["recurrent_parameters"] for m in models]
    colors = [PALETTE[m] for m in models]

    y = np.arange(len(models))
    bars = ax.barh(y, totals, color=colors, height=0.55, edgecolor='#333333', linewidth=1.1)

    ax.set_title("Total Trainable Parameters Comparison", fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel("Number of Trainable Parameters", fontsize=11, fontweight='bold')
    ax.set_yticks(y)
    ax.set_yticklabels(models, fontsize=10, fontweight='bold')
    ax.set_xlim(0, max(totals) * 1.2)

    for bar, rec in zip(bars, recurrents):
        width = bar.get_width()
        ax.annotate(f'{width:,} (Recurrent: {rec:,})',
                    xy=(width, bar.get_y() + bar.get_height()/2),
                    xytext=(6, 0), textcoords="offset points",
                    ha='left', va='center', fontsize=10, fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[Saved] {output_path}")


def plot_training_time_comparison(training_times: dict, output_path: str = "training_time_comparison.png"):
    """Bar chart comparing actual wall-clock training time."""
    fig, ax = plt.subplots(figsize=(8, 5))
    models = list(training_times.keys())
    times = [training_times[m] for m in models]
    colors = [PALETTE[m] for m in models]

    bars = ax.bar(models, times, color=colors, width=0.55, edgecolor='#333333', linewidth=1.1)
    ax.set_title("Training Time Comparison (25 Epochs on Same CPU)", fontsize=13, fontweight='bold', pad=15)
    ax.set_ylabel("Wall-Clock Training Time (Seconds)", fontsize=11, fontweight='bold')
    ax.set_ylim(0, max(times) * 1.25)

    for bar in bars:
        h = bar.get_height()
        ax.annotate(f'{h:.2f}s', xy=(bar.get_x() + bar.get_width()/2, h),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=11, fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[Saved] {output_path}")


def plot_loss_curves(histories: dict, output_path: str = "loss_curves.png"):
    """2x2 grid of training vs validation loss curves."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 9), sharex=True)
    axes = axes.flatten()

    for idx, (m_name, hist) in enumerate(histories.items()):
        ax = axes[idx]
        epochs = hist["epochs"]
        color = PALETTE[m_name]
        ax.plot(epochs, hist["train_loss"], label="Train Loss", color=color, linewidth=2.0)
        ax.plot(epochs, hist["val_loss"], label="Val Loss", color=color, linestyle="--", linewidth=2.0)
        ax.set_title(f"{m_name} — Loss Dynamics", fontsize=11, fontweight='bold')
        ax.set_ylabel("Cross-Entropy Loss", fontsize=10)
        ax.set_xlabel("Epoch", fontsize=10)
        ax.legend(loc="upper right", frameon=True)
        ax.grid(True, linestyle=":", alpha=0.6)

    plt.suptitle("Training and Validation Loss Across 25 Epochs", fontsize=14, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[Saved] {output_path}")


def plot_accuracy_curves(histories: dict, output_path: str = "accuracy_curves.png"):
    """2x2 grid of training vs validation accuracy curves."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 9), sharex=True)
    axes = axes.flatten()

    for idx, (m_name, hist) in enumerate(histories.items()):
        ax = axes[idx]
        epochs = hist["epochs"]
        color = PALETTE[m_name]
        ax.plot(epochs, hist["train_acc"], label="Train Acc", color=color, linewidth=2.0)
        ax.plot(epochs, hist["val_acc"], label="Val Acc", color=color, linestyle="--", linewidth=2.0)
        ax.set_title(f"{m_name} — Accuracy Dynamics", fontsize=11, fontweight='bold')
        ax.set_ylabel("Accuracy (%)", fontsize=10)
        ax.set_xlabel("Epoch", fontsize=10)
        ax.set_ylim(0, 105)
        ax.legend(loc="lower right", frameon=True)
        ax.grid(True, linestyle=":", alpha=0.6)

    plt.suptitle("Training vs Validation Accuracy Across 25 Epochs", fontsize=14, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[Saved] {output_path}")


def plot_gradient_norm_analysis(histories: dict, output_path: str = "gradient_norm_analysis.png"):
    """
    Tracks recurrent gradient norms across epochs to visually expose
    vanishing vs stable gradient propagation behavior.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

    for m_name, hist in histories.items():
        epochs = hist["epochs"]
        color = PALETTE[m_name]
        ax1.plot(epochs, hist["grad_norm_mean"], label=m_name, color=color, linewidth=2.0, marker='o', markersize=4)
        ax2.plot(epochs, hist["grad_norm_max"], label=m_name, color=color, linewidth=1.8, linestyle="--")

    ax1.set_title("Mean Recurrent Gradient Norm per Epoch", fontsize=12, fontweight='bold')
    ax1.set_xlabel("Epoch", fontsize=10, fontweight='bold')
    ax1.set_ylabel("Gradient L2 Norm ||∇W||₂", fontsize=10, fontweight='bold')
    ax1.set_yscale("log")
    ax1.legend(loc="best", frameon=True)
    ax1.grid(True, linestyle=":", alpha=0.6)

    ax2.set_title("Peak Gradient Norm per Epoch (Explosion Detection)", fontsize=12, fontweight='bold')
    ax2.set_xlabel("Epoch", fontsize=10, fontweight='bold')
    ax2.set_ylabel("Max Step Gradient L2 Norm", fontsize=10, fontweight='bold')
    ax2.set_yscale("log")
    ax2.legend(loc="best", frameon=True)
    ax2.grid(True, linestyle=":", alpha=0.6)

    plt.suptitle("Vanishing & Exploding Gradient Dynamics Across Recurrent Architectures", fontsize=13, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[Saved] {output_path}")


def plot_confusion_matrices(results: dict, class_names: list = ["Horizontal (0°)", "Vertical (90°)", "Inverted (180°)"], output_path: str = "confusion_matrices.png"):
    """Plots confusion matrices side-by-side."""
    fig, axes = plt.subplots(1, 4, figsize=(18, 4.5))

    for idx, (m_name, res) in enumerate(results.items()):
        ax = axes[idx]
        cm = np.array(res["confusion_matrix"])
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False,
                    xticklabels=class_names, yticklabels=class_names, ax=ax)
        ax.set_title(f"{m_name}\nAcc: {res['accuracy']:.1f}% | F1: {res['f1_macro']:.1f}%", fontsize=11, fontweight='bold')
        ax.set_xlabel("Predicted Label", fontsize=9)
        if idx == 0:
            ax.set_ylabel("True Label", fontsize=9)
        else:
            ax.set_ylabel("")

    plt.suptitle("Test Set Confusion Matrices Across All Four Architectures", fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    safe_savefig(fig, output_path, dpi=300, bbox_inches='tight')


def generate_all_visualizations(histories: dict, eval_results: dict, param_counts: dict, training_times: dict):
    """Generates and saves all required plots."""
    print("\n" + "=" * 60)
    print("GENERATING EXPERIMENTAL VISUALIZATION CHARTS")
    print("=" * 60)
    plot_accuracy_comparison(eval_results)
    plot_f1_comparison(eval_results)
    plot_parameter_count_comparison(param_counts)
    plot_training_time_comparison(training_times)
    plot_loss_curves(histories)
    plot_accuracy_curves(histories)
    plot_gradient_norm_analysis(histories)
    plot_confusion_matrices(eval_results)
    print("All 8 visualization charts generated successfully!")
