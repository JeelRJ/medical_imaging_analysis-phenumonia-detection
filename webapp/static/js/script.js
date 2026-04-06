document.addEventListener('DOMContentLoaded', () => {
    // Nav Elements
    const navDiag = document.getElementById('nav-diag');
    const navRecords = document.getElementById('nav-records');
    const navAnalytics = document.getElementById('nav-analytics');

    const diagTab = document.getElementById('diagnostic-tab');
    const recordsTab = document.getElementById('records-tab');
    const analyticsTab = document.getElementById('analytics-tab');

    // DOM Elements - Diagnostic
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const previewContainer = document.getElementById('preview-container');
    const previewImg = document.getElementById('preview-img');
    const analyzeBtn = document.getElementById('analyze-btn');
    const clearBtn = document.getElementById('clear-btn');
    const loadingOverlay = document.getElementById('loading-overlay');
    const resultsDisplay = document.getElementById('results-display');
    const resultsPlaceholder = document.getElementById('results-placeholder');
    const heatmapCanvas = document.getElementById('heatmap-canvas');

    // Chart Handles
    let charts = {
        probability: null,
        comparison: null,
        volume: null,
        accuracy: null,
        distribution: null
    };

    // --- TAB SWITCHING ---
    function switchTab(activeNav, activeTab) {
        [navDiag, navRecords, navAnalytics].forEach(n => n.classList.remove('active'));
        [diagTab, recordsTab, analyticsTab].forEach(t => t.classList.add('hidden'));

        activeNav.classList.add('active');
        activeTab.classList.remove('hidden');

        if (activeTab === recordsTab) loadRecords();
        if (activeTab === analyticsTab) loadAnalytics();
    }

    navDiag.onclick = () => switchTab(navDiag, diagTab);
    navRecords.onclick = () => switchTab(navRecords, recordsTab);
    navAnalytics.onclick = () => switchTab(navAnalytics, analyticsTab);

    // --- CHART INITIALIZATION (Diagnostic) ---

    function initProbChart(normal, pneumonia) {
        const ctx = document.getElementById('prob-chart').getContext('2d');
        if (charts.probability) charts.probability.destroy();

        charts.probability = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Normal', 'Pneumonia'],
                datasets: [{
                    data: [normal, pneumonia],
                    backgroundColor: ['#10b981', '#ef4444'],
                    borderRadius: 4
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { max: 100, ticks: { color: '#64748b' }, grid: { display: false } },
                    y: { ticks: { color: '#1e293b', font: { weight: '600' } } }
                }
            }
        });
    }

    function initComparisonChart(left, right) {
        const ctx = document.getElementById('lung-comparison-chart').getContext('2d');
        if (charts.comparison) charts.comparison.destroy();

        charts.comparison = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Left Lung', 'Right Lung'],
                datasets: [{
                    data: [left, right],
                    backgroundColor: ['#3b82f6', '#3b82f6'],
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { max: 100, ticks: { display: false }, grid: { display: false } },
                    x: { ticks: { color: '#64748b' } }
                }
            }
        });
    }

    // --- RECORDS TAB ---
    async function loadRecords() {
        try {
            const response = await fetch('/patients_data');
            const data = await response.json();
            const tableBody = document.getElementById('patients-table-body');
            tableBody.innerHTML = '';
            
            data.forEach(p => {
                const row = document.createElement('tr');
                row.style.borderBottom = '1px solid var(--border-light)';
                row.innerHTML = `
                    <td style="padding: 1rem; font-weight: 600;">PR-${p.id}</td>
                    <td style="padding: 1rem;">${p.name}</td>
                    <td style="padding: 1rem;"><span class="diagnosis-badge badge-${p.status.toLowerCase()}">${p.status}</span></td>
                    <td style="padding: 1rem; color: var(--text-muted);">${p.date}</td>
                    <td style="padding: 1rem;">
                        <a href="/download_report/${p.id}" target="_blank" style="color: var(--primary-blue); text-decoration: none;"><i class="fa-solid fa-file-pdf"></i> REPORT</a>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        } catch (error) {
            console.error('Failed to load records:', error);
        }
    }

    // --- ANALYTICS TAB ---
    async function loadAnalytics() {
        try {
            const response = await fetch('/analytics_data');
            const data = await response.json();

            // Volume Chart
            if (charts.volume) charts.volume.destroy();
            charts.volume = new Chart(document.getElementById('volumeChart'), {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Total Scans',
                        data: data.predictions,
                        borderColor: '#2563eb',
                        backgroundColor: 'rgba(37, 99, 235, 0.1)',
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
            });

            // Accuracy Chart
            if (charts.accuracy) charts.accuracy.destroy();
            charts.accuracy = new Chart(document.getElementById('accuracyChart'), {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Accuracy %',
                        data: data.accuracy,
                        backgroundColor: '#10b981',
                        borderRadius: 4
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
            });

            // Distribution Chart
            if (charts.distribution) charts.distribution.destroy();
            charts.distribution = new Chart(document.getElementById('distributionChart'), {
                type: 'doughnut',
                data: {
                    labels: Object.keys(data.distribution),
                    datasets: [{
                        data: Object.values(data.distribution),
                        backgroundColor: ['#22c55e', '#ef4444'],
                        borderWidth: 0
                    }]
                },
                options: { 
                    responsive: true, 
                    maintainAspectRatio: false,
                    plugins: { legend: { position: 'bottom' } }
                }
            });

        } catch (error) {
            console.error('Failed to load analytics:', error);
        }
    }

    // --- DIAGNOSTIC LOGIC ---
    function handleFiles(files) {
        if (files.length > 0) {
            const file = files[0];
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    previewImg.src = e.target.result;
                    previewContainer.classList.remove('hidden');
                    dropZone.classList.add('hidden');
                    resultsPlaceholder.classList.remove('hidden');
                    resultsDisplay.classList.add('hidden');
                };
                reader.readAsDataURL(file);
                currentFile = file;
            }
        }
    }

    let currentFile = null;

    dropZone.onclick = () => fileInput.click();
    fileInput.onchange = (e) => handleFiles(e.target.files);

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(evt => {
        dropZone.addEventListener(evt, e => {
            e.preventDefault();
            e.stopPropagation();
        });
    });

    dropZone.addEventListener('drop', e => handleFiles(e.dataTransfer.files));

    clearBtn.onclick = () => {
        previewContainer.classList.add('hidden');
        dropZone.classList.remove('hidden');
        previewImg.src = '';
        currentFile = null;
        resultsDisplay.classList.add('hidden');
        resultsPlaceholder.classList.remove('hidden');
    };

    analyzeBtn.onclick = async () => {
        if (!currentFile) return;

        const formData = new FormData();
        formData.append('file', currentFile);
        formData.append('patient_name', document.getElementById('patient-name').value || 'Anonymous');
        formData.append('patient_age', document.getElementById('patient-age').value || 0);

        loadingOverlay.classList.remove('hidden');

        try {
            const response = await fetch('/predict', { method: 'POST', body: formData });
            const data = await response.json();
            displayResults(data);
        } catch (error) {
            alert('Radiological analysis failed.');
        } finally {
            loadingOverlay.classList.add('hidden');
        }
    };

    function displayResults(data) {
        resultsPlaceholder.classList.add('hidden');
        resultsDisplay.classList.remove('hidden');

        const diagBadge = document.getElementById('diag-badge-main');
        const diagText = document.getElementById('diag-text-main');
        diagText.textContent = data.label;
        diagBadge.textContent = data.severity;
        diagBadge.className = `diagnosis-badge badge-${data.label.toLowerCase()}`;
        document.getElementById('last-updated').textContent = `Analysis Complete: ${new Date().toLocaleTimeString()} (Radiology v2.1)`;

        document.getElementById('summary-diag').textContent = data.label;
        document.getElementById('summary-conf').textContent = `${data.confidence}%`;
        document.getElementById('summary-region').textContent = data.affected_region || 'Both Lungs';
        document.getElementById('summary-rec').textContent = data.suggestion;
        document.getElementById('report-download-btn').href = data.report_url;

        initProbChart(data.label === 'NORMAL' ? data.confidence : 100 - data.confidence, 
                      data.label === 'PNEUMONIA' ? data.confidence : 100 - data.confidence);
        initComparisonChart(data.left_lung || 15, data.right_lung || 45); 
        
        document.getElementById('infection-area-text').textContent = `${data.infection_area || '4.2'}%`;

        if (data.heatmap_url) {
            overlayHeatmap(data.heatmap_url);
        }
    }

    function overlayHeatmap(url) {
        const ctx = heatmapCanvas.getContext('2d');
        const img = new Image();
        img.onload = () => {
            heatmapCanvas.width = previewImg.clientWidth;
            heatmapCanvas.height = previewImg.clientHeight;
            ctx.drawImage(img, 0, 0, heatmapCanvas.width, heatmapCanvas.height);
        };
        img.src = url;
    }
});
