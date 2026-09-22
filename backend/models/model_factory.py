"""
Model Factory & Parameter Counting
==================================
Provides parameter calculation utilities and registry of all four architectures.
"""

import torch.nn as nn
from .vanilla_rnn import VanillaRNNModel
from .bidirectional_rnn import BiRNNModel
from .lstm import LSTMModel
from .gru import GRUModel


def count_parameters(model: nn.Module) -> dict:
    """Calculates total, recurrent, and classifier trainable parameters."""
    total = sum(p.numel() for p in model.parameters() if p.requires_grad)
    recurrent = sum(p.numel() for p in model.recurrent.parameters() if p.requires_grad)
    classifier = sum(p.numel() for p in model.classifier.parameters() if p.requires_grad)
    return {
        "total_parameters": total,
        "recurrent_parameters": recurrent,
        "classifier_parameters": classifier
    }


def get_all_models(input_dim: int = 32, num_classes: int = 3) -> dict:
    """Instantiates all 4 models with standard controlled hidden sizes."""
    return {
        "Vanilla RNN": VanillaRNNModel(input_dim=input_dim, hidden_dim=64, num_classes=num_classes),
        "Bidirectional RNN": BiRNNModel(input_dim=input_dim, hidden_dim=32, num_classes=num_classes),
        "LSTM": LSTMModel(input_dim=input_dim, hidden_dim=64, num_classes=num_classes),
        "GRU": GRUModel(input_dim=input_dim, hidden_dim=64, num_classes=num_classes)
    }
