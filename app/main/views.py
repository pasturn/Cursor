__author__ = 'Pasturn'

from flask import render_template, session, redirect
from . import main
from .. import db
from ..models import Users


@main.route('/')
@main.route('/index')
def index():
    user = { 'nickname': 'Miguel' } # fake user
    return render_template("index.html",
        title = 'Home',
        user = session.get('user'))


@main.route('/mail', methods = ['GET', 'POST'])
def mail():
    return render_template('mailbox.html',
                           title = 'Mailbox')

@main.route('/mail/sent', methods = ['GET', 'POST'])
def sendmail():
    return render_template('sendmail.html',
                           title = 'Sendmail')
