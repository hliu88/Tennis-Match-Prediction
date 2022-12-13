from flask import Flask, jsonify, Response, abort
from flask_restx import Resource, Api
from .predict import predict_m
from gevent.pywsgi import WSGIServer
import json
from flask_cors import CORS


app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r'/*': {'origins': '*'}})

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

@api.route('/predict/test')
class predict_matches(Resource):
    """
    predict
    """
    def get(self):
        # output = json.dumps(predict_m())
        output = predict_m()
        if(output == 'No Matches Avaliable'):
            return{'message': 'NA'}
        output0 = output[0].tolist()
        output0 = json.dumps(output0)
        if(output[1] == -1):
            return {'message': json.loads(output0)}
        return {'message': json.loads(output0), 'F1_Score': output[1]}

@api.route('/predict/today')
class predict_matches_today(Resource):
    """
    predict
    """
    def get(self):
        output = predict_m('today')
        if(output == 'No Matches Avaliable'):
            return{'message': 'NA'}
        output0 = output[0].tolist()
        output0 = json.dumps(output0)
        if(output[1] == -1):
            return {'message': json.loads(output0)}
        return {'message': json.loads(output0), 'F1_Score': output[1]}

@api.route('/predict/tomorrow')
class predict_matches_today(Resource):
    """
    predict
    """
    def get(self):
        output = predict_m('tomorrow')
        if(output == 'No Matches Avaliable'):
            return{'message': 'NA'}
        output0 = output[0].tolist()
        output0 = json.dumps(output0)
        if(output[1] == -1):
            return {'message': json.loads(output0)}
        return {'message': json.loads(output0), 'F1_Score': output[1]}

@api.route('/predict/yesterday')
class predict_matches_today(Resource):
    """
    predict
    """
    def get(self):
        output = predict_m('yesterday')
        if(output == 'No Matches Avaliable'):
            return{'message': 'NA'}
        output0 = output[0].tolist()
        output0 = json.dumps(output0)
        if(output[1] == -1):
            return {'message': json.loads(output0)}
        return {'message': json.loads(output0), 'F1_Score': output[1]}

if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
    # app.run()