const express = require('express');
const cors = require('cors');
// const fetch = require('node-fetch');
const cheerio = require('cheerio');
const path = require('path');
const { json } = require('body-parser');


const app = express();
const PORT = 8000;

app.use(cors());


app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'yahoofinance.html'));
});


app.get('/api/stocks', async (req, res) => {
    try {
       const response = await fetch(`https://finance.yahoo.com/most-active`);
       const html = await response.text();
       const tableBody = document.getElementById('portfolio-table-body');
        if (!html) {
              return res.status(404).json({ error: 'No data found' });
         }       
       tableBody.innerHTML = '';

       html.forEach(stock => {
           const row = document.createElement('tr');
           row.innerHTML = `
               <td>${stock.symbol}</td><td>${stock.name}</td>
               <td>${stock.price}</td><td>${stock.change}</td>  
                <td>${stock.percentChange}</td><td>${stock.volume}</td>
                <td>${stock.avgVolume}</td><td>${stock.marketCap}</td>
                <td>${stock.peRatio}</td>
           `;
           tableBody.appendChild(row);
       });
       
    //    $('table.W(100%) tbody tr').each((i, el) => {
    //     const symbol = $(el).find('td:nth-child(1) a').text().trim();
    //     const name = $(el).find('td:nth-child(2)').text().trim();
    //     const price = $(el).find('td:nth-child(3)').text().trim();
    //     const change = $(el).find('td:nth-child(4)').text().trim();
    //     const percentChange = $(el).find('td:nth-child(5)').text().trim();
    //     const volume = $(el).find('td:nth-child(6)').text().trim();
    //     const avgVolume = $(el).find('td:nth-child(7)').text().trim();
    //     const marketCap = $(el).find('td:nth-child(8)').text().trim();
    //     const peRatio = $(el).find('td:nth-child(9)').text().trim();
        
    //     // rows.push({
    //     //     symbol,
        //     name,
        //     price,
        //     change,
        //     percentChange,
        //     volume,
        //     avgVolume,
        //     marketCap,
        //     peRatio
        // });
   
    
    res.json(rows);
} catch (error) {
    console.error('Error fetching data:', error)
    res.status(500).json({ error: 'Failed to fetch stock data' });
}

});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});

