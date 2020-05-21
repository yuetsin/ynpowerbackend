from flask import Flask, request
from flask_restful import Resource, Api
import pandas as pd
from Controller import uploadData


app = Flask(__name__)
api = Api(app)


class UploadCSV(Resource):
    def post(self):
        file = request.files['file']
        data = pd.read_csv(file)
        print(data)
        uploadData(data)


api.add_resource(UploadCSV, "/upload")

if __name__ == '__main__':
    app.run()
