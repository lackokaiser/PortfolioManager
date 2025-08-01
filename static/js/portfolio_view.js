async function fetchPasswords() {
    try {
        const response = await fetch('/api/portfolio'); // Call the API endpoint
        const passwords = await response.json(); // Parse the JSON response
        const tableBody = document.getElementById('portfolio-table-body');

        tableBody.innerHTML = '';

        // Populate the table with data
        passwords.forEach(password => {
            console.log(password)
            const row = document.createElement('tr');
            row.innerHTML = `<td>${password.name}</td><td>${password.ticker}</td><td>${password.value}</td><td>${password.quantity}</td>`;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error('Error fetching passwords:', error);
    }
}

// Fetch passwords when the page loads
window.onload = fetchPasswords;