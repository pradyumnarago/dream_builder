from flask import Blueprint, abort, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app.models.habit_model import Habit
from app.extensions import db

habit_bp = Blueprint('habit', __name__)

# View habits route
@habit_bp.route('/habit', methods=['GET'])
def view_habits():
    # Fetch all habits for the logged-in user
    user_id = 1  # This should be dynamically fetched based on the logged-in user
    habits = Habit.query.filter_by(user_id=user_id).all()

    return render_template('habit.html', habits=habits)

# Add habit route
@habit_bp.route('/habit/add', methods=['GET', 'POST'])
def add_habit():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description', '')  # Optional, default empty string
        frequency = request.form.get('frequency')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        # Validate input
        if not name or not frequency:
            flash('Please fill in all required fields.', 'danger')
            return redirect(url_for('habit.add_habit'))

        # Add new habit to the database
        user_id = 1  # This should be dynamically fetched based on the logged-in user
        new_habit = Habit(name=name, description=description, frequency=frequency, start_date = start_date, end_date = end_date,progress = 0, user_id=user_id)

        db.session.add(new_habit)
        db.session.commit()

        flash('Habit added successfully!', 'success')
        return redirect(url_for('dashboard.dashboard'))
    
    return render_template('add_habit.html')

# Edit habit route
@habit_bp.route('/habit/edit/<int:habit_id>', methods=['GET', 'POST'])
def edit_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)

    if request.method == 'POST':
        habit.name = request.form['name']
        habit.description = request.form['description']
        habit.frequency = request.form['frequency']

        # Commit the changes
        db.session.commit()

        flash('Habit updated successfully!', 'success')
        return redirect(url_for('dashboard.dashboard'))

    return render_template('habit.html', habit=habit)

# Delete habit route
@habit_bp.route('/habit/delete/<int:habit_id>', methods=['POST'])
def delete_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)

    # Delete the habit from the database
    db.session.delete(habit)
    db.session.commit()

    flash('Habit deleted successfully!', 'success')
    return redirect(url_for('dashboard.dashboard'))

@habit_bp.route('/edit/<int:habit_id>', methods=['GET'])
@login_required
def edit_habit_with_login(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    if habit.user_id != current_user.id:
        abort(403)  # Forbidden if the user doesn't own the habit
    return render_template('habit.html', habit=habit)

@habit_bp.route('/update', methods=['POST'])
@login_required
def update_habit():
    habit_id = request.form.get('habit_id')
    habit = Habit.query.get_or_404(habit_id)
    if habit.user_id != current_user.id:
        abort(403)

    # Update habit details
    habit.name = request.form['name']
    habit.description = request.form['description']
    habit.frequency = request.form['frequency']
    habit.start_date = request.form['start_date']
    habit.end_date = request.form['end_date']
    db.session.commit()

    flash('Habit updated successfully!', 'success')
    return redirect(url_for('dashboard.dashboard'))
