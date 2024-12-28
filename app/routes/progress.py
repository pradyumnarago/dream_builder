from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.extensions import db
from app.models.schedule_tracking_model import ScheduleTracking
from app.models.habit_tracking_model import HabitTracking
import datetime
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
import io
import base64

# Define the progress blueprint
progress_bp = Blueprint('progress', __name__)

# Route to view progress
@progress_bp.route('/progress')
@login_required
def progress():
    # Get today's date
    today = datetime.date.today()

    # Get the schedule and habit tracking data for the current user
    schedule_data = ScheduleTracking.query.filter_by(user_id=current_user.id).all()
    habit_data = HabitTracking.query.filter_by(user_id=current_user.id).all()

    # Process the data to get the progress (number of tasks/habits followed)
    schedule_progress = calculate_progress(schedule_data)
    habit_progress = calculate_progress(habit_data)

    # Generate the progress charts
    schedule_chart = generate_progress_chart(schedule_progress)
    habit_chart = generate_progress_chart(habit_progress)

    return render_template('progress.html', 
                           schedule_progress=schedule_progress, 
                           habit_progress=habit_progress, 
                           schedule_chart=schedule_chart,
                           habit_chart=habit_chart)

def calculate_progress(tracking_data):
    """
    Calculate the progress of schedule or habit by checking how many tasks/habits were followed.
    """
    total_items = len(tracking_data)
    
    if total_items == 0:
        return {
            'total': 0,
            'followed': 0,
            'percentage': 0  # No progress to report
        }
    
    followed_items = sum(1 for item in tracking_data if item.followed)

    return {
        'total': total_items,
        'followed': followed_items,
        'percentage': (followed_items / total_items) * 100
    }


def generate_progress_chart(progress_data):
    """
    Generate a progress chart (pie chart) for the user’s progress.
    Returns a base64-encoded image to be rendered in the HTML.
    """
    total = progress_data['total']
    followed = progress_data['followed']
    not_followed = total - followed

    # Handle the case where there is no data
    if total == 0:
        # Return a placeholder message in the chart
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, 'No Data Available', ha='center', va='center', fontsize=12)
        ax.axis('off')  # Hide axes

        # Save the plot to a BytesIO object
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)

        # Encode the image to base64
        chart_data = base64.b64encode(img.getvalue()).decode('utf-8')

        # Close the plot
        plt.close(fig)

        return chart_data

    # Create a pie chart
    fig, ax = plt.subplots()
    ax.pie([followed, not_followed], labels=['Followed', 'Not Followed'], autopct='%1.1f%%', startangle=90, colors=['#4CAF50', '#FF6347'])
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode the image to base64
    chart_data = base64.b64encode(img.getvalue()).decode('utf-8')

    # Close the plot
    plt.close(fig)

    return chart_data