"""
Routes package initialization
Imports all route blueprints
"""
from flask import Blueprint, render_template, send_from_directory, current_app
from flask_login import current_user
import os

# Main blueprint for homepage
bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Homepage route"""
    from app.models import Item
    
    # Get recent items (6 most recent)
    recent_lost = Item.query.filter_by(status='lost', is_resolved=False)\
        .order_by(Item.created_at.desc()).limit(6).all()
    recent_found = Item.query.filter_by(status='found', is_resolved=False)\
        .order_by(Item.created_at.desc()).limit(6).all()
    
    return render_template('index.html', 
                         recent_lost=recent_lost,
                         recent_found=recent_found)


@bp.route('/about')
def about():
    """About page route"""
    return render_template('about.html')


# Serve favicon from project-level assets folder
@bp.route('/favicon.ico')
def favicon():
    assets_dir = os.path.abspath(os.path.join(current_app.root_path, '..', 'assets'))
    return send_from_directory(assets_dir, 'favicon.webp')
