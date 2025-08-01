
    fetch('http://localhost:5000/api/data')
    .then(res => res.json())
    .then(data => console.log('GET response:', data));

//Helper function to create a table row with cells
// fucntion createRow(cells) {
//  const tr = document.creatElement('tr)
//   cells.forEach(cell => {
//     const td = document.createElement('td); 
//     if (typeof cell === 'string' || typeof cell === 'number') {
//       td.textContent = cell           
//     } else if (cell instanceof HTMLElement) {
//       td.appendChild(cell);
//    }
//      
//      tr.appendChild(td);
// });
// return tr;
// }

// Format gain/loss with color
// function formatGainLoss(value) {
//   const span = document.createElement('span');
//   const formatted = '$${parseFloat(value).toFixed(2)}';
//   span.textContent = formatted;
//   span.style.color = valur >= 0 ? 'green' : 'red';
//   return span;
// }

// Fetch and display portfolio data

// async function loadPortfolio() {
// try {
//   const response = await fetch('http://localhost:5000/api/v1/portfolio');
//   const portfolio - await response.json();
//   const tbody = document.querySelector('#portfolio-table tbody');
//   tbody.inerHTML = '': // clear existing rows


// portfolio.forEach(stock => {
//   const gainLoss = ((stock.current_price - stock.avg_buy_price) * stock.shares).toFixed(2);
//   const buyBtn = document.createElement('button);
//   buyBTN.textContent = 'Buy';
//   buyBtn.onclick = () => buyStock(stock.symbol, 1);

//   const sellBtn = document.createElement('button);
//   sellBtn.textContent = 'Sell';
//   sellBtn.onclick = () => sellStock(stock.symbol, 1);

//   const rows = creatRow([
//   stock.symbol, 
//   stock.shares, 
//   '$${stock.avg_buy_price.toFixed(2)}',
//   '$${stock.current_price.toFixed(2)}',
//    formatGainLoss(gainLoss),
//    buyBtn, 
//    sellBtn
// ]);
// tbody.appendChild(row);
//});
// } catch (error) {
// console.error('Error loading portfolo;', error);
//}
//}

// fetch and display market data yahoo finance

// async function loadMarketData() {
// try
//   const response = await fetch('http://localhost:5000/api/v1/stock/feed')
//   if (!response.ok) throw new Error('Failed to fetch market data')
//   const marketData = await response.json();
//
//   const tbody = document.querySelector('#market-table tbdoy');
//   tbody.innerHTML = '';

//   marketData.forEach(stock => {
//   const change = stock.change >= 0 ? '+${stock.change.toFixed(2)}' : stock.change.toFixed(2);
//   const percentChange = stock.percent_change >= 0 ? '+${Stock.percent_change.toFixed(2)}%' : '${Stock.percent_change.toFixed(2)}%';
//   
//   const row = createRow([
//     stock.symbol, 
//     stock.company_name,
//     '$${stock.price.toFixed(2)}',
//     change, 
 //    percentChange
 //   ]);
 //   tbody.appendChild(row);
 // });
 // } catch (error) {
 //   console.error('Error loading market data:', error);
 // }
//}

// Buy Stock 
// async function buyStock(ticker, amount) {
//   try {
//     const res = await fetch('http://localhost:5000/api/v1/stock/${ticker}/buy/${amount}', {
//       method: 'POST'
//     });
//     const result = await res.json();
//     console.log('Buy result:', result);
//     loadPortfolio();
// } catch (error) {
//   console.error('Error buying stock:, error);
//  }
//}

// Sell stock
// async function sellStock(ticker, amount) {
//   try {
//     const res = await fetch('http://localhost:5000/api/v1/stock/${ticker}/sell/${amount}', {
//      method: 'POST'
//    });
//     const result = await res.json();
//     console.log('Sell result:', result);
//     loadPortfolio();
// } catch(error) {
//   console.error('Error selling stock:', error);
//  }
//}

// Initialize both tables
// window.addEventListener('DOMContentLoaded', () => {
//    loadPortfolio();
//    loadMarketData();

//   Auto refresh every 5 minutes - if we would like 
//    setInterval(() => {
//       loadPortfolio();
//       loadMarketData();
// },    5 * 60 *1000);
//});