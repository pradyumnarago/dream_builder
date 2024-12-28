from flask import render_template, request, redirect, url_for, Blueprint
from flask_login import login_required, current_user
from datetime import datetime, time
from app.models.chat_model import Chat
from app.models.schedule_model import Schedule
from app.models.habit_model import Habit
from app.utils.ai_api import generate_response
from app.extensions import db
from app.utils.ai_api import configure_ai_api
import json

counselling_bp = Blueprint('counselling', __name__)

API_KEY = "AIzaSyAOS_zaRwq_h_7UMVwrwfE9EAE66B7nPqQ"
configure_ai_api(API_KEY)

@counselling_bp.route('/counselling', methods=['GET', 'POST'])
@login_required
def counselling():
    # Retrieve chat history from the database for the current user
    chat_history = [
        {'role': 'user', 'parts': [chat.prompt]} if chat.prompt else
        {'role': 'model', 'parts': [chat.response]} 
        for chat in Chat.query.filter_by(user_id=current_user.id).all()
    ]

    if request.method == 'POST':
        # Save user answers to questions in the database
        answers = request.form.getlist('answers[]')
        questions = request.form.getlist('questions[]')

        for question, answer in zip(questions, answers):
            new_chat = Chat(
                user_id=current_user.id,
                prompt=question,
                response=answer,
                created_at=datetime.utcnow()
            )
            db.session.add(new_chat)
        db.session.commit()

        # Update the chat history
        chat_history = [
            {'role': 'user', 'parts': [chat.response]} if chat.prompt else
            {'role': 'model', 'parts': [chat.prompt]} 
            for chat in Chat.query.filter_by(user_id=current_user.id).all()
        ]

        # Generate the next set of questions
        new_question, chat_history = generate_response("Generate the next counselling question", chat_history)
        if len(chat_history) >= 10:  # Assuming each interaction has both user and model messages
            # Generate schedule and habits
            schedule_prompt = (
                "Based on the user's inputs and goals, generate a detailed personalized schedule.Make sure it alligns with the users routine like college,work,school. Only output the JSON array and it should not have 'json' like : ```json[{'title': 'Morning Mindfulness'"
                "[{'title': <string>, 'description': <string>, 'start_time': <HH:MM:SS>, 'end_time': <HH:MM:SS>}]."
            )
            habits_prompt = (
                "Suggest specific productive habits for the user based on the history of conversation. Only output the JSON array and it should not have 'json' like : ```json[{'title': 'Morning Mindfulness': "
                "[{'name': <string>, 'description': <string>, 'frequency': <string>, "
                "'start_date': <YYYY-MM-DD>, 'end_date': <YYYY-MM-DD>}]."
            )

            schedule_response, _ = generate_response(schedule_prompt, chat_history)
            habits_response, _ = generate_response(habits_prompt, chat_history)

            # Parse and save schedule
            try:
                if isinstance(schedule_response, str):
                    print('It is a string')
                    schedule_data = json.loads(schedule_response[7:-4])  # Parse JSON string
                elif isinstance(schedule_response, list):
                    schedule_data = schedule_response  # Already parsed

                print(schedule_data)
                for item in schedule_data:
                    new_schedule = Schedule(
                        user_id=current_user.id,
                        title=item['title'],
                        description=item['description'],
                        start_time=time.fromisoformat(item['start_time']),
                        end_time=time.fromisoformat(item['end_time']),
                        created_at=datetime.utcnow()
                    )
                    db.session.add(new_schedule)
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"Error parsing schedule response: {e}")
            print('schedule_responce:')
            print(schedule_response[7:-4])

            # Parse and save habits
            try:
                if isinstance(habits_response, str):
                    habits_data = json.loads(habits_response[7:-4])  # Parse JSON string
                elif isinstance(habits_response, list):
                    habits_data = habits_response  # Already parsed

                for habit in habits_data:
                    new_habit = Habit(
                        user_id=current_user.id,
                        name=habit['name'],
                        description=habit['description'],
                        frequency=habit['frequency'],
                        start_date=datetime.fromisoformat(habit['start_date']).date(),
                        end_date=datetime.fromisoformat(habit['end_date']).date(),
                        progress=0.0  # Default progress
                    )
                    db.session.add(new_habit)
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"Error parsing habits response: {e}")

            db.session.commit()
            return redirect(url_for('dashboard.dashboard'))

        return render_template('counselling.html', questions=[new_question])

    # On GET request, start counselling with the first question
    if not chat_history:
        initial_question, chat_history = generate_response("Start counselling session", [])
        return render_template('counselling.html', questions=[initial_question])

    return render_template('counselling.html', questions=[])
