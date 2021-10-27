from ..app import app
from ..services.service import autocomplete, charge_models, load_titles, make_recommendation
from ..database import db
from ..utils.handle_error import handle_error
from ..utils.jsonfy import jsonfy
from ..utils.json_response import json_response
from flask import request

@app.route("/recommender/init", methods=['GET'])
@handle_error
def init():
    
    res  = charge_models()

    data = {
        "status": "OK",
        "response": res
    }
    
    return json_response(data)


@app.route("/recommender/predict",methods=['POST'])
@handle_error
def predict():

    data  = request.json

    user = data['user']
    model = data['model']

    res = make_recommendation(user,model)

    data = {
        "status": "OK",
        "response": res
    }
    
    return json_response(data)


@app.route("/load",methods=['GET'])
@handle_error
def load():
    
    res = load_titles()

    data = {
        "status": "OK",
        "response": res
    }
    
    return json_response(data)

@app.route("/auto",methods=['GET'])
@handle_error
def autocom():

    data  = request.args.get('title')
    
    res = autocomplete(data)

    data = {
        "status": "OK",
        "response": res
    }
    
    return json_response(data)