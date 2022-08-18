from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=120)],
                           render_kw={"placeholder": "Username"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)],
                             render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')],
                                     render_kw={"placeholder": "Confirm password"})
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            flash('This email is taken. Please choose a different one', 'danger')
            raise ValidationError('This email is taken. Please choose a different one')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)],
                             render_kw={"placeholder": "Password"})
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class VerifyForm(FlaskForm):
    otp = StringField('otp', validators=[DataRequired(), Length(min=6, max=6)],
                      render_kw={"placeholder": "6-digits code"})
    submit = SubmitField('Verify')


class TypeMailCountry(FlaskForm):
    state_country = SelectField(label='Select a country ',
                        choices=['Norway', 'Poland', 'Thailand', 'Latvia', 'Lithuania', 'Spain'])
    state_mail = SelectMultipleField(label='Select a type of mailing',
                        choices=['Courses', 'Air tickets', 'Vacancies for visa application'],
                        option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=True))
    submit = SubmitField('Save')


# class MultiCheck(SelectMultipleField):
#     widget = wi
#
# class TypeCountry(FlaskForm):
#     state = SelectField(label='Select a country ',
#                         choices=['Norway', 'Poland', 'Thailand', 'Latvia', 'Lithuania', 'Spain'])
