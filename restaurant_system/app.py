# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Dish, Order, OrderItem, RestaurantInfo
from functools import wraps
import json

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            
            if user.role == 'customer':
                return redirect(next_page or url_for('customer_dashboard'))
            elif user.role == 'staff':
                return redirect(next_page or url_for('staff_dashboard'))
            elif user.role == 'manager':
                return redirect(next_page or url_for('manager_dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'customer')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'danger')
            return redirect(url_for('register'))
        
        user = User(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('auth/register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Customer routes
@app.route('/customer/dashboard')
@login_required
@role_required('customer')
def customer_dashboard():
    return render_template('customer/dashboard.html')

@app.route('/customer/menu')
@login_required
@role_required('customer')
def customer_menu():
    category = request.args.get('category', 'all')
    search = request.args.get('search', '')
    
    query = Dish.query.filter_by(is_available=True)
    
    if category != 'all':
        query = query.filter_by(category=category)
    
    if search:
        query = query.filter(Dish.name.ilike(f'%{search}%') | Dish.description.ilike(f'%{search}%'))
    
    dishes = query.all()
    return render_template('customer/menu.html', dishes=dishes, category=category, search=search)

@app.route('/customer/dish/<int:dish_id>')
@login_required
@role_required('customer')
def dish_detail(dish_id):
    dish = Dish.query.get_or_404(dish_id)
    suggestions = []
    
    if dish.suggested_dishes:
        suggestion_ids = [int(id) for id in dish.suggested_dishes.split(',')]
        suggestions = Dish.query.filter(Dish.id.in_(suggestion_ids), Dish.is_available == True).all()
    
    return render_template('customer/dish_detail.html', dish=dish, suggestions=suggestions)

@app.route('/customer/cart')
@login_required
@role_required('customer')
def customer_cart():
    return render_template('customer/cart.html')

# API routes for customer
@app.route('/api/cart/add', methods=['POST'])
@login_required
@role_required('customer')
def api_add_to_cart():
    data = request.get_json()
    dish_id = data.get('dish_id')
    quantity = data.get('quantity', 1)
    
    # In a real application, you would store cart in session or database
    # This is a simplified version
    return jsonify({'success': True})

@app.route('/api/cart/update', methods=['POST'])
@login_required
@role_required('customer')
def api_update_cart():
    data = request.get_json()
    # Update cart logic
    return jsonify({'success': True})

@app.route('/api/order/place', methods=['POST'])
@login_required
@role_required('customer')
def api_place_order():
    data = request.get_json()
    table_number = data.get('table_number')
    items = data.get('items', [])
    
    # Create order
    order = Order(
        table_number=table_number,
        customer_id=current_user.id,
        status='pending'
    )
    
    total_amount = 0
    for item in items:
        dish = Dish.query.get(item['dish_id'])
        order_item = OrderItem(
            dish_id=item['dish_id'],
            quantity=item['quantity'],
            price=dish.price
        )
        order.items.append(order_item)
        total_amount += dish.price * item['quantity']
    
    order.total_amount = total_amount
    db.session.add(order)
    db.session.commit()
    
    return jsonify({'success': True, 'order_id': order.id})

# Staff routes
@app.route('/staff/dashboard')
@login_required
@role_required('staff')
def staff_dashboard():
    orders = Order.query.filter(Order.status != 'paid').all()
    return render_template('staff/dashboard.html', orders=orders)

@app.route('/api/order/<int:order_id>/update', methods=['POST'])
@login_required
@role_required('staff')
def api_update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    status = request.json.get('status')
    
    if status in ['preparing', 'delivered']:
        order.status = status
        db.session.commit()
        return jsonify({'success': True})
    
    return jsonify({'success': False, 'error': 'Invalid status'})

# Manager routes
@app.route('/manager/dashboard')
@login_required
@role_required('manager')
def manager_dashboard():
    return render_template('manager/dashboard.html')

@app.route('/manager/dishes')
@login_required
@role_required('manager')
def manager_dishes():
    dishes = Dish.query.all()
    return render_template('manager/manage_dishes.html', dishes=dishes)

@app.route('/manager/dishes/add', methods=['GET', 'POST'])
@login_required
@role_required('manager')
def add_dish():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        description = request.form.get('description')
        category = request.form.get('category')
        image_url = request.form.get('image_url')
        ar_model_url = request.form.get('ar_model_url')
        suggested_dishes = request.form.get('suggested_dishes')
        
        dish = Dish(
            name=name,
            price=price,
            description=description,
            category=category,
            image_url=image_url,
            ar_model_url=ar_model_url,
            suggested_dishes=suggested_dishes
        )
        
        db.session.add(dish)
        db.session.commit()
        
        flash('Dish added successfully', 'success')
        return redirect(url_for('manager_dishes'))
    
    return render_template('manager/add_dish.html')

@app.route('/manager/dishes/<int:dish_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('manager')
def edit_dish(dish_id):
    dish = Dish.query.get_or_404(dish_id)
    
    if request.method == 'POST':
        dish.name = request.form.get('name')
        dish.price = request.form.get('price')
        dish.description = request.form.get('description')
        dish.category = request.form.get('category')
        dish.image_url = request.form.get('image_url')
        dish.ar_model_url = request.form.get('ar_model_url')
        dish.suggested_dishes = request.form.get('suggested_dishes')
        dish.is_available = request.form.get('is_available') == 'on'
        
        db.session.commit()
        
        flash('Dish updated successfully', 'success')
        return redirect(url_for('manager_dishes'))
    
    return render_template('manager/edit_dish.html', dish=dish)

@app.route('/manager/orders')
@login_required
@role_required('manager')
def manager_orders():
    orders = Order.query.all()
    return render_template('manager/orders.html', orders=orders)

@app.route('/manager/history')
@login_required
@role_required('manager')
def manager_history():
    orders = Order.query.filter(Order.status == 'paid').all()
    return render_template('manager/history.html', orders=orders)

@app.route('/manager/settings', methods=['GET', 'POST'])
@login_required
@role_required('manager')
def manager_settings():
    restaurant_info = RestaurantInfo.query.first()
    if not restaurant_info:
        restaurant_info = RestaurantInfo(
            name="Restaurant Name",
            address="Restaurant Address",
            phone="+1234567890",
            email="info@restaurant.com",
            opening_hours="9:00 AM - 10:00 PM",
            description="About our restaurant",
            quote="Our restaurant quote"
        )
        db.session.add(restaurant_info)
        db.session.commit()
    
    if request.method == 'POST':
        restaurant_info.name = request.form.get('name')
        restaurant_info.address = request.form.get('address')
        restaurant_info.phone = request.form.get('phone')
        restaurant_info.email = request.form.get('email')
        restaurant_info.opening_hours = request.form.get('opening_hours')
        restaurant_info.description = request.form.get('description')
        restaurant_info.quote = request.form.get('quote')
        
        db.session.commit()
        flash('Restaurant information updated successfully', 'success')
    
    return render_template('manager/settings.html', restaurant=restaurant_info)

@app.route('/api/order/<int:order_id>/bill')
@login_required
@role_required('manager')
def generate_bill(order_id):
    order = Order.query.get_or_404(order_id)
    restaurant = RestaurantInfo.query.first()
    
    return render_template('manager/bill.html', order=order, restaurant=restaurant)

if __name__ == '__main__':
    app.run(debug=True)