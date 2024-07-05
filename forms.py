from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    first_currency = State()
    second_currency = State()
    quantity = State()