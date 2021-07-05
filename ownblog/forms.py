from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , SubmitField ,TextAreaField 
from wtforms.validators import DataRequired, EqualTo ,ValidationError , Email

class LoginForm(FlaskForm):
    username= StringField('Username', validators=[DataRequired()])
    password= PasswordField('Password', validators=[DataRequired()])
    submit= SubmitField('Login')

class RegistrationForm(FlaskForm):
    username=StringField('Username' , validators=[DataRequired()])
    password=PasswordField('Password', validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit= SubmitField('Sign Up')

class PostForm(FlaskForm):
    title= StringField('Title', validators=[DataRequired()])
    post=TextAreaField('Post' , validators=[DataRequired()])
    submit= SubmitField('Post It')
    
class CommentForm(FlaskForm):
    post=TextAreaField('Post' , validators=[DataRequired()])
    submit= SubmitField('Comment')
