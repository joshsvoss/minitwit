from app import db

def get_all_messages():
    """Query the database for all messages from all users"""
    from user import User
    return db.session.query(Message, User). \
        filter(Message.author_id == User.user_id)

def get_messages(user_id):
    """Query the database for all messages by user_id"""
    from user import User
    return db.session.query(Message, User).filter(Message.author_id == user_id)

class Message(db.Model):
    """Tweet mapping"""
    message_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    text = db.Column(db.Text)
    pub_date = db.Column(db.Integer)

    def __init__(self, author_id, text, pub_date):
        self.author_id = author_id
        self.text = text
        self.pub_date = pub_date

    def insert(self, commit=True):
        """Insert and commit this message"""
        db.session.add(self)
        if commit:
            db.session.commit()
