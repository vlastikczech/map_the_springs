import flask
import sys
sys.path.append('..\scraper')

import scrape
from scraper import Scraper
import settings

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = '../output'

result = {}


@app.route('/', methods=['GET'])
def home():
    return "<h1>Hot Springs</h1><p>This site is a prototype API for list of hot springs in the world.</p>"

@app.route('/api/v1/resources/download', methods=['GET'])
def download_c2v():
        return flask.send_from_directory(app.config['UPLOAD_FOLDER'] ,
                               '10_12_2019_output.csv', as_attachment=True)

@app.route('/api/v1/resources/generate', methods=['GET'])
def generate_c2v():
        scrape.Scraper(settings.settings)
        return "success"

@app.route('/api/v1/resources/json', methods=['GET'])
def produce_json():
        return Scraper.produceJson('')

app.run()