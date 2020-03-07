from app import app, db
from flask import render_template, request
from models import Post, Photos, User, Alert
from functions import allowed_file
from flask_security import login_required, current_user
from PIL import Image
from models import slugify
from config import UPLOAD_FOLDER, rusWeekDays, rusMonths
import base64
import re
import os
import io
import json


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and request.form.get('query'):
        posts = Post.query.msearch(request.form.get('query'), fields=["title"])
    else:
        posts = Post.query.order_by(Post.id.desc())
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    last_post = Post.query.order_by(Post.id.desc()).first()
    last_alert = Alert.query.order_by(Alert.id.desc()).first()
    pages = posts.paginate(page=page, per_page=5)

    return render_template('index.html', pages=pages, last_post=last_post,
                           last_alert=last_alert, weekDays=rusWeekDays, months=rusMonths)


@app.route('/alerts', methods=['POST', 'GET'])
def alerts():
    if request.method == 'POST':
        slug = request.form.get('slug')
        alert = Alert.query.filter(Alert.slug == slug).first()
        Photos.query.filter(Photos.alert_id == alert.id).delete()
        Alert.query.filter(Alert.slug == slug).delete()
        db.session.commit()
    res = []
    alerts = Alert.query.all()
    for i in range(0, len(alerts)):
        res.append([])
        res[i].append(alerts[i])
        res[i].append(Photos.query.filter(Photos.alert_id == alerts[i].id).first().link)

    last_post = Post.query.order_by(Post.id.desc()).first()
    last_alert = Alert.query.order_by(Alert.id.desc()).first()

    return render_template('alerts.html', res=res, last_post=last_post,
                           last_alert=last_alert, weekDays=rusWeekDays, months=rusMonths)


@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        try:
            title = request.form.get('title')
            body = request.form.get('body')
            author = current_user.login
            p = Post(title=title, body=body, author=author)
            db.session.add(p)
            db.session.commit()
        except Exception:
            raise(Exception)

        photos = request.form.get('files')
        photos = json.loads(photos)

        for photo in photos:
            if allowed_file(photo['name']):
                img = Photos(link='static/images/' + slugify(str(p.created), '') + photo['name'], post_id=p.id)
                db.session.add(img)
                db.session.commit()
                image_data = re.sub('^data:image/.+;base64,', '', photo['dataURL'])
                image = Image.open(io.BytesIO(base64.decodebytes(image_data.encode())))
                image.save(UPLOAD_FOLDER + '/' + slugify(str(p.created), '') + photo['name'], 'JPEG')

    last_post = Post.query.order_by(Post.id.desc()).first()
    last_alert = Alert.query.order_by(Alert.id.desc()).first()

    return render_template('create_post.html', last_post=last_post, last_alert=last_alert,
                           weekDays=rusWeekDays, months=rusMonths)


@app.route('/post_detail/<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first()
    if not post:
        return
    else:
        photos = Photos.query.filter(Photos.post_id == post.id).all()

    last_post = Post.query.order_by(Post.id.desc()).first()
    last_alert = Alert.query.order_by(Alert.id.desc()).first()

    return render_template('post.html', post=post, photos=photos, last_post=last_post,
                           last_alert=last_alert, weekDays=rusWeekDays, months=rusMonths)


@app.route('/red_posts')
def red_posts():
    posts = Post.query.filter(Post.author == current_user.login).order_by(Post.id.desc())
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    pages = posts.paginate(page=page, per_page=5)

    last_post = Post.query.order_by(Post.id.desc()).first()
    last_alert = Alert.query.order_by(Alert.id.desc()).first()

    return render_template('index.html', pages=pages, last_post=last_post, last_alert=last_alert,
                           weekDays=rusWeekDays, months=rusMonths)


@app.route('/update_post/<slug>', methods=['POST', 'GET'])
def update_post(slug):
    if request.method == 'POST':
        post = Post.query.filter(Post.slug == slug).first()
        post.body = request.form.get('body')
        post.title = request.form.get('title')
        db.session.add(post)
        db.session.commit()
    post = Post.query.filter(Post.slug == slug).first()
    #photos = Photos.query.filter(Photos.post_id == post.id).all()

    last_post = Post.query.order_by(Post.id.desc()).first()
    last_alert = Alert.query.order_by(Alert.id.desc()).first()

    return render_template('update_post.html', body=post.body, title=post.title, slug=slug,
                           last_post=last_post, last_alert=last_alert, weekDays=rusWeekDays, months=rusMonths)


@app.route('/delete/<slug>', methods=['GET', 'POST'])
def delete_post(slug):
    last_post = Post.query.order_by(Post.id.desc()).first()
    last_alert = Alert.query.order_by(Alert.id.desc()).first()
    if request.method == 'POST':
        p = Post.query.filter(Post.slug == slug).first()
        photos = Photos.query.filter(Photos.post_id == p.id).all()
        for photo in photos:
            os.remove(photo.link)
        Photos.query.filter(Photos.post_id == p.id).delete()
        Post.query.filter(Post.slug == slug).delete()
        return render_template('delete.html', status=True, last_post=last_post,
                               last_alert=last_alert, weekDays=rusWeekDays, months=rusMonths)

    return render_template('delete.html', status=False, last_post=last_post,
                           last_alert=last_alert, weekDays=rusWeekDays, months=rusMonths)


@app.route('/create_alert', methods=['GET', 'POST'])
def create_alert():
    if request.method == 'POST':
        body = request.form.get('body')
        file = request.files['file']
        alert = Alert(body=body, author=current_user.login)
        db.session.add(alert)
        db.session.commit()
        photo = Photos(link=(UPLOAD_FOLDER + '/' + slugify(str(alert.created), '')+file.filename), alert_id=alert.id)
        db.session.add(photo)
        db.session.commit()
        file.save(os.path.join(UPLOAD_FOLDER, slugify(str(alert.created), '')+file.filename))


    last_post = Post.query.order_by(Post.id.desc()).first()
    last_alert = Alert.query.order_by(Alert.id.desc()).first()

    return render_template('create_alert.html', last_post=last_post,
                           last_alert=last_alert, weekDays=rusWeekDays, months=rusMonths)


@app.route('/contacts')
def contacts():
    last_post = Post.query.order_by(Post.id.desc()).first()
    last_alert = Alert.query.order_by(Alert.id.desc()).first()
    return render_template('contacts.html', last_post=last_post,
                           last_alert=last_alert, weekDays=rusWeekDays, months=rusMonths)


@app.route('/about_us')
def about():
    last_post = Post.query.order_by(Post.id.desc()).first()
    last_alert = Alert.query.order_by(Alert.id.desc()).first()
    return render_template('about_us.html', last_post=last_post,
                           last_alert=last_alert, weekDays=rusWeekDays, months=rusMonths)



