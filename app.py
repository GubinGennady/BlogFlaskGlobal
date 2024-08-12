import os
from flask import render_template, request, flash, redirect, send_from_directory
from flask_migrate import Migrate
from forms import LoginForm, FDataBase
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash
from models import create_app, db
from datetime import datetime

app = create_app()
app.config['UPLOAD_FOLDER'] = 'uploads'
UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__, )), 'uploads')
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth'


@app.route('/uploads/<filename>')
def upload_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@login_manager.user_loader
def load_user(user_id):
    from models import User
    return db.session.query(User).get(int(user_id))


@app.route('/')
def container():
    from models import Post
    post_all = db.session.query(Post).all()
    return render_template('index.html', post_all=post_all)


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        from models import User
        login = request.form.get('login')
        password = generate_password_hash(request.form.get('password'))
        user = User(login=login, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect('/auth')
    return render_template('registretion.html')


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    form = LoginForm()
    error = ''
    if form.validate_on_submit():
        from models import User
        user = db.session.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect('/')
        else:
            error += 'Login error'
    return render_template('auth.html', form=form, error=error)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route("/add_post", methods=["POST", "GET"])
def addPost():
    # db = get_db()
    dbase = FDataBase()

    if dbase.validate_on_submit():

        title = dbase.title.data
        description = dbase.description.data

        if len(title) > 4 and len(description) > 10 and 'image' in request.files:
            image = request.files['image']
            path = os.path.join('static', app.config['UPLOAD_FOLDER'], image.filename)
            path_t = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(path)
            # res = dbase.addPost(request.form['name'], request.form['post'])
            from models import Post
            res = Post(title=title, description=description, user=current_user.id, image=path_t)
            db.session.add(res)
            db.session.commit()

            if not res:
                flash('Ошибка добавления статьи', category='error')
            else:
                return redirect('/')
        else:
            flash('Ошибка добавления статьи', category='error')

    return render_template('add_post.html', form=dbase, title="Добавление статьи")


@app.route('/delete/<int:id_post>')
@login_required
def delete(id_post):
    from models import Post, Comment

    post = Post.query.get_or_404(id_post)

    if post.user != current_user.id:
        flash('У вас нет прав на удаление этой статьи', category='error')
        return redirect('/')
        
    if Comment.query.filter_by(post=id_post).first():
        flash('Есть комментарий, удолить пост не возможно', category='error')
        return redirect('/')

    db.session.delete(post)
    db.session.commit()
    flash('Статья успешно удалена!', category='success')
    return redirect('/')


@app.route('/search', methods=['POST'])
def search():
    title = request.form.get('text')
    from models import Post
    posts = Post.query.filter(Post.title.like('%' + title + '%')).all()
    str = '<uL class="res_search_items">'
    for post in posts:
        str += f'<li><a href="/post/{post.id}">{post.title}</a></li>'
    str += '</ul>'
    return str


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    id = int(id)
    from models import Post
    post = Post.query.get_or_404(id)
    if post.user != current_user.id:
        flash('У вас нет прав на редактирование поста', category='error')
        return redirect('/')
    else:
        form = FDataBase(obj=post)
        if form.validate_on_submit():
            form.populate_obj(post)
            db.session.commit()
            flash('Вы успешно обновили пост', category='success')
            return redirect('/')
        return render_template('edit_post.html', form=form, post=post)


@app.route('/view/<int:id>', methods=['GET', 'POST'])
def view_post(id):
    id = int(id)
    from models import Comment, User, Post, Like
    likes = len(Like.query.filter_by(post=id, type='like').all())
    dislikes = len(Like.query.filter_by(post=id, type='dislike').all())
    is_like = False
    if not Like.query.filter_by(post=id, user=current_user.id, type='like').first():
        is_like = True

    is_dislike = False
    if not Like.query.filter_by(post=id, user=current_user.id,  type='dislike').first():
        is_dislike = True
    comments = Comment.query.filter_by(post=id).all()
    comment_new = []
    for comment in comments:
        user_obj = User.query.get_or_404(comment.user)
        datetime_string = str(comment.timestamp)
        date = datetime.strptime(datetime_string, '%Y-%m-%d %H:%M:%S.%f')
        formatted_date = date.strftime('%d.%m.%Y')

        comment_new.append({
            'comment': comment.comment,
            'login': user_obj.login,
            'date': formatted_date
        })


    if request.method == 'POST':

        id_user = current_user.id
        comment = request.form.get('comment')
        com = Comment(user=id_user, comment=comment, post=id)
        db.session.add(com)
        db.session.commit()
        flash('Вы оставили комментарий', 'success')
        return redirect(f'/view/{id}')
    else:
        post = Post.query.get_or_404(id)
        return render_template('view_post.html', post=post, comments=comment_new,likes=likes, is_like=is_like, is_dislike=is_dislike,dislikes=dislikes)


@app.route('/addlike/<int:id>')
def addlike(id):
    if current_user.is_authenticated:
        from models import Like
        user = current_user.id
        post = id
        type = 'like'
        if not Like.query.filter_by(post=post,user=user).first():
            add_likes = Like(post=post, user=user, type=type)
            db.session.add(add_likes)
            db.session.commit()
        else:
            l = Like.query.filter_by(post=post,user=user).first()
            like = Like.query.get_or_404(l.id)
            db.session.delete(like)
            db.session.commit()
        return redirect(f'/view/{id}')
    else:
        return redirect('/')


@app.route('/adddislike/<int:id>')
def adddislike(id):
    if current_user.is_authenticated:
        from models import Like
        user = current_user.id
        post = id
        type = 'dislike'
        if not Like.query.filter_by(post=post,user=user).first():
            add_dislikes = Like(post=post, user=user, type=type)
            db.session.add(add_dislikes)
            db.session.commit()
        else:
            l = Like.query.filter_by(post=post,user=user).first()
            dislike = Like.query.get_or_404(l.id)
            db.session.delete(dislike)
            db.session.commit()
        return redirect(f'/view/{id}')
    else:
        return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
