"""
Vanilla RNN Architecture
========================
Standard Unidirectional Elman RNN:
h_t = tanh(W_ih * x_t + b_ih + W_hh * h_{t-1} + b_hh)
"""

import torch
import torch.nn as nn


class VanillaRNNModel(nn.Module):
    def __init__(self, input_dim: int = 32, hidden_dim: int = 64, num_classes: int = 3):
        super().__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.recurrent = nn.RNN(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=1,
            batch_first=True,
            nonlinearity='tanh'
        )
        self.classifier = nn.Sequential(
            nn.Linear(hidden_dim, 32),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(32, num_classes)
        )

    def forward(self, x):
        out, _ = self.recurrent(x)
        last_hidden = out[:, -1, :]
        return self.classifier(last_hidden)

    def get_recurrent_weights(self):
        return [self.recurrent.weight_hh_l0, self.recurrent.weight_ih_l0]
