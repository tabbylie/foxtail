from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, MultipleFileField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username*', validators=[DataRequired()])
    password = PasswordField('Password*', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')

class SignUpForm(FlaskForm):
    username = StringField('Username*', validators=[DataRequired()])
    email = StringField('Email*', validators=[DataRequired(), Email()])
    password = PasswordField('Password*', validators=[DataRequired(),  Length(min=7, max=15)])
    confirm_pass = PasswordField('Repeat Password*', validators=[DataRequired(), EqualTo('password', message="Passwords must match.")])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class CancelForm(FlaskForm):
    confirm = StringField('Confirm Order Name', validators=[DataRequired()])
    submit = SubmitField('Cancel it')

class BasicAppForm(FlaskForm):
    order_name = StringField('Name of Application*', validators=[DataRequired()])
    order_description = StringField('Describe your application*', validators=[DataRequired()])
    order_examps = StringField('Example Applications (if any)')
    submit = SubmitField('Submit order')

class ComplexAppForm(FlaskForm):
    order_name = StringField('Name of Application*', validators=[DataRequired()])
    order_description = StringField('Describe your Application*', validators=[DataRequired()])
    order_examps = StringField('Example applications (if any)')
    submit = SubmitField('Submit order')

class FrontEndForm(FlaskForm):
    order_name = StringField("Order Name*", validators=[DataRequired()])
    order_description = StringField('Describe the purpose*', validators=[DataRequired()])
    design_or_no = SelectField(u'Have a Design?*', choices=[('1', 'Yes'), ('2', 'No')])
    submit = SubmitField('Submit order')

class DatabaseForm(FlaskForm):
    order_name = StringField('Order name*', validators=[DataRequired()])
    order_description = StringField('Describe its use*', validators=[DataRequired()])
    submit = SubmitField('Submit order')

class CMSForm(FlaskForm):
    order_name = StringField('Order name*', validators=[DataRequired()])
    order_description = StringField('Describe its purpose*', validators=[DataRequired()])
    submit = SubmitField('Submit order')

class CDForm(FlaskForm):
    order_name = StringField('Order Name*', validators=[DataRequired()])
    order_description = StringField('Describe your design*', validators=[DataRequired()])
    order_reference = MultipleFileField('Any References?', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Submit Order')