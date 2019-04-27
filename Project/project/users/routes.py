from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from project import db, bcrypt
from project.models import User, Post
from project.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from project.users.utils import (save_picture, send_reset_email,
                                generate_confirmation_token, confirm_token,
                                send_email, check_confirmed)

#Blueprint for the registration page 
users = Blueprint('users', __name__)


#A register method that entials all the information that needs to filled out
#That comes with a confirmation token and if sent to be verified by administration
@users.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password,
                    firstName=form.firstName.data,
                    middleName=form.middleName.data,
                    lastName=form.lastName.data,
                    address=form.address.data,
                    phone=form.phone.data,
                    doctor=form.doctor.data,
                    drLicenseNum=form.drLicenseNum.data,
                    dateOfBirth=form.dateOfBirth.data,
                    gender=form.gender.data,
                    ssn=form.ssn.data,
                    race=form.race.data,
                    emergencyName=form.emergencyName.data,
                    emergencyRelation=form.emergencyRelation.data,
                    emergencyAddress=form.emergencyAddress.data,
                    emergencyPhone=form.emergencyPhone.data,
                    majorSurgery=form.majorSurgery.data,
                    smoking=form.smoking.data,
                    confirmed=False)
        db.session.add(user)
        db.session.commit()
        token = generate_confirmation_token(user.email)
        confirm_url = url_for('users.confirm_email', token=token, _external=True)
        html = render_template('user/activate.html', confirm_url=confirm_url, user=user)
        subject = "Confirm Email"
        send_email('noreply.mednet@gmail.com', subject, html)
        flash('Your account has been created! Please wait till we verify your account', 'success')
        return redirect(url_for('users.unconfirmed'))
    return render_template('register.html', title='Register', form=form)

#A reroute for the user if they arent confirmed and if they are they will be returned to the main page
@users.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect('main.home')
    return render_template('unconfirmed.html')

#Login form that the user can use and log in correctly if they are authenticated
#If authenticated they will redirected to their main page that is unique to them
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

@users.route('/confirm/<token>')
@login_required

#Just a confirmation for the user that the email is confirmed and if they do not do it in time
#The confirmation link will be expired 
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('users.login'))

#A friends page that can be clicked on the main page with a 404 error if it does not load correctly
@users.route("/friends")
@login_required
def friends():
    users = User.query.all()
    user = User.query.filter_by(username=current_user.username).first_or_404()
    friends = user.friended.all()
    return render_template('friends.html', title='Friends', friends=friends, user=user, users=users)

#Friending method if you click on the add friend button and they will be added tot he db
@users.route('/friend/<nickname>')
@login_required
def friend(nickname):
    user = User.query.filter_by(username=nickname).first()
    u = current_user.friend(user)
    db.session.add(u)
    db.session.commit()
    flash('You are now friends with ' + nickname + '!', 'success')
    return redirect(url_for('users.friends', title='Friends', users=users))

#Unfriending method if you click on the remove friend button after they have been friended
# and they will be added to the db as not a friend
@users.route('/unfriend/<nickname>')
@login_required
def unfriend(nickname):
    user = User.query.filter_by(username=nickname).first()
    u = current_user.unfriend(user)
    db.session.add(u)
    db.session.commit()
    flash('You have unfriended ' + nickname + '!','success')
    return redirect(url_for('users.friends', title='Friends', users=users))

#A logout button for the user if they are logged in
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

#A method to check out all of the account information taht is specialized to them in particular
#This method also is used to update their information
@users.route("/account", methods=['GET','POST'])
@login_required
@check_confirmed
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
        current_user.drLicenseNum = form.drLicenseNum.data
        current_user.dateOfBirth = form.dateOfBirth.data
        current_user.gender = form.gender.data
        current_user.ssn = form.ssn.data
        current_user.race = form.race.data
        current_user.emergencyName = form.emergencyName.data
        current_user.emergencyRelation = form.emergencyRelation.data
        current_user.emergencyAddress = form.emergencyAddress.data
        current_user.emergencyPhone = form.emergencyPhone.data
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
        form.drLicenseNum.data = current_user.drLicenseNum
        form.dateOfBirth.data = current_user.dateOfBirth
        form.gender.data = current_user.gender
        form.ssn.data = current_user.ssn
        form.race.data = current_user.race
        form.emergencyName.data = current_user.emergencyName
        form.emergencyRelation.data = current_user.emergencyRelation
        form.emergencyAddress.data = current_user.emergencyAddress
        form.emergencyPhone.data = current_user.emergencyPhone
        form.majorSurgery.data = current_user.majorSurgery
        form.smoking.data = current_user.smoking

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form, legend='New Post')

#You can check out a users posts with this method
@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)

#A reset password function for a user 
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

#A token that is used to confirm and ensure that the password resetting is valid and is changed in time
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
