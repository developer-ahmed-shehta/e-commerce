from flask import Blueprint, render_template, redirect, flash, request, jsonify
from .models import Product, Cart, Order
from flask_login import current_user, login_required
from . import db
import random

views = Blueprint('views', __name__)


@views.route('/')
def home():
    items = Product.query.filter_by(flash_sale=True)
    return render_template('home.html', items=items, cart=Cart.query.filter_by(
        customer_link=current_user.id).all() if current_user.is_authenticated else [])


@views.route('/add-to-cart/<int:item_id>')
@login_required
def add_to_cart(item_id):
    item = Product.query.filter_by(id=item_id).first()
    item_exist = Cart.query.filter_by(product_link=item_id, customer_link=current_user.id).first()
    if item_exist:
        try:
            item_exist.quantity += 1
            db.session.commit()
            flash(f'Quantity of {item_exist.product.name} has been updated')
            return redirect(request.referrer)
        except Exception as e:
            print('Quantity not updated', e)
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
        print('Item not added to cart', e)
        flash(f'{new_cart_item.product.name} has not been added to cart')
    return redirect(request.referrer)


@views.route('/cart')
@login_required
def show_cart():
    cart = Cart.query.filter_by(customer_link=current_user.id).all()
    amount = 0
    for item in cart:
        amount += item.product.current_price * item.quantity

    return render_template('cart.html', cart=cart, amount=amount, total=amount + 200)


@views.route('/pluscart')
@login_required
def pluscart():
    if request.method == "GET":
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        cart_item.quantity += 1
        db.session.commit()
        amount = 0
        for item in Cart.query.filter_by(customer_link=current_user.id).all():
            amount += item.product.current_price * item.quantity

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount + 200
        }
        return jsonify(data)


@views.route('/minuscart')
@login_required
def minuscart():
    if request.method == "GET":
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        if cart_item.quantity != 1:
            cart_item.quantity -= 1
        db.session.commit()

        amount = 0
        for item in Cart.query.filter_by(customer_link=current_user.id):
            amount += item.product.current_price * item.quantity

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount + 200
        }
        print(data)
        return jsonify(data)


@views.route('/removecart')
@login_required
def remove():
    if request.method == "GET":
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)

        db.session.delete(cart_item)
        db.session.commit()

        amount = 0
        for item in Cart.query.filter_by(customer_link=current_user.id).all():
            amount += item.product.current_price * item.quantity

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount + 200
        }
        print(data)
        return jsonify(data)


@views.route('/place-order')
@login_required
def place_order():
    customer_cart = Cart.query.filter_by(customer_link=current_user.id).all()

    if customer_cart:
        try:
            total = 0  # will use in bill extraction
            for cart in customer_cart:
                total += cart.product.current_price * cart.quantity

            # implement payment method

            for cart in customer_cart:
                new_order = Order()
                new_order.quantity = cart.quantity
                new_order.price = cart.product.current_price
                new_order.status = "Pending"  # change later
                new_order.payment_id = random.randint(1, 1000)  # change later

                new_order.customer_link = cart.customer_link
                new_order.product_link = cart.product_link

                db.session.add(new_order)
                db.session.commit()
            flash('Order has been placed')
            return redirect('/order')
        except Exception as e:
            print('Order not placed', e)
            flash('Order not placed')
            return redirect('/')
    else:
        flash('Your Cart is Empty')
        return redirect('/')

@views.route('/orders')
@login_required
def order():
    orders = Order.query.filter_by(customer_link=current_user.id).all()
    return render_template('orders.html', orders=orders)