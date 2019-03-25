from flask import current_app
from app import db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    image_file = db.Column(db.String(), nullable=False, default='default.svg')
    password = db.Column(db.String(64), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f'User id: {self.id} | {self.username} | {self.email}'

    def get_psw_reset_token(self, expires_sec=3600):
        t = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return t.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_psw_reset_token(token):
        t = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = t.loads(token)['user_id']
            return User.query.get(user_id)
        except:
            return None

@login_manager.user_loader
def load_user(user_id):
    '''Finds user by its id and returns it'''
    return User.query.get(int(user_id))
