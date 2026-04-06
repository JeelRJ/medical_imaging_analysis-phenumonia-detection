import sys
import os

# Add webapp to path
sys.path.append(os.path.join(os.getcwd(), 'webapp'))

from app import app, db, User, bcrypt

with app.app_context():
    print("Initializing database...")
    db.create_all()
    # Create default admin if not exists
    if not User.query.filter_by(username='admin').first():
        hashed_pw = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin = User(username='admin', email='admin@pneumoscan.ai', password=hashed_pw, role='Admin')
        db.session.add(admin)
        db.session.commit()
        print("Default admin created (admin/admin123)")
    else:
        print("Database already initialized.")
