from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
from flask.logging import create_logger
import logging
import bcrypt
import json
import requests
import subprocess
import numpy as np
import tensorflow as tf

app = Flask(__name__)
api = Api(app)

LOG = create_logger(app)
LOG.setLevel(logging.INFO)

class Classify(Resource):
    def post(self):
        postedData = request.get_json()
        url = postedData["url"]

        img = requests.get(url, stream=True)
        retJson = {}

        with open("temp.jpg", "wb") as f:
            f.write(img.content)
            proc = subprocess.Popen('python classify_image.py --image ./temp.jpg')
            proc.communicate()[0]
            proc.wait() # wait will subprocess is done
            LOG.info(f"Openining text.txt")
            with open("text.txt") as res:
                LOG.info(f"Prediction Value: \n{res}")
                retJson = json.load(res)

        return retJson

api.add_resource(Classify, '/classify')

if __name__=="__main__":
    app.run(host='0.0.0.0')