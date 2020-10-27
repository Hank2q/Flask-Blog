from flaskblog import POSTS_PER_PAGE
from flaskblog.model import Post
from flask import Blueprint, render_template, request, jsonify
main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    # ! no need to specify parent dir if its named templates, else have to mention i.e. pages/home.html
    posts = Post.query.order_by(
        Post.post_date.desc()).paginate(per_page=POSTS_PER_PAGE, page=1)
    return render_template('home.html', posts=posts)


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/contact')
def contact():
    return render_template('contact.html')


@main.route('/data')
def data():
    posts = Post.query.all()
    json = [{'id': p.id, 'title': p.title,
             'authour': p.author.username, 'date': p.post_date} for p in posts]
    return jsonify(json)


@main.route('/more')
def more():
    page = request.args.get('page', 2, type=int)
    posts = Post.query.order_by(
        Post.post_date.desc()).paginate(per_page=POSTS_PER_PAGE)
    if 1 < page <= posts.pages:
        next_posts = posts.query.paginate(per_page=POSTS_PER_PAGE, page=page)
        return render_template('more.html', posts=next_posts)
