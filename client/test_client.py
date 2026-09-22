"""
NeuralFlow Client Integration Test
==================================
Validates that the client SDK accurately interfaces with the server.
"""

import os
import sys

CLIENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CLIENT_DIR not in sys.path:
    sys.path.insert(0, CLIENT_DIR)

from api_client import NeuralFlowClient


def run_tests(base_url="http://127.0.0.1:8000"):
    print(f">>> Running NeuralFlow Client Verification against {base_url}...")
    client = NeuralFlowClient(base_url=base_url)

    try:
        health = client.health_check()
        assert health.get("status") == "healthy" or health.get("version") is not None
        print("  [PASS] Health check passed")
    except Exception as e:
        print(f"  [FAIL] Health check failed (ensure server is running): {e}")
        return False

    try:
        summary = client.get_model_summary()
        assert len(summary) >= 4, "Expected at least 4 models"
        print(f"  [PASS] Model summary passed ({len(summary)} models detected)")
    except Exception as e:
        print(f"  [FAIL] Model summary failed: {e}")
        return False

    try:
        metrics = client.get_metrics()
        assert "LSTM" in metrics or "Bidirectional RNN" in metrics
        print("  [PASS] Evaluation metrics query passed")
    except Exception as e:
        print(f"  [FAIL] Evaluation metrics failed: {e}")
        return False

    print(">>> All client integration checks passed successfully!")
    return True


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"
    success = run_tests(base_url=url)
    sys.exit(0 if success else 1)
