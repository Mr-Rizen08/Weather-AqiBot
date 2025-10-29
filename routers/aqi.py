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


@router.message(F.text, StateMod.aqi_search)
async def air_polution_handler(message:Message, state: FSMContext):
    result = get_weather(message.text)
    print(result['coord']['lon'], result['coord']['lat'])
    aqi_result = get_aqi(result['coord']['lon'], result['coord']['lat'])
    await message.answer(f"Качество воздуха 💨 {aqi_result['list'][0]['main']['aqi']},\n"
                         f"Угарный газ Co [ {aqi_result['list'][0]['components']['co']} mg/m³],\n"
                         f"Мелкие частицы Pm2.5 [ {aqi_result['list'][0]['components']['pm2_5']} µg/m³],\n"
                         f"Крупные частицы Pm10 [ {aqi_result['list'][0]['components']['pm10']} µg/m³],\n"
                         f"Диоксид серы SO₂ [{aqi_result['list'][0]['components']['so2']} µg/m³],\n"
                         f"Аммиак NH₃ [{aqi_result['list'][0]['components']['nh3']} µg/m³],\n"
                         f"Озон O₃ [ {aqi_result['list'][0]['components']['o3']} µg/m³]", reply_markup=end_task_kb())
    await state.set_state(StateMod.end)

@router.message(F.text == "End->", StateMod.end)
async def end_task_handler(message:Message, state: FSMContext):
    await state.clear()
    await message.answer("Вы вернулись", reply_markup=weatherbot_start())
    await state.set_state(StateMod.search)