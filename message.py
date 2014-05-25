from app import db

class Message(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    text = db.Column(db.Text)
    pub_date = db.Column(db.Integer)

    def __init__(self, author_id, text, pub_date):
        self.author_id = author_id
        self.text = text
        self.pub_date = pub_date

    def insert(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
