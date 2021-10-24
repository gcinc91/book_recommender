from app import app
import os

import src.controllers.recommender

PORT =  app.run(host="localhost", port=os.environ.get('PORT', 5000), debug=True)
app.run("0.0.0.0", PORT, debug=True)