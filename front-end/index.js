import 'ol/ol.css';
import Feature from 'ol/Feature';
import OSM from 'ol/source/OSM';
import Map from 'ol/Map';
import Overlay from 'ol/Overlay';
import View from 'ol/View';
import {toStringHDMS} from 'ol/coordinate';
import {toLonLat} from 'ol/proj';
import Point from 'ol/geom/Point';
import {Tile as TileLayer, Vector as VectorLayer} from 'ol/layer';
import {fromLonLat} from 'ol/proj';
import TileJSON from 'ol/source/TileJSON';
import VectorSource from 'ol/source/Vector';
import {Icon, Style} from 'ol/style';
import GeoJSON from 'ol/format/GeoJSON';
import { listenerCount } from 'cluster';
import { totalmem } from 'os';

let url = 'http://127.0.0.1:5000/api/v1/resources/json'
fetch(url).then(function(response) {
    return response.json();
  }).then(function(data) {

      fetch('http://127.0.0.1:5000/api/v1/resources/geojson').then(function(response) {
      return response.json();
    }).then(function(data) {
        var key = 'pk.eyJ1Ijoidmxhc3Rpa2N6ZWNoIiwiYSI6ImNrM3dmbHd6dzAxY3Qza3FtbTBjenc2ZGwifQ.En3JITruEXqtp8NCqxM-gA';

        /**
         * Elements that make up the popup.
         */
        var container = document.getElementById('popup');
        var content = document.getElementById('popup-content');
        var closer = document.getElementById('popup-closer');

        var geojsonObject = data
        var coordinates = geojsonObject['features'].map(el => {return el['geometry']['coordinates'] = fromLonLat([el['geometry']['coordinates'][0], el['geometry']['coordinates'][1]])})

        /**
         * Create an overlay to anchor the popup to the map.
         */
        var overlay = new Overlay({
          element: container,
          autoPan: true,
          autoPanAnimation: {
            duration: 250
          }
        });


        /**
         * Add a click handler to hide the popup.
         * @return {boolean} Don't follow the href.
         */
        closer.onclick = function() {
          overlay.setPosition(undefined);
          closer.blur();
          return false;
        };

        var vectorSource = new VectorSource({
        features: (new GeoJSON()).readFeatures(geojsonObject)
        });
    
        var vectorLayer = new VectorLayer({
        source: vectorSource
        });
        
        var rasterLayer = new TileLayer({
          source: new TileJSON({
            url: 'https://api.tiles.mapbox.com/v4/mapbox.natural-earth-hypso-bathy.json?access_token=' + key,
            crossOrigin: 'anonymous'
          })
        })
          
        const map = new Map({
          target: 'map',
          layers: [rasterLayer, vectorLayer],
          overlays: [overlay],
          view: new View({
            center: [-11000000, 4600000],
            zoom: 4
          })
        });

        /**
       * Add a click handler to the map to render the popup.
       */
      map.on('singleclick', function(evt) {
        var feature = map.forEachFeatureAtPixel(evt.pixel,
          function(feature) {
            return feature;
          });
        var coordinate = evt.coordinate;
        var hdms = toStringHDMS(toLonLat(coordinate));
        var title, url;
        try {
          title = feature['values_']['title'];
          url = feature['values_']['url'];
        } catch {
          title = null;
          url = null;
        }
        
        if(title !== null) {
          content.innerHTML = '<h4>' + title +
          '</h4><a href='+ url +'>' + url + '</a>' +
          '</br><code>' + hdms + '</code>';
          overlay.setPosition(coordinate);
        }
      });
    }).catch(function(error) {
        console.log(error);
    });
  }).catch(function(error) {
    console.log(error);
});

fetch('http://127.0.0.1:5000/api/v1/resources/csvjson').then(function(response) {
    return response.json();
}).then(function(data) {
  //Getting all the column names
  var cols = Headers(data, '#table_id');

  //Traverse through the JSON data
  for (var i = 0; i < data.Lat.length; i++) {
    var row = $('<tr/>');

    var lat = data.Lat[i];
    var long = data.Long[i];
    var title = data.Title[i];
    var url = data.URL[i];

    row.append($('<td/>').html(title));
    row.append($('<td/>').html("<a href='"+url+"'>"+url+"</a>"));
    row.append($('<td/>').html(lat));
    row.append($('<td/>').html(long));

    // Add each row to the table
    $('#table_body').prepend(row);
  }

  $('#table_id').DataTable();
})

function Headers(list, selector) { 
  var header = $('<thead/>'); 
  var row = $('<tr/>')
  header.append(row)

  list = Object.keys(list)
  var columns = list.length; 

  row.append($('<th/>').html(list[2])); 
  row.append($('<th/>').html(list[3])); 
  row.append($('<th/>').html(list[0])); 
  row.append($('<th/>').html(list[1])); 

  // Append the header to the table 
  $(selector).append(header); 
      return columns; 
}         

// Hide submenus
$('#body-row .collapse').collapse('hide'); 

// Collapse/Expand icon
$('#collapse-icon').addClass('fa-angle-double-left'); 

// Collapse click
$('[data-toggle=sidebar-colapse]').click(function() {
    SidebarCollapse();
});

function SidebarCollapse () {
    $('.menu-collapsed').toggleClass('d-none');
    $('.sidebar-submenu').toggleClass('d-none');
    $('.submenu-icon').toggleClass('d-none');
    $('#sidebar-container').toggleClass('sidebar-expanded sidebar-collapsed');
    
    // Treating d-flex/d-none on separators with title
    var SeparatorTitle = $('.sidebar-separator-title');
    if ( SeparatorTitle.hasClass('d-flex') ) {
        SeparatorTitle.removeClass('d-flex');
    } else {
        SeparatorTitle.addClass('d-flex');
    }
    
    // Collapse/Expand icon
    $('#collapse-icon').toggleClass('fa-angle-double-left fa-angle-double-right');
}