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
async def air_polution_handler(message:Message):
    result = get_weather(message.text)
    print(result['coord']['lon'], result['coord']['lat'])
    result = get_aqi(result['coord']['lon'], result['coord']['lat'])
    await message.answer(f" Угарный газ Co [ {result['list'][0]['components']['co']} ]\n"
                         f" Мелкие частицы Pm2.5 [ {result['list'][0]['components']['pm2_5']} ]\n"
                         f" Крупные частицы Pm10 [ {result['list'][0]['components']['pm10']} ]\n"
                         f" Озон O3 [ {result['list'][0]['components']['o3']} ]", reply_markup=end_task_kb())

@router.message(F.text == "End->", StateMod.aqi_search)
async def end_task_handler(message:Message, state: FSMContext):
    await message.answer("Вы вернулись")
    await state.clear()
    await message.answer("Hello", reply_markup=weatherbot_start())
    await state.set_state(StateMod.search)