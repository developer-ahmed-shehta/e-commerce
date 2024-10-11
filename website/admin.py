from flask import Blueprint, render_template, flash, redirect, send_from_directory, request, jsonify
from flask_login import login_required, current_user
from .forms import ShopItemForm, FileRequired, FileField, FileAllowed, OrderForm
from werkzeug.utils import secure_filename
from .models import Product, Order, Customer
from . import db
admin = Blueprint('admin', __name__)


@admin.route('/media/<path:filename>')
def get_image(filename):
    return send_from_directory('../media', filename)


@admin.route('/admin')
def create():
    return 'this is the admin page'


@admin.route('/add-shop-items', methods=['GET', 'POST'])
@login_required
def add_shop():
    if current_user.id == 1:

        form = ShopItemForm()
        if form.validate_on_submit():
            product_name = form.product_name.data
            current_price = form.current_price.data
            previous_price = form.previous_price.data

            in_stock = form.in_stock.data
            flash_sale = form.flash_sale.data

            product_picture_file = form.product_picture.data

            product_picture_name = secure_filename(product_picture_file.filename)  # if we hava special character it replaced by _

            file_path = f'./media/{product_picture_name}'
            product_picture_file.save(file_path)

            new_product = Product()
            new_product.name = product_name
            new_product.current_price = current_price
            new_product.previous_price = previous_price
            new_product.stock = in_stock
            new_product.flash_sale = flash_sale
            new_product.picture = file_path
            try :
                db.session.add(new_product)
                db.session.commit()
                flash(f'{product_name} Added Successfully!')
                return render_template('add_shop_item.html', form=form)
            except Exception as e:
                print(e)
                flash(f'Item Not Added!')

        return render_template('add_shop_item.html', form=form)


    return render_template('404.html')


@admin.route('/shop-items', methods=['GET', 'POST'])
@login_required
def shop_items():
    if current_user.id == 1:
        items = Product.query.order_by(Product.date_added).all()
        return render_template('shop_items.html', items=items)

    return render_template('404.html')


@admin.route('/update-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def update_item(item_id):
    if current_user.id == 1:
        form = ShopItemForm()
        item = Product.query.get(item_id)
        form.product_name.render_kw={'placeholder':item.name}
        form.current_price.render_kw={'placeholder':item.current_price}
        form.previous_price.render_kw={'placeholder':item.previous_price}
        form.in_stock.render_kw={'placeholder':item.stock}
        form.flash_sale.render_kw={'placeholder':item.flash_sale}

        # form.product_name.data=item.name
        # form.current_price.data=item.current_price
        # form.previous_price.data=item.previous_price
        # form.in_stock.data=item.stock
        # form.flash_sale.data=item.flash_sale
        # form.product_picture.data=

        if form.validate_on_submit():
            item_name = form.product_name.data
            current_price = form.current_price.data
            previous_price = form.previous_price.data
            in_stock = form.in_stock.data
            flash_sale = form.flash_sale.data

            file = form.product_picture.data
            file_name=secure_filename(file.filename)
            file_path = f'./media/{file_name}'
            file.save(file_path)
            try:
                Product.query.filter_by(id=item_id).update(dict(name=item_name,
                                                                current_price=current_price,
                                                                previous_price=previous_price,
                                                                stock=in_stock,
                                                                flash_sale=flash_sale,picture=file_path))
                db.session.commit()
                flash(f'{item_name} Updated Successfully!')
                return redirect('/shop-item')
            except Exception as e:
                print(e)
                flash(f'Item Not Updated!')

        return render_template('update_item.html', form=form)


    return render_template('404.html')


@admin.route('/delete-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def delete_item(item_id):
    if current_user.id == 1:
        try:
            item = Product.query.get(item_id)
            db.session.delete(item)
            db.session.commit()
            flash(f'{item.name} Deleted Successfully!')
            return redirect('/shop-item')
        except Exception as e:
            print(e)
            flash(f'Item Not Deleted!')
    return render_template('404.html')


@admin.route('/view-orders')
@login_required
def view_order():
    if current_user.id == 1:
        orders = Order.query.all()
        return render_template('view_orders.html', orders=orders)

    return render_template('404.html')


@admin.route('/update-order/<int:order_id>', methods=["GET", "POST"])
@login_required
def update_order(order_id):
    if current_user.id == 1:
        form = OrderForm()
        order = Order.query.get(order_id)

        if form.validate_on_submit():
            status = form.order_status.data
            order.status = status
            try:
                db.session.commit()
                flash(f'Order {order_id} Updated Successfully!')
                return redirect('/view-orders')
            except Exception as e:
                print(e)
                flash(f'Order {order_id} Not Updated!')
                return redirect('/view-orders')

        return render_template('order_update.html',form=form)

    return render_template('404.html')


@admin.route('/customers')
@login_required
def customers():
    if current_user.id == 1:
        customers = Customer.query.all()
        return render_template('customers.html',customers=customers)

    return render_template('404.html')


@admin.route('/admin-page')
@login_required
def admin_page():
    if current_user.id == 1:
        return render_template('admin.html')

    return render_template('404.html')
