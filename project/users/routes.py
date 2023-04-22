from . import users_blueprint
from flask import render_template, flash, abort, request, current_app, redirect, url_for
from .forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, login_required, logout_user
from project.models import User
from project import db
from sqlalchemy.exc import IntegrityError
from urllib.parse import urlparse


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                new_user = User(form.email.data, form.password.data)
                db.session.add(new_user)
                db.session.commit()
                flash(f'Thanks for registering, {new_user.email}!')
                current_app.logger.info(
                    f'Registered new user: {form.email.data}!')
                return redirect(url_for('urls.index'))
            except IntegrityError:
                db.session.rollback()
                flash(
                    f'ERROR! Email ({form.email.data}) already exists.', 'error')
        else:
            flash(f"Error in form data!")

    return render_template('users/register.html', form=form)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # If the user is already logged in, don't allow them to try to log in again
    if current_user.is_authenticated:
        flash('Already logged in!')
        current_app.logger.info(
            f'Duplicate login attempt by user: {current_user.email}')
        return redirect(url_for('urls.index'))

    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.is_password_correct(form.password.data):
                # User's credentials have been validated, so log them in
                login_user(user, remember=form.remember_me.data)
                flash(f'Thanks for logging in, {current_user.email}!')
                current_app.logger.info(
                    f'Logged in user: {current_user.email}')
                # return redirect(url_for('urls.index'))

                # If the next URL is not specified, redirect to the user profile - NEW!!
                if not request.args.get('next'):
                    return redirect(url_for('users.user_profile'))

                # Process the query to determine if the user should be redirected after logging in - NEW!!
                next_url = request.args.get('next')
                if urlparse(next_url).scheme != '' or urlparse(next_url).netloc != '':
                    current_app.logger.info(
                        f'Invalid next path in login request: {next_url}')
                    logout_user()
                    return abort(400)

                current_app.logger.info(
                    f'Redirecting after valid login to: {next_url}')
                return redirect(next_url)

        flash('ERROR! Incorrect login credentials.', 'error')
    return render_template('users/login.html', form=form)


@users_blueprint.route('/logout')
@login_required
def logout():
    current_app.logger.info(f'Logged out user: {current_user.email}')
    logout_user()
    flash('Goodbye!')
    return redirect(url_for('urls.index'))


@users_blueprint.route('/profile')
@login_required
def user_profile():
    return render_template('users/profile.html')


@users_blueprint.route('/stats')
@login_required
def stats():
    return render_template('users/stats.html')
