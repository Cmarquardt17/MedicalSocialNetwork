from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from project import db
from project.models import Post
from project.posts.forms import PostForm

#Blueprint/layout for the post layout
posts = Blueprint('posts', __name__)


#This method requires a login and you can create a post and it will redirect the user to their home page
@posts.route("/post/new", methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(patient=form.patient.data, condition=form.condition.data, medication=form.medication.data,
                    description=form.description.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form)

#This is the template for the posts and they are in order based on id and post date
@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', condition=post.condition, post=post)


#Must be logged in, this method can update and replace a current condition
@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.patient = form.patient.data
        post.condition = form.condition.data
        post.medication = form.medication.data
        post.description = form.description.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.patient.data = post.patient
        form.condition.data = post.condition
        form.medication.data = post.medication
        form.description.data = post.description
    return render_template('create_post.html', title='Update Post', form=form,
                           legend='Update Post')

#If a user no longer has that condition or it is faulty they can delete the post if they choose
@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
