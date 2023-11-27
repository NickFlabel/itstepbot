import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
import config
import api
import states
from aiogram.fsm.context import FSMContext
from aiogram.types import BotCommand

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@dp.message(Command("ads"))
async def command_ads_handler(message: Message) -> None:
    await message.answer("Here are your ads:")
    ads = await api.Ad.get_ads()
    try:
        for ad in ads:
            await message.answer(f"{ad['id']}: {ad['title']}")
    except (TypeError, KeyError):
        await message.answer("You don't have any ads yet")
    else:
        await message.answer("To get more info about an ad, type /ad")

@dp.message(Command("ad"))
async def command_ad_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Please enter an ad id:")
    await state.set_state(states.AdForm.ad_id)

@dp.message(states.AdForm.ad_id)
async def ad_id_handler(message: Message, state: FSMContext) -> None:
    ad_id = message.text
    ad = await api.Ad.get_ad(ad_id)
    try:
        await message.answer(f"{str(ad['id'])}: {ad['title']}\n{ad['description']}\nPrice: {ad['price']}")
    except (TypeError, KeyError):
        await message.answer("No such ad found")
    await state.clear()

@dp.message(Command("create_ad"))
async def command_create_ad_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Please enter an ad title:")
    await state.set_state(states.AdForm.title)

@dp.message(states.AdForm.title)
async def ad_title_handler(message: Message, state: FSMContext) -> None:
    title = message.text
    await message.answer("Please enter an ad description:")
    await state.update_data(title=title)
    await state.set_state(states.AdForm.description)

@dp.message(states.AdForm.description)
async def ad_description_handler(message: Message, state: FSMContext) -> None:
    description = message.text
    await message.answer("Please enter an ad price:")
    await state.update_data(description=description)
    await state.set_state(states.AdForm.price)

@dp.message(states.AdForm.price)
async def ad_price_handler(message: Message, state: FSMContext) -> None:
    if not message.text.isdigit():
        await message.answer("Please enter a valid price")
        return
    price = message.text
    await state.update_data(price=price)
    data = await state.get_data()
    await api.Ad.post_ad(data)
    await message.answer("Ad created successfully")
    await state.clear()

@dp.message(Command("update_ad"))
async def command_update_ad_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Please enter an ad id:")
    await state.set_state(states.AdUpdateForm.ad_id)

@dp.message(states.AdUpdateForm.ad_id)
async def ad_update_id_handler(message: Message, state: FSMContext) -> None:
    ad_id = message.text
    ad = await api.Ad.get_ad(ad_id)
    try:
        await message.answer(f"{ad['id']}: {ad['title']}\n{ad['description']}\nPrice: {ad['price']}")
    except (TypeError, KeyError):
        await message.answer("No such ad found")
    else:
        await message.answer("Please enter an ad title:")
        await state.update_data(ad_id=ad_id)
        await state.set_state(states.AdUpdateForm.title)

@dp.message(states.AdUpdateForm.title)
async def ad_update_title_handler(message: Message, state: FSMContext) -> None:
    title = message.text
    await message.answer("Please enter an ad description:")
    await state.update_data(title=title)
    await state.set_state(states.AdUpdateForm.description)

@dp.message(states.AdUpdateForm.description)
async def ad_update_description_handler(message: Message, state: FSMContext) -> None:
    description = message.text
    await message.answer("Please enter an ad price:")
    await state.update_data(description=description)
    await state.set_state(states.AdUpdateForm.price)

@dp.message(states.AdUpdateForm.price)
async def ad_update_price_handler(message: Message, state: FSMContext) -> None:
    if not message.text.isdigit():
        await message.answer("Please enter a valid price")
        return
    price = message.text
    await state.update_data(price=price)
    data = await state.get_data()
    await api.Ad.put_ad(data['ad_id'], data)
    await message.answer("Ad updated successfully")
    await state.clear()

@dp.message(Command("delete_ad"))
async def command_delete_ad_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Please enter an ad id:")
    await state.set_state(states.AdForm.ad_id)

@dp.message(states.AdForm.ad_id)
async def ad_delete_id_handler(message: Message, state: FSMContext) -> None:
    ad_id = message.text
    ad = await api.Ad.get_ad(ad_id)
    try:
        await message.answer(f"{ad['id']}: {ad['title']}\n{ad['description']}\nPrice: {ad['price']}")
    except (TypeError, KeyError):
        await message.answer("No such ad found")
    else:
        await api.Ad.delete_ad(ad_id)
        await message.answer("Ad deleted successfully")
    await state.clear()

@dp.message(Command("cancel"))
async def command_cancel_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Cancelled")
    await state.clear()



async def main() -> None:
    bot = Bot(config.TELEGRAM_BOT_TOKEN, parse_mode=ParseMode.HTML)
    await bot.set_my_commands([
        BotCommand(command="ads", description="List your ads"),
        BotCommand(command="ad", description="Get an ad"),
        BotCommand(command="create_ad", description="Create an ad"),
        BotCommand(command="update_ad", description="Update an ad"),
        BotCommand(command="delete_ad", description="Delete an ad"),
        BotCommand(command="cancel", description="Cancel current operation")
    ])
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())