from flask import Flask
from flask import url_for
from flask import render_template
from flask import request
from flask import redirect

app = Flask(__name__)

def handle_request(product_name):
    return f'Your product is: {product_name}'

@app.route('/')
def welcome():
    return redirect(url_for('query'))

@app.route('/query')
def query():
    product_name = request.args.get('product_name', '')
    if product_name != '':
        return render_template('result.html', product_name=product_name)
    else:
        return render_template('query.html')


camera = cv2.VideoCapture(0)


'''
@app.route('/hello_world')
def hello_world():
    return redirect(url_for('hello'))

@app.route('/any_string/<bar>')
def foo(bar):
    return f'Input string: {bar}'
'''
