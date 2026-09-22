"""
Recurrent Neural Network Architectures
======================================
Architectures for controlled comparative study:
1. Vanilla RNN (Standard Elman RNN with tanh)
2. Bidirectional RNN (Forward + Backward temporal passes)
3. Long Short-Term Memory (LSTM with Cell State, Input, Forget, Output gates)
4. Gated Recurrent Unit (GRU with Reset and Update gates)

All models share:
- Identical input dimension: 32
- Identical sequence length: 32
- Identical recurrent representation dimension: 64
- Identical classification head: Linear(64, 32) -> ReLU -> Dropout(0.2) -> Linear(32, 3)
- Identical weight initialization seed
"""

import torch
import torch.nn as nn


class VanillaRNNModel(nn.Module):
    """
    Standard Unidirectional Elman RNN:
    h_t = tanh(W_ih * x_t + b_ih + W_hh * h_{t-1} + b_hh)
    """
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
        # x shape: (B, T=32, D=32)
        out, h_n = self.recurrent(x)
        # out[:, -1, :] is the hidden state at the last timestep T
        last_hidden = out[:, -1, :]
        logits = self.classifier(last_hidden)
        return logits

    def get_recurrent_weights(self):
        """Returns recurrent weight tensors for gradient norm tracking."""
        return [self.recurrent.weight_hh_l0, self.recurrent.weight_ih_l0]


class BiRNNModel(nn.Module):
    """
    Bidirectional RNN:
    Computes forward hidden sequence (h_fwd) and backward hidden sequence (h_bwd).
    To maintain fair 64-dim representation entering the classifier, hidden_dim=32 per direction.
    Concatenated representation: 32 + 32 = 64.
    """
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
        # Combined forward + backward representation = hidden_dim * 2 = 64
        self.classifier = nn.Sequential(
            nn.Linear(hidden_dim * 2, 32),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(32, num_classes)
        )

    def forward(self, x):
        out, h_n = self.recurrent(x)
        # out[:, -1, :hidden_dim] is forward last state; out[:, 0, hidden_dim:] is backward last state
        # In PyTorch, h_n has shape (num_directions, B, hidden_dim).
        # We concatenate forward and backward final hidden states:
        fwd_final = h_n[0, :, :]
        bwd_final = h_n[1, :, :]
        combined = torch.cat([fwd_final, bwd_final], dim=1)
        logits = self.classifier(combined)
        return logits

    def get_recurrent_weights(self):
        return [
            self.recurrent.weight_hh_l0, self.recurrent.weight_ih_l0,
            self.recurrent.weight_hh_l0_reverse, self.recurrent.weight_ih_l0_reverse
        ]


class LSTMModel(nn.Module):
    """
    Long Short-Term Memory (LSTM) with additive Cell State (c_t) and 
    three multiplicative gates:
      - Forget Gate: f_t = sigmoid(W_f * [h_{t-1}, x_t] + b_f)
      - Input Gate:  i_t = sigmoid(W_i * [h_{t-1}, x_t] + b_i)
      - Output Gate: o_t = sigmoid(W_o * [h_{t-1}, x_t] + b_o)
      - Cell State:  c_t = f_t * c_{t-1} + i_t * tanh(W_c * [h_{t-1}, x_t] + b_c)
      - Hidden State: h_t = o_t * tanh(c_t)
    """
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
        out, (h_n, c_n) = self.recurrent(x)
        last_hidden = h_n[-1, :, :]
        logits = self.classifier(last_hidden)
        return logits

    def get_recurrent_weights(self):
        return [self.recurrent.weight_hh_l0, self.recurrent.weight_ih_l0]


class GRUModel(nn.Module):
    """
    Gated Recurrent Unit (GRU):
    Combines cell state and hidden state, using two multiplicative gates:
      - Reset Gate:  r_t = sigmoid(W_r * [h_{t-1}, x_t] + b_r)
      - Update Gate: z_t = sigmoid(W_z * [h_{t-1}, x_t] + b_z)
      - Candidate:   n_t = tanh(W_n * [r_t * h_{t-1}, x_t] + b_n)
      - Hidden State: h_t = (1 - z_t) * n_t + z_t * h_{t-1}
    """
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
        out, h_n = self.recurrent(x)
        last_hidden = h_n[-1, :, :]
        logits = self.classifier(last_hidden)
        return logits

    def get_recurrent_weights(self):
        return [self.recurrent.weight_hh_l0, self.recurrent.weight_ih_l0]


def count_parameters(model: nn.Module) -> dict:
    """
    Counts total, recurrent, and classifier trainable parameters.
    """
    total = sum(p.numel() for p in model.parameters() if p.requires_grad)
    recurrent = sum(p.numel() for p in model.recurrent.parameters() if p.requires_grad)
    classifier = sum(p.numel() for p in model.classifier.parameters() if p.requires_grad)
    return {
        "total_parameters": total,
        "recurrent_parameters": recurrent,
        "classifier_parameters": classifier
    }
