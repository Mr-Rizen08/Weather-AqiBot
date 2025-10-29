from aiogram import Bot, Dispatcher
from routers.start import router as start
from routers.weather import router as weather
from routers.aqi import router as aqi
from routers.full import router as full
import asyncio

bot = Bot("Your_Token")
dp = Dispatcher()

async def main():
    dp.include_router(start)
    dp.include_router(weather)
    dp.include_router(aqi)
    dp.include_router(full)
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())