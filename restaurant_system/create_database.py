#!/usr/bin/env python3
"""
Database initialization script for Restaurant Management System
Run this script to create and populate the database with sample data
"""

import os
import sys
from datetime import datetime

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User, Dish, RestaurantInfo

def init_db():
    """Initialize the database with sample data"""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Created database tables.")
        
        # Check if we already have data
        if User.query.first() is not None:
            print("Database already contains data. Skipping sample data insertion.")
            return
        
        # Create sample users
        users = [
            User(
                username='manager',
                email='manager@restaurant.com',
                role='manager',
                table_number=None
            ),
            User(
                username='staff1',
                email='staff1@restaurant.com',
                role='staff',
                table_number=None
            ),
            User(
                username='staff2',
                email='staff2@restaurant.com',
                role='staff',
                table_number=None
            ),
            User(
                username='customer1',
                email='customer1@example.com',
                role='customer',
                table_number=5
            ),
            User(
                username='customer2',
                email='customer2@example.com',
                role='customer',
                table_number=3
            )
        ]
        
        # Set passwords
        for user in users:
            user.set_password('password123')
        
        db.session.add_all(users)
        print("Created sample users.")
        
        # Create sample dishes
        dishes = [
            Dish(
                name="Classic Burger",
                price=12.99,
                description="Juicy beef patty with lettuce, tomato, onion, and our special sauce",
                category="lunch",
                image_url="/static/images/dishes/burger.jpg",
                ar_model_url="/static/images/ar-models/burger.glb",
                is_available=True,
                suggested_dishes="2,3,7"
            ),
            Dish(
                name="Caesar Salad",
                price=9.99,
                description="Fresh romaine lettuce with Caesar dressing, croutons, and parmesan cheese",
                category="lunch",
                image_url="/static/images/dishes/caesar_salad.jpg",
                ar_model_url="",
                is_available=True,
                suggested_dishes="1,7"
            ),
            Dish(
                name="French Fries",
                price=4.99,
                description="Crispy golden fries served with ketchup",
                category="sides",
                image_url="/static/images/dishes/fries.jpg",
                ar_model_url="",
                is_available=True,
                suggested_dishes="1,4"
            ),
            Dish(
                name="Chocolate Milkshake",
                price=6.99,
                description="Creamy chocolate milkshake topped with whipped cream",
                category="drinks",
                image_url="/static/images/dishes/milkshake.jpg",
                ar_model_url="",
                is_available=True,
                suggested_dishes="1,3"
            ),
            Dish(
                name="Pancake Breakfast",
                price=8.99,
                description="Fluffy pancakes served with maple syrup and butter",
                category="breakfast",
                image_url="/static/images/dishes/pancakes.jpg",
                ar_model_url="",
                is_available=True,
                suggested_dishes="6,7"
            ),
            Dish(
                name="Fresh Orange Juice",
                price=3.99,
                description="Freshly squeezed orange juice",
                category="breakfast",
                image_url="/static/images/dishes/orange_juice.jpg",
                ar_model_url="",
                is_available=True,
                suggested_dishes="5,8"
            ),
            Dish(
                name="Bacon and Eggs",
                price=10.99,
                description="Crispy bacon with two eggs any style and toast",
                category="breakfast",
                image_url="/static/images/dishes/bacon_eggs.jpg",
                ar_model_url="",
                is_available=True,
                suggested_dishes="5,6"
            ),
            Dish(
                name="Coffee",
                price=2.99,
                description="Freshly brewed coffee",
                category="drinks",
                image_url="/static/images/dishes/coffee.jpg",
                ar_model_url="",
                is_available=True,
                suggested_dishes="5,7"
            ),
            Dish(
                name="Steak Dinner",
                price=24.99,
                description="Grilled steak with roasted vegetables and mashed potatoes",
                category="dinner",
                image_url="/static/images/dishes/steak.jpg",
                ar_model_url="/static/images/ar-models/steak.glb",
                is_available=True,
                suggested_dishes="10,11"
            ),
            Dish(
                name="Red Wine",
                price=8.99,
                description="Glass of house red wine",
                category="drinks",
                image_url="/static/images/dishes/red_wine.jpg",
                ar_model_url="",
                is_available=True,
                suggested_dishes="9,12"
            ),
            Dish(
                name="Garlic Bread",
                price=5.99,
                description="Toasted bread with garlic butter",
                category="sides",
                image_url="/static/images/dishes/garlic_bread.jpg",
                ar_model_url="",
                is_available=True,
                suggested_dishes="9,13"
            ),
            Dish(
                name="Chocolate Cake",
                price=7.99,
                description="Rich chocolate cake with chocolate frosting",
                category="dessert",
                image_url="/static/images/dishes/chocolate_cake.jpg",
                ar_model_url="",
                is_available=True,
                suggested_dishes="9,10"
            ),
            Dish(
                name="Ice Cream",
                price=5.99,
                description="Vanilla ice cream with chocolate sauce",
                category="dessert",
                image_url="/static/images/dishes/ice_cream.jpg",
                ar_model_url="",
                is_available=True,
                suggested_dishes="9,12"
            )
        ]
        
        db.session.add_all(dishes)
        print("Created sample dishes.")
        
        # Create restaurant info
        restaurant_info = RestaurantInfo(
            name="Gourmet Restaurant",
            address="123 Main Street, City, Country",
            phone="+1 234 567 8900",
            email="info@gourmetrestaurant.com",
            opening_hours="Monday to Sunday: 8:00 AM - 11:00 PM",
            description="Welcome to Gourmet Restaurant, where we serve the finest dishes prepared by our expert chefs using fresh, locally sourced ingredients.",
            quote="Exquisite dining experience"
        )
        
        db.session.add(restaurant_info)
        print("Created restaurant information.")
        
        # Commit all changes
        db.session.commit()
        print("Database initialization complete!")
        
        # Print login information
        print("\nLogin credentials:")
        print("Manager - Username: manager, Password: password123")
        print("Staff - Username: staff1, Password: password123")
        print("Customer - Username: customer1, Password: password123")

if __name__ == '__main__':
    init_db()