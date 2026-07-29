# Event Management System

A full-featured, role-based Event Management System built with Flask, MySQL, and Bootstrap 5. Designed as a production-style 3rd-year B.Tech IT Software Engineering project with clean modular architecture, professional UI, and industry-standard coding practices.

## Features

### Admin
- Secure login/logout with session management
- Dashboard with live statistics and charts
- Add, edit, and delete events with image upload
- Manage event categories
- View all registered users and participants
- Search and filter across all modules
- Export participant list to CSV

### User
- Register/login with session management
- Browse upcoming events with search and category filter
- View detailed event information
- Register for events with confirmation
- Cancel registration
- View all my registered events
- Edit personal profile

### General
- Responsive UI (mobile, tablet, desktop)
- Flash notifications for all actions
- Input validation (client + server)
- Pagination for large datasets
- Image upload for event banners
- Custom 404 and 500 error pages
- Dark mode toggle
- Smooth CSS animations

## Technologies Used

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, JavaScript, Bootstrap 5, Bootstrap Icons |
| Backend | Python 3, Flask |
| Database | MySQL 8 / SQLite (auto-fallback) |
| Version Control | Git & GitHub |
| IDE | VS Code |

## Folder Structure

```
Event-Management-System/
├── app.py                  # Main Flask application entry point
├── config.py               # Configuration settings
├── wsgi.py                 # Production WSGI entry point
├── requirements.txt        # Python dependencies
├── Procfile                # Render deployment config
├── .gitignore              # Git ignore rules
├── README.md               # Project documentation
│
├── database/
│   ├── schema.sql          # Database table definitions
│   └── sample_data.sql     # Sample data for testing
│
├── models/
│   ├── __init__.py         # Package init
│   └── db.py               # Database connection and query helpers
│
├── routes/
│   ├── __init__.py         # Blueprint registration
│   ├── auth.py             # Login / logout / register
│   ├── admin.py            # Admin management routes
│   ├── user.py             # User profile routes
│   ├── events.py           # Event browsing and detail routes
│   └── registrations.py    # Registration management routes
│
├── templates/
│   ├── base.html           # Base layout (admin/user/public)
│   ├── landing.html        # Landing/home page
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   ├── dashboard_admin.html    # Admin dashboard
│   ├── dashboard_user.html     # User dashboard
│   ├── admin_events.html       # Admin event list
│   ├── admin_event_form.html   # Admin add/edit event
│   ├── admin_categories.html   # Category management
│   ├── admin_users.html        # User list for admin
│   ├── events.html             # Public event listing
│   ├── event_detail.html       # Event detail page
│   ├── my_events.html          # User's registered events
│   ├── profile.html            # Edit profile
│   ├── 404.html                # Page not found
│   └── 500.html                # Internal server error
│
├── static/
│   ├── css/style.css       # Custom styles + dark mode
│   ├── js/script.js        # Custom JavaScript
│   └── images/             # Static images
│
├── uploads/                # User-uploaded event banners
├── screenshots/            # Application screenshots
└── docs/                   # Documentation and UML diagrams
```

## Screenshots

###Landing Page
<img width="1919" height="951" alt="ems" src="https://github.com/user-attachments/assets/87db1393-70ff-49ff-9872-59ea014a4706" />

###Login Page
<img width="1919" height="780" alt="lp" src="https://github.com/user-attachments/assets/740f0fed-864a-43dc-90e4-9de712b01d1f" />

###Admin Dashboard
<img width="1070" height="1008" alt="Gemini_Generated_Image_q1nsvnq1nsvnq1ns" src="https://github.com/user-attachments/assets/3b134bd2-b7c2-4439-8fd7-a75b91b06263" />

###User Dashboard
<img width="1070" height="1008" alt="Gemini_Generated_Image_e1jxobe1jxobe1jx" src="https://github.com/user-attachments/assets/56ef0ed5-2755-4c81-afac-31890e2bab82" />

###Event Listing 
<img width="1070" height="1008" alt="Gemini_Generated_Image_eh5ndgeh5ndgeh5n" src="https://github.com/user-attachments/assets/e4430f74-256a-4473-8d0a-9bf0559c50c4" />

###Event Booking
<img width="1070" height="1008" alt="Gemini_Generated_Image_f3z8cdf3z8cdf3z8" src="https://github.com/user-attachments/assets/359ec2f5-33f0-4245-8259-9fd5503f6bd6" />

## Installation Guide

### Prerequisites
- Python 3.8 or higher
- MySQL 8.0 or higher (optional - SQLite auto-fallback available)
- pip
- Git

### Step-by-Step

```bash
# 1. Clone the repository
git clone https://github.com/hassannn434/event-management-system.git
cd event-management-system

# 2. Create a virtual environment
python -m venv venv

# 3. Activate the virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. (Optional) Configure MySQL
mysql -u root -p
```

```sql
CREATE DATABASE event_management;
USE event_management;
SOURCE database/schema.sql;
SOURCE database/sample_data.sql;
```

```bash
# 6. Update config.py with your MySQL credentials
# Or skip step 5-6 to use SQLite auto-fallback

# 7. Run the Flask server
python app.py
```

The application starts at `http://127.0.0.1:5000`.

## Default Login Credentials

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@events.com | admin123 |
| User | john@email.com | user123 |
| User | jane@email.com | user123 |

## Database Schema

| Table | Description |
|-------|-------------|
| `admins` | Admin user accounts |
| `users` | Registered user profiles |
| `categories` | Event categories |
| `events` | Event listings with details |
| `registrations` | User-event registration records |

## UML Diagrams

All UML diagrams are in the `docs/` folder:
- **ER Diagram** - Entity relationships
- **Use Case Diagram** - Actor interactions
- **Class Diagram** - Object structure
- **Sequence Diagram** - Login and registration flows
- **Activity Diagram** - Event registration workflow
- **Flowchart** - System process flow

## Future Improvements

- Email notifications for event reminders
- Payment integration for paid events
- Event check-in with QR codes
- Social media sharing
- Event calendar view
- REST API for mobile app
- Multi-language support
- Real-time notifications with WebSockets

## Learning Outcomes

- Full-stack web development with Flask
- Role-based authentication and session management
- CRUD operations with relational database design
- Responsive UI with Bootstrap 5
- File upload handling
- Modular application architecture with Flask Blueprints
- Database normalization and constraint design
- Version control with Git

## Author

**Hassan**
B.Tech AIML

GitHub: [hassannn434](https://github.com/hassannn434)

## License

This project is licensed under the MIT License.
