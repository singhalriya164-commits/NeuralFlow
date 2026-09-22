"""
Training & Gradient Instrumentation Engine
===========================================
Performs controlled training for all recurrent models while logging:
1. Training Loss & Validation Loss
2. Training Accuracy & Validation Accuracy
3. Gradient Norms of recurrent weights (detecting vanishing/exploding gradients)
4. Precise Wall-Clock Training Duration (using time.perf_counter())
"""

import time
import copy
import torch
import torch.nn as nn
import numpy as np


def compute_gradient_norm(model) -> float:
    """
    Computes the L2 norm of the gradients across all recurrent layer weights.
    ||g||_2 = sqrt(sum(||g_i||_2^2))
    """
    recurrent_weights = model.get_recurrent_weights()
    total_norm_sq = 0.0
    for w in recurrent_weights:
        if w.grad is not None:
            param_norm = w.grad.detach().data.norm(2)
            total_norm_sq += param_norm.item() ** 2
    return total_norm_sq ** 0.5


def train_single_model(model_name: str,
                       model: nn.Module,
                       train_loader,
                       val_loader,
                       epochs: int = 25,
                       lr: float = 1e-3,
                       device: str = "cpu") -> dict:
    """
    Trains a model under strictly controlled conditions and tracks gradient dynamics.
    """
    print(f"\n---> Training {model_name} on {device} (Epochs: {epochs}, LR: {lr}) <---")
    model = model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    history = {
        "model_name": model_name,
        "epochs": [],
        "train_loss": [],
        "val_loss": [],
        "train_acc": [],
        "val_acc": [],
        "grad_norm_mean": [],
        "grad_norm_max": [],
        "grad_norm_min": [],
        "all_step_grad_norms": [],
        "training_time_seconds": 0.0,
        "vanishing_detected": False,
        "exploding_detected": False
    }

    best_val_acc = -1.0
    best_weights = None

    # Measure actual wall-clock training time
    start_time = time.perf_counter()

    for epoch in range(1, epochs + 1):
        model.train()
        running_loss = 0.0
        correct_train = 0
        total_train = 0
        epoch_step_grad_norms = []

        for batch_x, batch_y in train_loader:
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)

            optimizer.zero_grad()
            logits = model(batch_x)
            loss = criterion(logits, batch_y)
            loss.backward()

            # Measure gradient norm BEFORE optimizer step
            grad_norm = compute_gradient_norm(model)
            epoch_step_grad_norms.append(grad_norm)

            optimizer.step()

            running_loss += loss.item() * batch_x.size(0)
            preds = torch.argmax(logits, dim=1)
            correct_train += (preds == batch_y).sum().item()
            total_train += batch_y.size(0)

        epoch_train_loss = running_loss / total_train
        epoch_train_acc = (correct_train / total_train) * 100.0

        # Validation Phase
        model.eval()
        val_running_loss = 0.0
        correct_val = 0
        total_val = 0

        with torch.no_grad():
            for val_x, val_y in val_loader:
                val_x, val_y = val_x.to(device), val_y.to(device)
                val_logits = model(val_x)
                v_loss = criterion(val_logits, val_y)

                val_running_loss += v_loss.item() * val_x.size(0)
                v_preds = torch.argmax(val_logits, dim=1)
                correct_val += (v_preds == val_y).sum().item()
                total_val += val_y.size(0)

        epoch_val_loss = val_running_loss / total_val
        epoch_val_acc = (correct_val / total_val) * 100.0

        # Gradient norm statistics for the epoch
        mean_g = float(np.mean(epoch_step_grad_norms)) if epoch_step_grad_norms else 0.0
        max_g = float(np.max(epoch_step_grad_norms)) if epoch_step_grad_norms else 0.0
        min_g = float(np.min(epoch_step_grad_norms)) if epoch_step_grad_norms else 0.0

        history["epochs"].append(epoch)
        history["train_loss"].append(epoch_train_loss)
        history["val_loss"].append(epoch_val_loss)
        history["train_acc"].append(epoch_train_acc)
        history["val_acc"].append(epoch_val_acc)
        history["grad_norm_mean"].append(mean_g)
        history["grad_norm_max"].append(max_g)
        history["grad_norm_min"].append(min_g)
        history["all_step_grad_norms"].extend(epoch_step_grad_norms)

        if epoch_val_acc > best_val_acc:
            best_val_acc = epoch_val_acc
            best_weights = copy.deepcopy(model.state_dict())

        if epoch % 5 == 0 or epoch == 1 or epoch == epochs:
            print(f"[{model_name}] Epoch {epoch:2d}/{epochs} | "
                  f"Train Loss: {epoch_train_loss:.4f} | Train Acc: {epoch_train_acc:5.1f}% | "
                  f"Val Loss: {epoch_val_loss:.4f} | Val Acc: {epoch_val_acc:5.1f}% | "
                  f"Grad Norm (mean): {mean_g:.4e}")

    end_time = time.perf_counter()
    duration = end_time - start_time
    history["training_time_seconds"] = duration

    # Check for Vanishing or Exploding Gradients
    overall_mean_grad = float(np.mean(history["grad_norm_mean"]))
    overall_max_grad = float(np.max(history["grad_norm_max"]))

    if overall_mean_grad < 1e-4:
        history["vanishing_detected"] = True
    if overall_max_grad > 50.0:
        history["exploding_detected"] = True

    # Restore best weights
    if best_weights is not None:
        model.load_state_dict(best_weights)

    print(f"Finished {model_name}: {duration:.2f}s | Best Val Acc: {best_val_acc:.1f}%")
    return history, model


if __name__ == "__main__":
    print("=" * 70)
    print("Direct execution of train.py detected.")
    print("Delegating to run_experiment.py for complete comparative benchmark...")
    print("=" * 70)
    import run_experiment
    run_experiment.main()
