from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    SelectField,
    MultipleFileField,
    BooleanField,
    DecimalField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo,
    ValidationError,
    Optional,
)
from wtforms.fields import FileField
from app.models import User


class LoginForm(FlaskForm):
    username = StringField("Username*", validators=[DataRequired()])
    password = PasswordField("Password*", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Sign In")


class SignUpForm(FlaskForm):
    username = StringField("Username*", validators=[DataRequired()])
    email = StringField("Email*", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password*", validators=[DataRequired(), Length(min=7, max=15)]
    )
    confirm_pass = PasswordField(
        "Repeat Password*",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )
    tos_confirm = BooleanField(
        "By creating an account, you agree to the ", validators=[DataRequired()]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address.")


class ResetPasswordForm(FlaskForm):
    email = StringField("Enter your email*", validators=[DataRequired(), Email()])
    submit = SubmitField("Submit")


class ResetPasswordVerifiedForm(FlaskForm):
    newPass = PasswordField("Enter your new password*", validators=[DataRequired()])
    submit = SubmitField("Submit")


class CancelForm(FlaskForm):
    confirm = StringField("Confirm Order Name", validators=[DataRequired()])
    submit = SubmitField("Cancel it")


class CustomizeForm(FlaskForm):
    order_name = StringField("Order Name*", validators=[DataRequired()])
    order_description = StringField("Describe your Order*", validators=[DataRequired()])
    order_reference = MultipleFileField(
        "Any files needed?",
        validators=[
            FileAllowed(
                ["jpg", "png", "txt", "pdf", "jpeg", "gif"],
                "File extension Not allowed!",
            )
        ],
    )
    submit = SubmitField("Submit Order")


class SupportForm(FlaskForm):
    issue = StringField("Enter your issue*", validators=[DataRequired()])
    submit = SubmitField("Submit your issue")


class ProductsFormAdmin(FlaskForm):
    name = StringField("Enter the name")
    desc = StringField("Enter the description")
    price = DecimalField("Enter the price", validators=[Optional()])
    types = SelectField(
        "Enter what to do",
        validators=[DataRequired()],
        choices=[("list", "List"), ("add", "Add"), ("del", "Delete")],
    )
    submit1 = SubmitField("Submit")


class OrdersFormAdmin(FlaskForm):
    order_name = StringField("Enter the order name")
    types = SelectField(
        "Enter what to do",
        validators=[DataRequired()],
        choices=[("list", "List"), ("del", "Delete"), ("complete", "Complete")],
    )
    submit2 = SubmitField("Submit")


class UsersFormAdmin(FlaskForm):
    username = StringField("Enter the username")
    types = SelectField(
        "Enter what you wanna do",
        validators=[DataRequired()],
        choices=[("list", "List"), ("search", "Search"), ("delete", "Delete")],
    )
    submit3 = SubmitField("Submit")


class EditForm(FlaskForm):
    name = StringField("Enter name: ")
    profileimg = FileField("Select a profile image")
    submit2 = SubmitField("Submit")