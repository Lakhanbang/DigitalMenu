# database.py
from app import app, db
from models import User, Dish, RestaurantInfo

def init_db():
    with app.app_context():
        db.create_all()
        
        # Create default admin user if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@restaurant.com', role='manager')
            admin.set_password('admin123')
            db.session.add(admin)
        
        # Create default staff user if not exists
        if not User.query.filter_by(username='staff').first():
            staff = User(username='staff', email='staff@restaurant.com', role='staff')
            staff.set_password('staff123')
            db.session.add(staff)
        
        # Create default restaurant info if not exists
        if not RestaurantInfo.query.first():
            restaurant = RestaurantInfo(
                name="Gourmet Restaurant",
                address="123 Main Street, City, Country",
                phone="+1 234 567 8900",
                email="info@gourmetrestaurant.com",
                opening_hours="Monday to Sunday: 8:00 AM - 11:00 PM",
                description="Welcome to Gourmet Restaurant, where we serve the finest dishes prepared by our expert chefs using fresh, locally sourced ingredients.",
                quote="Exquisite dining experience"
            )
            db.session.add(restaurant)
        
        db.session.commit()

if __name__ == '__main__':
    init_db()