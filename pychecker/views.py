from pychecker import app
from flask import render_template
from flask import request

print app.config


# seems like a bad idea
@app.route('/css/<path:filename>')
def send_css(filename):
    return send_from_directory('/static/css', filename)


@app.route('/')
def index():
    return render_template('index.html', name="ya")


@app.route('/register',  methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        return "Success"
    elif request.method == 'GET':
        return render_template('register.html')
    else:
        return "error"


@app.route('/login')
def login():
    return 'login'


@app.route('/logout')
def logout():
    return 'logout'


@app.route('/product/')
def product():
    return 'add new product or list all products'


@app.route('/product/<int:product_id>')
def product(product_id):
    return 'product %s' % (product_id)


@app.route('/user/')
def user():
    return 'add new user'


@app.route('/user/<username>')
def user(username):
    return 'user with name %s' % (username)
