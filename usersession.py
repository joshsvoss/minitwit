"""User functions: Register, Login and Logout"""

from flask import (Blueprint, g, redirect,
                   url_for, session,
                   flash, render_template, request)


USER_SESSION = Blueprint('USER_SESSION', __name__,
                         template_folder='templates')


@USER_SESSION.route('/login', methods=['GET', 'POST'])
def login():
    """Log in user if not logged in, the redirect to timeline"""
    from user import User #Prevent circular import!
    if g.user:
        return redirect('/')
    error = None
    if request.method == 'POST':
        user = User.query.filter_by(username=
                                    request.form['username']).first()
        if user is None:
            error = 'Invalid Username'
        #elif not check_password_hash(user['pw_hash'], request.form['password'])
        else:
            flash('You were logged in')
            session['user_id'] = user.user_id
        return redirect(url_for('timeline'))
    return render_template('login.html', error=error)

@USER_SESSION.route('/logout')
def logout():
    """Logs the user out."""
    flash('You were logged out')
    session.pop('user_id', None)
    return redirect('/public')


@USER_SESSION.route('/register', methods=['GET', 'POST'])
def register():
    """registers the user"""
    from user import User #Prevent circular import!
    if g.user:
        return redirect('/')
    error = None
    if request.method == 'POST':
        if not request.form['username']:
            error = 'You have to enter a username'
        elif not request.form['email'] or \
             '@' not in request.form['email']:
            error = 'You have to enter a valid email address'
        elif not request.form['password']:
            error = 'You have to enter a password'
        elif request.form['password'] != request.form['password2']:
            error = 'The two passwords do not match'
        elif User.query.filter_by(username=
                                  request.form['username']).first() is not None:
            error = 'The username is already taken'
        else:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            User(username, email, password).insert()
            flash('You were successfully registered and can login now')
            return redirect('/login')
    return render_template('register.html', error=error)
