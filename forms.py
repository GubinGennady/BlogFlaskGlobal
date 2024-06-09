from wtforms import StringField, SubmitField, TextAreaField, BooleanField, PasswordField
from wtforms.validators import DataRequired, ValidationError
from flask_wtf import FlaskForm


# from models import User


class LoginForm(FlaskForm):
    login = StringField("login", validators=[DataRequired()], render_kw={'class': 'form-control'})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={'class': 'form-control'})
    remember = BooleanField("Remember Me", render_kw={'class': 'form-check-input'})
    submit = SubmitField(render_kw={'class': 'btn btn-primary'})
    '''
    def validate_login(self, login):
        user = User.query.filter_by(login=login).first()
        if user is not None:
            raise ValidationError('Error login')

    '''
