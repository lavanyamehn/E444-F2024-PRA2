from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap 
from flask_moment import Moment
from datetime import datetime, timezone
from flask_wtf import FlaskForm
import email_validator
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_application_key_is_difficult_to_guess'
bootstrap = Bootstrap(app)
moment = Moment(app)

class LoginForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])

    # def validate_email(form, field):
    #     if "utoronto" not in field.data:
    #         raise ValidationError("Email must be a valid UofT email address!")

    email = StringField('What is your UofT email?', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        old_email = session.get('email')
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!')
        session['name'] = form.name.data
        session['email'] = form.email.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), email=session.get('email'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=session.get('name'), current_time=datetime.now(timezone.utc))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
