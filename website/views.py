from flask import Blueprint, render_template, redirect, flash,request
from .models import Product, Cart
from flask_login import current_user, login_required
from . import db
views = Blueprint('views', __name__)


@views.route('/')
def home():
    items = Product.query.filter_by(flash_sale=True)

    return render_template('home.html', items=items,cart=Cart.query.filter_by(customer_link=current_user.id).all()
                                                                                                if current_user.is_authenticated else None)

@views.route('/add-to-cart/<int:item_id>')
@login_required
def add_to_cart(item_id):
    item = Product.query.filter_by(id=item_id).first()
    item_exist = Cart.query.filter_by(product_link=item_id,customer_link=current_user.id).first()
    if item_exist:
        try:
            item_exist.quantity += 1
            db.session.commit()
            flash(f'Quantity of {item_exist.product.name} has been updated')
            return redirect(request.referrer)
        except Exception as e:
            print('Quantity not updated',e)
            flash(f'Quantity of {item_exist.product.name} has been updated')
            return redirect(request.referrer)

    new_cart_item = Cart()
    new_cart_item.quantity = 1
    new_cart_item.product_link = item.id
    new_cart_item.customer_link = current_user.id

    try:
        db.session.add(new_cart_item)
        db.session.commit()
        flash(f'{new_cart_item.product.name} added successfully to cart')

    except Exception as e:
        print('Item not added to cart',e)
        flash(f'{new_cart_item.product.name} has not been added to cart')
    return redirect(request.referrer)

@views.route('/cart')
@login_required
def show_cart():
    cart = Cart.query.filter_by(customer_link=current_user.id).all()
    amount=0
    for item in cart:
        amount += item.product.current_price * item.quantity

    return render_template('cart.html', cart=cart,amount=amount,total=amount+200)


@views.route('/pluscart')
@login_required
def pluscart():
    pass

@views.route('/minuscart')
@login_required
def minuscart():
    pass
