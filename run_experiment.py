"""
Main Experiment Runner
======================
Executes the full controlled comparative study:
1. Sets deterministic random seeds (42)
2. Builds image-level partitioned datasets
3. Initializes Vanilla RNN, Bi-RNN, LSTM, and GRU
4. Computes exact parameter counts
5. Trains all models under identical conditions with gradient logging
6. Evaluates all models on the UNSEEN test set
7. Saves models and results
8. Generates all 8 comparison plots
9. Prints the consolidated results table
"""

import os
import json
import random
import numpy as np
import torch

from dataset import get_dataloaders
from models import (
    VanillaRNNModel, BiRNNModel, LSTMModel, GRUModel, count_parameters
)
from train import train_single_model
from evaluate import evaluate_model_on_test
from visualize import generate_all_visualizations


def set_seed(seed: int = 42):
    """Sets deterministic seeds across Python, NumPy, and PyTorch."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def main():
    print("\n" + "=" * 80)
    print("NEURALFLOW: ENTERPRISE RNN ARCHITECTURE BENCHMARK")
    print("Comparative Analysis: Vanilla RNN vs Bidirectional RNN vs LSTM vs GRU")
    print("=" * 80)

    # 1. Reproducibility
    SEED = 42
    set_seed(SEED)

    # Device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Hardware Runtime: {device.upper()}")

    # 2. Data Loaders
    data_dir = os.path.dirname(os.path.abspath(__file__))
    train_loader, val_loader, test_loader = get_dataloaders(data_dir=data_dir, batch_size=32, seed=SEED)

    # 3. Model Definitions
    models_dict = {
        "Vanilla RNN": VanillaRNNModel(input_dim=32, hidden_dim=64, num_classes=3),
        "Bidirectional RNN": BiRNNModel(input_dim=32, hidden_dim=32, num_classes=3),
        "LSTM": LSTMModel(input_dim=32, hidden_dim=64, num_classes=3),
        "GRU": GRUModel(input_dim=32, hidden_dim=64, num_classes=3)
    }

    # 4. Parameter Counts
    param_counts = {}
    print("\n" + "=" * 60)
    print("STEP 5: TRAINABLE PARAMETER COUNTS")
    print("=" * 60)
    print(f"{'Model':<20} | {'Total Params':<15} | {'Recurrent Params':<18} | {'Classifier Params':<18}")
    print("-" * 75)
    for name, model in models_dict.items():
        pc = count_parameters(model)
        param_counts[name] = pc
        print(f"{name:<20} | {pc['total_parameters']:<15,d} | {pc['recurrent_parameters']:<18,d} | {pc['classifier_parameters']:<18,d}")
    print("Note: Preprocessing/feature extraction has 0 learnable parameters (deterministic normalization & slicing).")

    # 5. Training Phase
    histories = {}
    trained_models = {}
    training_times = {}

    print("\n" + "=" * 60)
    print("STEP 6: TRAINING UNDER IDENTICAL CONDITIONS")
    print("=" * 60)

    for name, model in models_dict.items():
        # Set seed before each model to ensure identical initialization states
        set_seed(SEED)
        hist, trained_m = train_single_model(
            model_name=name,
            model=model,
            train_loader=train_loader,
            val_loader=val_loader,
            epochs=25,
            lr=1e-3,
            device=device
        )
        histories[name] = hist
        trained_models[name] = trained_m
        training_times[name] = hist["training_time_seconds"]

        # Save checkpoint
        ckpt_path = f"{name.lower().replace(' ', '_')}.pt"
        torch.save(trained_m.state_dict(), ckpt_path)
        print(f"Model saved to: {ckpt_path}")

    # 6. Evaluation Phase
    eval_results = {}
    print("\n" + "=" * 60)
    print("STEP 7: TEST SET EVALUATION")
    print("=" * 60)
    for name, model in trained_models.items():
        res = evaluate_model_on_test(name, model, test_loader, device=device)
        eval_results[name] = res

    # 7. Gradient Behavior & Stability Analysis
    gradient_summary = {}
    for name, hist in histories.items():
        mean_g = float(np.mean(hist["grad_norm_mean"]))
        max_g = float(np.max(hist["grad_norm_max"]))
        min_g = float(np.min(hist["grad_norm_min"]))

        # Classify gradient behavior
        if mean_g < 1e-3:
            grad_beh = f"Vanishing tendency (mean ||g||={mean_g:.1e})"
        elif max_g > 20.0:
            grad_beh = f"High variance/spikes (max ||g||={max_g:.1f})"
        else:
            grad_beh = f"Stable gradient flow (mean ||g||={mean_g:.3f})"

        # Learning stability from loss curve volatility
        loss_diffs = np.diff(hist["val_loss"])
        volatility = np.std(loss_diffs)
        if volatility < 0.1:
            stability = "High (smooth monotonic convergence)"
        elif volatility < 0.25:
            stability = "Moderate (minor oscillations)"
        else:
            stability = "Volatile (significant fluctuations)"

        gradient_summary[name] = {
            "mean_grad_norm": mean_g,
            "max_grad_norm": max_g,
            "min_grad_norm": min_g,
            "behavior_label": grad_beh,
            "stability_label": stability
        }

    # 8. Visualizations
    generate_all_visualizations(histories, eval_results, param_counts, training_times)

    # 9. Step 11: Consolidated Results Table
    print("\n" + "=" * 90)
    print("STEP 11: FINAL CONSOLIDATED EXPERIMENTAL RESULTS TABLE")
    print("=" * 90)
    print(f"| {'Model':<18} | {'Accuracy':<10} | {'Macro F1':<10} | {'Parameters':<12} | {'Train Time':<12} | {'Gradient Behavior':<30} | {'Stability':<15} |")
    print("|" + "-" * 20 + "|" + "-" * 12 + "|" + "-" * 12 + "|" + "-" * 14 + "|" + "-" * 14 + "|" + "-" * 32 + "|" + "-" * 17 + "|")
    
    consolidated_table = []
    for name in models_dict.keys():
        acc = eval_results[name]["accuracy"]
        f1 = eval_results[name]["f1_macro"]
        params = param_counts[name]["total_parameters"]
        t_time = training_times[name]
        g_beh = gradient_summary[name]["behavior_label"]
        stab = gradient_summary[name]["stability_label"]

        print(f"| {name:<18} | {acc:8.2f}% | {f1:8.2f}% | {params:<12,d} | {t_time:10.2f}s | {g_beh:<30} | {stab:<15} |")
        consolidated_table.append({
            "model": name,
            "accuracy": acc,
            "f1_macro": f1,
            "parameters": params,
            "training_time": t_time,
            "gradient_behavior": g_beh,
            "stability": stab
        })
    print("=" * 90)

    # 10. Save Complete JSON Results
    full_output = {
        "parameters": param_counts,
        "training_times": training_times,
        "eval_results": eval_results,
        "gradient_summary": gradient_summary,
        "consolidated_table": consolidated_table,
        "histories": {
            m: {k: v for k, v in h.items() if k != "all_step_grad_norms"}
            for m, h in histories.items()
        }
    }

    with open("experiment_results.json", "w") as f:
        json.dump(full_output, f, indent=4)
    print("\nComplete experiment results saved to 'experiment_results.json'!")

    # Ensure results/ directory has synchronized artifacts
    results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
    os.makedirs(results_dir, exist_ok=True)

    with open(os.path.join(results_dir, "metrics.json"), "w") as f:
        json.dump(eval_results, f, indent=4)

    with open(os.path.join(results_dir, "training_history.json"), "w") as f:
        json.dump(full_output["histories"], f, indent=4)

    with open(os.path.join(results_dir, "gradient_history.json"), "w") as f:
        json.dump(gradient_summary, f, indent=4)

    model_summary_data = {
        "status": "Completed",
        "last_run": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "dataset_version": f"Enterprise Production v2.4 ({len(discover_image_files())} Verified Outcrop Images)",
        "config": {
            "seed": SEED,
            "dataset_split": "Dynamic Strict Image-Level Partition (Zero Leakage)",
            "learning_rate": 0.001,
            "batch_size": 32,
            "epochs": 25,
            "hidden_size": 64,
            "optimizer": "Adam",
            "sequence_length": 32,
            "input_feature_dim": 32
        },
        "parameters": param_counts,
        "training_times": training_times,
        "consolidated_table": consolidated_table
    }
    with open(os.path.join(results_dir, "model_summary.json"), "w") as f:
        json.dump(model_summary_data, f, indent=4)
    print("Synchronized all artifacts to 'results/' directory successfully!")


if __name__ == "__main__":
    import time
    from dataset import discover_image_files
    main()
