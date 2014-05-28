from minitwit import db

Follower = db.Table('follower',
    db.Column('who_id', db.Integer, db.ForeignKey('user.user_id')),
    db.Column('whom_id', db.Integer, db.ForeignKey('user.user_id')))


def follows(follower, user): #TODO: Test this!
    return Follower.select(who_id=follower.user_id,
                           whom_id=user.user_id)
