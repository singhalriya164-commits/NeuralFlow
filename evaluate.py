"""
Evaluation Module
=================
Evaluates all models on the UNSEEN test set (images 10 and 11).
Computes:
- Test Accuracy
- Precision (Macro & Weighted)
- Recall (Macro & Weighted)
- F1-Score (Macro & Weighted)
- Confusion Matrix
"""

import torch
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
)


def evaluate_model_on_test(model_name: str, model, test_loader, device: str = "cpu") -> dict:
    """
    Evaluates a trained model on the identical test set.
    """
    model.eval()
    all_preds = []
    all_targets = []

    with torch.no_grad():
        for batch_x, batch_y in test_loader:
            batch_x = batch_x.to(device)
            logits = model(batch_x)
            preds = torch.argmax(logits, dim=1).cpu().numpy()
            targets = batch_y.cpu().numpy()

            all_preds.extend(preds)
            all_targets.extend(targets)

    all_preds = np.array(all_preds)
    all_targets = np.array(all_targets)

    acc = accuracy_score(all_targets, all_preds) * 100.0
    macro_prec = precision_score(all_targets, all_preds, average="macro", zero_division=0) * 100.0
    macro_rec = recall_score(all_targets, all_preds, average="macro", zero_division=0) * 100.0
    macro_f1 = f1_score(all_targets, all_preds, average="macro", zero_division=0) * 100.0

    weighted_f1 = f1_score(all_targets, all_preds, average="weighted", zero_division=0) * 100.0
    cm = confusion_matrix(all_targets, all_preds)

    print(f"\n--- Evaluation Results: {model_name} ---")
    print(f"Test Accuracy:     {acc:.2f}%")
    print(f"Macro Precision:   {macro_prec:.2f}%")
    print(f"Macro Recall:      {macro_rec:.2f}%")
    print(f"Macro F1-Score:    {macro_f1:.2f}%")
    print(f"Weighted F1-Score: {weighted_f1:.2f}%")
    print(f"Confusion Matrix:\n{cm}")

    return {
        "model_name": model_name,
        "accuracy": acc,
        "precision_macro": macro_prec,
        "recall_macro": macro_rec,
        "f1_macro": macro_f1,
        "f1_weighted": weighted_f1,
        "confusion_matrix": cm.tolist()
    }
