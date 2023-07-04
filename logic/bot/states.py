from aiogram.dispatcher.filters.state import StatesGroup, State


class DateStatesGroup(StatesGroup):
    date = State()
