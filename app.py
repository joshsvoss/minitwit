# -*- coding: utf-8 -*-
"""
    MiniTwit
    ~~~~~~~~

    A microblogging application written with Flask

    :copyright: (c) 2014 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

from flask import Flask, request, g, redirect, session, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy
import time

from filters import set_jinja_filters
from usersession import USER_SESSION

app = Flask(__name__)
app.config.from_envvar('MINITWIT_SETTINGS', silent=True)
app.config['SECRET_KEY'] = "dev"

db = SQLAlchemy(app)


@app.route('/')
def timeline():
    """Shows users a timeline or if no user i logged in it will
    redirect to the public timeline.  This timeline shows the user's
    messages as well as all the messages of followed users"""
    if not g.user:
        return redirect('/public')
    return render_template('timeline.html',
                           messages=get_messages(g.user.user_id))

@app.route('/public')
def public_timeline():
    """Displays the latest messages of all users."""
    from message import Message #prevent circular import
    from user import User
    return render_template('timeline.html', messages=get_messages())

@app.route('/add_message', methods=['POST'])
def add_message():
    """Registers a new message for the user."""
    from message import Message #prevent circular import
    if 'user_id' not in session:
        about(401)
    if request.form['text']:
        Message(session['user_id'], request.form['text'],
                int(time.time())).insert()
        flash('Your message was recorded')
    return redirect('/')

@app.before_request
def before_request():
    """Make sure the global object has a user"""
    from user import User #prevent circular import
    g.user = None
    if 'user_id' in session:
        g.user = User.query.filter_by(user_id=session['user_id']).first()

def get_messages(user_id=None):
    from message import Message
    from user import User
    if user_id is None:
        return db.session.query(Message, User
                            ).filter(Message.author_id == User.user_id)
    return db.session.query(Message, User
                            ).filter(Message.author_id == user_id)

set_jinja_filters(app)
app.register_blueprint(USER_SESSION)

if __name__ == '__main__':
    app.run(debug=True)
