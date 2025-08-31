from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bson import ObjectId


def change_state_of_task(idx = ObjectId, done = bool):
    keyboard = InlineKeyboardBuilder()
    if not done:
        keyboard.add(InlineKeyboardButton(text='done', callback_data=f'done:{idx}'))
    else:
        keyboard.add(InlineKeyboardButton(text='undone', callback_data=f'done:{idx}'))
    keyboard.add(InlineKeyboardButton(text='edit', callback_data = f'edit:{idx}'))
    keyboard.add(InlineKeyboardButton(text='delete', callback_data=f'delete:{idx}'))
    return keyboard.adjust(3).as_markup()
        
add_key_board = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='/add'),
    KeyboardButton(text='/list'),
    KeyboardButton(text='/help')]],
    resize_keyboard=True,
    one_time_keyboard=False)