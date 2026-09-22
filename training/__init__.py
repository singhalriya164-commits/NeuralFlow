"""
Training Package
================
Exposes train_model, evaluate_model, compute_recurrent_grad_norm, and analyze_gradient_dynamics.
"""

from .train import train_model
from .evaluate import evaluate_model
from .gradient_analysis import compute_recurrent_grad_norm, analyze_gradient_dynamics

__all__ = [
    "train_model",
    "evaluate_model",
    "compute_recurrent_grad_norm",
    "analyze_gradient_dynamics"
]
