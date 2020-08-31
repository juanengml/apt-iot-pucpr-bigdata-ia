# https://repl.it/repls/TintedNimbleCompilerbug
from flask import Flask
from flask_restful import Resource, Api
from datetime import datetime as dt 
from uuid import * 
from flask_restful import reqparse



app = Flask(__name__)
api = Api(app)

db = []


class HealthCheck(Resource):
  def get(self):
    return {"HealthCheck":"alive","dt":str(dt.now())}

class GENERATE_ID(Resource):
    def get(self):
        return {'ID': str(uuid4()),"dt":str(dt.now())}

class ReceiveSensors(Resource):
  def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('umidade')
        parser.add_argument('temperatura')
        parser.add_argument('relay_flag')
        args = parser.parse_args()
        print(args)
        return {"data":True,"dt":str(dt.now()),"iot":args},200
 
api.add_resource(GENERATE_ID, '/api/iot/v1/GENERATE_ID')
api.add_resource(ReceiveSensors, '/api/iot/v1/SEND')
api.add_resource(HealthCheck, '/')


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
