# NeuralFlow: Production Operations & Deployment Runbook

**Enterprise Operations Manual, Security Hardening Checklist, API Specification & Incident Response Procedures**

---

## 1. System Architecture & Component Topology

```
                          ┌───────────────────────────┐
                          │   Client Web Browser /    │
                          │   Enterprise REST Client  │
                          └─────────────┬─────────────┘
                                        │ HTTPS / HTTP
                                        ▼
                          ┌───────────────────────────┐
                          │    app.py HTTP Server     │
                          │   (ThreadingHTTPServer)   │
                          │ - Safe Path Boundary      │
                          │ - Security Headers (CSP)  │
                          │ - Rate & Bounds Validation│
                          └─────────────┬─────────────┘
                                        │
                 ┌──────────────────────┴──────────────────────┐
                 ▼                                             ▼
  ┌─────────────────────────────┐               ┌─────────────────────────────┐
  │   Static Assets & Telemetry │               │    dynamic_engine.py        │
  │ - ui/index.html             │               │  (Thread-Safe RLock Engine) │
  │ - ui/style.css              │               │ - PyTorch Forward Passes    │
  │ - ui/dashboard.js           │               │ - Scikit-Learn Live Eval    │
  │ - results/*.json            │               │ - BPTT Gradient Tracking    │
  │ - reports/*.html            │               │ - Analytical FLOP Scaler    │
  └─────────────────────────────┘               └──────────────┬──────────────┘
                                                               │
                                                               ▼
                                                ┌─────────────────────────────┐
                                                │   Hardware Execution Tier   │
                                                │ - NVIDIA CUDA (cuDNN Det.)  │
                                                │ - Multi-Core Host CPU       │
                                                │ - Weights (.pt) on Disk     │
                                                └─────────────────────────────┘
```

---

## 2. Production Deployment & Configuration

### 2.1 Prerequisites
- Python 3.10+ (64-bit)
- PyTorch 2.0+ (with CUDA 11.8/12.1+ support for GPU acceleration)
- 4 GB RAM minimum (8 GB recommended for CUDA execution)
- 500 MB free disk space for model checkpoints, logs, and datasets

### 2.2 Environment Installation
```bash
# Clone or navigate to the workspace
cd C:\Users\Chaha\OneDrive\Desktop\NeuralFlow

# Create and activate virtual environment (optional but recommended)
python -m venv venv
.\venv\Scripts\activate

# Install required production dependencies
pip install -r requirements.txt
```

### 2.3 Starting the Server
```bash
# Standard Production Mode (Bound to localhost:8000)
python app.py --port 8000 --host 127.0.0.1 --no-browser

# Or use the enterprise start script
.\start.bat
```

---

## 3. REST API Specification

### 3.1 Telemetry & Health Checks

#### `GET /healthz` | `GET /api/health`
Returns runtime health status, hardware capabilities, and uptime.
- **Response**: `200 OK`
```json
{
  "status": "healthy",
  "service": "NeuralFlow Enterprise AI Platform",
  "version": "2.4.0-enterprise",
  "uptime_seconds": 342.15,
  "timestamp": "2026-09-09T00:15:00Z",
  "hardware": {
    "device": "cuda",
    "device_name": "NVIDIA GeForce RTX 3050 Laptop GPU",
    "vram_total_mb": 4096.0,
    "vram_allocated_mb": 182.4,
    "is_gpu": true
  },
  "models_ready": true,
  "security": {
    "path_traversal_protection": "Active",
    "security_headers": "Active",
    "thread_safety": "Active"
  }
}
```

#### `GET /api/status`
Returns dynamic experiment execution status and last timestamp.
- **Response**: `200 OK`
```json
{
  "status": "Completed",
  "last_run": "2026-09-08T18:32:32Z",
  "dataset_version": "Enterprise Production v2.4 (11 Verified Outcrop Images)",
  "environment": "production"
}
```

---

### 3.2 Live Inference & Model Analytics

#### `GET /api/predict?image_id={ID}&trajectory={0|1|2}&seed={INT}`
Executes thread-safe live forward pass inference across all 4 recurrent models on the specified image and spatial trajectory.
- **Parameters**:
  - `image_id` *(string)*: Identifier or filename of image (e.g. `IMG-10`).
  - `trajectory` *(int, 0..2)*: `0` = Horizontal ($0^\circ$), `1` = Vertical ($90^\circ$), `2` = Inverted ($180^\circ$).
  - `seed` *(int, 0..1000000)*: Random seed for localized crop extraction.
- **Response**: `200 OK`
```json
{
  "status": "success",
  "image_id": "IMG-10",
  "image_filename": "WhatsApp Image 2026-07-31 at 11.52.55 AM (1).jpeg",
  "true_class": 0,
  "true_class_name": "Class 0 (Horizontal)",
  "sequence_shape": [32, 32],
  "models": {
    "Bidirectional RNN": {
      "model_name": "Bidirectional RNN",
      "probabilities": [34.5, 33.2, 32.3],
      "predicted_class": 0,
      "predicted_class_name": "Class 0 (Horizontal)",
      "confidence": 34.5,
      "is_correct": true,
      "latency_ms": 0.42
    },
    "Vanilla RNN": { ... },
    "LSTM": { ... },
    "GRU": { ... }
  }
}
```

#### `GET /api/live-evaluate`
Executes test set evaluation over the holdout partition and returns scikit-learn metrics.
- **Response**: `200 OK`

#### `GET /api/live-gradients`
Executes mini-batch backpropagation and returns true $L_2$ recurrent weight gradient norms.
- **Response**: `200 OK`

#### `GET /api/dynamic-parameters?hidden_dim={INT}&input_dim={INT}`
Calculates exact mathematical parameter formulas, theoretical MFLOPs, and live latency.
- **Bounds**: `hidden_dim` $\in [8, 512]$, `input_dim` $\in [8, 256]$.
- **Response**: `200 OK`

---

## 4. Security Hardening Checklist

| Security Control | Implementation | Verification Command |
|------------------|----------------|----------------------|
| **Path Traversal Immunity** | `safe_path_resolve()` uses `os.path.commonpath` | `curl -i http://127.0.0.1:8000/reports/../../app.py` → `404 Not Found` |
| **MIME Sniffing Prevention** | `X-Content-Type-Options: nosniff` header | Checked via HTTP response headers |
| **Clickjacking Mitigation** | `X-Frame-Options: SAMEORIGIN` header | Checked via HTTP response headers |
| **CORS Policy** | Explicit method & origin restrictions | Handled via `do_OPTIONS` |
| **Thread Safety** | Reentrant lock `_ENGINE_LOCK` wraps PyTorch | Verified under concurrent requests |
| **Input Clamping** | `validate_int()` & `validate_float()` | Requests with `hidden_dim=999999` clamped to `512` |

---

## 5. Incident Response & Troubleshooting

### Issue 1: Model check points not found (HTTP 404 on `/api/metrics`)
- **Root Cause**: Training benchmark has not yet executed.
- **Resolution**: Run `python run_experiment.py` to generate `.pt` weights and results artifacts.

### Issue 2: CUDA Out of Memory (OOM)
- **Root Cause**: Insufficient GPU VRAM when running parallel workloads.
- **Resolution**: NeuralFlow automatically falls back to CPU if CUDA fails or is unavailable. Set `CUDA_VISIBLE_DEVICES=""` to force CPU execution.

### Issue 3: Port 8000 Conflict
- **Root Cause**: Another service is bound to port 8000.
- **Resolution**: Pass `--port <PORT>` to `app.py`:
  ```bash
  python app.py --port 8080
  ```
