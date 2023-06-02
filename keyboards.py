from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)


def generate_save_city_menu(city_name: str):
    markup = InlineKeyboardMarkup()
    save_city_btn = InlineKeyboardButton(
        text="Shaharni saqlab qo'yish",
        callback_data=f"save:{city_name}"
    )

    markup.row(save_city_btn)

    return markup


def generate_cities_menu(cities: tuple):
    markup = ReplyKeyboardMarkup()

    start = 0
    end = 2
    in_row = 2

    rows = len(cities) // 2
    if len(cities) % 2 != 0:
        rows += 1

    for row in range(rows):
        buttons = []
        for city_id, user_id, city_name in cities[start:end]:
            # ( (1, 1, "Toshkent"), (2, 1, "Fargona"), (), (), ... )
            buttons.append(
                KeyboardButton(text=city_name)
            )
        markup.row(*buttons)
        start = end
        end += 2

    markup.row(
        KeyboardButton(text="❌ Shaharlar ro'yxatini tozalash")
    )
    return markup
