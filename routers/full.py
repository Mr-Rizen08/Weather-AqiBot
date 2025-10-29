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

@router.message(F.text, StateMod.full_search)
async def full_handler(message:Message):
    weather_result = get_weather(message.text)
    aqi_result = get_aqi(weather_result['coord']['lon'], weather_result['coord']['lat'])
    await message.answer(f"City Name {weather_result['name']}, Timezone {weather_result['timezone']}\n"
                         f"Weather 🌤️ {weather_result['weather'][0]['main']}, {weather_result['weather'][0]['description']}\n"
                         f"Temperature 🌡️ {weather_result['main']['temp']}, \nFeels Like {weather_result['main']['feels_like']}\n"
                         f"Visibility 👀 {weather_result['visibility']}\n"
                         f"Wind speed 🌬️ {weather_result['wind']['speed']} km/h \n"
                         f" Угарный газ Co [ {aqi_result['list'][0]['components']['co']} ]\n "
                         f" Мелкие частицы Pm2.5 [ {aqi_result['list'][0]['components']['pm2_5']} ]\n"
                         f" Крупные частицы Pm10 [ {aqi_result['list'][0]['components']['pm10']} ]\n"
                         f" Озон O3 [ {aqi_result['list'][0]['components']['o3']} ]", reply_markup=end_task_kb())

@router.message(F.text == "End->", StateMod.full_search)
async def end_task_handler(message:Message, state: FSMContext):
    await message.answer("Вы вернулись")
    await state.clear()
    await message.answer("Hello", reply_markup=weatherbot_start())
    await state.set_state(StateMod.search)
