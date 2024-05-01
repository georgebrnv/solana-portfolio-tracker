let chart;

function initializeChart(data) {
    const canvas = document.getElementById('walletBalanceChart');

    const labels = data.map(snapshot => snapshot.timestamp_datetime || snapshot.day);
    const datasets = [{
        label: '',
        data: data.map(snapshot => snapshot.wallet_balance),
        fill: true,
        borderColor: 'green',
        backgroundColor: createGradient(canvas, ['rgba(4, 255, 0, 1)', 'rgba(4, 255, 0, 0)']),
        tension: 0.1
    }];

    chart = new Chart(canvas, {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            tooltip: {
                displayColors: false
            },
            plugins: {
                legend: {
                    display: false
                }
            },
            animation: {
                duration: 700,
                easing: 'easeInOutElastic',
            },
            scales: {
                x: {
                    display: false,
                },
                y: {
                    display: true,
                }
            },
        }
    });
}

function createGradient(canvas, colors) {
    const ctx = canvas.getContext('2d');
    const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height*2.6);
    gradient.addColorStop(0, colors[0]); // Start color
    gradient.addColorStop(1, colors[1]); // End color
    return gradient;
}

// Event listeners for switching between charts
document.getElementById('dayBtn').addEventListener('click', function() {
    setActiveButton(this);
    chart.destroy();
    initializeChart(walletSnapshotsData['day_1']);
});

document.getElementById('weekBtn').addEventListener('click', function() {
    setActiveButton(this);
    chart.destroy();
    initializeChart(walletSnapshotsData['week_1']);
});

document.getElementById('monthBtn').addEventListener('click', function() {
    setActiveButton(this);
    chart.destroy();
    initializeChart(walletSnapshotsData['month_1']);
});

document.getElementById('month3Btn').addEventListener('click', function() {
    setActiveButton(this);
    chart.destroy();
    initializeChart(walletSnapshotsData['month_3']);
});

document.getElementById('month6Btn').addEventListener('click', function() {
    setActiveButton(this);
    chart.destroy();
    initializeChart(walletSnapshotsData['month_6']);
});

document.getElementById('yearBtn').addEventListener('click', function() {
    setActiveButton(this);
    chart.destroy();
    initializeChart(walletSnapshotsData['year_1']);
});

window.onload = function() {
    initializeChart(walletSnapshotsData['day_1']);
};

function setActiveButton(clickedButton) {
    const buttons = document.querySelectorAll('.chart-btn');
    buttons.forEach(button => {
        button.classList.remove('btn-secondary', 'text-dark');
    });
    clickedButton.classList.add('btn-secondary', 'text-dark');
}