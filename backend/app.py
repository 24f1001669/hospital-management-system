from flask import Flask
from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def create_admin():
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        admin_user = User(username='admin', password='admin123', role='admin')
        db.session.add(admin_user)
        db.session.commit()

with app.app_context():
    db.create_all()
    create_admin()

if __name__ == '__main__':
    app.run(debug=True)