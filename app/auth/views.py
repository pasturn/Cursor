__author__ = 'Pasturn'

from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_user, login_required, current_user
from ..email import send_email
from . import auth
from .. import db
from ..models import Users
from .forms import LoginForm, RegisterForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('Invalid username or password.')
    return render_template('auth/login.html', title='Login', form=form)


@auth.route('/logout')
def logout():
    login_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():


        user = Users(username=form.username.data,
                     password=form.password.data,
                     email=form.email.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account', 'auth/email/comfirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', title='Register',form=form)



@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirm your accout. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.confirmed and request.endpoint[:5] != 'auth.'and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate.confirmation_token()
    send_email(current_user, 'Confirm You Account', 'auth/email/confirm', user = current_user, token = token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))