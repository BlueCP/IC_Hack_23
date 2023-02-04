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
    return redirect(url_for('query'))

@app.route('/query')
def query():
    product_name = request.args.get('product_name', '')
    if product_name != '':
        handle_request(product_name)
        return render_template('result.html', product_name=product_name)
    else:
        return render_template('query.html')

@app.route('/query/camera')
def camera_query():
    try:
        f = request.files['image']
        f.save('image.png')
        return render_template('result.html', product_name='foo')
    except:
        return render_template('camera.html')
