from flask import (
    render_template,
    redirect,
    url_for,
    flash
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

from app.authentication import authentication
from .models import AuthUser
from .forms import RegisterForm, UserForm


@authentication.route('/login', methods=['POST', 'GET'])
def login():

    form = UserForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = AuthUser.filter(email=email).first()
        if not AuthUser.select().where(AuthUser.email == email, check_password_hash(user.password, password)):
            flash('Please check your login details and try again.')
            return redirect(url_for('authentication.login'))
        login_user(user)
        return redirect(url_for('authentication.profile'))

    return render_template(
        'authentication/login.html',
        title='Login',
        form=form
    )


@authentication.route('/profile')
@login_required
def profile():
    return render_template(
        'authentication/profile.html',
        name=current_user.name
    )


@authentication.route('/signup', methods=['POST', 'GET'])
def signup():

    form = RegisterForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        user = AuthUser.filter(email=email).first()
        message = f'User with name {name} already registered'
        if not AuthUser.select().where(AuthUser.email == email, AuthUser.password == password):
            user = AuthUser(name=name, email=email, password=generate_password_hash(password, method='sha256'))
            user.save()
            message = f'User with name {name} just registered'
        flash(message)

    return render_template(
        'authentication/signup.html',
        title='Sign up',
        form=form
    )


@authentication.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('authentication.login'))
