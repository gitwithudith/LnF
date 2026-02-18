# Quick Setup Guide - Campus Lost & Found


This guide will help you get the project running and understand it well enough.

## ⚡ Quick Start (5 minutes)

### Step 1: Extract and Navigate
```bash
# Extract the zip file
unzip campus-lost-and-found.zip
cd campus-lost-and-found
```

### Step 2: Install Dependencies
```bash
# Create virtual environment (recommended)
python3 -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### Step 3: Run the App
```bash
python run.py
```

That's it! Visit `http://localhost:5000` in your browser.

---

## Understanding the Project 

### What Does This App Do?

It's a Lost and Found system for campus. Think of it as a digital bulletin board where:
- Students can post items they've **lost** (e.g., "Lost my black iPhone")
- Students can post items they've **found** (e.g., "Found a set of keys")
- People can message each other to arrange returns

### Why This Tech Stack?

**Python Flask**: 
- Easy to learn and explain
- You already know Python basics
- Perfect for web applications

**SQLite**:
- No separate database server needed
- All data in one file
- Easy to understand and explain

**Tailwind CSS**:
- Makes the UI look professional without writing much CSS
- Responsive (works on mobile)

---

##  Key Features to Highlight:

### 1. User Authentication
**File**: `app/routes/auth.py`

```python
@bp.route('/register', methods=['GET', 'POST'])
def register():
    # Creates new user account
    # Hashes password for security
    # Checks if username/email already exists
```



### 2. Item Management
**File**: `app/routes/items.py`

```python
@bp.route('/post', methods=['GET', 'POST'])
@login_required  # Only logged-in users can post
def post():
    # Handle form submission
    # Upload image if provided
    # Save to database
```


### 3. Search & Filter
**File**: `app/routes/items.py`

```python
query = Item.query.filter_by(is_resolved=False)
if status_filter != 'all':
    query = query.filter_by(status=status_filter)
if search_query:
    query = query.filter(Item.title.ilike(f'%{search_query}%'))
```


### 4. Messaging System
**File**: `app/routes/messages.py`

```python
@bp.route('/compose', methods=['GET', 'POST'])
@login_required
def compose():
    # Create new message
    # Link to item if relevant
    # Send to receiver
```


---

##  Database Schema Explanation

### Three Main Tables:

**1. Users**
- Stores user accounts
- Password is hashed, never plain text
- Links to items and messages

**2. Items**
- Each lost/found item is a row
- `status` field: "lost" or "found"
- `is_resolved`: marks if item was returned
- Foreign key to user who posted it

**3. Messages**
- Communication between users
- Has sender and receiver (both foreign keys to Users)
- Can link to an item

---

## How the Frontend Works

### Templates (Jinja2)
```html
{% extends "base.html" %}
{% block content %}
    <!-- Page-specific content -->
{% endblock %}
```



### Styling (Tailwind CSS)
```html
<button class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
    Submit
</button>
```


---

---


## If Something Breaks

### Database Reset
```bash
rm instance/lost_found.db
python run.py  # Recreates database
```

### Clear Cache
```bash
# Remove Python cache
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete
```

---

##
---

## 🎓 Bonus: Deployment

Try deploying to Render or Railway:

**Render**:
1. Push to GitHub
2. Create Render account
3. New Web Service → Connect repo
4. It auto-detects Python and deploys!

Having a live URL is impressive: "You can see it live at..."

---
