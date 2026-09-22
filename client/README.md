# NeuralFlow Client SDK & CLI

The **Client** category provides developer SDKs and terminal CLI tools for interacting with the NeuralFlow backend services without needing a web browser.

## Features
- **Python SDK (`api_client.py`)**: Zero-dependency Python library (`NeuralFlowClient`) for programmatic model evaluation and inference.
- **CLI Utility (`cli.py`)**: Interactive command-line interface to inspect models, check server health, and run predictions.
- **JavaScript SDK (`client.js`)**: Universal JavaScript client SDK compatible with browser and Node.js environments.
- **Integration Test (`test_client.py`)**: Automated verification script testing client-server communication.

## Quickstart (Python CLI)
```bash
# Check server health
python cli.py health

# Display comparative metrics table
python cli.py metrics

# Inspect model architectures & parameters
python cli.py summary

# Run live inference on sample
python cli.py predict --image IMG-10
```

## Python SDK Example
```python
from api_client import NeuralFlowClient

client = NeuralFlowClient("http://127.0.0.1:8000")
health = client.health_check()
print("Health:", health)

predictions = client.predict(image_id="IMG-10")
print("Inference results:", predictions)
```
