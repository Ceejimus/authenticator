from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Email

class LoginForm(Form):
	email = StringField('email', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
	#remember_me = BooleanField('remember_me', default=False)

class CreateUserForm(Form):
	email = StringField('email', 
		validators=[
			DataRequired(),
			Email(message="Invalid E-mail Address")
		]
	)
	password = PasswordField('password',
		validators=[
			DataRequired()
		]
	)
	confirm_password = PasswordField('confirm_password',
		validators=[
			DataRequired(),
			EqualTo('password', message="Oops! Passwords don't match...")
		]
	)