"""
Message routes
Handles messaging between users about items
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Message, User, Item

bp = Blueprint('messages', __name__, url_prefix='/messages')


@bp.route('/inbox')
@login_required
def inbox():
    """View user's inbox"""
    # Get all received messages
    messages = Message.query.filter_by(receiver_id=current_user.id)\
        .order_by(Message.created_at.desc()).all()
    
    # Count unread messages
    unread_count = Message.query.filter_by(receiver_id=current_user.id, is_read=False).count()
    
    return render_template('messages/inbox.html', messages=messages, unread_count=unread_count)


@bp.route('/sent')
@login_required
def sent():
    """View user's sent messages"""
    messages = Message.query.filter_by(sender_id=current_user.id)\
        .order_by(Message.created_at.desc()).all()
    
    return render_template('messages/sent.html', messages=messages)


@bp.route('/compose', methods=['GET', 'POST'])
@login_required
def compose():
    """Compose a new message"""
    if request.method == 'POST':
        # Get form data
        receiver_username = request.form.get('receiver')
        subject = request.form.get('subject')
        body = request.form.get('body')
        item_id = request.form.get('item_id')  # Optional
        
        # Validation
        if not all([receiver_username, subject, body]):
            flash('Please fill in all required fields.', 'error')
            return render_template('messages/compose.html')
        
        # Find receiver
        receiver = User.query.filter_by(username=receiver_username).first()
        if not receiver:
            flash('User not found.', 'error')
            return render_template('messages/compose.html')
        
        # Can't send message to yourself
        if receiver.id == current_user.id:
            flash('You cannot send a message to yourself.', 'error')
            return render_template('messages/compose.html')
        
        # Create message
        message = Message(
            subject=subject,
            body=body,
            sender_id=current_user.id,
            receiver_id=receiver.id,
            item_id=int(item_id) if item_id else None
        )
        
        db.session.add(message)
        db.session.commit()
        
        flash('Message sent successfully!', 'success')
        return redirect(url_for('messages.sent'))
    
    # GET request - pre-fill if responding to an item
    item_id = request.args.get('item_id')
    receiver_username = request.args.get('to')
    
    item = None
    if item_id:
        item = Item.query.get(item_id)
    
    return render_template('messages/compose.html', 
                         item=item,
                         receiver_username=receiver_username)


@bp.route('/<int:message_id>')
@login_required
def view(message_id):
    """View a specific message"""
    message = Message.query.get_or_404(message_id)
    
    # Check if user is sender or receiver
    if message.sender_id != current_user.id and message.receiver_id != current_user.id:
        flash('You do not have permission to view this message.', 'error')
        return redirect(url_for('messages.inbox'))
    
    # Mark as read if receiver is viewing
    if message.receiver_id == current_user.id and not message.is_read:
        message.is_read = True
        db.session.commit()
    
    return render_template('messages/view.html', message=message)


@bp.route('/<int:message_id>/reply', methods=['GET', 'POST'])
@login_required
def reply(message_id):
    """Reply to a message"""
    original_message = Message.query.get_or_404(message_id)
    
    # Check if user can reply (must be receiver of original)
    if original_message.receiver_id != current_user.id:
        flash('You can only reply to messages you received.', 'error')
        return redirect(url_for('messages.inbox'))
    
    if request.method == 'POST':
        body = request.form.get('body')
        
        if not body:
            flash('Message body cannot be empty.', 'error')
            return render_template('messages/reply.html', original_message=original_message)
        
        # Create reply
        reply_message = Message(
            subject=f"Re: {original_message.subject}",
            body=body,
            sender_id=current_user.id,
            receiver_id=original_message.sender_id,
            item_id=original_message.item_id
        )
        
        db.session.add(reply_message)
        db.session.commit()
        
        flash('Reply sent successfully!', 'success')
        return redirect(url_for('messages.sent'))
    
    return render_template('messages/reply.html', original_message=original_message)


@bp.route('/<int:message_id>/delete', methods=['POST'])
@login_required
def delete(message_id):
    """Delete a message"""
    message = Message.query.get_or_404(message_id)
    
    # Check if user is sender or receiver
    if message.sender_id != current_user.id and message.receiver_id != current_user.id:
        flash('You do not have permission to delete this message.', 'error')
        return redirect(url_for('messages.inbox'))
    
    db.session.delete(message)
    db.session.commit()
    
    flash('Message deleted.', 'info')
    return redirect(url_for('messages.inbox'))
