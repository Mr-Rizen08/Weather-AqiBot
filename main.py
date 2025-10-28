from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
import asyncio
from state import StateMod
from aiogram.fsm.context import FSMContext
from weaterinfo import get_weather, get_aqi
from keyboard import weatherbot_start

bot = Bot("")
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await message.answer("Hello", reply_markup=weatherbot_start())
    await  state.set_state(StateMod.state1)


@dp.message(F.text == "WeatherSearch", StateMod.state1)
async def weather_city_handler(message:Message, state: FSMContext):
    await message.answer("Напиши город", reply_markup=ReplyKeyboardRemove())
    await state.set_state(StateMod.search)


@dp.message(F.text, StateMod.search)
async def weather_result_handler(message:Message):
    result = get_weather(message.text)
    await message.answer(f"City Name {result['name']}, Timezone {result['timezone']}\n"
                        f"Weather 🌤️ {result['weather'][0]['main']}, {result['weather'][0]['description']}\n"
                        f"Temperature 🌡️ {result['main']['temp']}, Feels Like {result['main']['feels_like']}\n"
                        f"Visibility {result['visibility']}\n"
                        f"Wind speed 🌬️ {result['wind']['speed']}")



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
