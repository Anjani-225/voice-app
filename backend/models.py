from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    # __tablename__ = 'users'
    # user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    audio_files = db.relationship('AudioFile', backref='user', lazy=True)

class AudioFile(db.Model):
    __tablename__ = 'audio_files'

    audio_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_path = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    def __init__(self, file_path, user_id):
        self.file_path = file_path
        self.user_id = user_id


# InferenceResult Model
class InferenceResult(db.Model):
    __tablename__ = 'inference_results'

    inference_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    result = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    user = db.relationship('User', backref='inference_results', lazy=True)

    def __init__(self, result, user_id):
        self.result = result
        self.user_id = user_id

