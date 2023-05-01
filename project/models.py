from project import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Url(db.Model):
    """
    Class that represents the urls that will be shortened. 
    """

    __tablename__ = 'urls'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    original_url = db.Column(db.String, nullable=False)
    short_url = db.Column(db.String, nullable=True)
    clicks = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # def __init__(self, created, original_url, clicks, user_id):
    #     self.created = created
    #     self.original_url = original_url
    #     self.clicks = clicks
    #     self.user_id = user_id


class User(db.Model):
    """
    Class that represents a user of the application
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    password_hashed = db.Column(db.String(128))
    urls = db.relationship('Url', backref='user', lazy='dynamic')

    def __init__(self, email, password_plaintext):
        self.email = email
        self.password_hashed = self._generate_password_hash(password_plaintext)

    def is_password_correct(self, password_plaintext: str):
        return check_password_hash(self.password_hashed, password_plaintext)

    @staticmethod
    def _generate_password_hash(password_plaintext):
        return generate_password_hash(password_plaintext)

    def __repr__(self):
        return f'<User: {self.email}>'

    @property
    def is_authenticated(self):
        """Return True if the user has been successfully registered."""
        return True

    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True

    @property
    def is_anonymous(self):  # NEW!!
        """Always False, as anonymous users aren't supported."""
        return False

    def get_id(self):  # NEW!!
        """Return the user ID as a unicode string (`str`)."""
        return str(self.id)
