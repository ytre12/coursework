from flask import Flask, render_template, request, redirect, url_for, jsonify
from DB import db, Forest, User, Comits, Forum, Favorite
from datetime import datetime
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy import func

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
@app.route('/api/forests', methods=['GET'])
def get_forests():
    forests = Forest.query.all()
    
    favorite_forest_ids = []
    if current_user.is_authenticated:
        # Змінено user_id на userID
        user_favs = Favorite.query.filter_by(userID=current_user.id).all()
        # Змінено forest_id на forestID
        favorite_forest_ids = [fav.forestID for fav in user_favs]

    return jsonify([{
        'id': forest.id,
        'mainForest': forest.mainForest,
        'forest': forest.forest,
        'typeCutting': forest.typeCutting,
        'quarter': forest.quarter,
        'department': forest.department,
        'area': forest.area,
        'volumeForestManagement': forest.volumeForestManagement,
        'month': forest.month,
        'decade': forest.decade,
        'year': forest.year,
        'is_favorite': forest.id in favorite_forest_ids 
    } for forest in forests])

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
    # Отримуємо параметри з URL (наприклад: ?sort=year&order=desc)
    sort_by = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')

    # Список дозволених колонок (щоб уникнути помилок, якщо в URL введуть щось зайве)
    valid_columns = [
        'id', 'mainForest', 'forest', 'typeCutting', 'quarter', 
        'department', 'area', 'volumeForestManagement', 'month', 'decade', 'year'
    ]

    if sort_by in valid_columns:
        # Динамічно отримуємо колонку з моделі Forest (еквівалентно Forest.year, Forest.area тощо)
        column = getattr(Forest, sort_by)
        
        # Визначаємо напрямок сортування
        if order == 'desc':
            all_forests = Forest.query.order_by(column.desc()).all()
        else:
            all_forests = Forest.query.order_by(column.asc()).all()
    else:
        # Якщо параметра немає, або він неправильний — видаємо все за замовчуванням
        all_forests = Forest.query.all()
    
    # 1. Загальна кількість записів (всі рубки)
    total_cuttings = Forest.query.count()
    
    # 2. Кількість УНІКАЛЬНИХ лісництв (наприклад, скільки різних mainForest у базі)
    unique_forests = db.session.query(func.count(func.distinct(Forest.forest))).scalar()
    
    # 3. Загальна площа (сума всіх значень у колонці area)
    total_area = db.session.query(func.sum(Forest.area)).scalar() 
    # Якщо база порожня, sum поверне None, тому робимо перевірку:
    total_area = round(total_area, 2) if total_area else 0.0

    # 4. (Бонус) Загальний об'єм
    total_volume = db.session.query(func.sum(Forest.volumeForestManagement)).scalar()
    total_volume = round(total_volume, 2) if total_volume else 0.0

    # Передаємо ці змінні у шаблон
    return render_template('change.html', 
                           forests=all_forests, # твоя відсортована база
                           total_cuttings=total_cuttings,
                           unique_forests=unique_forests,
                           total_area=total_area,
                           total_volume=total_volume)

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
    # Отримуємо параметри сортування
    sort_by = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')

    # Дозволені колонки для таблиці User
    valid_columns = ['id', 'username', 'gmail', 'isAdmin']

    if sort_by in valid_columns:
        # Динамічно отримуємо колонку (User.id, User.username тощо)
        column = getattr(User, sort_by)
        
        if order == 'desc':
            users = User.query.order_by(column.desc()).all()
        else:
            users = User.query.order_by(column.asc()).all()
    else:
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
        new_comment = Forum(username=current_user.username, comment=comment, userID=current_user.id, date=datetime.utcnow(), isAdmin=current_user.isAdmin)
        db.session.add(new_comment)
        db.session.commit()
        return redirect('/forum')

    all_comments = Forum.query.order_by(Forum.date.desc()).all()
    
    return render_template('forum.html', comments=all_comments)

@app.route('/delete_forum_comment/<int:id>', methods=['POST', 'GET'])
@login_required
@admin_required
def delete_forum_comment(id):
    comment = Forum.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    return redirect('/forum')

@app.route('/about_ass')
@login_required
def about_ass():
    return render_template('about_ass.html')

@app.route('/favorite')
@login_required
def favorite():
    # Змінено user_id на userID
    user_favorites = Favorite.query.filter_by(userID=current_user.id).all()
    
    # Змінено forest_id на forestID
    forest_ids = [fav.forestID for fav in user_favorites]
    
    favorite_forests = Forest.query.filter(Forest.id.in_(forest_ids)).all()

    return render_template('favorite.html', forests=favorite_forests)

@app.route('/api/toggle_favorite', methods=['POST'])
def toggle_favorite():
    if not current_user.is_authenticated:
        return jsonify({'error': 'Необхідно увійти в систему'}), 401

    data = request.get_json()
    # Це значення приходить з JS, тому тут залишається forest_id (як ми писали в JS)
    forest_id_from_js = data.get('forest_id')

    # Змінено filter_by на userID та forestID
    favorite = Favorite.query.filter_by(userID=current_user.id, forestID=forest_id_from_js).first()

    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({'status': 'removed'})
    else:
        # Змінено імена полів при створенні нового запису
        new_favorite = Favorite(userID=current_user.id, forestID=forest_id_from_js)
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify({'status': 'added'})

if __name__ == '__main__':    
    with app.app_context():
        db.create_all() 
    app.run(debug=True)