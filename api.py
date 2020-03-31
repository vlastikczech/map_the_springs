from flask import Flask, send_from_directory
from flask_restx import Api, Resource, fields
from flask_cors import CORS

import scraper.scrape
from scraper.scraper import Scraper
from scraper.settings import settings

app = Flask(__name__)
api = Api(app, version='1.0', title='Map The Springs',
description='Hot Springs API',
)
CORS(app)
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = './output'

# namespace appear under a given heading in Swagger
name_space = api.namespace('', description='Hot Springs APIs')

@name_space.route("/api/v1/resources/download")
class Download(Resource):
    def get(self):
        '''Downloads a csv file'''
        return send_from_directory(app.config['UPLOAD_FOLDER'] ,
                                'output.csv', as_attachment=True)


@name_space.route("/api/v1/resources/generate")
class Generate(Resource):
    def get(self):
        '''Generates a csv file'''
        Scraper(settings)
        return {
            "status": "200"
        }

@name_space.route("/api/v1/resources/json")
class ProduceJson(Resource):
    def get(self):
        '''Returns a object list'''
        return Scraper.produceJson('')
        
@name_space.route("/api/v1/resources/geojson")
class ProductGeoJson(Resource):
    def get(self):
        '''Returns a object list in geo format'''
        return Scraper.produceGeoJsonFromCSV('')

@name_space.route("/api/v1/resources/csvjson")
class ProduceCsvJson(Resource):
    def get(self):
        '''Returns a object list containing all the csv data'''
        return Scraper.produceCSVJson('')

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)