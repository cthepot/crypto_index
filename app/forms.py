from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, IndexAsset, Asset, Index


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')


class CreateIndexForm(FlaskForm):
    name = StringField('Index name', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    # currency = SelectField('Currency', validators=[DataRequired()])
    submit = SubmitField('Create Index')


class CreateIndexAssetForm(FlaskForm):
    asset_id = SelectField('Asset name',coerce=int, validators=[DataRequired()])
    allocation = FloatField('%', validators=[DataRequired()])
    submit = SubmitField('Add Asset in Basket')
