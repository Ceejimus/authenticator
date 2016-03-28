from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Email

class LoginForm(Form):
	email = StringField('email', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
	#remember_me = BooleanField('remember_me', default=False)

class CreateUserForm(Form):
	email = StringField('email', validators=[DataRequired(), Email(message="Invalid E-mail Address")])
	password = StringField('password',
		validators=[
			DataRequired(),
			EqualTo('confirm_password', message="Oops! Passwords don't match...")
		]
	)
	confirm_password = StringField('confirm_password')