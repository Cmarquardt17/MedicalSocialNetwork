from flask import render_template, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from project.models import Post, User

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    friends = User.query.filter_by(username=current_user.username).first_or_404()
    #posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    posts = friends.followed_posts()
    return render_template('home.html', posts=posts, friends=friends)
