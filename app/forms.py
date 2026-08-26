from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    SelectField
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    NumberRange
)

from wtforms import IntegerField, TextAreaField, DateField


class LoginForm(FlaskForm):

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )

    submit = SubmitField("Login")


class RegisterForm(FlaskForm):

    name = StringField(
        "Full Name",
        validators=[DataRequired(), Length(min=3)]
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    phone = StringField(
        "Phone",
        validators=[DataRequired()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6)]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password")
        ]
    )

    role = SelectField(
        "Register As",
        choices=[
            ("user", "Trekker"),
            ("staff", "Trek Staff")
        ]
    )

    submit = SubmitField("Register")

class TrekForm(FlaskForm):

    name = StringField(
        "Trek Name",
        validators=[DataRequired()]
    )

    location = StringField(
        "Location",
        validators=[DataRequired()]
    )

    difficulty = SelectField(
        "Difficulty",
        choices=[
            ("Easy","Easy"),
            ("Moderate","Moderate"),
            ("Hard","Hard")
        ]
    )

    duration = IntegerField(
        "Duration (Days)",
        validators=[DataRequired()]
    )

    available_slots = IntegerField(
        "Available Slots",
        validators=[DataRequired()]
    )

    start_date = DateField(
        "Start Date",
        format="%Y-%m-%d"
    )

    end_date = DateField(
        "End Date",
        format="%Y-%m-%d"
    )

    altitude = IntegerField(
    "Altitude (in ft)",
    validators=[
        DataRequired(),
        NumberRange(min=0, message="Altitude cannot be negative.")
    ]
)
    status = SelectField(
        "Status",
        choices=[
            ("Open","Open"),
            ("Closed","Closed"),
            ("Completed","Completed")
        ]
    )

    description = TextAreaField(
        "Description"
    )

    staff_id = SelectField(
    "Assign Staff",
    coerce=int
    )
    submit = SubmitField("Save Trek")

class StaffTrekUpdateForm(FlaskForm):
    available_slots = IntegerField(
        "Available Slots",
        validators=[DataRequired()]
    )

    status = SelectField(
        "Status",
        choices=[
            ("Open", "Open"),
            ("Closed", "Closed"),
            ("Completed", "Completed")
        ]
    )

    submit = SubmitField("Update Trek")    

class ProfileForm(FlaskForm):

    name = StringField(
        "Name",
        validators=[DataRequired()]
    )

    phone = StringField(
        "Phone",
        validators=[DataRequired()]
    )

    submit = SubmitField("Update Profile")    

class StaffProfileForm(FlaskForm):

    name = StringField(
        "Full Name",
        validators=[DataRequired()]
    )

    phone = StringField(
        "Phone Number",
        validators=[DataRequired()]
    )

    submit = SubmitField("Update Profile")    