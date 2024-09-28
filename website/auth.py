from flask import Blueprint, render_template, flash, redirect
from sqlalchemy.testing.pickleable import User
from .models import Customer
from .forms import SignupForm, LoginForm, ChangePasswordForm
from . import db
from flask_login import login_user, logout_user, login_required
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        customer = Customer.query.filter_by(email=email).first()

        if customer:
            if customer.verify_password(password):
                login_user(customer)
                return redirect('/')
            else:
                flash('Invalid email or password')
        else:
            flash('Invalid email or password')

    return render_template('login.html', form=form)


@auth.route('/sign-up',methods=['GET','POST'])
def sign_up():
    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password1 = form.password1.data
        password2 = form.password2.data
        if password1 == password2:
            newCustomer = Customer()

            if Customer.query.filter_by(email=email).first() != email:  # check if email already exist

                newCustomer.email = email
                newCustomer.username = username
                newCustomer.password = password1
                try:
                    db.session.add(newCustomer)
                    db.session.commit()
                    flash('Account created successfully! ')
                    return redirect('/login')
                except Exception as e:
                    print(e)
                    flash('Something went wrong. Please try again.')
            else:
                flash('Account already exists. Please try again.')
        else:
            flash('Your password and confirmation password do not match.')

        form.email.data = ''
        form.username.data = ''
        form.password1.data = ''
        form.password2.data = ''

    return render_template('signup.html', form=form)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect('/')


@auth.route('/profile/<int:customer_id>')
@login_required
def profile(customer_id):
    customer = Customer.query.filter_by(id=customer_id).first()
    return render_template('profile.html',customer=customer)


@auth.route('/change-password/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def change_password(customer_id):
    customer = Customer.query.filter_by(id=customer_id).first()
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_password = form.current_password.data
        new_password = form.new_password.data
        confirm_password = form.confirm_password.data
        if customer.verify_password(current_password):  # check is correct password
            if current_password != new_password:  # check it is not same password
                if new_password == confirm_password:  # check confirm is a same the new
                    customer.password = confirm_password
                    db.session.commit()
                    flash('Your password has been updated.')
                    return redirect('/profile/{}'.format(customer_id))
                else:
                    flash('Your new password and confirmation password do not match.')
            else:
                flash('Use Different Password')
        else:
            flash('Current password does not match. Please try again.')

    return render_template('change_password.html',form=form)