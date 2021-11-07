from productivity import app, db, url_timestamp, url_viewtime, prev_url
from flask import render_template, Response, redirect, url_for, flash, jsonify, request
from productivity.cam import camera, gen_frames,process_frames
from productivity.forms import RegisterForm, LoginForm, CamStop
from productivity.models import User
from productivity.url_parse import url_strip
from productivity.webWithMostHits import mostHits
from productivity.cleanViewDict import editViewTimes
from flask_login import login_user, logout_user, login_required, current_user
import time


@app.route('/')
def confirm_page():
    return render_template('confirmPage.html')

@app.route('/home', methods=['GET', 'POST'])
def home_page():
    stop = CamStop()
    if request.method == 'POST':
        loop = request.form.get('loop')
        if loop == "False":
            camera.release()
        return redirect(url_for('home_page'))
    else:
        return render_template('index.html', stop=stop)

@app.route('/distractionCount')
def distractionCount():
    return process_frames()

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successfully! You are now logged in as {user_to_create.username}')
        return redirect(url_for('home_page'))
    if form.errors != {}: # If there are errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}')
            return redirect(url_for('home_page'))
        else:
            flash('Username & password do not match! Please try again.')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out!')
    return redirect(url_for('home_page'))

@app.route('/send_url', methods=['POST'])
def send_url():
    resp_json = request.get_data()
    params = resp_json.decode()
    url = params.replace("url=", "")
    print("currently viewing: " + url_strip(url))
    parent_url = url_strip(url)

    global url_timestamp
    global url_viewtime
    global prev_url

    print("initial db prev tab: ", prev_url)
    print("initial db timestamp: ", url_timestamp)
    print("initial db viewtime: ", url_viewtime)

    if parent_url not in url_timestamp.keys():
        url_viewtime[parent_url] = 0

    if prev_url != '':
        time_spent = int(time.time() - url_timestamp[prev_url])
        url_viewtime[prev_url] = url_viewtime[prev_url] + time_spent

    x = int(time.time())
    url_timestamp[parent_url] = x
    prev_url = parent_url
    print("final timestamps: ", url_timestamp)
    print("final viewtimes: ", url_viewtime)

    return jsonify({'message': 'success!'}), 200

@app.route('/quit_url', methods=['POST'])
def quit_url():
    resp_json = request.get_data()
    print("Url closed: " + resp_json.decode())
    return jsonify({'message': 'quit success!'}), 200

@app.route('/start')
def start_page():
    url_timestamp = {}
    url_viewtime = {}
    prev_url = ""
    return redirect(url_for('home_page'))


@app.route('/end')
def end_page():
    return redirect(url_for('home_page'))


@app.route('/Tables')
def tables_page():
    dic = {'url':6,'google.com':156,'gmail.com':2}
    return render_template('Tables.html',url_viewtime=url_viewtime,websites=mostHits(url_viewtime.copy()))