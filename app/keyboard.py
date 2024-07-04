from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.config import re_flags


def create_inline_keyboard(button_tuples, prefix, width=3):
    builder = InlineKeyboardBuilder()

    for button, callback_data in button_tuples:
        builder.button(text=str(button), callback_data=f"{prefix}:{callback_data}")

    builder.row()
    builder.button(text="X", callback_data="exit:")

    return builder.adjust(width).as_markup()


command_keyboard = create_inline_keyboard(
    [
        ("find", "find"),
        ("findall", "findall"),
    ],
    prefix="command",
)

language_keyboard = create_inline_keyboard(
    [("🇷🇺", "ru"), ("🇬🇧", "en"), ("🇯🇵", "ja")], prefix="lang"
)

flag_keyboard = create_inline_keyboard(
    [(flag, flag) for flag in re_flags.keys()], prefix="flag"
)
