let chart;

console.log("history.js loaded");  // Script running?

function loadStockHistory() {
    const ticker = document.getElementById('tickerInput').value.toUpperCase().trim().replace(/[^A-Z0-9.]/g, '');
    const time_mode = document.querySelector('input[name="mode"]:checked');

    console.log("loadStockHistory() called"); 

    if (!ticker) {
        alert('Please enter a stock ticker.');
        return;
    }

    if (!time_mode) {
        alert("Please select a time period.");
        return;
    }

    const mode = time_mode.value;
    console.log(`Ticker: ${ticker}, Mode: ${mode}`);  // Ticker and Mode?

    // Correct canvas element ID here:
    const ctx = document.getElementById('stockChart').getContext('2d');

    fetch(`/api/v1/stock/${ticker}/history/${mode}`)
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(data => {
            const history = data.history;
            console.log("Data received:", history);  

            const dates = history.map(point => {
                const date = new Date(point.Date);
                return date.toLocaleDateString('en-US', { 
                    month: 'short', 
                    day: 'numeric',
                });
            });            
            const prices = history.map(point => point.Close);

            if (chart) {
                chart.destroy();
            }


            chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: dates,
                    datasets: [{
                        label: `${data.ticker} Price`,
                        data: prices,
                        borderColor: 'blue',
                        fill: false,
                        tension: 0.3
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: `Stock Price History for ${data.ticker}`
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: false,
                            title: {
                                display: true,
                                text: 'Price (USD)'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Date'
                            }
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error("Error fetching stock data:", error);
            alert("Failed to load stock data.");
        });
}