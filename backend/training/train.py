"""
Training Module
===============
Controlled training engine tracking wall-clock training time, epoch-wise loss,
accuracy, and recurrent gradient norms.
"""

import time
import copy
import numpy as np
import torch
import torch.nn as nn
from .gradient_analysis import compute_recurrent_grad_norm


def train_model(model_name: str,
                model: nn.Module,
                train_loader,
                val_loader,
                epochs: int = 25,
                lr: float = 1e-3,
                device: str = "cpu") -> tuple:
    """Trains a model with controlled optimizer, loss, and gradient instrumentation."""
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
        "training_time_seconds": 0.0
    }

    best_val_acc = -1.0
    best_weights = None

    start_time = time.perf_counter()

    for epoch in range(1, epochs + 1):
        model.train()
        running_loss = 0.0
        correct_train = 0
        total_train = 0
        step_grads = []

        for batch_x, batch_y in train_loader:
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)

            optimizer.zero_grad()
            logits = model(batch_x)
            loss = criterion(logits, batch_y)
            loss.backward()

            g_norm = compute_recurrent_grad_norm(model)
            step_grads.append(g_norm)

            optimizer.step()

            running_loss += loss.item() * batch_x.size(0)
            preds = torch.argmax(logits, dim=1)
            correct_train += (preds == batch_y).sum().item()
            total_train += batch_y.size(0)

        epoch_train_loss = running_loss / total_train
        epoch_train_acc = (correct_train / total_train) * 100.0

        # Validation
        model.eval()
        val_loss = 0.0
        correct_val = 0
        total_val = 0

        with torch.no_grad():
            for val_x, val_y in val_loader:
                val_x, val_y = val_x.to(device), val_y.to(device)
                val_logits = model(val_x)
                v_loss = criterion(val_logits, val_y)
                val_loss += v_loss.item() * val_x.size(0)
                v_preds = torch.argmax(val_logits, dim=1)
                correct_val += (v_preds == val_y).sum().item()
                total_val += val_y.size(0)

        epoch_val_loss = val_loss / total_val
        epoch_val_acc = (correct_val / total_val) * 100.0

        mean_g = float(np.mean(step_grads)) if step_grads else 0.0
        max_g = float(np.max(step_grads)) if step_grads else 0.0
        min_g = float(np.min(step_grads)) if step_grads else 0.0

        history["epochs"].append(epoch)
        history["train_loss"].append(epoch_train_loss)
        history["val_loss"].append(epoch_val_loss)
        history["train_acc"].append(epoch_train_acc)
        history["val_acc"].append(epoch_val_acc)
        history["grad_norm_mean"].append(mean_g)
        history["grad_norm_max"].append(max_g)
        history["grad_norm_min"].append(min_g)

        if epoch_val_acc > best_val_acc:
            best_val_acc = epoch_val_acc
            best_weights = copy.deepcopy(model.state_dict())

    duration = time.perf_counter() - start_time
    history["training_time_seconds"] = duration

    if best_weights is not None:
        model.load_state_dict(best_weights)

    return history, model
