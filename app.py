from flask import Flask, render_template, request, redirect, url_for
from forest_DB import forest_db, Forest

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forest.db'

forest_db.init_app(app)

@app.route('/')
def main():
    forestsDb = Forest.query.all()

    return render_template('index.html', forests=forestsDb)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        mainForest = request.form['mainForest']
        forest = request.form['forest']
        typeCutting = request.form['typeCutting']
        quarter = request.form['quarter']
        department = request.form['department']
        area = request.form['area']
        volumeForestManagement = request.form['volumeForestManagement']
        month = request.form['month']
        decade = request.form['decade']
        year = request.form['year']

        new_forest = Forest(
            mainForest=mainForest, 
            forest=forest, 
            typeCutting=typeCutting, 
            quarter=quarter, 
            department=department, 
            area=area, 
            volumeForestManagement=volumeForestManagement, 
            month=month, 
            decade=decade, 
            year=year
        )

        forest_db.session.add(new_forest)
        forest_db.session.commit()
        return redirect('/admin')

    return render_template('admin.html')



if __name__ == '__main__':    
    with app.app_context():
        forest_db.create_all()
    app.run(debug=True)