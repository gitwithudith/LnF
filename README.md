# Campus Lost & Found

A web-based Lost and Found management system for campus communities, built with Flask and SQLite.

## 🎯 Project Overview

This application helps students and staff report and find lost items on campus. Users can post items they've lost or found, search through listings, and message each other to arrange returns.

**Built for**: GDG on Campus Application  
**Tech Stack**: Python Flask, SQLite, HTML/CSS (Tailwind), JavaScript  
**Author**: [Your Name]

## ✨ Features

### Core Features
- **User Authentication**: Secure registration and login system
- **Post Items**: Report lost or found items with photos
- **Browse & Search**: Filter items by status, category, and search keywords
- **Messaging System**: Contact item owners through built-in messaging
- **User Dashboard**: Track your posted items and their status
- **Image Upload**: Attach photos to item listings

### Additional Features
- Responsive design (mobile-friendly)
- Mark items as resolved when returned
- Edit and delete your own items
- Pagination for large item lists
- Category-based organization
- Date and location tracking

## 🛠️ Technical Architecture

### Backend (Python Flask)
- **Framework**: Flask 3.0
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login for session management
- **File Handling**: Werkzeug for secure file uploads
- **Password Security**: Werkzeug password hashing

### Frontend
- **Styling**: Tailwind CSS (CDN)
- **Icons**: Font Awesome
- **JavaScript**: Vanilla JS for interactivity

### Database Schema
```
Users Table:
- id, username, email, password_hash, full_name, phone, created_at

Items Table:
- id, title, description, category, status (lost/found), 
  location, date_lost_found, image_filename, is_resolved, 
  created_at, updated_at, user_id (foreign key)

Messages Table:
- id, subject, body, is_read, created_at, 
  sender_id (foreign key), receiver_id (foreign key), 
  item_id (foreign key, optional)
```

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd campus-lost-and-found
```

### 2. Create Virtual Environment (Recommended)
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
```bash
# Copy the example env file
cp .env.example .env

# Edit .env and set a secure SECRET_KEY
# You can generate one with: python -c "import secrets; print(secrets.token_hex(32))"
```

### 5. Run the Application
```bash
python run.py
```

The application will start at `http://localhost:5000`

## 📱 Usage Guide

### For Users:

1. **Register an Account**
   - Click "Sign Up" in the navigation
   - Fill in username, email, and password
   - Optionally add full name and phone number

2. **Post a Lost Item**
   - Click "Post Item"
   - Select "Lost Item"
   - Fill in details (title, description, category, location, date)
   - Upload a photo (optional but recommended)
   - Submit

3. **Post a Found Item**
   - Same as above, but select "Found Item"

4. **Browse Items**
   - Click "Browse Items"
   - Use filters to narrow down (status, category)
   - Use search bar for keywords
   - Click on items to view details

5. **Contact Item Owner**
   - On item detail page, click "Contact [username]"
   - Compose and send message
   - Check inbox for replies

6. **Mark Item as Resolved**
   - When item is returned, go to item detail page
   - Click "Mark as Resolved"

## 🗂️ Project Structure

```
campus-lost-and-found/
├── app/
│   ├── __init__.py              # Flask app initialization
│   ├── models.py                # Database models
│   ├── routes/
│   │   ├── __init__.py          # Main routes
│   │   ├── auth.py              # Authentication routes
│   │   ├── items.py             # Item management routes
│   │   └── messages.py          # Messaging routes
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css        # Custom styles
│   │   ├── js/
│   │   │   └── main.js          # JavaScript
│   │   └── uploads/             # User uploaded images
│   └── templates/
│       ├── base.html            # Base template
│       ├── index.html           # Homepage
│       ├── auth/                # Authentication templates
│       ├── items/               # Item templates
│       ├── messages/            # Message templates
│       └── dashboard.html       # User dashboard
├── instance/
│   └── lost_found.db            # SQLite database (auto-generated)
├── config.py                    # Configuration
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🔑 Key Code Explanations (For Interview)

### 1. Flask Application Factory Pattern (`app/__init__.py`)
```python
def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    # ... register blueprints
    return app
```
**Why**: Allows multiple instances with different configs (testing, production)

### 2. Database Models (`app/models.py`)
```python
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # ... relationships
```
**Why**: SQLAlchemy ORM makes database operations Pythonic and safe

### 3. Route with Authentication (`app/routes/items.py`)
```python
@bp.route('/post', methods=['GET', 'POST'])
@login_required  # Decorator ensures user is logged in
def post():
    if request.method == 'POST':
        # Handle form submission
```
**Why**: Protects routes, separates GET (show form) and POST (process form)

### 4. File Upload Handling
```python
if 'image' in request.files:
    file = request.files['image']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Create unique filename to avoid conflicts
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{user_id}_{timestamp}_{filename}"
```
**Why**: Prevents security issues, handles duplicates

### 5. Database Queries with Filters
```python
query = Item.query.filter_by(is_resolved=False)
if status_filter != 'all':
    query = query.filter_by(status=status_filter)
if search_query:
    query = query.filter(Item.title.ilike(f'%{search_query}%'))
```
**Why**: Efficient, composable queries; ilike = case-insensitive search

## 🎨 Design Decisions

1. **SQLite Database**: Simple, no separate server needed, perfect for campus scale
2. **Tailwind CSS**: Rapid UI development without writing custom CSS
3. **Blueprint Architecture**: Modular routes for better organization
4. **Session-based Auth**: Simpler than JWT for server-rendered apps
5. **Server-side Rendering**: Better SEO, simpler deployment than SPA

## 🚢 Deployment Options

### Option 1: Render (Recommended)
1. Push code to GitHub
2. Connect Render to your repository
3. Set environment variables
4. Deploy!

### Option 2: PythonAnywhere
1. Upload code via Git
2. Create web app
3. Set WSGI configuration
4. Deploy!

### Option 3: Railway
1. Connect GitHub repository
2. Configure Python buildpack
3. Set environment variables
4. Deploy!

## 📊 Future Enhancements

- [ ] Email notifications for new messages
- [ ] Admin panel for moderation
- [ ] QR code generation for items
- [ ] Advanced search with filters
- [ ] Location-based search (map view)
- [ ] Mobile app version
- [ ] Integration with campus ID system
- [ ] Statistics dashboard
- [ ] Multi-campus support

## 🐛 Troubleshooting

### Database Issues
```bash
# Delete and recreate database
rm instance/lost_found.db
python run.py  # Will auto-create new database
```

### Port Already in Use
```bash
# Change port in run.py or:
PORT=8000 python run.py
```

### Missing Dependencies
```bash
pip install -r requirements.txt --upgrade
```

## 📝 License

This project is created for educational purposes as part of a GDG on Campus application.

## 👤 Contact

[Your Name]  
[Your Email]  
[Your GitHub]

---

**Note**: Remember to replace placeholder content with your actual information before submission!
