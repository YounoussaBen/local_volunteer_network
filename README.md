</thinking>

# Local Volunteer Network

<div align="center">
  <h3>Connecting Volunteers with Opportunities in Accra</h3>
  
  [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
  [![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://www.djangoproject.com/)
  [![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)
  [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
</div>

## 📋 Overview

Local Volunteer Network is a web platform designed to bridge the gap between volunteers and organizations in Accra, Ghana. The platform creates a centralized hub where volunteers can discover meaningful opportunities based on their skills and interests, while organizations can efficiently find dedicated volunteers for their initiatives.

### 🌟 Key Features

- **Intelligent Matching**: Connects volunteers with opportunities that align with their skills, interests, and availability
- **User Profiles**: Detailed profiles for both volunteers and organizations
- **Opportunity Management**: Organizations can create, edit, and manage volunteer opportunities
- **Application System**: Streamlined application process with feedback mechanisms
- **Dashboard Analytics**: Insightful statistics and management tools
- **Responsive Design**: Optimized user experience on both mobile and desktop devices

## 💻 Tech Stack

- **Backend**: Django 4.2+
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5.3
- **Database**: SQLite (development)
- **Other Technologies**: Crispy Forms, AOS (Animate On Scroll) Library

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (optional)

### Setup Instructions

#### 1. Clone the Repository (if using Git)

```bash
git clone https://github.com/YB-CG/local-volunteer-network.git
cd local-volunteer-network
```

If you're not using Git, simply download and extract the project to your preferred location.

#### 2. Create and Activate a Virtual Environment

**For Windows:**

```powershell
# Create virtual environment
python -m venv venv

# Enable script execution (if needed)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# Activate virtual environment
.\venv\Scripts\activate
```

**For macOS/Linux:**

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install django
pip install pillow
pip install django-crispy-forms
pip install crispy-bootstrap5
```


#### 4. Setup the Project

The project includes a custom management command to handle database setup, migrations, and initial data loading:

```bash
# Make migrations for our apps
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Load initial data
python manage.py setup_project --reset
```

This command will:
- Create a new database
- Apply all migrations
- Load initial data (skills, interests, organizations, volunteers, etc.)
- Create a default admin user

After running this command, you'll have a fully populated system ready for testing.

**Default Login Credentials:**

| User Type    | Username              | Password      |
|--------------|----------------------|--------------|
| Admin        | admin                | adminpassword |
| Volunteer    | kofi_mensah          | adminpassword |
| Volunteer    | adwoa_boateng        | adminpassword |
| Volunteer    | kwame_asante         | adminpassword |
| Organization | hope_foundation      | adminpassword |
| Organization | green_ghana          | adminpassword |
| Organization | accra_arts_collective | adminpassword |

> **⚠️ Note:** For production, please change these default passwords!

### 🏃‍♂️ Running the Project

Once setup is complete, you can run the development server:

```bash
python manage.py runserver
```

The application will be available at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## 📂 Project Structure

```
local_volunteer_network/
├── accounts/                 # User accounts, profiles, and authentication
├── core/                     # Core functionality and shared components
├── opportunities/            # Volunteer opportunities and applications
├── static/                   # Static files (CSS, JS, images)
├── templates/                # Base templates
├── fixtures/                 # Initial data
├── manage.py                 # Django management script
├── volunteer_network/        # Project configuration
└── README.md                 # Project documentation
```

## 📱 Features Tour

### Home Page
The landing page showcases the platform's mission, featured opportunities, and impact statistics with beautiful animations and a modern interface.

### Registration & Profiles
Users can register as either volunteers or organizations with a guided step-by-step process:
- **Volunteers**: Create a profile with skills, interests, and availability preferences
- **Organizations**: Set up a detailed profile with mission, focus areas, and contact info

### Opportunity Discovery
The platform features a robust search system with:
- Advanced filtering options
- Grid and list view options
- Visual status indicators
- Location information
- Skills and interest tags

### Application Management
- **For Organizations**: Review applications, accept/decline volunteers, provide feedback
- **For Volunteers**: Track application status, view upcoming commitments, provide feedback

### Dashboard & Analytics
Both user types get personalized dashboards with:
- Visual statistics on engagement
- Recommended opportunities for volunteers
- Application management for organizations
- Upcoming commitments and events

## 🛠️ Project Features in Detail

### For Volunteers
- Create and manage personal profiles
- Browse and filter opportunities
- Apply to opportunities with personalized messages
- Track application status
- Provide feedback after volunteering
- View personalized opportunity recommendations

### For Organizations
- Create and manage organization profiles
- Post and manage volunteer opportunities
- Review and respond to volunteer applications
- Provide feedback to volunteers
- Track volunteer engagement statistics
- Manage event logistics


## 🤝 Contributing

We welcome contributions to improve the Local Volunteer Network! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📃 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 About

This project was developed as part of the final project for the Department of Information Technology at the Advanced School of Studies of Systems and Data (ASSDAS).

---

<div align="center">
  <p>Made with ❤️ for the Accra community</p>
  <p>© 2025 Local Volunteer Network</p>
</div>