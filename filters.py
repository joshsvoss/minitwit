from hashlib import md5
from datetime import datetime

def format_datetime(timestamp):
    """Format a timestamp for display."""
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')


def gravatar_url(email, size=80):
    """Return the gravatar image for the given email address."""
    return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
        (md5(email.strip().lower().encode('utf-8')).hexdigest(), size)

def set_jinja_filters(app):
    app.jinja_env.filters['datetimeformat'] = format_datetime
    app.jinja_env.filters['gravatar'] = gravatar_url
