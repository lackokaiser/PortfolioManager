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

// Fetch passwords when the page loads
window.onload = fetchStocks;