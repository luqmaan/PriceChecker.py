from flask.ext.wtf import Form, TextField, PasswordField, validators, SelectField
from pychecker.models import User
from pychecker.database import db_session
from pychecker import models
import re


class LoginForm(Form):
    username = TextField(label='username',
                         validators=[validators.Required()],
                         description='Username')
    password = PasswordField(label='password',
                             validators=[validators.Required()],
                             description='Password')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = db_session.query(models.User).filter(
            models.User.username == self.username.data).first()

        if user is None:
            self.username.errors.append('Unknown username')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        self.user = user
        return True


class ProductForm(Form):
    url = TextField(label='url',
                    validators=[validators.Required()],
                    description="URL To Product")

    name = TextField(label='Product Name',
                     validators=[validators.Required()],
                     description="Name of Product")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        domain = re.findall("[www.{0,1}\.]*[a-z.0-9]+\.com", self.url.data)
        if len(domain) < 1:
            self.url.errors.append('Invalid URL')
            return False
        else:
            domain = domain[0]
            sel = models.Selector.query.filter(models.Selector.domain == domain)
            if sel.count() < 1:
                self.url.errors.append('This site is not yet supported.')

        return True


class RegisterForm(Form):
    username = TextField(label='username',
                         validators=[validators.Required()],
                         description="Username")
    password = TextField(label='password',
                         validators=[validators.Required()],
                         description="Password")
    email = TextField(label='email',
                      validators=[validators.Required()],
                      description="Email Address")
    phone = TextField(label='phone',
                      validators=[validators.Required()],
                      description="Phone Number")
    twitter = TextField(label='twitter',
                        validators=[validators.Required()],
                        description="Twitter")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        if not valid_product(self.url.data):
            self.url.errors.append('Invalid URL')
            return False

        return True
