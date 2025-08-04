async function fetchStocks() {
    try {
        const response = await fetch('/api/portfolio'); // Call the API endpoint
        const passwords = await response.json(); // Parse the JSON response
        const tableBody = document.getElementById('portfolio-table-body');

        tableBody.innerHTML = '';

        // Populate the table with data
        passwords.forEach(password => {
            console.log(password)
            const row = document.createElement('tr');
            row.innerHTML = `<td>${password.name}</td><td>${password.ticker}</td><td>${password.value}</td><td>${password.quantity}</td>
           <td> <input class="sell-input" type="number" id="sellQuantity-${password.ticker}" name="sellQuantity" min="0" max='${password.quantity}' />
             <button class="sell-styled" type="button" onclick="sellStock('${password.ticker}', document.getElementById('sellQuantity-${password.ticker}').value)">Sell</button></td>`;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error('Error fetching passwords:', error);
    }
}

async function sellStock(ticker,amount) {
    try {
        const response = await fetch(`/api/v1/${ticker}/sell/${amount}`, {
            method: 'PUT'
        });

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

function validateInput(input) {
    if (/[^a-zA-Z0-9]/.test(input)) {
        alert('Only alphanumeric characters are allowed.');
        return false;
    }
    else return true;
}


// Fetch passwords when the page loads
window.onload = fetchStocks;