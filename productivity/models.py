from productivity import db, login_manager, bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email_address = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(60), nullable=False)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password): 
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class Session(db.Model):
    session_id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.DateTime(), nullable=False)

class SessionRecord(db.Model):
    session_id = db.Column(db.Integer(), primary_key=True)
    