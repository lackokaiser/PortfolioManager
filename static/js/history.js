/* need to test

let chartInstance = null;

function fetchAndRenderChart(ticker, mode) {
  const xValues = [];
  const yValues = [];

  fetch(`/api/v1/stock/${ticker}/history/${mode}`)
    .then(response => response.json())
    .then(data => {
      data.forEach(item => {
        xValues.push(item.date);
        yValues.push(item.close);
      });

      if (chartInstance) {
        chartInstance.destroy();
      }

      chartInstance = new Chart("myChart", {
        type: "line",
        data: {
          labels: xValues,
          datasets: [{
            label: `${ticker} Closing Price`,
            fill: false,
            pointRadius: 2,
            borderColor: "rgba(75,192,192,1)",
            data: yValues
          }]
        },
        options: {
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: `Stock Price History: ${ticker} (${mode.toUpperCase()})`
            }
          },
          scales: {
            x: {
              title: { display: true, text: "Date" }
            },
            y: {
              title: { display: true, text: "Price ($)" }
            }
          }
        }
      });
    })
    .catch(err => console.error("Error fetching chart data:", err));
}

document.addEventListener("DOMContentLoaded", () => {
  const tickerSelect = document.getElementById("tickerSelect");

  function updateChart() {
    const ticker = tickerSelect.value;
    const mode = document.querySelector('input[name="mode"]:checked').value;
    fetchAndRenderChart(ticker, mode);
  }

  tickerSelect.addEventListener("change", updateChart);
  document.querySelectorAll('input[name="mode"]').forEach(radio => {
    radio.addEventListener("change", updateChart);
  });

  fetchAndRenderChart("AAPL", "w");
});*/