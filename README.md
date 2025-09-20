# Heart Rate Monitor API
![Python](https://img.shields.io/badge/python-3.13-blue)
![Django](https://img.shields.io/badge/django-5.2.6-green)
![DRF](https://img.shields.io/badge/django--rest--framework-3.16-red)


#
# **Project Overview**
- The Heart Monitor API is a Django REST Framework-based backend system designed for hospitals and healthcare centers to:
  - Manage patient admissions
  - Allocate heart monitoring devices
  - Monitor patient heart rates in real-time
  - Provide secure authentication and role-based access control
  - The API ensures that only authorized users (Doctors or Nurses) can monitor patients’ heart rates, while sensitive actions like adding devices or admitting patients are restricted to admins. JWT tokens are stored in HttpOnly cookies to enhance security.
#
# **Key Features**
- Patient Management: Admit, view, update, and delete patients.
- Device Management: Add and manage heart monitoring devices via the admin panel only.
- Patient-Device Mapping: Each patient is assigned a device at admission.
- Role-Based Access Control: Only Doctors and Nurses can access patient heart rate monitoring endpoints.
- Secure Authentication: Email activation, login, logout, and password reset.
#
# **Assumptions & Workflow**
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
#  
# **Tech Stack Used**
- Backend Framework: Django 5.2.6, Django REST Framework
- Authentication: JWT (via djangorestframework-simplejwt) with HttpOnly cookies
- Database: SQLite for local dev
- Email Service: Gmail SMTP for account activation & password reset
- Environment Management: python-decouple for .env variables
- Documentation: DRF Swagger / Redoc
- Language: Python 3.13
#
# **Project Structure**


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
     
│   ├── choices.py            # provides user_role choices

│   └── urls.py               # user authentication,creation routes

│

├── manage.py                 # Django management script

├── requirements.txt          # Python dependencies

├── .env.example              # Example environment variables

├── .gitignore

└── README.md                 # Project documentation
#
# **Installation & Setup**
1. Clone the Repository
   - git clone https://github.com/Darshan756/heart-monitor-api.git
   - cd heart-monitor-api
2. Create Virtual Environment
   - python -m venv env
   - source env/bin/activate # for linux/mac
   - env\Scripts\activate      # For Windows
3. Install Dependencies
   - pip install -r requirements.txt
4. Environment Variables
   
   Copy .env.example to .env and configure values
   - cp .env.example .env

   Update with your credentials (email backend, secret key).
5. Run Migrations
   - python manage.py makemigrations
   - python manage.py migrate
6. Create Superuser (for admin panel access)
   - python manage.py createsuperuser
7. Run Development Server
   - python manage.py runserver
   - 
Project will be available at:
- http://127.0.0.1:8000/
#
# **API Endpoints**
- Authentication
  - POST  http://127.0.0.1:8000/api/auth/register/ → Register a new user (activation link sent via email)
  - POST  http://127.0.0.1:8000/api/auth/activate/<uidb64>/<token>/ → Activate user using token from email
  - POST  http://127.0.0.1:8000/api/auth/signin/ → Login (JWT issued in HttpOnly cookie)
  - POST  http://127.0.0.1:8000/api/auth/refresh/ → Get a new access token using the refresh token (sent in HttpOnly cookie) + CSRF token for security
  - POST  http://127.0.0.1:8000/api/auth/logout/ → Logout and clear cookies
  - POST  http://127.0.0.1:8000/api/auth/reset-password/ → Request password reset link (sent via email)
  - POST  http://127.0.0.1:8000/api/auth/confirm-reset-password/<uidb64>/<token>/ → Reset password using token from email
  - GET  http://127.0.0.1:8000/api/auth/profile/ → Get details of the currently logged-in user (protected endpoint)
- Patients
  - POST  http://127.0.0.1:8000/api/patients/ → Register or update patient details
  - GET  http://127.0.0.1:8000/api/patients/ → Get all registered patients
  - GET  http://127.0.0.1:8000/api/patients/{id}/ → Get single patient details
    
  Note: These endpoints are registered via DRF’s DefaultRouter, which provides automatic RESTful routes.
- Admissions
  - POST  http://127.0.0.1:8000/api/admissions/ → Admit a patient (allocate device during admission)
  - GET  http://127.0.0.1:8000/api/admissions/ → List all admitted patients
  - GET  http://127.0.0.1:8000/api/admissions/{id}/ → Get details of a single admitted patient (includes device info, admitted by, etc.)
- Heart Rates
  - POST  http://127.0.0.1:8000/api/heartrates/ → Record a patient’s heart rate data
  - GET  http://127.0.0.1:8000/api/heartrates/ → Get all patients’ heart rate readings
  - GET  http://127.0.0.1:8000/api/heartrates/{id}/ → Get heart rate readings for a single patient
  
  Only users with the role of Doctor or Nurse are allowed to access heart rate monitoring endpoints.
#
# **Usage / Workflow Example**
1. User Registration & Activation
   - A new user (Doctor, Nurse, or Admin Staff) registers via /api/auth/register/.
   - An activation link is sent to the registered email.
   - After activation, the user can log in to the system.
2. Patient Registration
   - Admin or staff registers a patient using /api/patients/.
   - Basic details like name, age, gender are stored.
3. Device Allocation & Admission
   - Devices are pre-added via the Django admin panel.
   - At the time of admission, an available device is assigned to the patient via /api/admissions/.
4. Monitoring Patient Heart Rate
   - Doctor or Nurse logs in and monitors patient heart rates using /api/heartrates/.
   - Heart rate readings are stored in the database for real-time monitoring.
5. Account Security & Password Management
   - Users can reset their password by requesting a reset link via /api/auth/reset-password/.
   - A secure token is sent to their email, allowing them to set a new password.
   - JWT tokens are stored in HttpOnly cookies for secure authentication.
#
# Testing Section
 **Run Tests**
- Run all tests:
  python manage.py test

- Run tests for patients app:
  python manage.py test patients
#
# **API Documentation & Testing**
- The project provides Swagger and Redoc documentation for all API endpoints:
  - Swagger UI: http://127.0.0.1:8000/swagger/
  - Redoc UI: http://127.0.0.1:8000/redoc/
Authentication Note:
 - This API uses JWT stored in HttpOnly cookies for authentication.
 - All write actions (POST/PUT/PATCH/DELETE) require a valid CSRF token in the request headers.
 - Swagger UI cannot automatically send HttpOnly cookies or CSRF token, so protected endpoints will return 401 Unauthorized if tested directly in Swagger.
   
How to Test Protected Endpoints:
 - Use Postman or Insomnia for testing authenticated requests.
 - First, call /api/auth/signin/ with your credentials.
 - The server sets two cookies:
 - access (JWT for authentication)
 - csrftoken (CSRF token for secure POST/PUT/DELETE requests)
 - For write requests, include the CSRF token in the request header:
   - X-CSRFToken: <csrftoken>
Subsequent requests with cookies + CSRF header allow access to protected endpoints.

# **To refresh access token when it expires**

 POST to  http://127.0.0.1:8000/api/auth/refresh/ with:
- Refresh token cookie
- CSRF token header
  
This allows continued access without re-login.

  
    
     


   

  


  







