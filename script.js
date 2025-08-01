
    fetch('http://localhost:5000/api/data')
    .then(res => res.json())
    .then(data => console.log('GET response:', data));

//Helper function to create a table row with cells
// fucntion createRow(cells) {
//  const tr = document.creatElement('tr)
//   cells.forEach(text => {
//     const td = document.createElement('td); 
//      td.textContent = text
//      tr.appendChild(td);
// });
// return tr;
// }

// Fetch and display portfolio data
// async function loadPortfolio() {
// try {
//   const response = await fetch('http://localhost:5000/api/portfolio');
//   if (!response.ok) throw new Error('Failed to fetch portfolio');
//   const portfolio = await response.json();

//   const tbody = document.querySelector('portfolio-table tbody');
//   tbody.inerHTML = '': // clear existing rows


// portfolio.forEach(stock => {
// const gainLoss = ((stock.current_price - stock.avg_buy_price) * stock.shares).toFixed(2);
// const rows = creatRow([
//   stock.symbol, 
//   stock.shares, 
//   '$${stock.avg_boy_price.}
//])})