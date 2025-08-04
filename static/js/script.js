document.addEventListener("DOMContentLoaded", () => {
    const select = document.getElementById("stock-select");
    const tableBody = document.querySelector("stock-tablebody");

    // function to fetch data from API and to generate table once selected 
    fetch('http://localhost:5000/api/data')
    .then(res => res.json())
    .then(data => console.log('GET response:', data));
    stocks.forEach(stock => {
        const option = document.createElement("option");
        option.value = stock.symbol;
        option.textContent = stock.name || stock.ticker;
        select.appendChild(option);
    });
});


// Handle selection change
select.addEventListener("change", async () => {
    const symbol = select.value;
    if (!symbol) return;

    try {
        const response = await fetch('http://localhost:5000/api/v1/stocks/${symbol}');
        const data = await response.json();

        tableBody.innerHTML = ""; // clear existing rows

        data.forEach(entry => {
            const row = createRow([
                entry.ticker,
                entry.stocks,
                entry.avg_buy_price,
                entry.current_price,
                entry.gain/loss,
                entry.buy,
                entry.sell,
            ]);
            tableBody.appendChild(row);
        });

    } catch (err) {
        console.error("Error loading stock data:", err);
    }
});

// default function to create table rows
function createRow(cells) {
    const tr = document.creatElement('tr')
        cells.forEach(cell => {
            const td = document.createElement('td'); 
                if (typeof cell === 'string' || typeof cell === 'number') {
                           td.textContent = cell          
                             } else if (cell instanceof HTMLElement) {
                                       td.appendChild(cell);
                                        }      
                                        tr.appendChild(td);
                                    });
                                    return tr;
                                }





function formatGainLoss(value) {
    const span = document.createElement('span');
    const formatted = '$${parseFloat(value).toFixed(2)}';
    span.textContent = formatted;
    span.style.color = value >= 0 ? 'green' : 'red';
    return span;
}


// function to load portfolio stock data 
async function loadPortfolio() {
    try {
        const response = await fetch('http://localhost:5000/api/v1/portfolio');
        const portfolio = await response.json();
        const tbody = document.querySelector('#portfolio-table tbody');
        tbody.inerHTML = ''; // clear existing rows
        
    
        portfolio.forEach(stock => {
            const gainLoss = ((stock.current_price - stock.avg_buy_price) * stock.shares).toFixed(2);
            const buyBtn = document.createElement('button');
            buyBtn.textContent = 'Buy';
            buyBtn.onclick = () => buyStock(stock.symbol, 1);
            
            const sellBtn = document.createElement('button');
                sellBtn.textContent = 'Sell';
                sellBtn.onclick = () => sellStock(stock.symbol, 1);
            
                const rows = creatRow([
                    stock.symbol, 
                    stock.shares, 
                    '$${stock.avg_buy_price.toFixed(2)}',
                    '$${stock.current_price.toFixed(2)}',
                    formatGainLoss(gainLoss),
                    buyBtn, 
                    sellBtn
                ]);
                tbody.appendChild(row);
            });
        } catch (error) {
            console.error('Error loading portfolo;', error);
        }
    }

// function to load yahoo finance live market data
async function loadMarketData() {
    try {
    const response = await fetch('http://localhost:5000/api/v1/stock/feed')
    if (!response.ok) throw new Error('Failed to fetch market data')
        const marketData = await response.json();
    
    const tbody = document.querySelector('#market-table tbdoy');
    tbody.innerHTML = '';
    
    marketData.forEach(stock => {
        const change = stock.change >= 0 ? '+${stock.change.toFixed(2)}' : stock.change.toFixed(2);
        const percentChange = stock.percent_change >= 0 ? '+${Stock.percent_change.toFixed(2)}%' : '${Stock.percent_change.toFixed(2)}%';
        
        const row = createRow([
            stock.symbol, 
            stock.company_name,
            '$${stock.price.toFixed(2)}',
            change, 
            percentChange
 ]);
 
 tbody.appendChild(row);

});
 } catch (error) {
    console.error('Error loading market data:', error);
}
}


// function to buy
async function buyStock(ticker, amount) {
    try {
        const res = await fetch('http://localhost:5000/api/v1/stock/${ticker}/buy/${amount}', {
            method: 'POST'
});

const result = await res.json();
console.log('Buy result:', result);
loadPortfolio();
} catch (error) {
console.error('Error buying stock:, error');
}
}

// function to sell 
async function sellStock(ticker, amount) {
try {
    const res = await fetch('http://localhost:5000/api/v1/stock/${ticker}/sell/${amount}', {
        method: 'POST'
});
const result = await res.json();
console.log('Sell result:', result);
loadPortfolio();
} catch(error) {
    console.error('Error selling stock:', error);
}
}

// load the page 
window.addEventListener('DOMContentLoaded', () => {
    loadPortfolio();
    loadMarketData();

// reset page ever 5 minutes 
setInterval(() => {
    loadPortfolio();
    loadMarketData();
},    5 * 60 *1000);
});

