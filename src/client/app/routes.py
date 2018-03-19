from flask import render_template
from app import app
from app.forms import RegistrationForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)
