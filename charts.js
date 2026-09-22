/**
 * NEURALFLOW — Research-Grade Analytics Charts
 * Library: Chart.js
 * Design: Minimal, data-driven, publication quality. Zero emojis.
 */

const CHART_COLORS = {
    vanilla: {
        primary: '#E11D48',
        bg: 'rgba(225, 29, 72, 0.12)',
        border: '#E11D48'
    },
    birnn: {
        primary: '#7C3AED',
        bg: 'rgba(124, 58, 237, 0.12)',
        border: '#7C3AED'
    },
    lstm: {
        primary: '#2563EB',
        bg: 'rgba(37, 99, 235, 0.12)',
        border: '#2563EB'
    },
    gru: {
        primary: '#059669',
        bg: 'rgba(5, 150, 105, 0.12)',
        border: '#059669'
    },
    grid: '#E2E8F0',
    text: '#475569',
    textMuted: '#94A3B8'
};

const CHART_DEFAULTS = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: 'top',
            labels: {
                boxWidth: 12,
                font: { family: "'Inter', sans-serif", size: 12, weight: '500' },
                color: CHART_COLORS.text
            }
        },
        tooltip: {
            backgroundColor: '#0F172A',
            titleFont: { family: "'Inter', sans-serif", size: 12, weight: '600' },
            bodyFont: { family: "'Inter', sans-serif", size: 12 },
            padding: 10,
            cornerRadius: 4
        }
    },
    scales: {
        x: {
            grid: { color: 'rgba(226, 232, 240, 0.6)' },
            ticks: { font: { family: "'Inter', sans-serif", size: 11 }, color: CHART_COLORS.text }
        },
        y: {
            grid: { color: 'rgba(226, 232, 240, 0.6)' },
            ticks: { font: { family: "'Inter', sans-serif", size: 11 }, color: CHART_COLORS.text }
        }
    }
};

const chartInstances = {};

function destroyChart(id) {
    if (chartInstances[id]) {
        chartInstances[id].destroy();
        delete chartInstances[id];
    }
}

/**
 * 1. Overview Performance Chart (Accuracy vs F1-Score)
 */
function renderOverviewPerformanceChart(canvasId, summaryData) {
    destroyChart(canvasId);
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    const models = ['Vanilla RNN', 'Bidirectional RNN', 'LSTM', 'GRU'];
    const accuracies = models.map(m => {
        const item = summaryData.consolidated_table.find(r => r.model === m);
        return item ? Number(item.accuracy.toFixed(2)) : 0;
    });
    const f1Scores = models.map(m => {
        const item = summaryData.consolidated_table.find(r => r.model === m);
        return item ? Number(item.f1_macro.toFixed(2)) : 0;
    });

    chartInstances[canvasId] = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: models,
            datasets: [
                {
                    label: 'Test Accuracy (%)',
                    data: accuracies,
                    backgroundColor: '#2563EB',
                    borderRadius: 4,
                    barPercentage: 0.6,
                    categoryPercentage: 0.7
                },
                {
                    label: 'Macro F1-Score (%)',
                    data: f1Scores,
                    backgroundColor: '#0EA5E9',
                    borderRadius: 4,
                    barPercentage: 0.6,
                    categoryPercentage: 0.7
                }
            ]
        },
        options: {
            ...CHART_DEFAULTS,
            scales: {
                ...CHART_DEFAULTS.scales,
                y: {
                    ...CHART_DEFAULTS.scales.y,
                    beginAtZero: true,
                    max: 45,
                    title: { display: true, text: 'Percentage (%)', font: { size: 11, weight: '600' } }
                }
            }
        }
    });
}

/**
 * 2. Overview Computational Cost (Parameters & Training Time)
 */
function renderOverviewComputeChart(canvasId, summaryData) {
    destroyChart(canvasId);
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    const models = ['Vanilla RNN', 'Bidirectional RNN', 'LSTM', 'GRU'];
    const params = models.map(m => summaryData.parameters[m]?.total_parameters || 0);
    const times = models.map(m => Number((summaryData.training_times[m] || 0).toFixed(1)));

    chartInstances[canvasId] = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: models,
            datasets: [
                {
                    label: 'Trainable Parameters',
                    data: params,
                    backgroundColor: 'rgba(124, 58, 237, 0.85)',
                    yAxisID: 'yParams',
                    borderRadius: 4,
                    barPercentage: 0.5
                },
                {
                    label: 'Training Time (s)',
                    data: times,
                    backgroundColor: 'rgba(245, 158, 11, 0.85)',
                    yAxisID: 'yTime',
                    borderRadius: 4,
                    barPercentage: 0.5
                }
            ]
        },
        options: {
            ...CHART_DEFAULTS,
            scales: {
                x: CHART_DEFAULTS.scales.x,
                yParams: {
                    type: 'linear',
                    position: 'left',
                    grid: { color: 'rgba(226, 232, 240, 0.6)' },
                    title: { display: true, text: 'Parameter Count', font: { size: 11, weight: '600' } }
                },
                yTime: {
                    type: 'linear',
                    position: 'right',
                    grid: { drawOnChartArea: false },
                    title: { display: true, text: 'Training Time (s)', font: { size: 11, weight: '600' } }
                }
            }
        }
    });
}

/**
 * 3. Overview Gradient Stability Across Epochs
 */
function renderOverviewGradientChart(canvasId, historyData) {
    destroyChart(canvasId);
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    const epochs = Array.from({ length: 25 }, (_, i) => i + 1);

    chartInstances[canvasId] = new Chart(ctx, {
        type: 'line',
        data: {
            labels: epochs,
            datasets: [
                {
                    label: 'Vanilla RNN',
                    data: historyData['Vanilla RNN']?.grad_norm || [],
                    borderColor: CHART_COLORS.vanilla.primary,
                    backgroundColor: 'transparent',
                    borderWidth: 2,
                    pointRadius: 2,
                    tension: 0.2
                },
                {
                    label: 'Bidirectional RNN',
                    data: historyData['Bidirectional RNN']?.grad_norm || [],
                    borderColor: CHART_COLORS.birnn.primary,
                    backgroundColor: 'transparent',
                    borderWidth: 2,
                    pointRadius: 2,
                    tension: 0.2
                },
                {
                    label: 'LSTM',
                    data: historyData['LSTM']?.grad_norm || [],
                    borderColor: CHART_COLORS.lstm.primary,
                    backgroundColor: 'transparent',
                    borderWidth: 2,
                    pointRadius: 2,
                    tension: 0.2
                },
                {
                    label: 'GRU',
                    data: historyData['GRU']?.grad_norm || [],
                    borderColor: CHART_COLORS.gru.primary,
                    backgroundColor: 'transparent',
                    borderWidth: 2,
                    pointRadius: 2,
                    tension: 0.2
                }
            ]
        },
        options: {
            ...CHART_DEFAULTS,
            scales: {
                x: {
                    ...CHART_DEFAULTS.scales.x,
                    title: { display: true, text: 'Epoch', font: { size: 11, weight: '600' } }
                },
                y: {
                    ...CHART_DEFAULTS.scales.y,
                    title: { display: true, text: 'Mean Gradient Norm (||g||)', font: { size: 11, weight: '600' } },
                    beginAtZero: true
                }
            }
        }
    });
}

/**
 * 4. Overview Training & Validation Loss Curves
 */
function renderOverviewLossChart(canvasId, historyData) {
    destroyChart(canvasId);
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    const epochs = Array.from({ length: 25 }, (_, i) => i + 1);

    chartInstances[canvasId] = new Chart(ctx, {
        type: 'line',
        data: {
            labels: epochs,
            datasets: [
                {
                    label: 'Vanilla RNN (Train)',
                    data: historyData['Vanilla RNN']?.train_loss || [],
                    borderColor: CHART_COLORS.vanilla.primary,
                    borderWidth: 1.5,
                    pointRadius: 0,
                    tension: 0.1
                },
                {
                    label: 'Vanilla RNN (Val)',
                    data: historyData['Vanilla RNN']?.val_loss || [],
                    borderColor: CHART_COLORS.vanilla.primary,
                    borderDash: [4, 4],
                    borderWidth: 1.5,
                    pointRadius: 0,
                    tension: 0.1
                },
                {
                    label: 'BiRNN (Train)',
                    data: historyData['Bidirectional RNN']?.train_loss || [],
                    borderColor: CHART_COLORS.birnn.primary,
                    borderWidth: 1.5,
                    pointRadius: 0,
                    tension: 0.1
                },
                {
                    label: 'BiRNN (Val)',
                    data: historyData['Bidirectional RNN']?.val_loss || [],
                    borderColor: CHART_COLORS.birnn.primary,
                    borderDash: [4, 4],
                    borderWidth: 1.5,
                    pointRadius: 0,
                    tension: 0.1
                },
                {
                    label: 'LSTM (Train)',
                    data: historyData['LSTM']?.train_loss || [],
                    borderColor: CHART_COLORS.lstm.primary,
                    borderWidth: 1.5,
                    pointRadius: 0,
                    tension: 0.1
                },
                {
                    label: 'LSTM (Val)',
                    data: historyData['LSTM']?.val_loss || [],
                    borderColor: CHART_COLORS.lstm.primary,
                    borderDash: [4, 4],
                    borderWidth: 1.5,
                    pointRadius: 0,
                    tension: 0.1
                },
                {
                    label: 'GRU (Train)',
                    data: historyData['GRU']?.train_loss || [],
                    borderColor: CHART_COLORS.gru.primary,
                    borderWidth: 1.5,
                    pointRadius: 0,
                    tension: 0.1
                },
                {
                    label: 'GRU (Val)',
                    data: historyData['GRU']?.val_loss || [],
                    borderColor: CHART_COLORS.gru.primary,
                    borderDash: [4, 4],
                    borderWidth: 1.5,
                    pointRadius: 0,
                    tension: 0.1
                }
            ]
        },
        options: {
            ...CHART_DEFAULTS,
            scales: {
                x: {
                    ...CHART_DEFAULTS.scales.x,
                    title: { display: true, text: 'Epoch', font: { size: 11, weight: '600' } }
                },
                y: {
                    ...CHART_DEFAULTS.scales.y,
                    title: { display: true, text: 'Cross-Entropy Loss', font: { size: 11, weight: '600' } }
                }
            }
        }
    });
}

/**
 * 5. Performance Page Charts: Metric Bars
 */
function renderMetricBarChart(canvasId, title, metricKey, metricsData, isPercent = true) {
    destroyChart(canvasId);
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    const models = ['Vanilla RNN', 'Bidirectional RNN', 'LSTM', 'GRU'];
    const colors = [
        CHART_COLORS.vanilla.primary,
        CHART_COLORS.birnn.primary,
        CHART_COLORS.lstm.primary,
        CHART_COLORS.gru.primary
    ];

    const values = models.map(m => {
        const val = metricsData[m]?.[metricKey] || 0;
        return Number(val.toFixed(2));
    });

    chartInstances[canvasId] = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: models,
            datasets: [{
                label: title,
                data: values,
                backgroundColor: colors,
                borderRadius: 4,
                barPercentage: 0.55
            }]
        },
        options: {
            ...CHART_DEFAULTS,
            plugins: {
                ...CHART_DEFAULTS.plugins,
                legend: { display: false }
            },
            scales: {
                ...CHART_DEFAULTS.scales,
                y: {
                    ...CHART_DEFAULTS.scales.y,
                    beginAtZero: true,
                    title: { display: true, text: isPercent ? 'Percentage (%)' : 'Value', font: { size: 11, weight: '600' } }
                }
            }
        }
    });
}

/**
 * 6. Gradient Distribution Chart (Min, Mean, Max)
 */
function renderGradientDistributionChart(canvasId, gradData) {
    destroyChart(canvasId);
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    const models = ['Vanilla RNN', 'Bidirectional RNN', 'LSTM', 'GRU'];
    const minVals = models.map(m => Number((gradData[m]?.min_grad_norm || 0).toFixed(4)));
    const meanVals = models.map(m => Number((gradData[m]?.mean_grad_norm || 0).toFixed(4)));
    const maxVals = models.map(m => Number((gradData[m]?.max_grad_norm || 0).toFixed(4)));

    chartInstances[canvasId] = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: models,
            datasets: [
                {
                    label: 'Min Norm',
                    data: minVals,
                    backgroundColor: '#0EA5E9',
                    borderRadius: 4
                },
                {
                    label: 'Mean Norm',
                    data: meanVals,
                    backgroundColor: '#2563EB',
                    borderRadius: 4
                },
                {
                    label: 'Max Norm',
                    data: maxVals,
                    backgroundColor: '#F59E0B',
                    borderRadius: 4
                }
            ]
        },
        options: {
            ...CHART_DEFAULTS,
            scales: {
                ...CHART_DEFAULTS.scales,
                y: {
                    ...CHART_DEFAULTS.scales.y,
                    beginAtZero: true,
                    title: { display: true, text: 'Gradient L2 Norm (||g||)', font: { size: 11, weight: '600' } }
                }
            }
        }
    });
}

/**
 * 7. Training Analysis Interactive Curves
 */
function renderTrainingCurves(lossCanvasId, accCanvasId, gradCanvasId, selectedModel, historyData) {
    const epochs = Array.from({ length: 25 }, (_, i) => i + 1);

    // Destroy existing
    destroyChart(lossCanvasId);
    destroyChart(accCanvasId);
    destroyChart(gradCanvasId);

    const lossCtx = document.getElementById(lossCanvasId);
    const accCtx = document.getElementById(accCanvasId);
    const gradCtx = document.getElementById(gradCanvasId);

    const isAll = selectedModel === 'ALL';
    const modelsToRender = isAll ? ['Vanilla RNN', 'Bidirectional RNN', 'LSTM', 'GRU'] : [selectedModel];

    const modelColors = {
        'Vanilla RNN': CHART_COLORS.vanilla.primary,
        'Bidirectional RNN': CHART_COLORS.birnn.primary,
        'LSTM': CHART_COLORS.lstm.primary,
        'GRU': CHART_COLORS.gru.primary
    };

    // 1. Loss Chart
    if (lossCtx) {
        const lossDatasets = [];
        modelsToRender.forEach(m => {
            lossDatasets.push({
                label: `${m} (Train)`,
                data: historyData[m]?.train_loss || [],
                borderColor: modelColors[m],
                borderWidth: 2,
                pointRadius: isAll ? 0 : 2,
                tension: 0.15
            });
            lossDatasets.push({
                label: `${m} (Val)`,
                data: historyData[m]?.val_loss || [],
                borderColor: modelColors[m],
                borderDash: [5, 4],
                borderWidth: 1.8,
                pointRadius: isAll ? 0 : 2,
                tension: 0.15
            });
        });

        chartInstances[lossCanvasId] = new Chart(lossCtx, {
            type: 'line',
            data: { labels: epochs, datasets: lossDatasets },
            options: {
                ...CHART_DEFAULTS,
                scales: {
                    x: { ...CHART_DEFAULTS.scales.x, title: { display: true, text: 'Epoch', font: { size: 11, weight: '600' } } },
                    y: { ...CHART_DEFAULTS.scales.y, title: { display: true, text: 'Loss', font: { size: 11, weight: '600' } } }
                }
            }
        });
    }

    // 2. Accuracy Chart
    if (accCtx) {
        const accDatasets = [];
        modelsToRender.forEach(m => {
            accDatasets.push({
                label: `${m} (Train Acc)`,
                data: historyData[m]?.train_acc || [],
                borderColor: modelColors[m],
                borderWidth: 2,
                pointRadius: isAll ? 0 : 2,
                tension: 0.15
            });
            accDatasets.push({
                label: `${m} (Val Acc)`,
                data: historyData[m]?.val_acc || [],
                borderColor: modelColors[m],
                borderDash: [5, 4],
                borderWidth: 1.8,
                pointRadius: isAll ? 0 : 2,
                tension: 0.15
            });
        });

        chartInstances[accCanvasId] = new Chart(accCtx, {
            type: 'line',
            data: { labels: epochs, datasets: accDatasets },
            options: {
                ...CHART_DEFAULTS,
                scales: {
                    x: { ...CHART_DEFAULTS.scales.x, title: { display: true, text: 'Epoch', font: { size: 11, weight: '600' } } },
                    y: {
                        ...CHART_DEFAULTS.scales.y,
                        title: { display: true, text: 'Accuracy (%)', font: { size: 11, weight: '600' } },
                        beginAtZero: true
                    }
                }
            }
        });
    }

    // 3. Gradient Norm Chart
    if (gradCtx) {
        const gradDatasets = modelsToRender.map(m => ({
            label: `${m} Gradient Norm`,
            data: historyData[m]?.grad_norm || [],
            borderColor: modelColors[m],
            borderWidth: 2,
            pointRadius: isAll ? 0 : 2,
            tension: 0.15
        }));

        chartInstances[gradCanvasId] = new Chart(gradCtx, {
            type: 'line',
            data: { labels: epochs, datasets: gradDatasets },
            options: {
                ...CHART_DEFAULTS,
                scales: {
                    x: { ...CHART_DEFAULTS.scales.x, title: { display: true, text: 'Epoch', font: { size: 11, weight: '600' } } },
                    y: {
                        ...CHART_DEFAULTS.scales.y,
                        title: { display: true, text: '||g||', font: { size: 11, weight: '600' } },
                        beginAtZero: true
                    }
                }
            }
        });
    }
}
