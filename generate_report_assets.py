"""
Generates publication-grade figures and diagrams for the NeuralFlow 25-page project report.
"""
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_IMG_DIR = os.path.join(BASE_DIR, "report_assets")
os.makedirs(REPORT_IMG_DIR, exist_ok=True)

# Set high DPI and classic publication font
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 11
plt.rcParams['axes.labelsize'] = 10

def generate_outcrop_samples():
    """Collage of rock outcrop images showing concentric ring structures and patch sampling."""
    img_files = [
        "WhatsApp Image 2026-07-31 at 11.52.51 AM (1).jpeg",
        "WhatsApp Image 2026-07-31 at 11.52.52 AM.jpeg",
        "WhatsApp Image 2026-07-31 at 11.52.53 AM (1).jpeg",
        "WhatsApp Image 2026-07-31 at 11.52.54 AM.jpeg"
    ]
    
    fig, axes = plt.subplots(1, 4, figsize=(10, 3.2), dpi=300)
    titles = [
        "(a) Outcrop Sample 1: Bedding",
        "(b) Outcrop Sample 2: Ring Apex",
        "(c) Outcrop Sample 3: Concentric Rings",
        "(d) Outcrop Sample 4: Weathered Strata"
    ]
    
    for idx, fname in enumerate(img_files):
        fpath = os.path.join(BASE_DIR, fname)
        if os.path.exists(fpath):
            img = Image.open(fpath)
            axes[idx].imshow(img)
            # Add patch sampling bounding box demonstration
            w, h = img.size
            rect = patches.Rectangle((w*0.3, h*0.4), w*0.35, h*0.35, linewidth=2, edgecolor='cyan', facecolor='none', linestyle='--')
            axes[idx].add_patch(rect)
            axes[idx].text(w*0.32, h*0.38, "Sample Patch ROI", color='cyan', fontsize=8, weight='bold')
        axes[idx].set_title(titles[idx], fontsize=9, pad=5)
        axes[idx].axis('off')
        
    plt.tight_layout()
    out_path = os.path.join(REPORT_IMG_DIR, "fig_outcrop_samples.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")

def generate_sequence_formation():
    """Diagram illustrating conversion of 2D patch to 3 classes of sequences."""
    fig, ax = plt.subplots(figsize=(9, 4.2), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')
    
    # 2D Patch representation
    patch_rect = patches.Rectangle((0.5, 1.2), 2.6, 2.6, facecolor='#E2E8F0', edgecolor='#1E293B', linewidth=2)
    ax.add_patch(patch_rect)
    ax.text(1.8, 4.1, "Extracted 2D Spatial Patch\nP in R^{32 x 32}", ha='center', weight='bold', fontsize=10)
    
    # Grid lines inside patch
    for i in range(1, 6):
        ax.plot([0.5, 3.1], [1.2 + i*0.43, 1.2 + i*0.43], color='#94A3B8', linestyle=':', lw=1)
        ax.plot([0.5 + i*0.43, 0.5 + i*0.43], [1.2, 3.8], color='#94A3B8', linestyle=':', lw=1)
    
    # Arrow to Class 0
    ax.annotate("", xy=(4.2, 3.7), xytext=(3.3, 3.0), arrowprops=dict(arrowstyle="->", lw=2, color='#2563EB'))
    ax.text(3.6, 3.7, "Horizontal Scan (0 deg)\nx_t = P[t, :]", fontsize=9, weight='bold', color='#1E3A8A')
    
    # Class 0 representation
    c0_box = patches.Rectangle((4.5, 3.2), 4.8, 1.0, facecolor='#EFF6FF', edgecolor='#2563EB', linewidth=1.5)
    ax.add_patch(c0_box)
    ax.text(6.9, 3.7, "Class 0: Horizontal Spatial Trajectory", ha='center', weight='bold', fontsize=9, color='#1E3A8A')
    ax.text(6.9, 3.4, "t = 0 (Top Row) ---> t = 31 (Bottom Row) | (T=32, D=32)", ha='center', fontsize=8)
    
    # Arrow to Class 1
    ax.annotate("", xy=(4.2, 2.5), xytext=(3.3, 2.5), arrowprops=dict(arrowstyle="->", lw=2, color='#059669'))
    ax.text(3.6, 2.65, "Vertical Scan (90 deg)\nx_t = P[:, t]", fontsize=9, weight='bold', color='#065F46')
    
    # Class 1 representation
    c1_box = patches.Rectangle((4.5, 2.0), 4.8, 1.0, facecolor='#ECFDF5', edgecolor='#059669', linewidth=1.5)
    ax.add_patch(c1_box)
    ax.text(6.9, 2.5, "Class 1: Vertical Spatial Trajectory", ha='center', weight='bold', fontsize=9, color='#065F46')
    ax.text(6.9, 2.2, "t = 0 (Left Column) ---> t = 31 (Right Column) | (T=32, D=32)", ha='center', fontsize=8)
    
    # Arrow to Class 2
    ax.annotate("", xy=(4.2, 1.3), xytext=(3.3, 2.0), arrowprops=dict(arrowstyle="->", lw=2, color='#DC2626'))
    ax.text(3.6, 1.45, "Inverted Scan (180 deg)\nx_t = P[31-t, :]", fontsize=9, weight='bold', color='#991B1B')
    
    # Class 2 representation
    c2_box = patches.Rectangle((4.5, 0.8), 4.8, 1.0, facecolor='#FEF2F2', edgecolor='#DC2626', linewidth=1.5)
    ax.add_patch(c2_box)
    ax.text(6.9, 1.3, "Class 2: Inverted Spatial Trajectory", ha='center', weight='bold', fontsize=9, color='#991B1B')
    ax.text(6.9, 1.0, "t = 0 (Bottom Row) ---> t = 31 (Top Row) | (T=32, D=32)", ha='center', fontsize=8)
    
    plt.tight_layout()
    out_path = os.path.join(REPORT_IMG_DIR, "fig_sequence_formation.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")

def generate_system_architecture():
    """NeuralFlow overall architecture diagram."""
    fig, ax = plt.subplots(figsize=(9, 4.8), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    # Input Block
    in_box = patches.FancyBboxPatch((0.5, 1.8), 2.2, 2.4, boxstyle="round,pad=0.2", facecolor="#F1F5F9", edgecolor="#334155", lw=1.5)
    ax.add_patch(in_box)
    ax.text(1.6, 3.6, "Input Sequence\nTensor", ha='center', weight='bold', fontsize=9.5)
    ax.text(1.6, 2.8, "Batch Size: B=32\nTimesteps: T=32\nFeature Dim: D=32\nShape: (B, 32, 32)", ha='center', fontsize=8)
    ax.text(1.6, 2.1, "Normalized [0.0, 1.0]", ha='center', fontsize=7.5, style='italic', color='#475569')

    # Arrow 1
    ax.annotate("", xy=(3.4, 3.0), xytext=(2.9, 3.0), arrowprops=dict(arrowstyle="->", lw=2, color='#334155'))

    # Recurrent Backbone Block
    rec_box = patches.FancyBboxPatch((3.5, 1.2), 4.2, 3.6, boxstyle="round,pad=0.2", facecolor="#EFF6FF", edgecolor="#2563EB", lw=2)
    ax.add_patch(rec_box)
    ax.text(5.6, 4.4, "Recurrent Backbone Options\n(Hidden Dimension = 64)", ha='center', weight='bold', fontsize=10, color='#1E3A8A')
    
    models_info = [
        ("1. Vanilla RNN", "64 hidden units, 1 direction", "8,451 params"),
        ("2. Bidirectional RNN", "32 fwd + 32 bwd units", "6,403 params"),
        ("3. LSTM", "64 hidden units, 4 gates", "27,267 params"),
        ("4. GRU", "64 hidden units, 2 gates", "20,995 params")
    ]
    for idx, (m_name, m_desc, m_par) in enumerate(models_info):
        y_pos = 3.6 - idx*0.7
        r_sub = patches.Rectangle((3.7, y_pos - 0.25), 3.8, 0.55, facecolor="#DBEAFE", edgecolor="#3B82F6", lw=1)
        ax.add_patch(r_sub)
        ax.text(3.9, y_pos, f"{m_name}: {m_desc}", fontsize=8, weight='bold')
        ax.text(7.3, y_pos, m_par, fontsize=7.5, ha='right', color='#1E40AF')

    # Arrow 2
    ax.annotate("", xy=(8.4, 3.0), xytext=(7.9, 3.0), arrowprops=dict(arrowstyle="->", lw=2, color='#334155'))
    ax.text(8.15, 3.25, "h_out in R^64", ha='center', fontsize=7.5, weight='bold', color='#1E40AF')

    # Classifier Head Block
    head_box = patches.FancyBboxPatch((8.5, 1.5), 3.0, 3.0, boxstyle="round,pad=0.2", facecolor="#F0FDF4", edgecolor="#16A34A", lw=2)
    ax.add_patch(head_box)
    ax.text(10.0, 4.1, "Symmetric Classifier Head", ha='center', weight='bold', fontsize=9.5, color='#14532D')
    ax.text(10.0, 3.4, "Linear(64, 32)\nReLU Activation\nDropout (p = 0.2)\nLinear(32, 3)", ha='center', fontsize=8)
    ax.text(10.0, 2.4, "Cross-Entropy Softmax Logits", ha='center', fontsize=8, weight='bold', color='#15803D')
    ax.text(10.0, 1.8, "Outputs: Class 0, 1, 2", ha='center', fontsize=8, style='italic')

    plt.tight_layout()
    out_path = os.path.join(REPORT_IMG_DIR, "fig_system_architecture.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")

def generate_recurrent_cell_mechanisms():
    """Diagram showing internal cell gating mechanics of Vanilla RNN, Bi-RNN, LSTM, and GRU."""
    fig, axes = plt.subplots(2, 2, figsize=(10, 6.5), dpi=300)
    
    # 1. Vanilla RNN
    ax = axes[0, 0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title("(a) Vanilla Elman RNN Cell", fontsize=10, weight='bold', pad=8)
    box = patches.Rectangle((2, 2), 6, 6, facecolor="#F8FAFC", edgecolor="#64748B", lw=1.5)
    ax.add_patch(box)
    ax.text(5, 5, "tanh( W_{ih} x_t + W_{hh} h_{t-1} + b )", ha='center', weight='bold', fontsize=9)
    ax.annotate("", xy=(5, 8), xytext=(5, 9.5), arrowprops=dict(arrowstyle="<-", lw=1.5))
    ax.text(5.3, 9, "h_t", fontsize=9, weight='bold')
    ax.annotate("", xy=(5, 2), xytext=(5, 0.5), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.text(5.3, 1, "x_t", fontsize=9, weight='bold')
    ax.annotate("", xy=(2, 5), xytext=(0.5, 5), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.text(1, 5.3, "h_{t-1}", fontsize=9, weight='bold')
    ax.text(5, 2.5, "Single repeated matrix\nMultiplication chain", ha='center', fontsize=8, color='#64748B')

    # 2. Bidirectional RNN
    ax = axes[0, 1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title("(b) Bidirectional RNN Architecture", fontsize=10, weight='bold', pad=8)
    box_fwd = patches.Rectangle((1.5, 5.2), 7, 3.2, facecolor="#EFF6FF", edgecolor="#2563EB", lw=1.5)
    ax.add_patch(box_fwd)
    ax.text(5, 7.3, "Forward Recurrent Chain (-->)", ha='center', weight='bold', fontsize=8.5, color='#1E3A8A')
    ax.text(5, 6.0, "h_fwd = tanh(W x_t + U h_{t-1})", ha='center', fontsize=8)
    
    box_bwd = patches.Rectangle((1.5, 1.2), 7, 3.2, facecolor="#FDF2F8", edgecolor="#DB2777", lw=1.5)
    ax.add_patch(box_bwd)
    ax.text(5, 3.3, "Backward Recurrent Chain (<--)", ha='center', weight='bold', fontsize=8.5, color='#831843')
    ax.text(5, 2.0, "h_bwd = tanh(W x_t + U h_{t+1})", ha='center', fontsize=8)
    ax.text(5, 0.3, "Concatenated Output: [h_fwd || h_bwd] in R^64", ha='center', weight='bold', fontsize=8.5, color='#334155')

    # 3. LSTM
    ax = axes[1, 0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title("(c) Long Short-Term Memory (LSTM) Cell", fontsize=10, weight='bold', pad=8)
    box = patches.Rectangle((1.2, 1.2), 7.6, 7.6, facecolor="#F0FDF4", edgecolor="#16A34A", lw=1.5)
    ax.add_patch(box)
    # Cell state highway
    ax.plot([0.5, 9.5], [7.5, 7.5], color='#15803D', lw=2.5)
    ax.text(0.8, 7.9, "c_{t-1}", fontsize=8.5, weight='bold', color='#15803D')
    ax.text(9.2, 7.9, "c_t", fontsize=8.5, weight='bold', color='#15803D')
    ax.text(5, 8.2, "Constant Error Carousel (Additive Highway)", ha='center', fontsize=8, weight='bold', color='#15803D')
    
    # 4 gates
    gates = [("f_t", 2.2, "Forget Gate\nsigmoid"), ("i_t", 4.0, "Input Gate\nsigmoid"), ("~c_t", 5.8, "Candidate\ntanh"), ("o_t", 7.6, "Output Gate\nsigmoid")]
    for gname, gx, gdesc in gates:
        gbox = patches.Rectangle((gx - 0.7, 3.0), 1.4, 2.4, facecolor="#DCFCE7", edgecolor="#16A34A", lw=1)
        ax.add_patch(gbox)
        ax.text(gx, 4.4, gname, ha='center', weight='bold', fontsize=8.5)
        ax.text(gx, 3.5, gdesc, ha='center', fontsize=7)
    ax.text(5, 1.8, "h_t = o_t * tanh(c_t)", ha='center', weight='bold', fontsize=8.5)

    # 4. GRU
    ax = axes[1, 1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title("(d) Gated Recurrent Unit (GRU) Cell", fontsize=10, weight='bold', pad=8)
    box = patches.Rectangle((1.2, 1.2), 7.6, 7.6, facecolor="#FFFBEB", edgecolor="#D97706", lw=1.5)
    ax.add_patch(box)
    
    # 2 gates
    gbox1 = patches.Rectangle((2.0, 3.6), 2.5, 2.8, facecolor="#FEF3C7", edgecolor="#D97706", lw=1)
    ax.add_patch(gbox1)
    ax.text(3.25, 5.4, "r_t", ha='center', weight='bold', fontsize=9)
    ax.text(3.25, 4.2, "Reset Gate\nsigmoid\n(Discards history)", ha='center', fontsize=7.5)
    
    gbox2 = patches.Rectangle((5.5, 3.6), 2.5, 2.8, facecolor="#FEF3C7", edgecolor="#D97706", lw=1)
    ax.add_patch(gbox2)
    ax.text(6.75, 5.4, "z_t", ha='center', weight='bold', fontsize=9)
    ax.text(6.75, 4.2, "Update Gate\nsigmoid\n(Coupled retention)", ha='center', fontsize=7.5)
    
    ax.text(5, 7.5, "Candidate State: ~h_t = tanh(W x_t + U(r_t * h_{t-1}))", ha='center', fontsize=8, weight='bold')
    ax.text(5, 2.2, "Interpolation: h_t = (1 - z_t)*h_{t-1} + z_t * ~h_t", ha='center', weight='bold', fontsize=8.5, color='#92400E')

    plt.tight_layout()
    out_path = os.path.join(REPORT_IMG_DIR, "fig_recurrent_cell_mechanisms.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")

def generate_gradient_jacobian_flow():
    """Diagram illustrating Jacobian BPTT gradient propagation."""
    fig, ax = plt.subplots(figsize=(9, 4.2), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    ax.text(6, 5.4, "Backpropagation Through Time (BPTT) Gradient Flow Comparison", ha='center', weight='bold', fontsize=11)
    
    # Vanilla RNN flow
    ax.text(0.8, 4.2, "Vanilla RNN:", weight='bold', fontsize=9.5, color='#B91C1C')
    timesteps = [("t=1", 2.5), ("t=2", 4.3), ("...", 6.1), ("t=T-1", 7.9), ("t=T", 9.7)]
    for name, x in timesteps:
        box = patches.Rectangle((x-0.6, 3.6), 1.2, 0.9, facecolor="#FEE2E2", edgecolor="#DC2626", lw=1)
        ax.add_patch(box)
        ax.text(x, 4.05, name, ha='center', weight='bold', fontsize=8.5)
        if x > 2.5:
            ax.annotate("", xy=(x-0.7, 4.05), xytext=(x-1.1, 4.05), arrowprops=dict(arrowstyle="<-", lw=1.5, color='#DC2626'))
            ax.text(x-0.9, 4.4, "* W^T", fontsize=7.5, ha='center', color='#DC2626')
    ax.text(6, 3.1, "Exponential Decay: ||dL/dh_1|| <= ||W_hh||^{T-1} ||dL/dh_T||  --> 0 (Vanishing Gradient)", ha='center', fontsize=8, color='#B91C1C', weight='bold')

    # LSTM flow
    ax.text(0.8, 1.8, "LSTM (CEC):", weight='bold', fontsize=9.5, color='#15803D')
    for name, x in timesteps:
        box = patches.Rectangle((x-0.6, 1.2), 1.2, 0.9, facecolor="#DCFCE7", edgecolor="#16A34A", lw=1)
        ax.add_patch(box)
        ax.text(x, 1.65, name, ha='center', weight='bold', fontsize=8.5)
        if x > 2.5:
            ax.annotate("", xy=(x-0.7, 1.65), xytext=(x-1.1, 1.65), arrowprops=dict(arrowstyle="<-", lw=2, color='#15803D'))
            ax.text(x-0.9, 2.0, "dc_t/dc_{t-1}=f_t", fontsize=7.5, ha='center', color='#15803D')
    ax.text(6, 0.6, "Constant Error Carousel: When f_t ~ 1, Gradients Flow Undecayed Across All T Steps", ha='center', fontsize=8, color='#15803D', weight='bold')

    plt.tight_layout()
    out_path = os.path.join(REPORT_IMG_DIR, "fig_gradient_jacobian_flow.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")

def generate_dashboard_architecture():
    """NeuralFlow Streamlit application architecture."""
    fig, ax = plt.subplots(figsize=(9, 4.0), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5)
    ax.axis('off')
    
    ax.text(6, 4.5, "NeuralFlow Interactive Production Serving Architecture (Streamlit)", ha='center', weight='bold', fontsize=11)
    
    layers = [
        ("Presentation Layer", "Streamlit Multi-Page Dashboard\nLive Parameter Visualizers\nInference Confidence Meters\nInteractive ROC / Confusion Matrices", 1.8, "#EFF6FF", "#2563EB"),
        ("Dynamic Inference Engine", "dynamic_engine.py\nIn-Memory Model Checkpoints\nReal-time Spatial Sequence Slicing\nBatch Tensor Transformation", 6.0, "#F0FDF4", "#16A34A"),
        ("Trained Checkpoints & Data", "Torch Weights (.pt)\nexperiment_results.json\nRaw High-Res Outcrop JPEGs\nPreprocessed Tensors", 10.2, "#FEF3C7", "#D97706")
    ]
    
    for title, desc, x, bg, bd in layers:
        box = patches.FancyBboxPatch((x-1.8, 1.0), 3.6, 2.8, boxstyle="round,pad=0.2", facecolor=bg, edgecolor=bd, lw=1.5)
        ax.add_patch(box)
        ax.text(x, 3.4, title, ha='center', weight='bold', fontsize=9.5, color=bd)
        ax.text(x, 2.1, desc, ha='center', fontsize=8)
        
    ax.annotate("", xy=(3.9, 2.4), xytext=(4.3, 2.4), arrowprops=dict(arrowstyle="<->", lw=2, color='#475569'))
    ax.annotate("", xy=(8.1, 2.4), xytext=(8.5, 2.4), arrowprops=dict(arrowstyle="<->", lw=2, color='#475569'))

    plt.tight_layout()
    out_path = os.path.join(REPORT_IMG_DIR, "fig_dashboard_architecture.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")

if __name__ == "__main__":
    generate_outcrop_samples()
    generate_sequence_formation()
    generate_system_architecture()
    generate_recurrent_cell_mechanisms()
    generate_gradient_jacobian_flow()
    generate_dashboard_architecture()
    print("All report assets generated successfully!")
