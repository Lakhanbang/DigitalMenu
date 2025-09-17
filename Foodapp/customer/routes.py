# customer/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, session
from data import restaurants

customer_bp = Blueprint('customer', __name__,
                        template_folder='../templates',
                        static_folder='../static/customer')

# --- Helper function to find a dish by its ID ---
def find_dish(dish_id):
    for r in restaurants:
        for dish in r['menu']:
            if dish['id'] == dish_id:
                return dish
    return None

# --- NEW: AR View Route ---
@customer_bp.route('/ar_view/<int:dish_id>')
def ar_view(dish_id):
    dish = find_dish(dish_id)
    if not dish or not dish.get('ar_target') or not dish.get('ar_model'):
        return "AR content not found for this item.", 404
    return render_template('customer/ar_view.html', dish=dish)


# --- Existing routes ---
@customer_bp.route('/')
def index():
    query = request.args.get('q','').lower()
    results = [r for r in restaurants if query in r['name'].lower()] if query else restaurants
    return render_template('customer/index.html', restaurants=results, query=query)

@customer_bp.route('/restaurant/<int:rest_id>')
def restaurant(rest_id):
    rest = next((r for r in restaurants if r['id']==rest_id),None)
    if not rest: return redirect(url_for('customer.index'))
    menu_query = request.args.get('mq','').lower()
    menu = [m for m in rest['menu'] if menu_query in m['name'].lower()] if menu_query else rest['menu']
    cart = session.get('cart',{})
    return render_template('customer/restaurant.html', restaurant=rest, menu=menu, cart=cart, menu_query=menu_query)

# ... (rest of the customer routes are unchanged) ...
@customer_bp.route('/add/<int:item_id>')
def add(item_id):
    cart = session.get('cart',{})
    cart[str(item_id)] = cart.get(str(item_id), {'quantity':0})
    cart[str(item_id)]['quantity'] += 1
    session['cart'] = cart
    return redirect(request.referrer)

@customer_bp.route('/remove/<int:item_id>')
def remove(item_id):
    cart = session.get('cart',{})
    if str(item_id) in cart:
        cart[str(item_id)]['quantity'] -= 1
        if cart[str(item_id)]['quantity']<=0: cart.pop(str(item_id))
    session['cart'] = cart
    return redirect(request.referrer)

@customer_bp.route('/cart')
def show_cart():
    cart = session.get('cart',{})
    items=[]
    for r in restaurants:
        for m in r['menu']:
            if str(m['id']) in cart:
                items.append({'menu':m,'quantity':cart[str(m['id'])]['quantity']})
    return render_template('customer/cart.html', items=items)

@customer_bp.route('/order')
def order():
    session.pop('cart',None)
    return "<h1>Order placed successfully!</h1><a href='/'>Back to home</a>"