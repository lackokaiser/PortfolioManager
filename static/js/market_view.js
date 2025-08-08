async function getStockData() {
    const symbol = document.getElementById("symbol").value.trim().toUpperCase();
    const period = document.getElementById("period").value;

    if (!symbol) { 
        alert("Please enter a stock symbol.");
        return;
    }

    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = ""; // Clear previous results

    try {
        // Pass period as a query parameter
        const response = await fetch(`/api/v1/stocks/${symbol}/${period}`);
        if (!response.ok) throw new Error("Failed to fetch stock data.");
        const data = await response.json();

        if (!data || data.length === 0) {
            resultDiv.textContent = "No data found.";
            return;
        }

        const section = document.createElement("div");
        section.className = "stock-section";

        // Create Chart
        const canvas = document.createElement("canvas");
        canvas.id = `chart-${symbol}`;
        section.appendChild(canvas);

        const ctx = canvas.getContext("2d");
        const labels = data.map(point => {
            const date = new Date(point.Date);
            return date.toLocaleDateString('en-US', { 
                month: 'short', 
                day: 'numeric',
            });
        });            
        const priceChanges = data.map((row, i) => {
            if (i === 0) return 0;
            return +(row.Close - data[i-1].Close).toFixed(2);
        });

        new Chart(ctx, {
            type: "line",
            data: {
                labels: labels,
                datasets: [{
                    label: `${symbol} Daily Price Change`,
                    data: priceChanges,
                    borderColor: "green",
                    fill: false,
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: true } },
                scales: {
                    x: { title: { display: true, text: "Date" } },
                    y: { title: { display: true, text: "Price Change (USD)" } }
                }
            }
        });

        // Create Table
        const headers = Object.keys(data[0]);
        const table = document.createElement("table");
        const thead = document.createElement("thead");
        const tbody = document.createElement("tbody");

        const headerRow = document.createElement("tr");
        headers.forEach(h => {
            const th = document.createElement("th");
            th.textContent = h;
            headerRow.appendChild(th);
        });
        thead.appendChild(headerRow);
        table.appendChild(thead);

        data.forEach(row => {
            const tr = document.createElement("tr");
            headers.forEach(h => {
                const td = document.createElement("td");
                const value = row[h];
                td.textContent = typeof value === "number" ? value.toFixed(2) : value;
                tr.appendChild(td);
            });
            tbody.appendChild(tr);
        });
        table.appendChild(tbody);

        section.appendChild(table);
        resultDiv.appendChild(section);

    } catch (err) {
        console.error(err);
        resultDiv.textContent = `Error: ${err.message}`;
    }
}