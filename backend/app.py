from flask import Flask
from flask_jwt_extended import JWTManager
from models import db, User, Department
import config
from routes.auth import auth_bp
from routes.admin import admin_bp

app = Flask(__name__)
app.config.from_object(config)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from flask_cors import CORS
CORS(app)

db.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')

def seed_departments():
    if Department.query.first():
        return

    departments = [
        {"name": "Cardiology", "description": "Heart and blood vessel treatment"},
        {"name": "Oncology", "description": "Cancer diagnosis and treatment"},
        {"name": "Neurology", "description": "Brain and nervous system"},
        {"name": "Orthopedics", "description": "Bones and joints"},
        {"name": "Pediatrics", "description": "Child healthcare"},
        {"name": "Dermatology", "description": "Skin related treatments"},
        {"name": "Gynecology", "description": "Women's health"},
        {"name": "Psychiatry", "description": "Mental health"},
        {"name": "ENT", "description": "Ear, Nose, Throat"},
        {"name": "Urology", "description": "Urinary system"},
        {"name": "Radiology", "description": "Imaging and scans"},
        {"name": "Anesthesiology", "description": "Anesthesia and pain relief"},
        {"name": "General Medicine", "description": "General health issues"},
        {"name": "Emergency", "description": "Emergency care"},
        {"name": "Gastroenterology", "description": "Digestive system"}
    ]

    for d in departments:
        dept = Department(name=d["name"], description=d["description"])
        db.session.add(dept)

    db.session.commit()

def create_admin():
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        admin_user = User(username='admin', password='admin123', role='admin')
        db.session.add(admin_user)
        db.session.commit()

with app.app_context():
    db.create_all()
    seed_departments()
    create_admin()

if __name__ == '__main__':
    app.run(debug=True)