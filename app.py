from flask import Flask, send_file, make_response

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

@app.route('/load-data')
def load_data_endpoint():
    # Your load_data_endpoint endpoint logic here
    return 'load_data_endpoint endpoint'

@app.route('/export-data')
def export_data():

    # Return the response
    return response
