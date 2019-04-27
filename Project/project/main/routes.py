from flask import render_template, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from project.models import Post, User
from project.users.utils import check_confirmed

#This page is essentially the layout of our website and is used throughout 
main = Blueprint('main', __name__)

#This only becomes enabled if the user has logged in and has been authenticated
@main.route("/")
@main.route("/home")
@login_required
@check_confirmed
def home():
    page = request.args.get('page', 1, type=int)
    friends = User.query.filter_by(username=current_user.username).first_or_404()
    posts = friends.followed_posts()
    myPosts = Post.query.filter_by(author=current_user)\
        .order_by(Post.date_posted.desc())
    return render_template('home.html', title='Home', posts=posts, myPosts=myPosts, friends=friends)

#Takes you straight to the contact us page
@main.route("/contact")
def contact():
    return render_template('contact.html', title='Contact Us')
