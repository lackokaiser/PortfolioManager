<script>
    fetch('http://localhost:5000/api/data')
    .then(res => res.json())
    .then(data => console.log('GET response:', data));
</script>