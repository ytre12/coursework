from flask import Flask, render_template, request, redirect, url_for
from DB import db, Forest, User, Comits
from datetime import datetime
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from decorators import admin_required

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forests.db'
app.config['SECRET_KEY'] = 'your-secret-key-here'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

db.init_app(app)

@app.route('/')
def main():
    forestsDb = Forest.query.all()
    return render_template('index.html', forests=forestsDb)

@app.route('/admin', methods=['GET', 'POST'])
@login_required
@admin_required
def admin():
    if request.method == 'POST':
        new_forest = Forest(
            mainForest=request.form['mainForest'], 
            forest=request.form['forest'], 
            typeCutting=request.form['typeCutting'], 
            quarter=request.form['quarter'], 
            department=request.form['department'], 
            area=float(request.form['area']),
            volumeForestManagement=float(request.form['volumeForestManagement']), 
            month=request.form['month'], 
            decade=request.form['decade'], 
            year=int(request.form['year'])
        )

        db.session.add(new_forest) 
        db.session.commit()
        return redirect('/admin')

    return render_template('admin.html')

@app.route('/change', methods=['POST', 'GET'])
@login_required
@admin_required
def change():
    all_forests = Forest.query.all()
    return render_template('change.html', forests=all_forests)

@app.route('/delete/<int:id>', methods=['POST', 'GET'])
@login_required
@admin_required
def delete(id):
    forest = Forest.query.get_or_404(id)
    db.session.delete(forest)
    db.session.commit()
    return redirect('/change')

@app.route('/delete_user/<int:id>', methods=['POST', 'GET'])
@login_required
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/all_users')

@app.route('/toggle_admin/<int:id>', methods=['POST', 'GET'])
@login_required
@admin_required
def toggle_admin(id):
    user = User.query.get_or_404(id)
    user.isAdmin = not user.isAdmin
    db.session.commit()
    return redirect('/all_users')

@app.route('/edit/<int:id>', methods=['POST', 'GET'])
@login_required
@admin_required
def edit(id):
    forest = Forest.query.get_or_404(id)
    if request.method == 'POST':
        forest.mainForest = request.form['mainForest']
        forest.forest = request.form['forest']
        forest.typeCutting = request.form['typeCutting']
        forest.quarter = request.form['quarter']
        forest.department = request.form['department']
        forest.area = float(request.form['area'])
        forest.volumeForestManagement = float(request.form['volumeForestManagement'])
        forest.month = request.form['month']
        forest.decade = request.form['decade']
        forest.year = int(request.form['year'])

        db.session.commit()
        return redirect('/change')

    return render_template('edit.html', forest=forest)

@app.route('/all_users', methods=['POST', 'GET'])
@login_required
@admin_required
def all_users():
    users = User.query.all()
    return render_template('all_user.html', users=users)


# ============= Користувачі ============
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        gmail = request.form['gmail']
        password = request.form['password']

        existing_user = User.query.filter((User.username == username) | (User.gmail == gmail)).first()
        if existing_user:
            return "Користувач з таким ім'ям або поштою вже існує"

        new_user = User(username=username, gmail=gmail)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

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

@app.route('/comits', methods=['GET', 'POST'])
@login_required
@admin_required
def comits():
    if request.method == 'POST':
        username = request.form['username']
        comment = request.form['comment']
        new_commit = Comits(username=username, comment=comment, date=datetime.utcnow())
        db.session.add(new_commit)
        db.session.commit()
        return redirect('/comits')

    all_comits = Comits.query.all()
    
    return render_template('comits.html', comits=all_comits)

@app.route('/delete_commit/<int:id>', methods=['POST', 'GET'])
@login_required
@admin_required
def delete_commit(id):
    commit = Comits.query.get_or_404(id)
    db.session.delete(commit)
    db.session.commit()
    return redirect('/comits')

@app.route('/forum', methods=['GET', 'POST'])
@login_required
def forum():
    if request.method == 'POST':
        comment = request.form['comment']
        new_comment = Comits(username=current_user.username, comment=comment, date=datetime.utcnow(), isAdmin=current_user.isAdmin)
        db.session.add(new_comment)
        db.session.commit()
        return redirect('/forum')

    all_comments = Comits.query.order_by(Comits.date.desc()).all()
    
    return render_template('forum.html', comments=all_comments)

if __name__ == '__main__':    
    with app.app_context():
        db.create_all() 
    app.run(debug=True)