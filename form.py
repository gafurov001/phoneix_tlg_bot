from aiogram.fsm.state import StatesGroup, State


class LessonsQuestion(StatesGroup):
    user_id = State()
    modul = State()
    lesson = State()
    answer = State()
    curator = State()
    curator_id = State()
    question_id = State()
    full_name = State()
    phone_number = State()
    screenshot_check = State()
    reason_cancel_course = State()
    amalyot_group = State()
    platforma_group = State()








