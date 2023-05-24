from aiogram import types

def kb_get_main_menu():
    keys = [
        [types.InlineKeyboardButton(text="Магазин", callback_data="get_products")],
    ]
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb

def kb_get_main_products_menu():
    keys = [
        [types.InlineKeyboardButton(text='Список товаров полный', callback_data="prod_list")],
        [types.InlineKeyboardButton(text='список товаров простой', callback_data="product_list_lite")],
        [types.InlineKeyboardButton(text='Добавить товар', callback_data="add_prod")],
        [types.InlineKeyboardButton(text='Локации', callback_data='locations')],
        [types.InlineKeyboardButton(text='Добавить локацию', callback_data='add_location')],
        [types.InlineKeyboardButton(text='Денежки', callback_data='balance')],
        [types.InlineKeyboardButton(text='История покупок', callback_data='history')],
        [types.InlineKeyboardButton(text='Пользователи', callback_data='users')],
         ]  
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb

def kb_delete_button(i):
    keys = [
        [types.InlineKeyboardButton(text='Удалить', callback_data=f"del_prod_{i}")],
    ]
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb

def kb_go_to_start():
    keys = [
        [types.InlineKeyboardButton(text='Hа главную', callback_data="star")],
    ]
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb

def kb_go_to_products():
    keys = [
        [types.InlineKeyboardButton(text='Hа главную', callback_data="get_products")],
    ]
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb

def kb_cancel_but():
    keys = [
        [types.InlineKeyboardButton(text='Отмена', callback_data="cancel_adding")],
    ]
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb

def kb_get_add_location_button():
    keys = [
        [types.InlineKeyboardButton(text='Добавить локацию', callback_data='add_location')],
         ]  
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb


def kb_ban_button(user_id):
    keys = [
        [types.InlineKeyboardButton(text='Забанить', callback_data=f'ban_{user_id}')],
    ]
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb

def kb_unban_button(user_id):
    keys = [
        [types.InlineKeyboardButton(text='Разбанить', callback_data=f'unban_{user_id}')],
    ]
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb


def kb_location_del(loc_list):
    keys = []
    for loc in loc_list:
        keys.append([types.InlineKeyboardButton(text=f'Удалить {loc[1]}', callback_data=f'del_loc_{loc[0]}')])
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb