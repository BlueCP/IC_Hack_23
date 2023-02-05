from flask import Flask
from flask import url_for
from flask import render_template
from flask import request
from flask import redirect

app = Flask(__name__)

def handle_request(product_name):
    # Add more processing here in future.
    return

@app.route('/')
def welcome():
    return redirect(url_for('scanning'))

@app.route('/scanning')
def scanning():
    return render_template('result.html')

@app.route('/processing')
def processing():
    input_json = request.json
    