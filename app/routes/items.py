"""
Item routes
Handles browsing, posting, searching, and managing lost/found items
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models import Item, User
from datetime import datetime
import os

bp = Blueprint('items', __name__, url_prefix='/items')


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@bp.route('/browse')
def browse():
    """Browse all items with filtering and search"""
    # Get query parameters
    status_filter = request.args.get('status', 'all')  # 'all', 'lost', 'found'
    category_filter = request.args.get('category', 'all')
    search_query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    
    # Start with base query
    query = Item.query.filter_by(is_resolved=False)
    
    # Apply status filter
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    # Apply category filter
    if category_filter != 'all':
        query = query.filter_by(category=category_filter)
    
    # Apply search filter
    if search_query:
        search = f'%{search_query}%'
        query = query.filter(
            db.or_(
                Item.title.ilike(search),
                Item.description.ilike(search),
                Item.location.ilike(search)
            )
        )
    
    # Order by most recent first
    query = query.order_by(Item.created_at.desc())
    
    # Paginate results
    items = query.paginate(page=page, per_page=current_app.config['ITEMS_PER_PAGE'], error_out=False)
    
    # Categories for filter dropdown
    categories = [
        'Electronics', 'Books', 'Clothing', 'Accessories', 
        'Keys', 'Bags', 'Documents', 'Sports Equipment', 'Other'
    ]
    
    return render_template('items/browse.html',
                         items=items,
                         categories=categories,
                         status_filter=status_filter,
                         category_filter=category_filter,
                         search_query=search_query)


@bp.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    """Post a new lost or found item"""
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        status = request.form.get('status')
        location = request.form.get('location')
        date_lost_found = request.form.get('date_lost_found')
        
        # Validation
        if not all([title, description, category, status, date_lost_found]):
            flash('Please fill in all required fields.', 'error')
            return render_template('items/post.html')
        
        # Handle file upload
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                # Create unique filename
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                image_filename = f"{current_user.id}_{timestamp}_{filename}"
                
                # Save file
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename)
                file.save(filepath)
        
        # Parse date
        try:
            date_obj = datetime.strptime(date_lost_found, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format.', 'error')
            return render_template('items/post.html')
        
        # Create new item
        item = Item(
            title=title,
            description=description,
            category=category,
            status=status,
            location=location,
            date_lost_found=date_obj,
            image_filename=image_filename,
            user_id=current_user.id
        )
        
        # Save to database
        db.session.add(item)
        db.session.commit()
        
        flash(f'Your {status} item has been posted successfully!', 'success')
        return redirect(url_for('items.detail', item_id=item.id))
    
    # GET request - show form
    categories = [
        'Electronics', 'Books', 'Clothing', 'Accessories',
        'Keys', 'Bags', 'Documents', 'Sports Equipment', 'Other'
    ]
    return render_template('items/post.html', categories=categories)


@bp.route('/<int:item_id>')
def detail(item_id):
    """View details of a specific item"""
    item = Item.query.get_or_404(item_id)
    return render_template('items/detail.html', item=item)


@bp.route('/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(item_id):
    """Edit an existing item"""
    item = Item.query.get_or_404(item_id)
    
    # Check if user owns this item
    if item.user_id != current_user.id:
        flash('You can only edit your own items.', 'error')
        return redirect(url_for('items.detail', item_id=item_id))
    
    if request.method == 'POST':
        # Update item fields
        item.title = request.form.get('title')
        item.description = request.form.get('description')
        item.category = request.form.get('category')
        item.status = request.form.get('status')
        item.location = request.form.get('location')
        
        # Update date if provided
        date_str = request.form.get('date_lost_found')
        if date_str:
            item.date_lost_found = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Handle new image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                # Delete old image if exists
                if item.image_filename:
                    old_path = os.path.join(current_app.config['UPLOAD_FOLDER'], item.image_filename)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                
                # Save new image
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                image_filename = f"{current_user.id}_{timestamp}_{filename}"
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename)
                file.save(filepath)
                item.image_filename = image_filename
        
        db.session.commit()
        flash('Item updated successfully!', 'success')
        return redirect(url_for('items.detail', item_id=item_id))
    
    categories = [
        'Electronics', 'Books', 'Clothing', 'Accessories',
        'Keys', 'Bags', 'Documents', 'Sports Equipment', 'Other'
    ]
    return render_template('items/edit.html', item=item, categories=categories)


@bp.route('/<int:item_id>/resolve', methods=['POST'])
@login_required
def resolve(item_id):
    """Mark an item as resolved (claimed/returned)"""
    item = Item.query.get_or_404(item_id)
    
    # Check if user owns this item
    if item.user_id != current_user.id:
        flash('You can only resolve your own items.', 'error')
        return redirect(url_for('items.detail', item_id=item_id))
    
    item.is_resolved = True
    db.session.commit()
    
    flash('Item marked as resolved!', 'success')
    return redirect(url_for('items.detail', item_id=item_id))


@bp.route('/<int:item_id>/delete', methods=['POST'])
@login_required
def delete(item_id):
    """Delete an item"""
    item = Item.query.get_or_404(item_id)
    
    # Check if user owns this item
    if item.user_id != current_user.id:
        flash('You can only delete your own items.', 'error')
        return redirect(url_for('items.detail', item_id=item_id))
    
    # Delete image file if exists
    if item.image_filename:
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], item.image_filename)
        if os.path.exists(filepath):
            os.remove(filepath)
    
    db.session.delete(item)
    db.session.commit()
    
    flash('Item deleted successfully.', 'info')
    return redirect(url_for('items.browse'))


@bp.route('/dashboard')
@login_required
def dashboard():
    """User's personal dashboard showing their items"""
    # Get user's items
    lost_items = Item.query.filter_by(user_id=current_user.id, status='lost')\
        .order_by(Item.created_at.desc()).all()
    found_items = Item.query.filter_by(user_id=current_user.id, status='found')\
        .order_by(Item.created_at.desc()).all()
    
    return render_template('dashboard.html',
                         lost_items=lost_items,
                         found_items=found_items)
