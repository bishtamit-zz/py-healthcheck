let fetchStatus = async () => {
    let data = await fetch('http://127.0.0.1:8000/status/loba')
    let json_data = await data.json();

    console.log(json_data)
}

fetchStatus()