from flask import Flask
from flask_jwt_extended import JWTManager
from models import db, User, Department
import config
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.doctor import doctor_bp
from routes.patient import patient_bp

app = Flask(__name__)
app.config.from_object(config)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from flask_cors import CORS
CORS(app, supports_credentials=True)

db.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(doctor_bp, url_prefix='/doctor')
app.register_blueprint(patient_bp, url_prefix='/patient')

def seed_departments():
    if Department.query.first():
        return

    departments = [
        {
        "name": "Cardiology",
        "description": "The Cardiology Department focuses on the diagnosis, treatment, and prevention of heart-related conditions. It houses a team of experienced cardiologists and cardiac specialists who manage heart attacks, arrhythmias, hypertension, and congenital heart diseases. With advanced diagnostic tools and modern treatment techniques, the department ensures comprehensive cardiac care and long-term heart health management."
        },

        {
        "name": "Oncology",
        "description": "The Oncology Department is dedicated to the diagnosis, treatment, and care of patients with cancer. It includes medical, surgical, and radiation oncologists who collaborate to provide personalized treatment plans. Using advanced therapies and supportive care, the department ensures effective cancer management and improved quality of life."
        },

        {
        "name": "Neurology",
        "description": "The Neurology Department specializes in diagnosing and treating disorders of the brain, spinal cord, and nervous system. It manages conditions such as stroke, epilepsy, migraines, Parkinson’s disease, and multiple sclerosis. The department uses advanced imaging and neurological testing for precise diagnosis and treatment."
        },

        {
        "name": "Orthopedics",
        "description": "The Orthopedics Department focuses on the treatment of bones, joints, and muscles. It provides care for fractures, arthritis, sports injuries, and spinal disorders. With both surgical and non-surgical approaches, the department helps restore mobility and improve the quality of life for patients."
        },

        {
        "name": "Pediatrics",
        "description": "The Pediatrics Department offers specialized healthcare services for infants, children, and adolescents. It focuses on growth, development, immunizations, and treatment of childhood illnesses in a safe and child-friendly environment."
        },

        {
        "name": "Dermatology",
        "description": "The Dermatology Department deals with skin, hair, and nail conditions. It provides treatment for acne, eczema, psoriasis, infections, and cosmetic concerns. The department uses modern techniques to ensure healthy skin and improved patient confidence."
        },

        {
        "name": "ENT",
        "description": "The ENT Department specializes in treating conditions related to the ear, nose, and throat. It manages hearing disorders, sinus infections, throat problems, and voice-related issues using advanced diagnostic and surgical techniques."
        },

        {
        "name": "Gynecology",
        "description": "The Gynecology Department focuses on women's reproductive health. It provides services such as prenatal care, menstrual disorder treatment, fertility management, and menopause care with a patient-centered approach."
        },

        {
        "name": "Urology",
        "description": "The Urology Department treats conditions related to the urinary tract and male reproductive system. It manages kidney stones, infections, prostate issues, and bladder disorders using modern diagnostic tools and treatments."
        },

        {
        "name": "General Medicine",
        "description": "The General Medicine Department serves as the first point of contact for patients. It provides diagnosis, treatment, and prevention of common illnesses and ensures continuous and holistic healthcare for all age groups."
        },

        {
        "name": "Radiology",
        "description": "The Radiology Department provides advanced imaging services such as X-rays, CT scans, MRI, and ultrasound. It plays a crucial role in accurate diagnosis and treatment planning across all medical specialties."
        },

        {
        "name": "Anesthesiology",
        "description": "The Anesthesiology Department is responsible for pain management and anesthesia during surgical procedures. It ensures patient safety and comfort before, during, and after surgery using modern anesthetic techniques."
        },

        {
        "name": "Psychiatry",
        "description": "The Psychiatry Department focuses on mental health and emotional well-being. It treats conditions such as depression, anxiety, stress disorders, and other psychiatric illnesses through therapy and medication."
        },

        {
        "name": "Pulmonology",
        "description": "The Pulmonology Department specializes in respiratory system disorders. It manages asthma, chronic obstructive pulmonary disease (COPD), lung infections, and other breathing-related conditions."
        },

        {
        "name": "Gastroenterology",
        "description": "The Gastroenterology Department deals with digestive system disorders. It treats conditions related to the stomach, liver, intestines, and pancreas, ensuring proper digestive health and nutrition."
        }
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