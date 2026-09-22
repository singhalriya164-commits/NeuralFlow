/**
 * NeuralFlow JavaScript API Client SDK
 * Browser & Node.js compatible
 */
class NeuralFlowAPIClient {
    constructor(baseUrl = '') {
        this.baseUrl = baseUrl.replace(/\/$/, '');
    }

    async _fetch(endpoint, params = {}) {
        let url = `${this.baseUrl}${endpoint}`;
        const query = new URLSearchParams(params).toString();
        if (query) url += `?${query}`;

        const res = await fetch(url);
        if (!res.ok) {
            throw new Error(`NeuralFlow API Error: ${res.status} ${res.statusText}`);
        }
        return await res.json();
    }

    async getHealth() {
        return this._fetch('/healthz');
    }

    async getStatus() {
        return this._fetch('/api/status');
    }

    async getSummary() {
        return this._fetch('/api/summary');
    }

    async getMetrics() {
        return this._fetch('/api/metrics');
    }

    async getHistory() {
        return this._fetch('/api/history');
    }

    async getGradients() {
        return this._fetch('/api/gradients');
    }

    async predict(imageId = 'IMG-10', trajectory = 0, seed = 42) {
        return this._fetch('/api/predict', { image_id: imageId, trajectory, seed });
    }

    async getConclusion() {
        return this._fetch('/api/live-conclusion');
    }
}

// Export for ES Module, CommonJS, and Window
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { NeuralFlowAPIClient };
} else if (typeof window !== 'undefined') {
    window.NeuralFlowAPIClient = NeuralFlowAPIClient;
}
