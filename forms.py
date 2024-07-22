from wtforms import StringField, SubmitField, TextAreaField, BooleanField, PasswordField, FileField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    login = StringField("login", validators=[DataRequired()], render_kw={'class': 'form-control'})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={'class': 'form-control'})
    remember = BooleanField("Remember Me", render_kw={'class': 'form-check-input'})
    submit = SubmitField(render_kw={'class': 'btn btn-primary'})

class FDataBase(FlaskForm):
    title = StringField("title", validators=[DataRequired()], render_kw={'class': 'form-control'})
    description = TextAreaField("description", validators=[DataRequired()], render_kw={'class': 'form-control'})
    image = FileField('image', validators=[DataRequired()], render_kw={'class': 'form-control'})
    submit = SubmitField(render_kw={'class': 'btn btn-primary'})

