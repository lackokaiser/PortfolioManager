
let chart;

async function fetchStocks() {
    try {
        const tableBody = document.getElementById('portfolio-table-body');
        tableBody.innerHTML = '<tr><td colspan="6" style="text-align: center;">Loading...</td></tr>';

        const response = await fetch('/api/v1/stock/feed');
        const portfolioData = await response.json();

        tableBody.innerHTML = '';

        // Use DocumentFragment for better performance when adding multiple elements
        const fragment = document.createDocumentFragment();
        
        portfolioData.forEach(stock => {
            const row = document.createElement('tr');
            
            // Determine PnL arrow and color
            const pnlValue = parseFloat(stock.pnl);
            let pnlDisplay = '';
            let pnlClass = '';
            
            if (pnlValue > 0) {
                pnlDisplay = `▲ $${pnlValue.toFixed(2)}`;
                pnlClass = 'pnl-positive';
            } else if (pnlValue < 0) {
                pnlDisplay = `▼ $${Math.abs(pnlValue).toFixed(2)}`;
                pnlClass = 'pnl-negative';
            } else {
                pnlDisplay = `— $0.00`;
                pnlClass = 'pnl-neutral';
            }
            
            row.innerHTML = `
                <td>${stock.name}</td>
                <td>${stock.ticker}</td>
                <td>$${stock.currentValue.toFixed(2)}</td>
                <td>${stock.volumeCount}</td>
                <td class="${pnlClass}">${pnlDisplay}</td>
                <td>
                    <input class="sell-input" type="number" 
                           id="sellQuantity-${stock.ticker}" 
                           name="sellQuantity" 
                           min="0" 
                           max="${stock.volumeCount}" 
                           step="0.001" />
                    <button class="sell-styled" type="button" 
                            onclick="sellStock('${stock.ticker}', document.getElementById('sellQuantity-${stock.ticker}').value)">
                        Sell
                    </button>
                </td>`;
            fragment.appendChild(row);
        });
        
        tableBody.appendChild(fragment);
    } catch (error) {
        console.error('Error fetching Stock Data:', error);
        const tableBody = document.getElementById('portfolio-table-body');
        tableBody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: red;">Error loading data</td></tr>';
        toastr.error('Failed to load portfolio data. Please try again.', 'Error');
    }
}

async function sellStock(ticker,amount) {
    try {
        const response = await fetch(`/api/v1/stock/${ticker}/sell/${amount}`);
        if (response.ok) {
            console.log(`Successfully sold ${amount} of stock with ticker: ${ticker}`);
            toastr.success(`Successfully sold ${amount} shares of ${ticker}`, 'Sale Complete');
            fetchStocks();
        } else {
            console.error('Error selling stock:', response.statusText);
        }
    } catch (error) {
        console.error('Error selling stock:', error);
        toastr.error(errorMessage, 'Sale Failed');
    }
}

async function searchStocks() {
    const ticker = document.getElementById('stock-search').value.trim().toUpperCase();
    console.log(ticker);
    if (!ticker || !validateInput(ticker)) {
        alert('Please enter a valid ticker symbol');
        return;
    }
    const tickerResponse = await fetch(`/api/v1/stock/${ticker}/point`);
    if (!tickerResponse.ok) {
        alert('Stock not found');
        return;
    }
    const tableBody = document.getElementById('search-results-body');

    tableBody.innerHTML = ''; // Clear existing rows
    const stockData = await tickerResponse.json();
    stockData.forEach(stock => {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${ticker}</td><td>${stock[ticker]}</td><td> <input class="buy-input" type="number" id="buyQuantity-${ticker}" name="buyQuantity" min="0" />
            <button class="buy-styled" type="button" onclick="buyStock('${ticker}', document.getElementById('buyQuantity-${ticker}').value)">Buy</button></td>`;
        // Append the row to the table body
        tableBody.appendChild(row);
    });
}

function buyStock(ticker, amount) {
    if (!amount || isNaN(amount) || amount <= 0) {
        toastr.warning('Please enter a valid amount to buy', 'Invalid Input');
        return;
    }
    fetch(`/api/v1/stock/${ticker}/buy/${amount}`)
    .then(response => {
        if (response.ok) {
            console.log(`Successfully bought ${amount} of stock with ticker: ${ticker}`);
            fetchStocks();
            const inputField = document.getElementById(`buyQuantity-${ticker}`);
            if (inputField) {
                inputField.value = '';
            }
            toastr.success(`Successfully bought ${amount} shares of ${ticker}`, 'Purchase Complete');
        } else {
            console.error('Error buying stock:', response.statusText);
        }
    })
    .catch(error => {
        console.error('Error buying stock:', error);
        toastr.error('Network error occurred while buying stock', 'Connection Error');
    });
}

function validateInput(input) {
    if (/[^a-zA-Z0-9]/.test(input)) {
        alert('Only alphanumeric characters are allowed.');
        return false;
    }
    else return true;
}

// Fetch passwords when the page loads
window.onload = fetchStocks;

function loadPortfolioPerformance() {
    const time_mode = document.querySelector('input[name="mode"]:checked');

    if (!time_mode) {
        alert("Please select a time period.");
        return;
    }

    const mode = time_mode.value;
    const ctx = document.getElementById('portfolioChart').getContext('2d');

    fetch(`/api/v1/portfolio/performance/${mode}`)
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(data => {
            const dates = data.map(point => {
                const date = new Date(point.Date);
                return date.toLocaleDateString('en-US', { 
                    month: 'short', 
                    day: 'numeric',
                    year: mode === 'year' ? 'numeric' : undefined 
                });
            });
            const values = data.map(point => point.Value);

            if (chart) {
                chart.destroy();
            }

            chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: dates,
                    datasets: [{
                        label: `Total Portfolio Value`,
                        data: values,
                        borderColor: 'green',
                        fill: false,
                        tension: 0.3
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: `Portfolio Performance (${mode.toUpperCase()})`
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: false,
                            title: {
                                display: true,
                                text: 'Total Value (USD)'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Date',
                            }
                        }
                    }
                }
            });
            toastr.info('Portfolio performance chart updated successfully', 'Chart Updated');

        })
        .catch(error => {
            console.error("Error fetching portfolio performance data:", error);
            alert("Failed to load portfolio performance.");
        });
}