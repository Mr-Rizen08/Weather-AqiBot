from aiogram.utils.keyboard import ReplyKeyboardBuilder

def weatherbot_start():
    kb = ReplyKeyboardBuilder()
    kb.button(text="WeatherSearch")
    kb.button(text="AirPolution")
    kb.button(text="Full")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def back_kb():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Back->")
    return kb.as_markup(resize_keyboard=True)
