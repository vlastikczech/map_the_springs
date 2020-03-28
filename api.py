import flask
from flask_cors import CORS

import scraper.scrape
from scraper.scraper import Scraper
from scraper.settings import settings

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = './output'

result = {}

@app.route('/api/v1/resources/download', methods=['GET'])
def download_c2v():
        return flask.send_from_directory(app.config['UPLOAD_FOLDER'] ,
                               'output.csv', as_attachment=True)

@app.route('/api/v1/resources/generate', methods=['GET'])
def generate_c2v():
        Scraper(settings)
        return "success"

@app.route('/api/v1/resources/json', methods=['GET'])
def produce_json():
        return Scraper.produceJson('')

@app.route('/api/v1/resources/geojson', methods=['GET'])
def produce_geojson():
        return flask.jsonify(Scraper.produceGeoJsonFromCSV(''))

@app.route('/api/v1/resources/csvjson', methods=['GET'])
def produce_csvjson():
        return Scraper.produceCSVJson('')

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)