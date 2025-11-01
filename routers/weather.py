from aiogram import Router, F
from aiogram.types import Message
from state import StateMod
from aiogram.fsm.context import FSMContext
from weaterinfo import get_weather
from keyboard import back_kb, weatherbot_start, end_task_kb

router = Router()

@router.message(F.text == "WeatherSearch" , StateMod.search)
async def weather_city_handler(message:Message, state: FSMContext):
    await message.answer("Напиши город", reply_markup=back_kb())
    await state.set_state(StateMod.weather_search)

@router.message(F.text == "Back->", StateMod.weather_search)
async def back_handler(message:Message, state:FSMContext):
    await message.answer("Вы вернулись")
    await state.clear()
    await message.answer("Hello", reply_markup=weatherbot_start())
    await state.set_state(StateMod.search)

@router.message(F.text, StateMod.weather_search)
async def weather_result_handler(message:Message, state: FSMContext):
    result = get_weather(message.text, )
    await message.answer(f"City Name {result['name']}, Timezone {result['timezone']},\n"
                            f"Weather 🌤️ {result['weather'][0]['main']}°C, {result['weather'][0]['description']}°C,\n"
                            f"Temperature 🌡️ {result['main']['temp']}, \nFeels Like {result['main']['feels_like']},\n"
                            f"Wind speed 🌬️ {result['wind']['speed']} km/h", reply_markup=weatherbot_start())
    await state.clear()
    await state.set_state(StateMod.search)
