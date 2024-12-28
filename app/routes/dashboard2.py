from flask import Blueprint, jsonify, render_template, redirect, url_for,request,flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models.schedule_model import Schedule
from app.models.habit_model import Habit
from app.models.schedule_tracking_model import ScheduleTracking
from app.models.habit_tracking_model import HabitTracking
from app.models.user_model import User
from datetime import datetime, time
from app.utils.ai_api import generate_response

# Define the blueprint
dashboard_bp = Blueprint('dashboard', __name__)

# Route for the dashboard page
@dashboard_bp.route('/dashboard',methods=['GET', 'POST'])
@login_required
def dashboard():
    # Get the current date
    today = datetime.today()

    # Fetch all schedules for the user
    schedules = Schedule.query.filter(Schedule.user_id == current_user.id).all()

    # Ensure schedule entries exist in ScheduleTracking for today
    for schedule in schedules:
        tracking = ScheduleTracking.query.filter_by(
            schedule_id=schedule.id, date=today).first()
        if not tracking:
            # Insert missing tracking entry
            new_tracking = ScheduleTracking(
                schedule_id=schedule.id,
                date=today,
                followed=False,
                user_id=current_user.id
            )
            db.session.add(new_tracking)
    db.session.commit()

    # Fetch all habits for the user
    habits = Habit.query.filter(Habit.user_id == current_user.id).all()

    # Ensure habit entries exist in HabitTracking for today
    for habit in habits:
        tracking = HabitTracking.query.filter_by(
            habit_id=habit.id, date=today).first()
        if not tracking:
            # Insert missing tracking entry
            new_tracking = HabitTracking(
                habit_id=habit.id,
                date=today,
                followed=False,
                user_id=current_user.id
            )
            db.session.add(new_tracking)
    db.session.commit()

    # Fetch today's schedules and habits with tracking data
    today_schedules = Schedule.query.join(ScheduleTracking).filter(
        Schedule.user_id == current_user.id, ScheduleTracking.date == today).all()
    today_habits = Habit.query.join(HabitTracking).filter(
        Habit.user_id == current_user.id, HabitTracking.date == today).all()
    
    # if request.method == 'POST':
    #     # Process Schedule updates
    #     for schedule in schedules:
    #         schedule_id = schedule.id
    #         followed = f'schedule_{schedule_id}' in request.form
    #         schedule_tracking = ScheduleTracking.query.filter_by(schedule_id=schedule_id, user_id=current_user.id).first()
    #         if schedule_tracking:
    #             schedule_tracking.followed = followed
    #         else:
    #             # If no tracking entry exists, create a new one
    #             new_schedule_tracking = ScheduleTracking(
    #                 schedule_id=schedule_id,
    #                 user_id=current_user.id,
    #                 followed=followed,
    #                 date=today
    #             )
    #             db.session.add(new_schedule_tracking)

    #     # Process Habit updates
    #     for habit in habits:
    #         habit_id = habit.id
    #         followed = f'habit_{habit_id}' in request.form
    #         habit_tracking = HabitTracking.query.filter_by(habit_id=habit_id, user_id=current_user.id).first()
    #         if habit_tracking:
    #             habit_tracking.followed = followed
    #         else:
    #             # If no tracking entry exists, create a new one
    #             new_habit_tracking = HabitTracking(
    #                 habit_id=habit_id,
    #                 user_id=current_user.id,
    #                 followed=followed,
    #                 date=today
    #             )
    #             db.session.add(new_habit_tracking)

    #     # Commit the updates to the database
    #     db.session.commit()

    #     # Redirect back to the dashboard
    #     return redirect(url_for('dashboard.dashboard'))
    latest_chat = Chat.query.filter_by(user_id=current_user.id).order_by(Chat.created_at.desc()).first()

    # Fetch chat history for AI prompting
    chat_history = [
        {'role': 'user', 'parts': [chat.response]} if chat.prompt else
        {'role': 'model', 'parts': [chat.prompt]} 
        for chat in Chat.query.filter_by(user_id=current_user.id).all()
    ]

    if request.method == 'POST':
        # Get user input from the form
        user_input = request.form.get('entry')

        # Save the user's input to the Chat table
        new_chat = Chat(
            user_id=current_user.id,
            prompt=user_input,
            created_at=datetime.utcnow()
        )
        db.session.add(new_chat)
        db.session.commit()

        # Prompt AI for feedback
        ai_input = f"{user_input}. To give feedback."
        ai_response, chat_history = generate_response(ai_input, chat_history)

        # Save the AI response
        new_chat.response = ai_response
        db.session.commit()

        # Redirect to dashboard after processing
        return redirect(url_for('dashboard.dashboard'))

    return render_template(
        'dashboard.html',
        user=current_user,
        current_date=today,
        latest_chat=latest_chat,
        schedule=today_schedules,
        habits=today_habits
    )


# Route for editing schedule and habit after counselling
@dashboard_bp.route('/edit_schedule_habits', methods=['GET', 'POST'])
@login_required
def edit_schedule_habits():
    if request.method == 'POST':
        # Logic to handle schedule and habit editing
        # You can fetch the new schedule and habit data from the form and update the DB
        schedule_data = request.form.getlist('schedule')  # List of schedule ids from the form
        habit_data = request.form.getlist('habit')  # List of habit ids from the form

        for schedule_id in schedule_data:
            schedule = Schedule.query.get(schedule_id)
            schedule.followed = True  # Update the schedule to followed
            db.session.commit()

        for habit_id in habit_data:
            habit = Habit.query.get(habit_id)
            habit.followed = True  # Update the habit to followed
            db.session.commit()

        return redirect(url_for('dashboard.dashboard'))  # Redirect back to the dashboard
    
    return render_template('edit_schedule_habits.html')  # A form to edit schedules and habits

@dashboard_bp.route('/update_schedule_tracking/<int:task_id>', methods=['POST'])
@login_required
def update_schedule_tracking(task_id):
    data = request.get_json()
    followed = data.get('followed')  # True if checked, False if unchecked

    # Find the schedule tracking entry for the current date
    today = datetime.date.today()
    tracking = ScheduleTracking.query.filter_by(
        schedule_id=task_id, date=today, user_id=current_user.id).first()

    if tracking:
        tracking.followed = followed  # Update the followed field with the boolean value
        db.session.commit()

    return jsonify({'status': 'success'})

@dashboard_bp.route('/update_habit_tracking/<int:habit_id>', methods=['POST'])
@login_required
def update_habit_tracking(habit_id):
    data = request.get_json()
    followed = data.get('followed')  # True if checked, False if unchecked

    # Find the habit tracking entry for the current date
    today = datetime.date.today()
    tracking = HabitTracking.query.filter_by(
        habit_id=habit_id, date=today, user_id=current_user.id).first()

    if tracking:
        tracking.followed = followed  # Update the followed field with the boolean value
        db.session.commit()

    return jsonify({'status': 'success'})

from app.models import Chat  # Import the Chat model

@dashboard_bp.route('/delete_all_data', methods=['POST'])
@login_required
def delete_all_data():
    try:
        # Delete all schedules and related tracking data
        ScheduleTracking.query.filter_by(user_id=current_user.id).delete()
        Schedule.query.filter_by(user_id=current_user.id).delete()

        # Delete all habits and related tracking data
        HabitTracking.query.filter_by(user_id=current_user.id).delete()
        Habit.query.filter_by(user_id=current_user.id).delete()

        # Delete all chats related to the user
        Chat.query.filter_by(user_id=current_user.id).delete()

        # Commit the changes
        db.session.commit()
        flash('All your data, including chats, has been successfully deleted.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting your data. Please try again.', 'danger')

    # Redirect back to the dashboard
    return redirect(url_for('dashboard.dashboard'))
