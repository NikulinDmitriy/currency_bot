import os
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from api import API
from forms import Form

bot = Bot(token=os.getenv('TOKEN'))

dp = Dispatcher()


@dp.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    await message.answer("Hello, i can convert any currency in rub. Send me the currency abbreviation you need to "
                         "convert.")
    await state.set_state(Form.first_currency)


@dp.message(F.text and Form.first_currency)
async def get_first_currency(message: Message, state: FSMContext):
    if message.text.upper() in await API.check_supported_currencies():
        await state.update_data(first_currency=message.text)
        await message.answer('OK, now send me the currency you need to convert into.')
        await state.set_state(Form.second_currency)
    else:
        await message.answer('You sent me not the currency abbreviation or this currency is not supported')


@dp.message(F.text and Form.second_currency)
async def get_second_accurency(message: Message, state: FSMContext):
    if message.text.upper() in await API.check_supported_currencies():
        await state.update_data(second_currency=message.text)
        await message.answer('So send me the quantity of currency')
        await state.set_state(Form.quantity)
    else:
        await message.answer('You sent me not the currency abbreviation or this currency is not supported')


@dp.message(F.text and Form.quantity)
async def get_quanity(message: Message, state: FSMContext):
    try:
        if int(message.text):
            await state.update_data(quantity=int(message.text))
            data = await state.get_data()
            res = await API.convert_currency(
                cur1=data.get('first_currency'),
                cur2=data.get('second_currency'),
                quantity=data.get('quantity')
            )
            res = str(res)
            await message.answer(
                f'{str(data.get("quantity"))} {data.get("first_currency")} in {data.get("second_currency")} = {res}')
            await state.set_state(Form.default)
    except ValueError:
        await message.answer('This is not number')


@dp.message(Form.default)
async def default_mode(message: Message, state: FSMContext):
    if message.text.upper() in await API.check_supported_currencies():
        await state.update_data(first_currency=message.text)
        await message.answer('OK, now send me the currency you need to convert into.')
        await state.set_state(Form.second_currency)
    else:
        await message.answer('If you wanna start, send me the currency abbreviation you need to convert.')
        await state.set_state(Form.first_currency)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
