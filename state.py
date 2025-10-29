from aiogram.fsm.state import State, StatesGroup

class StateMod(StatesGroup):
    weather_search = State()
    aqi_search = State()
    full_search = State()
    search = State()
    end = State()