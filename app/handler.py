from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.database import RegexDB
from app.state import Exec, AddPattern, DeletePattern, AddFlag, ChangeLang
from app.keyboard import (
    create_inline_keyboard,
    command_keyboard,
    flag_keyboard,
    language_keyboard,
)
from app.util import regex_compile
from app.config import Lexicon, re_flags


db = RegexDB("main.db")
lexer = Lexicon()
router = Router()


@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    lang = await db.get_lang(message.from_user.id)
    await message.answer(lexer.get("start", lang))


@router.message(Command("help"))
async def help(message: Message, state: FSMContext):
    lang = await db.get_lang(message.from_user.id)
    await message.answer(lexer.get("help", lang))


@router.message(Command("lang"))
async def change_lang(message: Message, state: FSMContext):
    lang = await db.get_lang(message.from_user.id)
    await message.answer(lexer.get("lang", lang), reply_markup=language_keyboard)

    await state.set_state(ChangeLang.lang)


@router.callback_query(ChangeLang.lang, F.data.startswith("lang:"))
async def change_lang_2(callback: CallbackQuery, state: FSMContext):
    lang = callback.data.split(":")[1]
    await db.change_lang(callback.from_user.id, lang)

    await callback.message.edit_text(lexer.get("lang_changed", lang))
    await state.clear()


@router.message(Command("add_pattern"))
async def add_pattern(message: Message, state: FSMContext):
    lang = await db.get_lang(message.from_user.id)

    await state.set_state(AddPattern.pattern)

    await message.answer(lexer.get("add_pattern", lang))


@router.message(AddPattern.pattern)
async def add_pattern_2(message: Message, state: FSMContext):
    pattern = message.text
    lang = await db.get_lang(message.from_user.id)

    await db.add_pattern(pattern, message.from_user.id)
    await message.answer(lexer.get("added", lang))

    await state.clear()


@router.message(Command("delete_pattern"))
async def delete_pattern(message: Message, state: FSMContext):
    lang = await db.get_lang(message.from_user.id)
    payload = await db.get_patterns(message.from_user.id)

    await state.set_state(DeletePattern.pattern)

    if payload:
        await message.answer(
            lexer.get("pattern", lang),
            reply_markup=create_inline_keyboard(payload, prefix="delete"),
        )
    else:
        await message.answer(lexer.get("no_pattern", lang))
        await state.clear()


@router.callback_query(DeletePattern.pattern, F.data.startswith("delete:"))
async def delete_pattern_2(callback: CallbackQuery, state: FSMContext):
    pattern_id = int(callback.data.split(":")[1])
    lang = await db.get_lang(callback.from_user.id)

    await db.delete_pattern(pattern_id)
    await callback.message.edit_text(lexer.get("deleted", lang))

    await state.clear()


@router.message(Command("add_flag"))
async def add_flag(message: Message, state: FSMContext):
    lang = await db.get_lang(message.from_user.id)

    await state.set_state(AddFlag.flag)
    await message.answer(lexer.get("add_flag", lang), reply_markup=flag_keyboard)


@router.callback_query(AddFlag.flag, F.data.startswith("flag:"))
async def add_flag_2(callback: CallbackQuery, state: FSMContext):
    flag = callback.data.split(":")[1]
    lang = await db.get_lang(callback.from_user.id)
    payload = await db.get_patterns(callback.from_user.id)

    if payload:
        await state.update_data({"flag": flag})
        await state.set_state(AddFlag.pattern)
        await callback.message.edit_text(
            lexer.get("pattern", lang),
            reply_markup=create_inline_keyboard(payload, "pattern"),
        )
    else:
        await callback.message.edit_text(lexer.get("no_pattern", lang))
        await state.clear()


@router.callback_query(AddFlag.pattern, F.data.startswith("pattern:"))
async def add_flag_3(callback: CallbackQuery, state: FSMContext):
    pattern_id = int(callback.data.split(":")[1])
    flag = (await state.get_data())["flag"]
    lang = await db.get_lang(callback.from_user.id)

    await db.add_flag(pattern_id, flag)
    await callback.message.edit_text(lexer.get("flag_added", lang))

    await state.clear()


@router.message(Command("pattern_list"))
async def list_patterns(message: Message, state: FSMContext):
    lang = await db.get_lang(message.from_user.id)
    payload = await db.get_patterns(message.from_user.id)

    if payload:
        await message.answer(
            lexer.get("list", lang),
            reply_markup=create_inline_keyboard(payload, prefix="none"),
        )
    else:
        await message.answer(lexer.get("no_pattern", lang))


@router.message(Command("parse"))
async def execute_regex_1(message: Message, state: FSMContext):
    await state.set_state(Exec.command)

    lang = await db.get_lang(message.from_user.id)
    await message.answer(lexer.get("exec", lang), reply_markup=command_keyboard)


@router.callback_query(Exec.command, F.data.startswith("command:"))
async def execute_regex_2(callback: CallbackQuery, state: FSMContext):
    command = callback.data.split(":")[1]
    lang = await db.get_lang(callback.from_user.id)

    await state.update_data({"command": command})
    await state.set_state(Exec.text)

    await callback.message.edit_text(lexer.get("text", lang), reply_markup=None)


@router.message(Exec.text)
async def execute_regex_3(message: Message, state: FSMContext):
    text = message.text
    lang = await db.get_lang(message.from_user.id)
    payload = await db.get_patterns(message.from_user.id)

    await state.update_data({"text": text})
    await state.set_state(Exec.pattern)

    if payload:
        await message.answer(
            lexer.get("pattern", lang),
            reply_markup=create_inline_keyboard(payload, "pattern"),
        )
    else:
        await message.answer(lexer.get("no_pattern", lang))
        await state.clear()


@router.callback_query(Exec.pattern, F.data.startswith("pattern:"))
async def execute_regex_4(callback: CallbackQuery, state: FSMContext):
    pattern_id = int(callback.data.split(":")[1])
    lang = await db.get_lang(callback.from_user.id)
    flag = await db.get_flag(int(pattern_id))

    await state.update_data({"pattern_id": pattern_id})

    data = await state.get_data()

    try:
        result = regex_compile(
            data["command"],
            data["text"],
            await db.get_pattern(int(data["pattern_id"])),
            re_flags[flag],
        )
    except Exception as e:
        await callback.message.edit_text(lexer["error", lang] + str(e))
        return

    if result:
        await callback.message.edit_text(
            lexer.get("result", lang) + result,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=None,
        )
    else:
        await callback.message.edit_text(
            lexer.get("not_found", lang), reply_markup=None
        )
    await state.clear()


@router.callback_query(F.data.startswith("exit:"))
async def exit(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()


@router.message()
async def unknown(message: Message):
    lang = await db.get_lang(message.from_user.id)
    await message.answer(lexer.get("unknown", lang))
