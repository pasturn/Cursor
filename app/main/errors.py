# -*- coding: utf-8 -*-
__author__ = 'Pasturn'

from flask import render_template
from . import main

#404无法找到文件
@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


#500服务器错误
@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
