"""
Image-to-Sequence Extraction Pipeline
======================================
Converts raw 2D geological photographs into reproducible 1D temporal/spatial
feature sequences without data leakage across image boundaries.
"""

import os
import numpy as np
from PIL import Image
import torch
from torch.utils.data import Dataset, DataLoader

ALL_IMAGE_FILES = sorted([
    "WhatsApp Image 2026-07-31 at 11.52.51 AM (1).jpeg",
    "WhatsApp Image 2026-07-31 at 11.52.51 AM.jpeg",
    "WhatsApp Image 2026-07-31 at 11.52.52 AM (1).jpeg",
    "WhatsApp Image 2026-07-31 at 11.52.52 AM.jpeg",
    "WhatsApp Image 2026-07-31 at 11.52.53 AM (1).jpeg",
    "WhatsApp Image 2026-07-31 at 11.52.53 AM.jpeg",
    "WhatsApp Image 2026-07-31 at 11.52.54 AM (1).jpeg",
    "WhatsApp Image 2026-07-31 at 11.52.54 AM (2).jpeg",
    "WhatsApp Image 2026-07-31 at 11.52.54 AM.jpeg",
    "WhatsApp Image 2026-07-31 at 11.52.55 AM (1).jpeg",
    "WhatsApp Image 2026-07-31 at 11.52.55 AM.jpeg"
])

TRAIN_IMAGES = ALL_IMAGE_FILES[0:7]    # 7 images (~63.6%)
VAL_IMAGES   = ALL_IMAGE_FILES[7:9]    # 2 images (~18.2%)
TEST_IMAGES  = ALL_IMAGE_FILES[9:11]   # 2 images (~18.2%)


def load_and_preprocess_image(image_path: str) -> np.ndarray:
    """
    Loads raw JPEG image, converts to 8-bit Grayscale,
    and normalizes pixel values to [0.0, 1.0].
    """
    img = Image.open(image_path).convert('L')
    arr = np.array(img, dtype=np.float32) / 255.0
    return arr


def extract_sequences_from_image(image_arr: np.ndarray, 
                                 crops_per_image: int = 100, 
                                 seq_len: int = 32, 
                                 feat_dim: int = 32, 
                                 seed: int = 42) -> tuple:
    """
    Extracts balanced sequence samples across 3 classes:
      - Class 0: Horizontal Spatial Trajectory Scan (0 degrees)
      - Class 1: Vertical Spatial Trajectory Scan (90 degrees)
      - Class 2: Inverted Temporal Scan (180 degrees)
    """
    rng = np.random.RandomState(seed)
    H, W = image_arr.shape
    sequences = []
    labels = []

    for _ in range(crops_per_image):
        top = rng.randint(0, H - seq_len)
        left = rng.randint(0, W - feat_dim)
        patch = image_arr[top:top + seq_len, left:left + feat_dim]

        # Class 0: Horizontal scan (shape: 32 x 32)
        sequences.append(patch.copy())
        labels.append(0)

        # Class 1: Vertical scan (transposed patch: 32 x 32)
        sequences.append(patch.T.copy())
        labels.append(1)

        # Class 2: Inverted temporal scan (rows reversed)
        sequences.append(patch[::-1, :].copy())
        labels.append(2)

    return np.array(sequences, dtype=np.float32), np.array(labels, dtype=np.int64)


class GeologicalSequenceDataset(Dataset):
    """PyTorch Dataset for image-derived sequences."""
    def __init__(self, sequences: np.ndarray, labels: np.ndarray):
        self.sequences = torch.tensor(sequences, dtype=torch.float32)
        self.labels = torch.tensor(labels, dtype=torch.long)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return self.sequences[idx], self.labels[idx]


def resolve_image_path(filename: str, base_dir: str = ".") -> str:
    """Checks data/images first, then base_dir."""
    candidate1 = os.path.join(base_dir, "data", "images", filename)
    if os.path.exists(candidate1):
        return candidate1
    candidate2 = os.path.join(base_dir, filename)
    if os.path.exists(candidate2):
        return candidate2
    return candidate1


def build_datasets(data_dir: str = ".", seed: int = 42):
    """Builds Train, Validation, and Test Datasets with image-level isolation."""
    # 1. Train sequences (7 images)
    train_seqs, train_lbls = [], []
    for idx, fname in enumerate(TRAIN_IMAGES):
        path = resolve_image_path(fname, data_dir)
        img_arr = load_and_preprocess_image(path)
        s, l = extract_sequences_from_image(img_arr, crops_per_image=100, seed=seed + idx)
        train_seqs.append(s)
        train_lbls.append(l)
    X_train = np.concatenate(train_seqs, axis=0)
    y_train = np.concatenate(train_lbls, axis=0)

    # 2. Validation sequences (2 images)
    val_seqs, val_lbls = [], []
    for idx, fname in enumerate(VAL_IMAGES):
        path = resolve_image_path(fname, data_dir)
        img_arr = load_and_preprocess_image(path)
        s, l = extract_sequences_from_image(img_arr, crops_per_image=80, seed=seed + 100 + idx)
        val_seqs.append(s)
        val_lbls.append(l)
    X_val = np.concatenate(val_seqs, axis=0)
    y_val = np.concatenate(val_lbls, axis=0)

    # 3. Test sequences (2 images)
    test_seqs, test_lbls = [], []
    for idx, fname in enumerate(TEST_IMAGES):
        path = resolve_image_path(fname, data_dir)
        img_arr = load_and_preprocess_image(path)
        s, l = extract_sequences_from_image(img_arr, crops_per_image=80, seed=seed + 200 + idx)
        test_seqs.append(s)
        test_lbls.append(l)
    X_test = np.concatenate(test_seqs, axis=0)
    y_test = np.concatenate(test_lbls, axis=0)

    return (GeologicalSequenceDataset(X_train, y_train),
            GeologicalSequenceDataset(X_val, y_val),
            GeologicalSequenceDataset(X_test, y_test))


def get_dataloaders(data_dir: str = ".", batch_size: int = 32, seed: int = 42):
    """Returns PyTorch DataLoaders."""
    torch.manual_seed(seed)
    train_ds, val_ds, test_ds = build_datasets(data_dir=data_dir, seed=seed)
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    val_loader   = DataLoader(val_ds, batch_size=batch_size, shuffle=False)
    test_loader  = DataLoader(test_ds, batch_size=batch_size, shuffle=False)
    return train_loader, val_loader, test_loader
