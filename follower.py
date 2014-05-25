from app import db

class Follower(db.Model):
    who_id = db.Column(db.Integer, db.ForeignKey('person.user_id'))
    whom_id = db.Column(db.Integer, db.ForeignKey('person.user_id'))

    def __init__(self, who, whom):
        self.who_id = who
        self.whom_id = whom
