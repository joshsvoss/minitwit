from app import db
from werkzeug import generate_password_hash

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(256))
    pw_hash = db.Column(db.String(256))

    def __init__(self, username, email, pw_hash):
        self.username = username
        self.email = email
        self.pw_hash = generate_password_hash(pw_hash)

    def __repr__(self):
        return '<Name %r>' % self.username

    def insert(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
