from aiogram import Router, F
from aiogram.types import Message
from state import StateMod
from aiogram.fsm.context import FSMContext
from weaterinfo import get_aqi, get_weather
from keyboard import back_kb, weatherbot_start, end_task_kb


router = Router()

@router.message(F.text == "AirPolution" , StateMod.search)
async def aqi_city_handler(message:Message, state: FSMContext):
    await message.answer("Напиши город", reply_markup=back_kb())
    await state.set_state(StateMod.aqi_search)

@router.message(F.text == "Back->", StateMod.aqi_search)
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

@router.message(F.text, StateMod.aqi_search)
async def air_polution_handler(message:Message, state: FSMContext):
    result = get_weather(message.text)
    aqi_result = get_aqi(result['coord']['lon'], result['coord']['lat'])
    aqi_value = aqi_result['list'][0]['main']['aqi']
    aqi_text = aqi_rating(aqi_value)
    await message.answer(f"Качество воздуха {aqi_result['list'][0]['main']['aqi']} ({aqi_text}) \n"
                         f"Угарный газ Co [ {aqi_result['list'][0]['components']['co']} mg/m³],\n"
                         f"Мелкие частицы Pm2.5 [ {aqi_result['list'][0]['components']['pm2_5']} µg/m³],\n"
                         f"Крупные частицы Pm10 [ {aqi_result['list'][0]['components']['pm10']} µg/m³],\n"
                         f"Диоксид серы SO₂ [{aqi_result['list'][0]['components']['so2']} µg/m³],\n"
                         f"Аммиак NH₃ [{aqi_result['list'][0]['components']['nh3']} µg/m³],\n"
                         f"Озон O₃ [ {aqi_result['list'][0]['components']['o3']} µg/m³]", reply_markup=weatherbot_start())
    await state.clear()
    await state.set_state(StateMod.search)
