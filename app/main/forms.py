# -*- coding: utf-8 -*-
__author__ = 'Pasturn'

from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import Posts


class PostForm(Form):
    title = StringField("Input the title", validators=[DataRequired()])
    body = TextAreaField("What's on your mind", validators= [DataRequired()])
    submit = SubmitField("保存")