import jwt
from flask import render_template, flash, url_for, request, redirect, jsonify
from flask_login import login_user, login_required, logout_user, current_user

from user_auth.flask_app.models import User
from user_auth.flask_app.forms import RegistrationForm, LoginForm, VerifyForm, TypeMailCountry
from user_auth.flask_app import app, db, bcrypt
from user_auth.flask_app.otp_mail import generate_otp, send_email


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        token = jwt.encode({'email': form.email.data}, app.config['SECRET_KEY'], algorithm="HS256")
        otp_code = generate_otp()
        user = User(username=form.username.data, email=form.email.data, password=hashed_password,
                    token=token, otp_code=otp_code, is_verify=False)

        send_email(email=form.email.data, otp_code=otp_code)
        db.session.add(user)
        db.session.commit()
        flash('Thank for. To complete your registration please verify.', 'success')
        return redirect(url_for('verify', token=token))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Error in field "{}": {}'.format(getattr(form, field).label.text, error))

    return render_template('register.html', form=form, title='Registration')


@app.route('/verify/<string:token>', methods=['GET', 'POST'])
def verify(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = VerifyForm()
    if form.validate_on_submit():
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
        email = data['email']
        user = User.query.filter_by(email=email).first()
        if user and int(form.otp.data) == int(user.otp_code):
            user.is_verify = True
            db.session.commit()
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/')
        else:
            user.otp_code = generate_otp()
            send_email(user.email, user.otp_code)
            flash('Failed verification. Enter new code on your email', 'message')
            return redirect(url_for('verify', token=token))
    return render_template('verify.html', form=form, title='Verify')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.is_verify and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/')
        else:
            flash('Failed login. Please check you email or password', 'message')
    return render_template('login.html', form=form, title='Login')


# наш основной ui
@app.route('/', methods=['GET', 'POST'])
def pas():
    return render_template('index.html', title='Home', user=current_user.get_id())


# страница профиля
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    user = User.query.filter_by(id=current_user.get_id()).first()
    form = TypeMailCountry()
    if form.validate_on_submit() and request.method == "POST":
        from elasticsearch import Elasticsearch
        es = Elasticsearch(
            cloud_id='Nikita:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyRmMDNkNTM2NjZlZDc0ODg0OTZhNThmMjUxMGE0MDJkYSQwNGQzODU4ZDVlYTA0MTkxYmIxZjY4YmUwOGUxNmIxYQ==',
            http_auth=('elastic', 'EEekFX8RuRgffcR4QsD0tT4C')
        )
        info = dict()
        info['user'] = user.email
        info['type_mailing'] = form.state_mail.data
        info['country'] = form.state_country.data
        es.index(index='mailing', body=info)
        es.indices.refresh(index='mailing')
        return render_template('user.html', title='Profile setting', user=user, form = form, message='Your choice is saved!')

    return render_template('user.html', title='Profile setting',
                           user=user, form=form)


# @app.route('/to_elastic', methods=['GET', 'POST'])
# @login_required
# def to_elastic():
#     type = request.form.get('type')
#     country = request.form.get('type')
#
#     return render_template('user.html', title='Profile setting', user=user)


# логаут
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('pas'))
