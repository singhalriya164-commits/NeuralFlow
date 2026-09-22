"""
NeuralFlow Python Client SDK
============================
A lightweight, robust client library for interacting with the NeuralFlow REST API.
Compatible with standard library urllib (no third-party dependencies required).
"""

import json
import urllib.request
import urllib.parse
import urllib.error
from typing import Dict, Any, Optional


class NeuralFlowClient:
    """Client for the NeuralFlow Machine Learning & Analytics REST API."""

    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url.rstrip("/")

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        if params:
            query = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
            url = f"{url}?{query}"
        req = urllib.request.Request(url, headers={"User-Agent": "NeuralFlowClient/2.4"})
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                content = response.read().decode("utf-8")
                return json.loads(content)
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
        except urllib.error.URLError as e:
            raise ConnectionError(f"Could not connect to NeuralFlow server at {self.base_url}: {e.reason}")

    def health_check(self) -> Dict[str, Any]:
        """Verify server health and runtime telemetry."""
        return self._get("/healthz")

    def get_status(self) -> Dict[str, Any]:
        """Fetch server device, memory, and model status."""
        return self._get("/api/status")

    def get_model_summary(self) -> Dict[str, Any]:
        """Fetch architecture parameter counts and layer details."""
        return self._get("/api/summary")

    def get_metrics(self) -> Dict[str, Any]:
        """Fetch benchmark evaluation metrics (accuracy, F1, precision, recall, latency)."""
        return self._get("/api/metrics")

    def get_history(self) -> Dict[str, Any]:
        """Fetch epoch training and validation loss/accuracy curves."""
        return self._get("/api/history")

    def get_gradients(self) -> Dict[str, Any]:
        """Fetch backpropagation gradient norm distributions."""
        return self._get("/api/gradients")

    def get_dataset_stats(self) -> Dict[str, Any]:
        """Fetch geological dataset statistics."""
        return self._get("/api/dataset-stats")

    def get_conclusion(self) -> Dict[str, Any]:
        """Fetch multi-criteria algorithmic conclusion and optimal model recommendation."""
        return self._get("/api/live-conclusion")

    def predict(self, image_id: str = "IMG-10", trajectory: float = 0.0, seed: int = 42) -> Dict[str, Any]:
        """
        Execute live recurrent model inference on an input sample.
        Returns prediction probabilities for Vanilla RNN, Bi-RNN, LSTM, and GRU.
        """
        params = {"image_id": image_id, "trajectory": trajectory, "seed": seed}
        return self._get("/api/predict", params=params)


if __name__ == "__main__":
    client = NeuralFlowClient()
    print("Testing connection to NeuralFlow backend...")
    try:
        health = client.health_check()
        print(f"Server is healthy: Version {health.get('version')}, Uptime {health.get('uptime_seconds')}s")
        metrics = client.get_metrics()
        print(f"Models loaded: {list(metrics.keys())}")
    except Exception as e:
        print(f"Notice: {e}")
