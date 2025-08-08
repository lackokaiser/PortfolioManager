let chart;

async function fetchStocks() {
    const response = fetchPortfolio(); // Fetch portfolio data first
    try {
        const response = await fetch('/api/v1/stock/feed'); // Call the API endpoint
        const passwords = await response.json(); // Parse the JSON response
        const tableBody = document.getElementById('portfolio-table-body');

        tableBody.innerHTML = '';

        // Populate the table with data
        passwords.forEach(password => {
            console.log(password)
            const row = document.createElement('tr');
            row.innerHTML = `<td>${password.name}</td><td>${password.ticker}</td><td>${password.currentValue}</td><td>${password.volumeCount}</td>
           <td> <input class="sell-input" type="decimal" id="sellQuantity-${password.ticker}" name="sellQuantity" min="0" max='${password.volumeCount}' />
             <button class="sell-styled" type="button" onclick="sellStock('${password.ticker}', document.getElementById('sellQuantity-${password.ticker}').value)">Sell</button></td>`;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error('Error fetching passwords:', error);
    }
}

async function sellStock(ticker,amount) {
    try {
        const response = await fetch(`/api/v1/stock/${ticker}/sell/${amount}`);
        if (response.ok) {
            console.log(`Successfully sold ${amount} of stock with ticker: ${ticker}`);
            fetchStocks();
        } else {
            console.error('Error selling stock:', response.statusText);
        }
    } catch (error) {
        console.error('Error selling stock:', error);
    }
}

async function searchStocks() {
    const ticker = document.getElementById('stock-search').value.toUpperCase();
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
        alert('Please enter a valid amount to buy');
        return;
    }
    fetch(`/api/v1/stock/${ticker}/buy/${amount}`)
    .then(response => {
        if (response.ok) {
            console.log(`Successfully bought ${amount} of stock with ticker: ${ticker}`);
            fetchStocks();
        } else {
            console.error('Error buying stock:', response.statusText);
        }
    })
    .catch(error => {
        console.error('Error buying stock:', error);
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
            // const history = data.history;
            const dates = data.map(point => point.Date);
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
                                text: 'Date'
                            }
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error("Error fetching portfolio performance data:", error);
            alert("Failed to load portfolio performance.");
        });
}