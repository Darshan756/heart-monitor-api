**Heart Rate Monitor API**

**Project Overview**
- The Heart Monitor API is a Django REST Framework-based backend system designed for hospitals and healthcare centers to:
  - Manage patient admissions
  - Allocate heart monitoring devices
  - Monitor patient heart rates in real-time
  - Provide secure authentication and role-based access control
  - The API ensures that only authorized users (Doctors or Nurses) can monitor patients’ heart rates, while sensitive actions like adding devices or admitting patients are restricted to admins. JWT tokens are stored in HttpOnly cookies to enhance security.

**Key Features**
- Patient Management: Admit, view, update, and delete patients.
- Device Management: Add and manage heart monitoring devices via the admin panel only.
- Patient-Device Mapping: Each patient is assigned a device at admission.
- Role-Based Access Control: Only Doctors and Nurses can access patient heart rate monitoring endpoints.
- Secure Authentication: Email activation, login, logout, and password reset.

**Assumptions & Workflow**
1. **Patient Registration**
   - Patients are registered in the system first with their basic information (name, age, gender, etc.).
   - Registration can be handled by Admin / Staff.
3. **Devices**
   - Added only via the admin panel.
   - Each device has details like serial number, model,etc.
   - Patients are assigned a device at admission via a foreign key.
4. **Patient Admission**
   - Once a patient is registered and assigned a device, they are officially admitted into the system.
   - Admission is managed by Admin / Admin Staff.
5. **Monitoring**
   - Only Doctors and Nurses can monitor the heart rate of patients.
   - Patients cannot access or modify other patients’ data.
6. **Authentication & Security**
   - User registration requires email, password, and role.
   - Activation link is sent via email before login is allowed.
   - Password reset link is sent via email to allow users to securely reset their account password.
   - JWT tokens are stored in HttpOnly cookies for security.
   - Users can logout securely at any time.
     
**Tech Stack Used**
- Backend Framework: Django 5.2.6, Django REST Framework
- Authentication: JWT (via djangorestframework-simplejwt) with HttpOnly cookies
- Database: SQLite for local dev
- Email Service: Gmail SMTP for account activation & password reset
- Environment Management: python-decouple for .env variables
- Documentation: DRF Swagger / Redoc
- Language: Python 3.13

**Project Structure**


heartmonitor_api/

├── api_core/                 # Core Django project settings

│   ├── settings.py           # Main configuration (uses .env variables)

│   ├── urls.py               # Root URL routing

│   └── wsgi.py               # WSGI entry point

│

├── patients/                 # App for patient management & admissions

│   ├── models.py             # Patient & admission models

│   ├── views.py              # Endpoints for patient workflows

|   ├── tests.py              #test cases

│   ├── serializers.py        # Data serialization

│   └── urls.py               # Patient-related routes

│

├── user_account/             # Custom user management

│   ├── models.py             # Custom user model with roles

│   ├── views.py              # Auth endpoints (register, login, reset password, etc.)

│   ├── serializers.py        # User data serialization

│   └── urls.py               # user authentication,creation routes

│

├── manage.py                 # Django management script

├── requirements.txt          # Python dependencies

├── .env.example              # Example environment variables

├── .gitignore

└── README.md                 # Project documentation

**API Endpoints**
- Authentication
  - POST /api/auth/register/ → Register a new user (activation link sent via email)
  - POST /api/auth/activate/<uidb64>/<token>/ → Activate user using token from email
  - POST /api/auth/signin/ → Login (JWT issued in HttpOnly cookie)
  - POST /api/auth/refresh/ → Get a new access token using the refresh token (sent in HttpOnly cookie) + CSRF token for security
  - POST /api/auth/logout/ → Logout and clear cookies
  - POST /api/auth/reset-password/ → Request password reset link (sent via email)
  - POST /api/auth/confirm-reset-password/<uidb64>/<token>/ → Reset password using token from email
  - GET /api/auth/profile/ → Get details of the currently logged-in user (protected endpoint)
- Patients
  - POST /api/patients/ → Register or update patient details
  - GET /api/patients/ → Get all registered patients
  - GET /api/patients/{id}/ → Get single patient details
    
  Note: These endpoints are registered via DRF’s DefaultRouter, which provides automatic RESTful routes.
- Admissions
  - POST /api/admissions/ → Admit a patient (allocate device during admission)
  - GET /api/admissions/ → List all admitted patients
  - GET /api/admissions/{id}/ → Get details of a single admitted patient (includes device info, admitted by, etc.)
- Heart Rates
  - POST /api/heartrates/ → Record a patient’s heart rate data
  - GET /api/heartrates/ → Get all patients’ heart rate readings
  - GET /api/heartrates/{id}/ → Get heart rate readings for a single patient
  
  Only users with the role of Doctor or Nurse are allowed to access heart rate monitoring endpoints.
**Installation & Setup**
1. Clone the Repository
   - git clone

  


  







