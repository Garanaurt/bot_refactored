from aiogram import types

def kb_main_menu():
    keys = [
        [types.InlineKeyboardButton(text="Витрина", callback_data="get_products")],
        [types.InlineKeyboardButton(text="Пополнить баланс", callback_data="balance")],
        [types.InlineKeyboardButton(text="Профиль", callback_data="profile")],
        [types.InlineKeyboardButton(text="Написать админу", callback_data='@bo1124')],
         ]  
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb

def kb_get_buy_button(product):
    keys = [
        [types.InlineKeyboardButton(text='Купить этот товар', callback_data=f"buy_prod_{product[0]}")]
    ]
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb

def kb_confirm_buy(product):
    keys = [
        [types.InlineKeyboardButton(text='Покупаем', callback_data=f"processing_pay_{product[0]}")]
    ]
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb

def kb_processing_keyboard():
    keys = [
        [types.InlineKeyboardButton('Пополнить баланс', callback_data='balance')],
        [types.InlineKeyboardButton('На главную', callback_data='main_menu')]
    ]
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb

def kb_go_to_main_menu():
    keys = [
        [types.InlineKeyboardButton(text="В магазин", callback_data="main_menu")],
         ]  
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb

def kb_back_to_main():
    keys = [
        [types.InlineKeyboardButton(text="На главную", callback_data="main_menu")],
         ]  
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb

def kb_balance_menu_keyboard():
    keys = [
        [types.InlineKeyboardButton(text='CryptoBot', callback_data='crypto_bot')],
        [types.InlineKeyboardButton(text='Пополнить', callback_data='add_money')],
        [types.InlineKeyboardButton(text="На главную", callback_data="main_menu")]
     ]
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb


def kb_cancel_but():
    keys = [
        [types.InlineKeyboardButton(text='Отмена', callback_data="cancel_adding")],
    ]
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb


def kb_cryptopay_keyboard(inv_id, inv_sum):
    keys = [
        [types.InlineKeyboardButton(text='Оплачено', callback_data=f'paid_{inv_id}_{inv_sum}')],
        [types.InlineKeyboardButton(text='Отмена', callback_data="cancel_adding")]
    ]
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb
