from flask import Flask, render_template, request, redirect, url_for
from forest_DB import forest_db, Forest
from user_DB import user_db, User
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forest.db'
app.config['SECRET_KEY'] = 'your-secret-key-here'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

forest_db.init_app(app)
user_db.init_app(app)

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

@app.route('/change', methods=['POST', 'GET'])
def change():
    forest_db = Forest.query.all()

    return render_template('change.html', forests=forest_db)

@app.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete(id):
    forest = Forest.query.get_or_404(id)
    forest_db.session.delete(forest)
    forest_db.session.commit()
    return redirect('/change')

@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    forest = Forest.query.get_or_404(id)
    if request.method == 'POST':
        forest.mainForest = request.form['mainForest']
        forest.forest = request.form['forest']
        forest.typeCutting = request.form['typeCutting']
        forest.quarter = request.form['quarter']
        forest.department = request.form['department']
        forest.area = request.form['area']
        forest.volumeForestManagement = request.form['volumeForestManagement']
        forest.month = request.form['month']
        forest.decade = request.form['decade']
        forest.year = request.form['year']

        forest_db.session.commit()
        return redirect('/change')

    return render_template('edit.html', forest=forest)


#Користувачі
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        gmail = request.form['gmail']
        password = request.form['password']

        existing_user = User.query.filter((User.username == username) | (User.gmail == gmail)).first()
        if existing_user:
            return "Користувач з таким ім'ям вже існує"

        new_user = User(username=username, gmail=gmail)
        new_user.set_password(password)
        user_db.session.add(new_user)
        user_db.session.commit()

        return redirect('/')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect('/')
        else:
            return "Неправильне ім'я користувача або пароль"

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')



if __name__ == '__main__':    
    with app.app_context():
        forest_db.create_all()
        user_db.create_all()
    app.run(debug=True)