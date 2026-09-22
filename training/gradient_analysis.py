"""
Gradient Analysis Module
========================
Provides gradient norm tracking, vanishing gradient detection, and
exploding gradient detection across recurrent weight layers.
"""

import numpy as np
import torch


def compute_recurrent_grad_norm(model) -> float:
    """Computes the L2 norm across all recurrent weight gradient tensors."""
    recurrent_weights = model.get_recurrent_weights()
    total_norm_sq = 0.0
    for w in recurrent_weights:
        if w.grad is not None:
            param_norm = w.grad.detach().data.norm(2)
            total_norm_sq += param_norm.item() ** 2
    return total_norm_sq ** 0.5


def analyze_gradient_dynamics(history: dict) -> dict:
    """
    Analyzes logged gradient statistics to classify behavior into:
    - Vanishing gradient tendency (< 1e-3)
    - Stable gradient flow
    - Exploding gradient tendency (> 50.0)
    """
    mean_g = float(np.mean(history["grad_norm_mean"]))
    max_g = float(np.max(history["grad_norm_max"]))
    min_g = float(np.min(history["grad_norm_min"]))
    variance_g = float(np.var(history["grad_norm_mean"]))

    vanishing = mean_g < 1e-3 or min_g < 1e-4
    exploding = max_g > 50.0

    if vanishing:
        status = "Vanishing tendency detected"
    elif exploding:
        status = "Exploding gradient detected"
    else:
        status = "Stable gradient flow"

    return {
        "mean_grad_norm": mean_g,
        "max_grad_norm": max_g,
        "min_grad_norm": min_g,
        "variance_grad_norm": variance_g,
        "vanishing_detected": vanishing,
        "exploding_detected": exploding,
        "classification": status
    }
