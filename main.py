import os
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from forms import Form

bot = Bot(token=os.getenv('TOKEN'))

dp = Dispatcher()

@dp.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    await message.answer("Hello, i can convert any currency in rub. Send me the currency abbreviation you need to convert.")
    await state.set_state(Form.first_currency)



async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())