from ..database import db
from ..utils.handle_error import handle_error
from ..utils.jsonfy import jsonfy
from ..utils.json_response import json_response
from main import app

@app.route("/recommender/predict")
@handle_error
def predict():
    query = f"""
        SELECT *
        FROM books
        limit 10
    """
    result = list(db.execute(query))
    response = jsonfy(result)
    print('response --> ',response)

    data = {
        "status": "OK",
        "response": response
    }
    
    return json_response(data)