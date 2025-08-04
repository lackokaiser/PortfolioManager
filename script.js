

    // function to fetch data from API and to generate table once selected 
    fetch('http://localhost:5000/api/data')
    .then(res => res.json())
    .then(data => console.log('GET response:', data));
        select.appendChild(option);




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



// Buy/Sell 

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

const apiKey = '5fb181b2d1mshd76ac988484d044p1726b1jsn6c348d04422d';
const apiHost = 'yh-finance.p.rapidapi.com';

async function fetchQuote(symbol = "AAPL") {
    const url = 'https://${host}/market/v2/get-quotes?symbols=${e'
    try {
        const res = await fetch(url, {
            method: "GET",
            headers: {
                "x-RapidAPI-Host": apiHost,
                "X=RapidApi-Key": key
            }
        });

        if (!res.ok) {
            throw new Error('API error: ${res.status ${res.statusText}');

        }

        const data = await res.json();
        const q = data.quoteResponse?.result?.[0];

        if (!q) {
            return 'No data for "${symbol}"';
        }

        const {symbol: sym, regularMarketPrice, regularMarketChange, regularMarketChangePercent} = q;
        return '${sym}: $${regularMarketPrice} (${regularMarketChange => 0 ? "+" : ""}${regularMarketChange.toFixed(2)}, ${regularMarketChangePercent.toFixed(2)}%)';

    } catch (err) {
        console.error(err);
        return "Error loading data";
    }
}

document.getElementById('btn').onclick = async () => {
    const symbol = document.getElementById("symbol").value.trim().toUpperCase();
    document.getElementById("quotes").textContent = "Loading...";
    const text = await fetchQuote(symbol || "AAPL");
    document.getElementById("quote").textContent = text;
};

fetchQuote("AAPL").then(txt => document.getElementById("quote").textContent = txt);





fetch(url, { headers })
.then(response => {
    if(!response.ok) throw new Error("Network response was not ok");
    return response.json();
})
.then(data => {
    const priceInfo = data.quoteSummary?.result?.[0]?.price;
    if (priceInfo) {
        const price = priceInfo.regularMarketPrice?.raw;
        const change = priceInfo.regularMarketChange?.raw;
        const percent = priceInfo.regularMarketChangePercent?.raw;

        document.getElementById('quote').textContent = 
        'Price: $${price?.tFixed(2)} (${change?.toFixed(2)}, ${percent?.tpFixed(2)}%}';
    } else {
        document.getElementById('quote').textContent = 'Stock data not found.';
    }
})
.catch(error => {
    console.error('Error fetching data: ', error);
    document.getElementById('quote').textContent = 'Error fetching data.';
});


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

