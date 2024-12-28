from .user_model import User
from .chat_model import Chat
from .schedule_model import Schedule
from .habit_model import Habit

from .habit_tracking_model import HabitTracking
from .schedule_tracking_model import ScheduleTracking


# Initialize a list of all models for easy migration handling if needed
__all__ = ["User", "Chat", "Schedule", "Habit","HabitTracking","ScheduleTracking"]
