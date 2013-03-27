from flask.ext.wtf import Form, TextField, PasswordField, validators
from pychecker.models import User
from pychecker.scraper import valid_product


class LoginForm(Form):
    username = TextField('username', [validators.Required()])
    password = PasswordField('password', [validators.Required()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(
            username=self.username.data).first()
        if user is None:
            self.username.errors.append('Unknown username')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        self.user = user
        return True


class ProductForm(Form):
    url = TextField('URL', [validators.Required()])
    notify_price = TextField('Price to Notify', [validators.Required()])

    def __init__(self, *args, **kwargs):
	Form.__init__(self, *args, **kwargs)
	self.user = None

    def validate(self):
	rv = Form.validate(self)
	if not rv:
	    return False

	if not valid_product(self.url):
	    return False

	return True
