# owner/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from data import restaurants
import os
from werkzeug.utils import secure_filename

# --- Blueprint Setup ---
owner_bp = Blueprint('owner', __name__,
                    url_prefix='/owner',
                    template_folder='../templates/owner',
                    static_folder='../static/owner')

# --- Helper function to find a dish by its ID ---
def find_dish(dish_id):
    for r in restaurants:
        for dish in r['menu']:
            if dish['id'] == dish_id:
                return r, dish
    return None, None

# --- Existing Routes (Unchanged) ---
@owner_bp.route('/')
def dashboard():
    return render_template('dashboard.html', restaurants=restaurants)

@owner_bp.route('/add_restaurant', methods=['GET','POST'])
def add_restaurant():
    if request.method=='POST':
        new = {
            "id": len(restaurants)+1,
            "name": request.form['name'],
            "address": request.form['location'],
            "description": request.form['description'],
            "menu":[]
        }
        restaurants.append(new)
        return redirect(url_for('owner.dashboard'))
    return render_template('add_restaurant.html')

@owner_bp.route('/<int:rest_id>/add_dish', methods=['GET','POST'])
def add_dish(rest_id):
    rest = next((r for r in restaurants if r['id']==rest_id),None)
    if not rest: return redirect(url_for('owner.dashboard'))
    if request.method=='POST':
        # Safely find the next available ID
        all_ids = [m['id'] for r in restaurants for m in r['menu']]
        new_id = max(all_ids, default=100) + 1

        new_dish = {
            "id": new_id,
            "name": request.form['name'],
            "price": float(request.form['price']),
            "description": request.form['description'],
            "image": request.form['image'],
            "ar_target": None, # Initialize AR fields
            "ar_model": None,
            "common_with": request.form.getlist('common_with')
        }
        rest['menu'].append(new_dish)
        return redirect(url_for('owner.manage_dishes', rest_id=rest_id))
    return render_template('add_dish.html', restaurant=rest)


# --- NEW: Route to Edit a Dish ---
@owner_bp.route('/<int:rest_id>/edit_dish/<int:dish_id>', methods=['GET', 'POST'])
def edit_dish(rest_id, dish_id):
    rest, dish = find_dish(dish_id)
    if not dish:
        return redirect(url_for('owner.dashboard'))

    if request.method == 'POST':
        # Update dish details from the form
        dish['name'] = request.form['name']
        dish['price'] = float(request.form['price'])
        dish['description'] = request.form['description']
        dish['image'] = request.form['image']
        dish['common_with'] = request.form.getlist('common_with')
        flash(f"{dish['name']} updated successfully!", "success")
        return redirect(url_for('owner.manage_dishes', rest_id=rest_id))

    return render_template('edit_dish.html', restaurant=rest, dish=dish)


# --- NEW: Route to Manage AR files for a Dish ---
@owner_bp.route('/<int:rest_id>/manage_ar/<int:dish_id>', methods=['GET', 'POST'])
def manage_ar(rest_id, dish_id):
    rest, dish = find_dish(dish_id)
    if not dish:
        return redirect(url_for('owner.dashboard'))

    if request.method == 'POST':
        # Check if the post request has the file part
        if 'ar_target_file' in request.files:
            target_file = request.files['ar_target_file']
            if target_file.filename != '' and target_file.filename.endswith('.mind'):
                filename = f"target_{dish_id}.mind"
                filepath = os.path.join('uploads/targets', filename)
                target_file.save(filepath)
                dish['ar_target'] = f'/{filepath}' # Save URL path

        if 'ar_model_file' in request.files:
            model_file = request.files['ar_model_file']
            if model_file.filename != '' and (model_file.filename.endswith('.glb') or model_file.filename.endswith('.gltf')):
                filename = f"model_{dish_id}{os.path.splitext(model_file.filename)[1]}"
                filepath = os.path.join('uploads/models', filename)
                model_file.save(filepath)
                dish['ar_model'] = f'/{filepath}' # Save URL path

        flash(f"AR files for {dish['name']} updated.", "success")
        return redirect(url_for('owner.manage_dishes', rest_id=rest_id))

    return render_template('manage_ar.html', restaurant=rest, dish=dish)

# --- Updated Route with search functionality ---
@owner_bp.route('/<int:rest_id>/manage_dishes')
def manage_dishes(rest_id):
    rest = next((r for r in restaurants if r['id']==rest_id),None)
    if not rest: return redirect(url_for('owner.dashboard'))
    return render_template('manage_dishes.html', restaurant=rest)