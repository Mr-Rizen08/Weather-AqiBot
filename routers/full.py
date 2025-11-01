from aiogram import F, Router
from state import StateMod
from aiogram.fsm.context import FSMContext
from keyboard import back_kb, weatherbot_start, end_task_kb
from weaterinfo import get_aqi, get_weather
from aiogram.types import Message


router = Router()

@router.message(F.text == "Full", StateMod.search)
async def full_city_information_handler(message:Message, state: FSMContext):
    await message.answer("Напиши город", reply_markup=back_kb())
    await state.set_state(StateMod.full_search)

@router.message(F.text == "Back->", StateMod.full_search)
async def back_handler(message:Message, state:FSMContext):
    await message.answer("Вы вернулись")
    await state.clear()
    await message.answer("Hello", reply_markup=weatherbot_start())
    await state.set_state(StateMod.search)

def aqi_rating(value):
    if  value == 1:
        return "Очень хорошее (Very Good)"
    elif value == 2:
        return "Хорошее (Good)"
    elif value == 3:
        return "Умеренное (Moderate)"
    elif value == 4:
        return "Плохое (Poor)"
    elif value == 5:
        return "Очень плохое (Very Poor)"
    else:
        return "Такого значения нет"

@router.message(F.text, StateMod.full_search)
async def full_handler(message:Message, state: FSMContext):
    weather_result = get_weather(message.text)
    aqi_result = get_aqi(weather_result['coord']['lon'], weather_result['coord']['lat'])
    aqi_value = aqi_result['list'][0]['main']['aqi']
    aqi_text = aqi_rating(aqi_value)
    await message.answer(f"City Name {weather_result['name']}, Timezone {weather_result['timezone']},\n"
                         f"Weather 🌤️ {weather_result['weather'][0]['main']}, {weather_result['weather'][0]['description']},\n"
                         f"Temperature 🌡️ {weather_result['main']['temp']}°C, \nFeels Like {weather_result['main']['feels_like']}°C,\n"
                         f"Wind speed 🌬️ {weather_result['wind']['speed']} km/h,\n"
                         f"Качество воздуха {aqi_result['list'][0]['main']['aqi']} ({aqi_text}) \n"
                         f"Угарный газ Co [ {aqi_result['list'][0]['components']['co']} mg/m³],\n"
                         f"Мелкие частицы Pm2.5 [ {aqi_result['list'][0]['components']['pm2_5']} µg/m³],\n"
                         f"Крупные частицы Pm10 [ {aqi_result['list'][0]['components']['pm10']} µg/m³],\n"
                         f"Диоксид серы SO₂ [{aqi_result['list'][0]['components']['so2']} µg/m³],\n"
                         f"Аммиак NH₃ [{aqi_result['list'][0]['components']['nh3']} µg/m³],\n"
                         f"Озон O₃ [ {aqi_result['list'][0]['components']['o3']} µg/m³]", reply_markup=weatherbot_start())
    await state.clear()
    await state.set_state(StateMod.search)