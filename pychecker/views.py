from pychecker import app


@app.route('/')
def index():
    return 'Hello World!'


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


@app.route('/user/<username>')
def user(username):
    return 'user with name %s' % (username)
