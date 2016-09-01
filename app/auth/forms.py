__author__ = 'Pasturn'

from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import Users


class RegisterForm(Form):
    #用户名
    username = StringField(
        'Please Type Your Username',
        validators = [
            DataRequired(),
            Regexp(
                '^[A-Za-z][A-za-z0-9_.]*$',
                0,
                'Usernames must have only letters,'
                'numbers, dots or underscores'
            )
        ]
    )
    email = StringField(
        'Please Type Your Email',
        validators=[DataRequired()]
    )
    #密码
    password = PasswordField(
        'Please Type Your Password',
        validators = [
            DataRequired(),
            EqualTo(
                'password2',
                message = 'Passwords must match.'
            ),

        ]
    )

    # 确认密码
    password2 = PasswordField(
        'Confirm password',
        validators=[DataRequired()]
    )

    submit = SubmitField('Register')

    # 检查邮件重复性
    def validate_email(self, field):
        if Users.query.filter_by(email = field.data).first():
            raise ValidationError(u'邮箱已存在')

    # 检查用户名重复性
    def validate_username(self, field):
        if Users.query.filter_by(username = field.data).first():
            raise ValidationError(u'用户名已存在')


class LoginForm(Form):
    username = StringField(
        'Please Type Your Username',
        validators=[
            DataRequired(),
            Length(1,64)
        ]
    )
    password = PasswordField(
        'Please Type Your Password',
        validators=[
            DataRequired(),
            Length(6,16)
        ]
    )
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('LOGIN')