from src.app import app
import src.controllers.recommender
import os

PORT =  app.run(host="localhost", port=os.environ.get('PORT', 5000), debug=True)
app.run("0.0.0.0", PORT, debug=True)