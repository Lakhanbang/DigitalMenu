# app.py

from flask import Flask, send_from_directory
from customer.routes import customer_bp
from owner.routes import owner_bp
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Register blueprints
app.register_blueprint(customer_bp)
app.register_blueprint(owner_bp)

# NEW: Route to serve uploaded files
@app.route('/uploads/<path:filename>')
def uploaded_files(filename):
    return send_from_directory(os.path.join(app.root_path, 'uploads'), filename)


if __name__ == '__main__':
    # Ensure upload folders exist
    os.makedirs('uploads/targets', exist_ok=True)
    os.makedirs('uploads/models', exist_ok=True)
    app.run(debug=True, port=5001) # Using port 5001 to avoid conflicts