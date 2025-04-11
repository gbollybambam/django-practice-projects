document.addEventListener('DOMContentLoaded', () => {
    console.log("API_KEY:", apiKey)
    var map = L.map('map').setView([51.505, -0.09], 13);

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    // navigator.geolocation.getCurrentPosition((position) => {
    //     const lat = position.coords.latitude;
    //     const lon = position.coords.longitude;

    //     map.setView([lat, lon, 13]);
    //     L.marker([lat, lon]).addTo(map).bindPopup("You are here").openPopup();
    // })

    const fetchLocation = async function (lat, lon) {
        const url = `https://api.opencagedata.com/geocode/v1/json?q=${lat}+${lon}&key=${apiKey}`;
        try {
            const response = await fetch(url);
            const data = await response.json();
            console.log(data)

            if (data.results && data.results.length > 0) {
                const location = data.results[0].formatted;

                map.setView([lat, lon], 13);
                L.marker([lat, lon]).addTo(map).bindPopup(`Location: ${location}`).openPopup();
            } else {
                alert('No location data found');
            }
        } catch(error) {
            console.log('Error fetching location data:', error);
        }

    }

    map.on('click', function (e) {
        const { lat, lng } = e.latlng;
        fetchLocation(lat, lng);
    });
});
