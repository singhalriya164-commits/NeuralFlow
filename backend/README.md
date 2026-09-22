# NeuralFlow Backend

The **Backend** category hosts the core machine learning models, PyTorch inference pipeline, dataset feature extraction, and enterprise REST API server.

## Features
- **Production Server (`app.py`)**: Multi-threaded HTTP server with strict path traversal isolation and enterprise CSP security headers.
- **PyTorch Models (`models/`)**: Vanilla RNN, Bi-RNN, LSTM, and GRU architectures with trained checkpoints (`*.pt`).
- **Real-Time Dynamic Engine (`dynamic_engine.py`)**: Live evaluation, gradient analysis, live classification inference, and SSE training stream.
- **Report & Telemetry APIs**: Automated IEEE docx report generation, CSV/JSON metric export.

## Running Locally
```bash
python app.py --port 8000
```

## Running with Docker
```bash
docker build -t neuralflow-backend .
docker run -p 8000:8000 neuralflow-backend
```

## Deployment on Render
Deploy as a Python Web Service or use the included `render.yaml` Blueprint:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py --port $PORT --host 0.0.0.0 --no-browser`
- **Health Check Path**: `/healthz`
