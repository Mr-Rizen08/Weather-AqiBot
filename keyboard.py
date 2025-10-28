from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

def weatherbot_start():
    kb = ReplyKeyboardBuilder()
    kb.button(text="WeatherSearch")
    return kb.as_markup(resize_keyboard=True)

