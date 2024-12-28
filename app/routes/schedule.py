from datetime import datetime
from flask import Blueprint, abort, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app.models.schedule_model import Schedule
from app.extensions import db

schedule_bp = Blueprint('schedule', __name__)

# View schedule route
@schedule_bp.route('/schedule', methods=['GET'])
def view_schedule():
    # Fetch all schedule items for the logged-in user
    user_id = 1  # This should be dynamically fetched based on the logged-in user
    schedules = Schedule.query.filter_by(user_id=user_id).all()

    return render_template('schedule.html', schedules=schedules)

# Add schedule route
@schedule_bp.route('/schedule/add', methods=['GET', 'POST'])
def add_schedule():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        created_at = request.form['created_at']

        # Validate input
        if not title or not start_time or not end_time:
            flash('Please fill in all required fields.', 'danger')
            return redirect(url_for('schedule.add_schedule'))

        # Add new schedule to the database
        user_id = 1  # This should be dynamically fetched based on the logged-in user
        new_schedule = Schedule(title=title, description=description, start_time=start_time,created_at = created_at, end_time = end_time, user_id=user_id)

        db.session.add(new_schedule)
        db.session.commit()

        flash('Schedule added successfully!', 'success')
        return redirect(url_for('dashboard.dashboard'))
    now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M')
    return render_template('add_schedule.html', now=now)

# Edit schedule route
@schedule_bp.route('/schedule/edit/<int:schedule_id>', methods=['GET', 'POST'])
def edit_schedule(schedule_id):
    schedule = Schedule.query.get_or_404(schedule_id)

    if request.method == 'POST':
        schedule.title = request.form['title']
        schedule.description = request.form['description']
        schedule.start_time = request.form['start_time']
        schedule.end_time = request.form['end_time']

        # Commit the changes
        db.session.commit()

        flash('Schedule updated successfully!', 'success')
        return redirect(url_for('dashboard.dashboard'))

    return render_template('schedule.html', schedule=schedule)

# Delete schedule route
@schedule_bp.route('/schedule/delete/<int:schedule_id>', methods=['POST'])
def delete_schedule(schedule_id):
    schedule = Schedule.query.get_or_404(schedule_id)

    # Delete the schedule from the database
    db.session.delete(schedule)
    db.session.commit()

    flash('Schedule deleted successfully!', 'success')
    return redirect(url_for('dashboard.dashboard'))

@schedule_bp.route('/edit/<int:schedule_id>', methods=['GET'])
@login_required
def edit_schedule_with_login(schedule_id):
    schedule = Schedule.query.get_or_404(schedule_id)
    if schedule.user_id != current_user.id:
        abort(403)  # Forbidden if the user doesn't own the schedule
    return render_template('schedule.html', schedule=schedule)

@schedule_bp.route('/update', methods=['POST'])
@login_required
def update_schedule():
    schedule_id = request.form.get('schedule_id')
    schedule = Schedule.query.get_or_404(schedule_id)
    if schedule.user_id != current_user.id:
        abort(403)

    # Update schedule details
    schedule.title = request.form['title']
    schedule.description = request.form['description']
    schedule.start_time = request.form['start_time']
    schedule.end_time = request.form['end_time']
    db.session.commit()

    flash('Schedule updated successfully!', 'success')
    return redirect(url_for('dashboard.dashboard'))
