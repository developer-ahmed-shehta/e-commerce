from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, length, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired()])
    password1 = PasswordField('Enter Your Password', validators=[DataRequired(), length(min=8, max=50)])
    password2 = PasswordField('Confirm Your Password', validators=[DataRequired(), length(min=8, max=50)])
    submit = SubmitField('Sign Up')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired(), length(min=8, max=50)])
    new_password = PasswordField('New Password', validators=[DataRequired(), length(min=8, max=50)])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), length(min=8, max=50)])

    change_password = SubmitField('Change Password')


class ShopItemForm(FlaskForm):
    product_name = StringField('Name Of Product', validators=[DataRequired()])
    current_price = IntegerField('Current Price', validators=[DataRequired()])
    previous_price = IntegerField('Previous Price', validators=[DataRequired()])
    in_stock = IntegerField('In Stock', validators=[DataRequired()])
    product_picture = FileField('Product Picture', validators=[FileAllowed(['jpg', 'png']), FileRequired()])

    flash_sale = BooleanField('Flash Sale')

    add_product = SubmitField('Add Product')
    update_product = SubmitField('Update')

class OrderForm(FlaskForm):
    order_status = SelectField('Order Status', choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'),
                                                        ('Out for delivery', 'Out for delivery'),
                                                        ('Delivered', 'Delivered'), ('Canceled', 'Canceled')])
    update= SubmitField('Update Status')

