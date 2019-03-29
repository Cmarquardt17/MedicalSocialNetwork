from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from project import db, bcrypt
from project.models import User, Post
from project.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from project.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password,
                    firstName=form.firstName.data, middleName=form.middleName.data,
                    lastName=form.lastName.data, address=form.address.data,
                    phone=form.phone.data, doctor=form.doctor.data, dateOfBirth=form.dateOfBirth.data,
                    gender=form.gender.data, ssn=form.ssn.data, race=form.race.data,
                    emergency=form.emergency.data, majorSurgery=form.majorSurgery.data,
                    smoking=form.emergency.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/friends")
@login_required
def friends():
    users = User.query.all()
    friends = User.query.filter_by(username=current_user.username).first_or_404()
    return render_template('friends.html', title='Friends', friends=friends, users=users)

@users.route('/friend/<nickname>')
@login_required
def friend(nickname):
    user = User.query.filter_by(username=nickname).first()
    u = current_user.friend(user)
    db.session.add(u)
    db.session.commit()
    flash('You are now friends with ' + nickname + '!', 'success')
    return redirect(url_for('users.friends', title='Friends', users=users))

@users.route('/unfriend/<nickname>')
@login_required
def unfriend(nickname):
    user = User.query.filter_by(username=nickname).first()
    u = current_user.unfriend(user)
    db.session.add(u)
    db.session.commit()
    flash('You have are not friends with ' + nickname + '.','success')
    return redirect(url_for('users.friends', title='Friends', users=users))

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.firstName = form.firstName.data
        current_user.middleName = form.middleName.data
        current_user.lastName = form.lastName.data
        current_user.address = form.address.data
        current_user.phone = form.phone.data
        current_user.doctor = form.doctor.data
        current_user.dateOfBirth = form.dateOfBirth.data
        current_user.gender = form.gender.data
        current_user.ssn = form.ssn.data
        current_user.race = form.race.data
        current_user.emergency = form.emergency.data
        current_user.majorSurgery = form.majorSurgery.data
        current_user.smoking = form.smoking.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.firstName.data = current_user.firstName
        form.middleName.data = current_user.middleName
        form.lastName.data = current_user.lastName
        form.address.data = current_user.address
        form.phone.data = current_user.phone
        form.doctor.data = current_user.doctor
        form.dateOfBirth.data = current_user.dateOfBirth
        form.gender.data = current_user.gender
        form.ssn.data = current_user.ssn
        form.race.data = current_user.race
        form.emergency.data = current_user.emergency
        form.majorSurgery.data = current_user.majorSurgery
        form.smoking.data = current_user.smoking

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form, legend='New Post')


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)

@users.route("/reset_password", methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid or Expired Token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in.', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
