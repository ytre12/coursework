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