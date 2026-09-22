# NeuralFlow Frontend

The **Frontend** category is a research-grade analytics and real-time deep learning inference dashboard for comparative analysis of recurrent neural network architectures (Vanilla RNN, Bi-RNN, LSTM, GRU).

## Structure
- `index.html`: Main Single Page Application interface with 8 analytical views.
- `style.css`: Modern high-contrast dark theme design system with glassmorphism.
- `dashboard.js`: Reactive state management, REST API fetch controllers, and inference handlers.
- `charts.js`: Lightweight, zero-dependency HTML5 canvas charting engine.
- `vercel.json`: Edge routing configuration and automatic API reverse proxying to Render backend.

## Deployment to Vercel
1. Install Vercel CLI (`npm install -g vercel`) or connect via [vercel.com](https://vercel.com).
2. Set the Root Directory to `frontend` (or deploy from repository root with root `vercel.json`).
3. Set your backend URL in `vercel.json` rewrites or configure environment variable `VITE_API_URL` / `API_BASE_URL`.
