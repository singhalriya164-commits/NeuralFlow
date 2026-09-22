"""
Bidirectional RNN Architecture
==============================
Computes forward hidden sequence (h_fwd) and backward hidden sequence (h_bwd).
Hidden dimension = 32 per direction to maintain fair 64-dim representation
entering the classifier.
"""

import torch
import torch.nn as nn


class BiRNNModel(nn.Module):
    def __init__(self, input_dim: int = 32, hidden_dim: int = 32, num_classes: int = 3):
        super().__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.recurrent = nn.RNN(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=1,
            batch_first=True,
            bidirectional=True,
            nonlinearity='tanh'
        )
        self.classifier = nn.Sequential(
            nn.Linear(hidden_dim * 2, 32),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(32, num_classes)
        )

    def forward(self, x):
        out, h_n = self.recurrent(x)
        fwd_final = h_n[0, :, :]
        bwd_final = h_n[1, :, :]
        combined = torch.cat([fwd_final, bwd_final], dim=1)
        return self.classifier(combined)

    def get_recurrent_weights(self):
        return [
            self.recurrent.weight_hh_l0, self.recurrent.weight_ih_l0,
            self.recurrent.weight_hh_l0_reverse, self.recurrent.weight_ih_l0_reverse
        ]
