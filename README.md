# 🏥 Hospital Management System (HMS)

A full-stack Hospital Management System built using Flask, Vue.js, SQLite, and Celery + Redis.  
The system supports role-based access for Admin, Doctor, and Patient with appointment management, treatment tracking, and background job processing.

---

## 🚀 Features

### 👤 Patient
- Register and Login
- View departments and doctors
- Book appointments based on doctor availability
- Reschedule and cancel appointments
- View complete medical history
- Export treatment history as CSV (asynchronous)

### 👨‍⚕️ Doctor
- View upcoming appointments
- Manage patient treatments (diagnosis, prescription, tests, medicines)
- Set availability (morning/evening slots for 7 days)
- View patient history (only their cases)

### 🛠 Admin
- Manage departments and doctors
- View all users
- Access patient history (per patient)
- Full system control

### ⚙️ Background Jobs (Celery + Redis)
- Daily reminders for patients with appointments
- Monthly reports for doctors
- Asynchronous CSV export for patient history

---

## 🧱 Tech Stack

Backend:
- Python (Flask)
- Flask-SQLAlchemy
- Flask-JWT-Extended

Frontend:
- Vue.js (Vite)
- Bootstrap

Database:
- SQLite

Background Processing:
- Celery
- Redis

---

## ⚙️ Setup Instructions

1. **Backend Setup**

```
cd backend  
pip install -r requirements.txt  
python app.py
``` 

---

2. **Frontend Setup**

```
cd frontend  
npm install  
npm run dev  
```

---

3. **Run Redis**
   
```
redis-server  
```

---

4. **Run Celery Worker**

```
python -m celery -A celery_config.celery worker --loglevel=info  
```

---

5. **Run Celery Beat (Scheduler)**

```
python -m celery -A celery_config.celery beat --loglevel=info  
```

---

## 🔐 Authentication

- JWT-based authentication
- Role-based access control (Admin / Doctor / Patient)
- Protected routes in both frontend and backend

---

## 📊 Key Functionalities

### Appointment System
- Slot-based booking (Morning / Evening)
- Based on doctor availability
- Supports rescheduling and cancellation

### Treatment Management
- Stores diagnosis, prescription, tests, and medicines
- Linked to each appointment

### CSV Export
- Triggered by patient
- Processed asynchronously using Celery
- Generates downloadable file

### Background Jobs
- Daily reminders (simulated via console)
- Monthly reports (doctor-wise summary)

---

## 🧠 Design Decisions

- Role-based access control for secure data handling
- Reusable UI components for maintainability
- Asynchronous processing using Celery for scalability
- Separation of frontend and backend logic

---

## 🎯 Future Improvements

- Email/SMS notifications
- PDF report generation
- Online payment integration
- Real-time appointment tracking

---

## 🧑‍💻 Author

Vinu Srinivas R (24F1001669)

---
