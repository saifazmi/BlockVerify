import os
from flask import render_template, flash, url_for, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from app import app, db, gpg
from app.forms import RegistrationForm, LoginForm, AddFileForm, VerifyFileForm
from app.models import User
from app.file_handler import file_hash, file_signature, signature_key
from app.block_api import add_to_chain, chain_search_file


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.set_key()
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/add_file', methods=['GET', 'POST'])
@login_required
def add_file():
    form = AddFileForm()
    code = None
    response = None
    file_data = {}
    if form.validate_on_submit():
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(url_for('add_file'))
            file = request.files['file']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file:
                file_data['file_name'] = secure_filename(file.filename)

                file.save(os.path.join(
                    app.config['UPLOAD_FOLDER'], file_data['file_name']))

                file_data['file_hash'] = file_hash(file_data['file_name'])
                file_data['file_signature'] = file_signature(
                    file_data['file_hash'], current_user.key_fingerprint)
                file_data['sign_key'] = signature_key(
                    current_user.key_fingerprint)

                code, response = add_to_chain(file_data)
                return render_template(
                    'add_file.html', title='Add File', form=form, code=code,
                    response=response, file_data=file_data)

    return render_template(
        'add_file.html', title='Add File', form=form, code=code,
        response=response, file_data=file_data)


@app.route('/verify_file', methods=['GET', 'POST'])
def verify_file():
    form = VerifyFileForm()
    code = None
    response = None
    verify = None
    if form.validate_on_submit() and request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('verify_file'))
        file = request.files['file']
        if file:
            file_name = secure_filename(file.filename)
            file.save(os.path.join(
                app.config['UPLOAD_FOLDER'], file_name))
            verify_file_hash = file_hash(file_name)
            code, response = chain_search_file(verify_file_hash)
            if code is 200:
                verify = gpg.verify(response.get('txn').get('signature'))
            return render_template(
                    'verify_file.html', title='Verify File', form=form,
                    code=code, response=response, verify=verify)
    return render_template('verify_file.html', title='Verify File', form=form, code=code,response=response, verify=verify)


@app.route('/pub_key/<key_fingerprint>')
def pub_key_id(key_fingerprint):
    return '<pre>{}</pre>'.format(gpg.export_keys(key_fingerprint))


@app.route('/pub_key/<username>')
def pub_key_username(username):
    user = User.query.filter_by(username=username).first_or_404()
    return '<pre>{}</pre>'.format(gpg.export_keys(user.key_fingerprint))
