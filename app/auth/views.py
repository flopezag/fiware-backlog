__author__ = 'Manuel Escriche'

from flask import render_template, redirect, url_for, request
from flask_login import login_required, login_url, login_user, logout_user
from .Users import User, LoginForm
from app import login_manager
from . import auth

@auth.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm()
    if request.method == 'POST':
        try:
            validate = form.validate_on_submit()
        except Exception:
            error = 'Connection to JIRA server failed'
        else:
            if validate:
                user = form.get_user()
                login_user(user)
                _next = request.args.get('next')
                return redirect(_next or url_for('main.home'))
            else:
                error = 'Invalid Credentials'
    url =  login_url('auth.login', request.args.get('next'))
    return render_template('login.html', url=url, form=form, error=error)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
