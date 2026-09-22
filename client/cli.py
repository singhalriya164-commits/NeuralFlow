"""
NeuralFlow Command Line Interface (CLI)
=======================================
Developer tool for inspecting models, evaluating benchmarks, and testing predictions.
"""

import os
import sys
import argparse

CLIENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CLIENT_DIR not in sys.path:
    sys.path.insert(0, CLIENT_DIR)

from api_client import NeuralFlowClient


def format_table(headers, rows):
    widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            widths[i] = max(widths[i], len(str(val)))
    
    header_str = " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
    sep_str = "-+-".join("-" * widths[i] for i in range(len(headers)))
    row_strs = [" | ".join(str(val).ljust(widths[i]) for i, val in enumerate(row)) for row in rows]
    return f"{header_str}\n{sep_str}\n" + "\n".join(row_strs)


def main():
    parser = argparse.ArgumentParser(description="NeuralFlow CLI Utility")
    parser.add_argument("--url", default="http://127.0.0.1:8000", help="NeuralFlow backend URL")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    subparsers.add_parser("health", help="Check server health")
    subparsers.add_parser("status", help="Get hardware and device status")
    subparsers.add_parser("summary", help="Display model architecture summary")
    subparsers.add_parser("metrics", help="Display comparative performance metrics")
    
    predict_parser = subparsers.add_parser("predict", help="Run live PyTorch inference")
    predict_parser.add_argument("--image", default="IMG-10", help="Sample Image ID (e.g. IMG-10)")
    predict_parser.add_argument("--trajectory", type=float, default=0.0, help="Sequence trajectory offset")

    args = parser.parse_args()

    client = NeuralFlowClient(base_url=args.url)

    if not args.command or args.command == "health":
        try:
            h = client.health_check()
            print(f"[NeuralFlow] Status: {h.get('status', 'OK')} | Version: {h.get('version')} | Uptime: {h.get('uptime_seconds')}s")
        except Exception as e:
            print(f"[Error] {e}")
            sys.exit(1)

    elif args.command == "status":
        try:
            s = client.get_status()
            print(f"[NeuralFlow Status]\nDevice: {s.get('device')}\nPyTorch: {s.get('torch_version')}\nModels: {s.get('models_loaded')}")
        except Exception as e:
            print(f"[Error] {e}")
            sys.exit(1)

    elif args.command == "summary":
        try:
            summary = client.get_model_summary()
            headers = ["Model", "Parameters", "Layers", "Hidden Dim", "Memory (MB)"]
            rows = []
            for name, details in summary.items():
                rows.append([
                    name,
                    f"{details.get('total_parameters', 0):,}",
                    details.get('num_layers', 2),
                    details.get('hidden_dim', 64),
                    f"{details.get('memory_mb', 0):.2f}"
                ])
            print("\n" + format_table(headers, rows) + "\n")
        except Exception as e:
            print(f"[Error] {e}")
            sys.exit(1)

    elif args.command == "metrics":
        try:
            metrics = client.get_metrics()
            headers = ["Model", "Accuracy (%)", "F1 Score", "Precision", "Recall", "Latency (ms)"]
            rows = []
            for name, m in metrics.items():
                rows.append([
                    name,
                    f"{m.get('accuracy', 0)*100:.2f}%",
                    f"{m.get('f1_score', 0):.4f}",
                    f"{m.get('precision', 0):.4f}",
                    f"{m.get('recall', 0):.4f}",
                    f"{m.get('latency_ms', 0):.2f} ms"
                ])
            print("\n" + format_table(headers, rows) + "\n")
        except Exception as e:
            print(f"[Error] {e}")
            sys.exit(1)

    elif args.command == "predict":
        try:
            res = client.predict(image_id=args.image, trajectory=args.trajectory)
            print(f"\n[NeuralFlow Inference Results for {args.image}]")
            preds = res.get("predictions", {})
            headers = ["Model Architecture", "Predicted Class", "Confidence"]
            rows = []
            for model_name, p in preds.items():
                rows.append([
                    model_name,
                    p.get("predicted_class", "N/A"),
                    f"{p.get('confidence', 0)*100:.2f}%"
                ])
            print(format_table(headers, rows) + "\n")
        except Exception as e:
            print(f"[Error] {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
