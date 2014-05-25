# -*- coding: utf-8 -*-
"""
    MiniTwit
    ~~~~~~~~

    A microblogging application written with Flask

    :copyright: (c) 2014 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

from flask import Flask, request, g, redirect, session, render_template, flash, abort
from flask.ext.sqlalchemy import SQLAlchemy
import time
import controller

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
                           messages=controller.get_timeline(g.user))

@app.route('/public')
def public_timeline():
    """Displays the latest messages of all users."""
    return render_template('timeline.html',
                           messages=controller.get_all_timeline())

@app.route('/add_message', methods=['POST'])
def add_message():
    """Registers a new message for the user."""
    from message import Message #prevent circular import
    if 'user_id' not in session:
        about(401)
    if request.form['text']:
        user_id = session['user_id']
        text = request.form['text']
        pub_date = time.time()
        controller.create_message(user_id, text, pub_date)
        flash('Your message was recorded')
    return redirect('/')

@app.route('/<username>')
def user_timeline(username):
    """Displays a user's tweets."""
    profile_user = None
    if profile_user is None:
        abort(404)
    followed = False
    if g.user:
        followed = False #TODO: Check if the user is followed by you
        return render_template('timeline', messages=[], followed=followed,
                               profile_user=profile_user)

@app.route('/<username>/follow')
def follow_user(username):
    """Adds the current user as a follower of the given user"""
    if not g.user:
        abort(401)
    whom_id = 0 #TODO: Let's get this from the User object
    #TODO: Insert follower
    flash('You are now following "%s"' % username)
    return redirect('/' + username)


@app.route('/<username>/unfollow')
def unfollow_user(username):
    """Removes the current user as follower of the given user."""
    if not g.user:
        abort(401)
    whom_id = 0 #TODO: Let's get this from the User object
    if whom_id is None:
        abort(404)
    #TODO: Delete the follower relationship
    flash('You are no longer following "%s"' % username)
    return redirect('/' + username)

@app.before_request
def before_request():
    """Make sure the global object has a user"""
    from user import User #prevent circular import
    g.user = None
    if 'user_id' in session:
        g.user = User.query.filter_by(user_id=session['user_id']).first()

set_jinja_filters(app)
app.register_blueprint(USER_SESSION)

if __name__ == '__main__':
    app.run(debug=True)
