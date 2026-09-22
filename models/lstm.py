"""
Long Short-Term Memory (LSTM) Architecture
==========================================
Maintains internal cell state c_t and hidden state h_t with 3 gates:
- Forget Gate: f_t = sigmoid(W_f [h_{t-1}, x_t] + b_f)
- Input Gate:  i_t = sigmoid(W_i [h_{t-1}, x_t] + b_i)
- Output Gate: o_t = sigmoid(W_o [h_{t-1}, x_t] + b_o)
- Cell State:  c_t = f_t * c_{t-1} + i_t * tanh(W_c [h_{t-1}, x_t] + b_c)
- Hidden:      h_t = o_t * tanh(c_t)
"""

import torch
import torch.nn as nn


class LSTMModel(nn.Module):
    def __init__(self, input_dim: int = 32, hidden_dim: int = 64, num_classes: int = 3):
        super().__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.recurrent = nn.LSTM(
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
        _, (h_n, _) = self.recurrent(x)
        last_hidden = h_n[-1, :, :]
        return self.classifier(last_hidden)

    def get_recurrent_weights(self):
        return [self.recurrent.weight_hh_l0, self.recurrent.weight_ih_l0]
