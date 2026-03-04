from flask_sqlalchemy import SQLAlchemy

forest_db = SQLAlchemy()

class Forest(forest_db.Model):
    id = forest_db.Column(forest_db.Integer, primary_key=True)
    mainForest = forest_db.Column(forest_db.String(100), nullable=False)
    forest = forest_db.Column(forest_db.String(100), nullable=False)
    typeCutting = forest_db.Column(forest_db.String(100), nullable=False)
    quarter = forest_db.Column(forest_db.String(100), nullable=False)
    department = forest_db.Column(forest_db.String(100), nullable=False)
    area = forest_db.Column(forest_db.Float, nullable=False)
    volumeForestManagement = forest_db.Column(forest_db.Float, nullable=False)    
    month = forest_db.Column(forest_db.String(50), nullable=False)
    decade = forest_db.Column(forest_db.String(50), nullable=False)
    year = forest_db.Column(forest_db.Integer, nullable=False)


class User(UserMixin, user_db.Model):
    id = user_db.Column(user_db.Integer, primary_key=True)
    isAdmin = user_db.Column(user_db.Boolean, default=False)
    username = user_db.Column(user_db.String(150), unique=True, nullable=False)
    gmail = user_db.Column(user_db.String(150), unique=True, nullable=False)
    password_hash = user_db.Column(user_db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)