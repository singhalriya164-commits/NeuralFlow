"""
Gated Recurrent Unit (GRU) Architecture
=======================================
Gated recurrent architecture with 2 gates:
- Reset Gate:  r_t = sigmoid(W_r [h_{t-1}, x_t] + b_r)
- Update Gate: z_t = sigmoid(W_z [h_{t-1}, x_t] + b_z)
- Candidate:   n_t = tanh(W_in x_t + b_in + r_t * (W_hn h_{t-1} + b_hn))
- Hidden:      h_t = (1 - z_t) * n_t + z_t * h_{t-1}
"""

import torch
import torch.nn as nn


class GRUModel(nn.Module):
    def __init__(self, input_dim: int = 32, hidden_dim: int = 64, num_classes: int = 3):
        super().__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.recurrent = nn.GRU(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=1,
            batch_first=True
        )
        self.classifier = nn.Sequential(
            nn.Linear(hidden_dim, 32),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(32, num_classes)
        )

    def forward(self, x):
        _, h_n = self.recurrent(x)
        last_hidden = h_n[-1, :, :]
        return self.classifier(last_hidden)

    def get_recurrent_weights(self):
        return [self.recurrent.weight_hh_l0, self.recurrent.weight_ih_l0]
