from flask import Flask, render_template
from forest_DB import forest_db, Forest

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forest.db'

forest_db.init_app(app)

@app.route('/')
def main():
    forestsDb = Forest.query.all()

    return render_template('index.html', forests=forestsDb)

@app.route('/admin')
def admin():
    return render_template('admin.html')


if __name__ == '__main__':    
    with app.app_context():
        forest_db.create_all()
    app.run(debug=True)