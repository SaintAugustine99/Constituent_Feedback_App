# Constituent Feedback Platform

A comprehensive web application enabling efficient communication between elected officials, government agencies, independent commissions, and the public. This platform streamlines the collection and analysis of constituent feedback, provides access to government documents, and improves public participation in governance.

## 🚀 Features

### For Constituents
- **Account Management**: Register, login, and manage profile information
- **Feedback Submission**: Submit public or private feedback on local issues
- **Formal Complaints**: File official complaints to specific commissions or ombudsmen
- **Document Access**: View published government gazettes and reports
- **Geographic Integration**: Tag feedback with location data for better context
- **Status Tracking**: Monitor the progress of submitted feedback and complaints

### For Administrators
- **Dashboard**: Get overview statistics of platform activity
- **Analytics**: Analyze feedback trends, sentiment analysis, and geographic distribution
- **Response Management**: Provide official responses to constituent feedback
- **Publication Management**: Upload and manage official documents
- **User Management**: Verify users and manage district assignments

## 🛠️ Technology Stack

- **Backend**: Django 5.1 with Django REST Framework
- **Database**: SQLite (development), PostgreSQL (recommended for production)
- **Frontend**: Bootstrap 5, HTML, CSS, JavaScript
- **Authentication**: JWT authentication for API access
- **Analytics**: Custom analytics for sentiment analysis and data visualization

## 📋 Core Modules

The platform consists of several interlinked modules:

- **Accounts**: User management, authentication, and profile handling
- **Feedback**: Core system for submitting and responding to constituent concerns
- **Complaints**: Formal complaint submission and tracking system
- **Publications**: Management of official documents and reports
- **Analytics**: Data analysis and visualization tools
- **Search**: Cross-module search functionality

## 🏗️ Data Models

### User Models
- **User**: Custom user model with role-based access control
- **District**: Geographic districts for constituents

### Feedback Models
- **Category**: Hierarchical categorization of feedback
- **Feedback**: Core entity for constituent submissions
- **Response**: Official responses to feedback
- **Media**: Attachments for feedback (images, documents, etc.)

### Complaint Models
- **Complaint**: Formal complaints to specific commissions
- **ComplaintUpdate**: Status updates for complaints
- **ComplaintDocument**: Supporting documents for complaints

### Publication Models
- **Gazette**: Official government publications
- **Report**: Annual institutional reports

### Analytics Models
- **SentimentAnalysisResult**: Pre-computed sentiment analysis for feedback

## 🔐 Security Features

- Custom user authentication with email-based login
- JWT token authentication for API access
- Role-based access control (constituent vs. administrator)
- CSRF protection for all form submissions
- Secure password handling with Django's built-in security

## 🚦 API Endpoints

The platform provides a complete REST API for integration with mobile apps or other services:

### Authentication
- `/api/users/register/` - User registration
- `/api/users/login/` - Login (token generation)
- `/api/users/token/refresh/` - Refresh authentication token

### Feedback
- `/api/feedback/` - List and create feedback
- `/api/feedback/<id>/` - Retrieve, update, delete feedback
- `/api/feedback/<id>/responses/` - Add responses to feedback
- `/api/feedback/<id>/media/` - Upload media for feedback

### Complaints
- `/api/complaints/` - List and create complaints
- `/api/complaints/<id>/` - Retrieve, update, delete complaints
- `/api/complaints/<id>/status/` - Update complaint status

### Publications
- `/api/gazettes/` - List and create gazettes
- `/api/gazettes/<id>/` - Retrieve, update, delete gazettes
- `/api/reports/` - List and create reports
- `/api/reports/<id>/` - Retrieve, update, delete reports

### Analytics
- `/api/analytics/dashboard/` - Admin dashboard statistics
- `/api/analytics/feedback-analytics/` - Detailed feedback analysis
- `/api/analytics/geographic-analytics/` - Geographic analysis

### Search
- `/api/search/` - Cross-entity search functionality

## 📥 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/constituent-feedback-platform.git
   cd constituent-feedback-platform
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

7. Access the admin interface at http://127.0.0.1:8000/admin/

## 🔧 Configuration

### Required Environment Variables
- `SECRET_KEY` - Django secret key
- `DEBUG` - Set to False in production
- `ALLOWED_HOSTS` - List of allowed hosts for the application

### Media Storage
The platform uses local storage for media files during development. For production, consider using cloud storage solutions like AWS S3.

## 🌐 Deployment

For production deployment:

1. Set `DEBUG=False` in settings.py
2. Configure a proper database (PostgreSQL recommended)
3. Set up static files serving with a web server like Nginx
4. Consider using Gunicorn or uWSGI as the application server
5. Enable HTTPS with a valid SSL certificate

## 🧪 Testing

Run the test suite with:
```bash
python manage.py test
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
