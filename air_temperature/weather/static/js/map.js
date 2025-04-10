document.addEventListener('DOMContentLoaded', () => {
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

    const apiKey = '';
    function fetchLocation(lat, lon) {
        const url = `https://api.opencagedata.com/geocode/v1/json?q=${lat}+${lon}&key=${apiKey}`;
        

    }
});
