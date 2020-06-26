function prepareMap(){
    var mymap = L.map('sm_map').setView([34.0195, -118.4912], 14);
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: 'pk.eyJ1IjoiY29uY2VydGdvIiwiYSI6ImNrYml4cmlsMzBqc28yc3BteHBwN3Z0NjYifQ.WanmAKDYkCYVKWvUvKe-Vw'
    }).addTo(mymap);
}
prepareMap()