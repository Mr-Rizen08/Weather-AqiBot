from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from keyboard import weatherbot_start
from aiogram.fsm.context import FSMContext
from state import StateMod

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await message.answer("Hello", reply_markup=weatherbot_start())
    await state.set_state(StateMod.search)

