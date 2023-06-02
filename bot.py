from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove

from weather_parser import get_weather_info
from keyboards import generate_save_city_menu, generate_cities_menu
from database import db

from environs import Env

env = Env()
env.read_env()

TOKEN = env.str('BOT_TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands='start')
async def start(message: Message):
    full_name = message.from_user.full_name
    telegram_id = message.from_user.id

    try:
        db.register_user(
            telegram_id=telegram_id,
            fullname=full_name
        )
        await message.answer(text=f"Assalomu alaykum, {full_name} 👋\n"
                                  f"Siz muvaffaqiyatli ro'yxatga olindingiz")
    except:
        await message.answer(text=f"Assalomu alaykum, {full_name} 👋\n"
                                  f"Sizni yana ko'rib turganimizda xursandmiz 😊")


@dp.message_handler(commands='help')
async def get_help(message: Message):
    text = "/start - Botni ishga tushirish\n/help - Yordam olish"
    await message.answer(text=text)


@dp.message_handler(Text(equals="❌ Shaharlar ro'yxatini tozalash"))
async def clear_cities_list(message: Message):
    telegram_id = message.from_user.id
    user_id = db.get_user(telegram_id=telegram_id)[0]
    db.clear_cities_list(user_id=user_id)
    await message.answer(
        text="Shaharlar ro'yxati tozalandi ✅",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message_handler()
async def echo(message: Message):
    weather_info = get_weather_info(city_name=message.text)

    if weather_info is not None:
        await message.answer(
            text=weather_info,
            reply_markup=generate_save_city_menu(city_name=message.text)
        )
    else:
        await message.answer(text="Shahar topilmadi!")


async def update_reply_markup(call: CallbackQuery):
    telegram_id = call.from_user.id
    user_id = db.get_user(telegram_id=telegram_id)[0]  # (1, 717171, "...")
    cities = db.get_cities(user_id=user_id)
    await call.message.answer(
        text="Shahar qo'shildi!",
        reply_markup=generate_cities_menu(cities=cities)
    )


@dp.callback_query_handler()
async def save_city(call: CallbackQuery):
    city_name = call.data.split(":")[-1]  # "save:toshkent" --> ["save", "toshkent"]
    telegram_id = call.from_user.id  # 71712312313

    user_id = db.get_user(telegram_id=telegram_id)[0]  # (4, 710661311, "...")
    try:
        db.register_city(user_id=user_id, city_name=city_name.capitalize())

        await update_reply_markup(call=call)

        await call.answer(
            text=f"{city_name.capitalize()} shahri muvaffaqiyatli saqlandi",
            show_alert=True
        )
    except:
        await call.answer(
            text=f"{city_name.capitalize()} shahri allaqachon ro'yxatga olingan",
            show_alert=True
        )

    await bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=None
    )


executor.start_polling(dispatcher=dp, skip_updates=True)
