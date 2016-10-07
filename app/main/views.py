# -*- coding: utf-8 -*-
__author__ = 'Pasturn'

from flask import render_template, session, redirect, abort, url_for
from flask_login import login_user, login_required, current_user
from . import main
from .forms import PostForm
from .. import db
from ..models import Users, Permission, Posts


@main.route('/')
@main.route('/index')
@login_required
def index():
    user = {'nickname': 'Miguel'}  # fake user
    return render_template("index.html",
                           title='Home',
                           user=session.get('user'))


@main.route('/mail', methods=['GET', 'POST'])
def mail():
    return render_template('mailbox.html',
                           title='Mailbox')


@main.route('/mail/sent', methods=['GET', 'POST'])
def sendmail():
    return render_template('sendmail.html',
                           title='Sendmail')


@main.route('/user/<username>')
def user(username):
    user = Users.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user/setting.html', user=user)


@main.route('/post', methods=['GET', 'POST'])
def post():
    form = PostForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        post = Posts(title=form.title.data, body=form.body.data,
                     author=current_user._get_current_object())

        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.post'))
    posts = Posts.query.order_by(Posts.timestamp.desc()).all()
    return render_template('post/post.html', form=form, posts=posts)


@main.route('/post/list')
def post_list():
    posts = Posts.query.order_by(Posts.id.desc()).all()
    return render_template('post/list.html',posts=posts)
