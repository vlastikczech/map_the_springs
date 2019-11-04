import 'ol/ol.css';
import Feature from 'ol/Feature';
import OSM from 'ol/source/OSM';
import Map from 'ol/Map';
import View from 'ol/View';
import Point from 'ol/geom/Point';
import {Tile as TileLayer, Vector as VectorLayer} from 'ol/layer';
import {fromLonLat} from 'ol/proj';
import TileJSON from 'ol/source/TileJSON';
import VectorSource from 'ol/source/Vector';
import {Icon, Style} from 'ol/style';
import GeoJSON from 'ol/format/GeoJSON';



let url = 'http://127.0.0.1:5000/api/v1/resources/json'
fetch(url).then(function(response) {
    return response.json();
  }).then(function(data) {

    fetch('http://127.0.0.1:5000/api/v1/resources/geojson').then(function(response) {
        return response.json();
    }).then(function(data) {
        var geojsonObject = data
        var coordinates = geojsonObject['features'].map(el => {return el['geometry']['coordinates'] = fromLonLat([el['geometry']['coordinates'][0], el['geometry']['coordinates'][1]])})

        var vectorSource = new VectorSource({
        features: (new GeoJSON()).readFeatures(geojsonObject)
        });
    
        var vectorLayer = new VectorLayer({
        source: vectorSource
        });
        
        var rasterLayer = new TileLayer({
            source: new OSM()
        })
          
        const map = new Map({
          target: 'map',
          layers: [rasterLayer, vectorLayer],
          view: new View({
            center: [-11000000, 4600000],
            zoom: 4
          })
        });
    }).catch(function(error) {
        console.log(error);
    });
  }).catch(function(error) {
    console.log(error);
});



