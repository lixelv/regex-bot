from aiogram.fsm.state import State, StatesGroup


class Exec(StatesGroup):
    command = State()
    text = State()
    pattern = State()


class ChangeLang(StatesGroup):
    lang = State()


class AddFlag(StatesGroup):
    flag = State()
    pattern = State()


class DeletePattern(StatesGroup):
    pattern = State()


class AddPattern(StatesGroup):
    pattern = State()
