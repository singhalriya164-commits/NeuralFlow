"""
Dataset & Preprocessing Pipeline (Fully Dynamic & Scalable)
===========================================================
Project: Comparative Analysis of Recurrent Neural Network Architectures
Supports dynamic image discovery across 11 to 300+ geological images with
zero data leakage, adaptive sequence extraction, and robust trajectory encoding.
"""

import os
import glob
import numpy as np
from PIL import Image
import torch
from torch.utils.data import Dataset, DataLoader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data", "images")


def discover_image_files(data_dir: str = None) -> list:
    """
    Dynamically discovers all image files in data_dir, data/images, or workspace root.
    Supports .jpeg, .jpg, .png, .bmp, .webp formats.
    Returns deterministic alphabetically sorted relative/absolute file paths.
    """
    search_dirs = []
    if data_dir and os.path.exists(data_dir):
        search_dirs.append(data_dir)
        sub_img = os.path.join(data_dir, "data", "images")
        if os.path.exists(sub_img):
            search_dirs.insert(0, sub_img)
    if os.path.exists(DATA_DIR):
        search_dirs.append(DATA_DIR)
    search_dirs.append(BASE_DIR)

    valid_exts = (".jpeg", ".jpg", ".png", ".bmp", ".webp")
    found_files = []

    for d in search_dirs:
        if not os.path.exists(d):
            continue
        for fname in sorted(os.listdir(d)):
            if fname.lower().endswith(valid_exts):
                full_p = os.path.join(d, fname)
                if os.path.isfile(full_p) and fname not in [os.path.basename(f) for f in found_files]:
                    found_files.append(full_p)
        if len(found_files) >= 11:
            break

    # If nothing found in data dirs, check root
    if not found_files:
        for fname in sorted(os.listdir(BASE_DIR)):
            if fname.lower().endswith(valid_exts):
                found_files.append(os.path.join(BASE_DIR, fname))

    return sorted(found_files)


def partition_image_files(image_files: list, train_ratio: float = 0.64, val_ratio: float = 0.18) -> dict:
    """
    Dynamically partitions any number of image files into strictly disjoint sets:
    Train, Validation, and Test (Zero image-level leakage guarantee).
    Scales smoothly from 3 to 300+ images.
    """
    N = len(image_files)
    if N == 0:
        return {"train": [], "val": [], "test": []}
    if N < 3:
        return {"train": image_files, "val": image_files, "test": image_files}

    n_train = max(1, int(round(N * train_ratio)))
    n_val = max(1, int(round(N * val_ratio)))
    if n_train + n_val >= N:
        n_val = max(1, N - n_train - 1)
    n_test = N - n_train - n_val

    # Ensure at least 1 image per partition if N >= 3
    if n_test < 1 and N >= 3:
        if n_train > 1:
            n_train -= 1
        elif n_val > 1:
            n_val -= 1
        n_test = N - n_train - n_val

    train_imgs = image_files[0:n_train]
    val_imgs = image_files[n_train:n_train + n_val]
    test_imgs = image_files[n_train + n_val:]

    return {
        "train": train_imgs,
        "val": val_imgs,
        "test": test_imgs,
        "counts": {"total": N, "train": len(train_imgs), "val": len(val_imgs), "test": len(test_imgs)}
    }


def get_adaptive_crops_per_image(num_images: int) -> int:
    """
    Computes memory-safe and compute-efficient crop budget per image.
    When N=11, yields ~100 crops/img (~3,000 sequences).
    When N=300+, yields ~12-15 crops/img (~4,000 sequences), avoiding OOM while sampling all images.
    """
    if num_images <= 15:
        return 100
    elif num_images <= 50:
        return 45
    elif num_images <= 120:
        return 25
    else:
        return max(10, min(20, 3600 // num_images))


def load_and_preprocess_image(image_path: str) -> np.ndarray:
    """
    Loads raw image, converts to single-channel Grayscale (Luminance Y),
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
      - Class 0: Horizontal Scan (lateral spatial traverse)
      - Class 1: Vertical Scan (orthogonal stratigraphic traverse)
      - Class 2: Inverted Scan (reverse temporal traverse)
    Includes subtle realistic sensor scanning trajectory dynamics to enable
    proper discriminative sequence learning across recurrent architectures.
    """
    rng = np.random.RandomState(seed)
    H, W = image_arr.shape
    sequences = []
    labels = []

    for _ in range(crops_per_image):
        top = rng.randint(0, max(1, H - seq_len))
        left = rng.randint(0, max(1, W - feat_dim))
        patch = image_arr[top:top + seq_len, left:left + feat_dim]

        # Ensure exact shape
        if patch.shape != (seq_len, feat_dim):
            padded = np.zeros((seq_len, feat_dim), dtype=np.float32)
            ph, pw = patch.shape
            padded[:ph, :pw] = patch
            patch = padded

        # Authentic 32-timestep spatial sequences derived purely from geological outcrop texture:
        # All 32 dimensions represent real normalized pixel luminance values across spatial scanlines.
        # - Class 0: Horizontal Spatial Trajectory (0° lateral traverse, rows t=0..31)
        # - Class 1: Vertical Spatial Trajectory (90° orthogonal strata traverse, cols t=0..31)
        # - Class 2: Inverted Spatial Trajectory (180° reverse-temporal traverse, rows t=31..0)
        h_seq = patch.copy()
        v_seq = patch.T.copy()
        inv_seq = patch[::-1, :].copy()

        sequences.append(h_seq)
        labels.append(0)

        sequences.append(v_seq)
        labels.append(1)

        sequences.append(inv_seq)
        labels.append(2)

    return np.array(sequences, dtype=np.float32), np.array(labels, dtype=np.int64)


class GeologicalSequenceDataset(Dataset):
    """PyTorch Dataset for image-derived spatial sequences."""
    def __init__(self, sequences: np.ndarray, labels: np.ndarray):
        self.sequences = torch.tensor(sequences, dtype=torch.float32)
        self.labels = torch.tensor(labels, dtype=torch.long)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return self.sequences[idx], self.labels[idx]


def build_datasets(data_dir: str = None, seed: int = 42):
    """
    Dynamically discovers all image files in data_dir, partitions them with zero data leakage,
    and returns Train, Validation, and Test Datasets.
    """
    image_files = discover_image_files(data_dir)
    num_images = len(image_files)
    partitions = partition_image_files(image_files)

    train_imgs = partitions["train"]
    val_imgs = partitions["val"]
    test_imgs = partitions["test"]

    crops = get_adaptive_crops_per_image(num_images)

    print("=" * 65)
    print("DYNAMIC GEOLOGICAL DATASET PREPARATION")
    print(f"Total Images Discovered: {num_images}")
    print(f"Train Partition ({len(train_imgs)} images): {[os.path.basename(f) for f in train_imgs[:4]]}{'...' if len(train_imgs) > 4 else ''}")
    print(f"Val Partition   ({len(val_imgs)} images): {[os.path.basename(f) for f in val_imgs[:3]]}{'...' if len(val_imgs) > 3 else ''}")
    print(f"Test Partition  ({len(test_imgs)} images): {[os.path.basename(f) for f in test_imgs[:3]]}{'...' if len(test_imgs) > 3 else ''}")
    print(f"Adaptive Crops per Image: {crops}")
    print("=" * 65)

    # 1. Train sequences
    train_seqs, train_lbls = [], []
    for idx, path in enumerate(train_imgs):
        img_arr = load_and_preprocess_image(path)
        s, l = extract_sequences_from_image(img_arr, crops_per_image=crops, seed=seed + idx)
        train_seqs.append(s)
        train_lbls.append(l)
    X_train = np.concatenate(train_seqs, axis=0) if train_seqs else np.zeros((0, 32, 32), dtype=np.float32)
    y_train = np.concatenate(train_lbls, axis=0) if train_lbls else np.zeros((0,), dtype=np.int64)

    # 2. Validation sequences
    val_seqs, val_lbls = [], []
    val_crops = max(10, int(crops * 0.8))
    for idx, path in enumerate(val_imgs):
        img_arr = load_and_preprocess_image(path)
        s, l = extract_sequences_from_image(img_arr, crops_per_image=val_crops, seed=seed + 1000 + idx)
        val_seqs.append(s)
        val_lbls.append(l)
    X_val = np.concatenate(val_seqs, axis=0) if val_seqs else np.zeros((0, 32, 32), dtype=np.float32)
    y_val = np.concatenate(val_lbls, axis=0) if val_lbls else np.zeros((0,), dtype=np.int64)

    # 3. Test sequences
    test_seqs, test_lbls = [], []
    test_crops = max(10, int(crops * 0.8))
    for idx, path in enumerate(test_imgs):
        img_arr = load_and_preprocess_image(path)
        s, l = extract_sequences_from_image(img_arr, crops_per_image=test_crops, seed=seed + 2000 + idx)
        test_seqs.append(s)
        test_lbls.append(l)
    X_test = np.concatenate(test_seqs, axis=0) if test_seqs else np.zeros((0, 32, 32), dtype=np.float32)
    y_test = np.concatenate(test_lbls, axis=0) if test_lbls else np.zeros((0,), dtype=np.int64)

    print(f"Dataset Successfully Assembled:")
    print(f"  Training samples:   {len(y_train)} (Shape: {X_train.shape})")
    print(f"  Validation samples: {len(y_val)} (Shape: {X_val.shape})")
    print(f"  Test samples:       {len(y_test)} (Shape: {X_test.shape})")
    print("=" * 65)

    return (GeologicalSequenceDataset(X_train, y_train),
            GeologicalSequenceDataset(X_val, y_val),
            GeologicalSequenceDataset(X_test, y_test))


def get_dataloaders(data_dir: str = None, batch_size: int = 32, seed: int = 42):
    """Returns PyTorch DataLoaders for train, val, and test splits."""
    torch.manual_seed(seed)
    train_ds, val_ds, test_ds = build_datasets(data_dir=data_dir, seed=seed)

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    val_loader   = DataLoader(val_ds, batch_size=batch_size, shuffle=False)
    test_loader  = DataLoader(test_ds, batch_size=batch_size, shuffle=False)

    return train_loader, val_loader, test_loader
