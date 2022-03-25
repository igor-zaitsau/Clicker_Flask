from dbase import dbase
from UserLogin import UserLogin

from flask_login import LoginManager, login_required, login_user, current_user, logout_user

from flask import *
import sqlite3
import hashlib
import json

import os



DATABASE = 'DataBaseCourseWork.db'
SECRET_KEY = '45rtyfgvbnjkjiu'
DEBUG = True


app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'DataBaseCourseWork.db')))

login_manager = LoginManager(app)
login_manager.login_view = 'sign_up'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым разделам!"
login_manager.login_message_category = 'fail'


n = {'Home': 'Home', 'Buy': 'Buy', 'Top_players': 'Top players', 'Chat' : 'Chat'}


def connect_db():
    connection = sqlite3.connect('DataBaseCourseWork.db')
    connection.row_factory = sqlite3.Row
    return connection


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@login_manager.user_loader
def load_user(userID):
    return UserLogin().fromDB(userID, enter)


enter = None
@app.before_request
def befor_request():
    global enter
    enter = dbase(get_db())


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/save', methods=['POST'])
def save():
    if current_user.get_id() != None:
        qtc_data = int(request.get_json())
        enter.setScore(qtc_data, current_user.get_id())
        return jsonify({'processed': 'true'})

    return jsonify({'processed': 'false'})


@app.route('/LogOut')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
def index():
    if current_user.get_id() != None:
        score = enter.score(current_user.get_id())
        score = score[0]
    else:
        score = 0
    return render_template('index.html', n=n['Home'],  score=score)


@app.route('/Donat')
@login_required
def donat():
    return render_template('Donat.html', n=n['Buy'])


@app.route('/Rating')
def rating():
    r = enter.top_players()
    return render_template('rating.html', n=n['Top_players'], rows=r)


@app.route('/sign_up', methods=["POST", "GET"])
def sign_up():
    if request.method == 'POST':

        user = enter.getUserByEmail(request.form['email'])

        hash_object = hashlib.md5(request.form['password'].encode())

        if user and hash_object.hexdigest() == user['password']:
            userlogin = UserLogin().create(user)
            login_user(userlogin, remember=True)
            return redirect(request.args.get("next") or url_for('index'))

        flash('Неверный логин или пароль!!!', category='fail')

    return render_template('sign_up.html')


@app.route('/registration', methods=["POST", "GET"])
def registration():
    if request.method == 'POST':
        obj = enter.registration(request.form)
        if obj:
            return redirect(url_for('sign_up'))

    return render_template('registration.html')


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('Error404.html')


if __name__ == '__main__':
    app.run(debug=True)