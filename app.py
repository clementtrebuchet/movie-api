from flask import Flask, send_file, make_response

import csv
import io

app = Flask(__name__)

@app.route('/load-data')
def load_data_endpoint():
    # Your load_data_endpoint endpoint logic here
    return 'load_data_endpoint endpoint'

@app.route('/export-data')
def export_data():

    # Return the response
    return response
