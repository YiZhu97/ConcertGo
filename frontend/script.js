let venue_mapping = null
let mymap = null
function prepareMap(){
    mymap = L.map('sm_map').setView([34.0195, -118.4912], 15);
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: 'pk.eyJ1IjoiY29uY2VydGdvIiwiYSI6ImNrYml4cmlsMzBqc28yc3BteHBwN3Z0NjYifQ.WanmAKDYkCYVKWvUvKe-Vw'
    }).addTo(mymap);
}

function deleteMap(){
    mymap.remove()
}
function onLoad(){
    prepareMap()
    const venue_url = "http://54.144.49.125:5000/venues"
    const venue_list = document.getElementById('venues')
    console.log("Start")

    $.ajax({
        url : venue_url,
        type: 'GET',
        dataType: 'JSON',
        success: function(data){
            if(data){
                venue_mapping = data
                console.log(data)
                onVenueCallBack(data)
            }
        },
        error: (request, status, error) => {
            console.log(error, status, request);
        }
    });
    function onVenueCallBack(data){
        for(let i=0;i<data.length;i++) {
            //venue_mapping[data[i]['name']] = data[i]['id']
            let row = document.createElement('option')
            row.setAttribute("value",data[i]['name'])
            //row.innerHTML = data[i]['name']
            venue_list.appendChild(row)
        }
    }
}
function createTable(){
    var table = document.createElement('table')
    table.setAttribute("id","parking-table")
    document.body.appendChild(table)
    var header = table.createTHead();
    var row = header.insertRow(0);
    var cell = row.insertCell(0);
    cell.innerHTML = "Parking Lot&nbsp&nbsp&nbsp&nbsp&nbsp"
    var cell = row.insertCell(1);
    cell.innerHTML = "Recommend Time(min)"
}
function deleteTable(){
    var elem = document.getElementById("parking-table");
    if (elem){
        elem.parentNode.removeChild(elem);
    }

}
function onSubmit(){
    deleteTable()
    createTable()
    //console.log(venue_mapping)
    deleteMap()
    prepareMap()

    const event_name = document.getElementById("event-name").value
    const city = document.getElementById("city").value
    const venue_selected = document.getElementById('event-venue').value
    const time = document.getElementById("event-time").value
    const parking_table = document.getElementById("parking-table")
    let venue_record
    for (let venue of venue_mapping){
        if (venue['name']==venue_selected){
            venue_record = venue
            break;
        }
    }

    let data_submit = {}
    console.log(venue_record)
    data_submit['time'] = time
    data_submit['lat'] = venue_record['lat']
    data_submit['event_name'] = event_name
    data_submit['long'] = venue_record['long']
    data_submit['venue'] = venue_record['name']
    data_submit['city'] = city
    let submitUrl = "http://54.144.49.125:5000/suggestion/parking"
    //let mymap = document.getElementById('sm_map');

    console.log(data_submit)
    $.get(submitUrl,
        data_submit,
        function(data, status){
            console.log(data)


            for (let parking of data){

                let name = parking["name"]
                let long = parking["long"]
                let lat = parking["lat"]
                let recommend = parking["recommend"]
                var marker = L.marker([lat, long]).addTo(mymap);
                marker.bindPopup("<b>Parking Lot:</b><br>"+name+"<br><b>Recommend Time:</b><br>"+recommend).openPopup();
                // var popup = L.popup()
                //     .setLatLng([lat, long])
                //     .setContent("name: "+name+"\nRecommend Time: "+ recommend)
                //     .openOn(mymap);
                // const row = document.createElement('tr')
                // const first = document.createElement('td')
                // var first_1 = document.createTextNode(parking)
                // first.appendChild(first_1)
                // const second = document.createElement('td')
                // var second_1 = document.createTextNode(data[parking])
                // second.append(second_1)
                // row.appendChild(first)
                // row.appendChild(second)
                //parking_table.appendChild(row)
            }
    });

}
