from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from money.cryptobot import CryptoPay
from keyboards.kb_main_m import kb_main_menu, kb_get_buy_button, kb_confirm_buy, kb_go_to_main_menu
from keyboards.kb_main_m import kb_balance_menu_keyboard, kb_processing_keyboard, kb_back_to_main
from keyboards.kb_main_m import kb_cancel_but, kb_cryptopay_keyboard, kb_location_key_but, kb_back_to_products
import re
from dbss import db


router = Router()


class CryptoBotState(StatesGroup):
    CRBOT = State()


@router.callback_query(lambda c: c.data == "cancel_adding")
async def cancel_adding(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await main_menu(call)


@router.message(Command('start'))
async def cmd_start(message: types.Message):
    username = message.from_user.username
    await message.answer(f'Привет {username}! Рад тебя видеть!')
    db.db_check_and_create_user(message.from_user.id, username)
    await star(message)
    
async def star(message: types.Message):
    username = message.from_user.username
    user_id = message.from_user.id
    res = db.check_ban_user(user_id)
    if res[0] == 0:
        await message.answer(f'В магазин', reply_markup = kb_go_to_main_menu())
    else: 
        await message.answer(f'{username}, ты забанен')

@router.callback_query(lambda c: c.data == "main_menu")
async def main_menu(call: types.CallbackQuery):
    username = call.from_user.username
    user_id = call.from_user.id
    db.db_check_and_create_user(user_id, username)
    await call.message.answer(f'Привет {username}! Рад тебя видеть! Что будем делать?',
                          reply_markup = kb_main_menu())


@router.callback_query(lambda c: c.data == "get_products")
async def get_products(call: types.CallbackQuery):
    user_id = call.from_user.id
    res = db.check_ban_user(user_id)
    if res[0] == 0:
        msg = 'Наличие по районам: \n'
        
        locations = db.db_get_loc_where_product_now_count()
        for key, val in locations.items():
            loc_id = db.db_get_location_id(key[0])
            name_prod = db.db_get_products_name_where_location(loc_id[0])
            l=''
            for name in name_prod:
                l += f'{name[0]}, '
            msg += f"{key[0]} - {val[0]} шт, товары: {l}\n"
        await call.message.edit_text(text = f"{msg}", reply_markup=kb_location_key_but(locations.keys()))
        await call.message.answer(text = 'На главную', reply_markup=kb_back_to_main())
    else: 
        await call.message.answer(f'{call.from_user.username}, ты забанен')


@router.callback_query(lambda c: re.match(r'^show_prod_.*$', c.data))
async def show_prod_on_location(call: types.CallbackQuery):
    res = db.check_ban_user(call.from_user.id)
    if res[0] == 0:
        loc = call.data.split('_')[2]
        loc_id = db.db_get_location_id(loc)
        print(loc_id)
        products = db.db_get_products_where_location(loc_id[0])
        for p in products: 
            await call.message.answer(f'==========\nНазвание: {p[1]}\nВес: {p[2]}\nЛокация: {loc}\
                                 \nЦена: {p[4]}', reply_markup=kb_get_buy_button(p))
        await call.message.answer('Вернуться', reply_markup=kb_back_to_products())
    else: 
        await call.message.answer(f'{call.from_user.username}, ты забанен')
        

@router.callback_query(lambda c: re.match(r'^buy_prod_\d+$', c.data))
async def buy_product(call: types.CallbackQuery):
    res = db.check_ban_user(call.from_user.id)
    if res[0] == 0:
        id = call.data.split('_')[2]
        i = db.db_get_product_info(id)
        loc = db.db_get_location_name(i[0][3])
        await call.message.answer(f'Покупаете:{i[0][1]}\nВес: {i[0][2]} гр. \nЛокация: {loc}\
                               \nЦена {i[0][4]} usdt\nУверены?', reply_markup=kb_confirm_buy(id))
    else:
        await call.message.answer(f'{call.from_user.username}, ты забанен')
    


@router.callback_query(lambda c: re.match(r'^processing_pay_\d+$', c.data))
async def processing_pay(call: types.CallbackQuery):
    id = call.data.split('_')[2]
    buyer = call.from_user.id
    buyer_bal = db.db_get_user_balance(buyer)
    prod_price = db.db_get_product_price(id)
    res = db.check_ban_user(call.from_user.id)
    if res[0] == 0:
        if buyer_bal[0] >= prod_price[0]:
            new_buyer_bal = buyer_bal[0] - prod_price[0]
            db.db_update_user_bal(buyer, new_buyer_bal)
            p = db.db_get_product_info(id)
            await call.message.answer(f'Название:{p[0][1]} Вес:{p[0][2]} Локация:{p[0][3]} Цена:{p[0][4]}')
            await call.message.answer_photo(types.FSInputFile(p[0][5]))
            await call.message.answer_photo(types.FSInputFile(p[0][6]))
            await call.message.answer("Щастливого пути /start")
            db.db_set_bought_for_prod(id)
            db.db_add_purchase(buyer, id)
        else:
            await call.message.answer("У тебя недостаточно денег на баласе",
                                   reply_markup=kb_processing_keyboard())
    else:
        await call.message.answer(f'{call.from_user.username}, ты забанен')

        

@router.callback_query(lambda c: c.data == 'balance')
async def balance_menu(call: types.CallbackQuery):
    buyer_id = call.from_user.id
    bal = db.db_get_user_balance(buyer_id)
    res = db.check_ban_user(buyer_id)
    if res[0] == 0:
        await call.message.edit_text(f'Ваш баланс: {bal[0]} Кнопка "Пополнить" добавляет \
                              100 к балансу для тестов, криптобот разработан но не протестирован',
                              reply_markup=kb_balance_menu_keyboard())
    else:
        await call.message.answer(f'{call.from_user.username}, ты забанен')
    

@router.callback_query(lambda c: c.data == 'add_money')
async def add_money(call: types.CallbackQuery):
    buyer_id = call.from_user.id
    buyer_bal = db.db_get_user_balance(buyer_id)
    new_buyer_bal = buyer_bal[0] + 100
    db.db_update_user_bal(buyer_id, new_buyer_bal)
    updated_bal = db.db_get_user_balance(buyer_id)
    await call.message.answer(f'Ваш новый баланс: {updated_bal[0]}')


@router.callback_query(lambda c: c.data == 'crypto_bot')
async def crypto_bot(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(CryptoBotState.CRBOT)
    await call.message.edit_text('Введите сумму в USDT на которую хотите пополнить баланс',
                               reply_markup=kb_cancel_but())
    
@router.message(CryptoBotState.CRBOT, F.text)
async def processing_crypto_bot(message: types.Message, state: FSMContext):
    summ = message.text
    if not summ.isdigit():
        await message.answer("Вы ввели не число, введите число:", reply_markup=kb_cancel_but())
        return
    crypto = CryptoPay()
    await crypto.initialize()
    try:
        invoice = await crypto.get_invoice(sum=summ)
        invoice_url = invoice.pay_url
        invoice_id = invoice.invoice_id
    finally:
        await crypto.cleanup()
    await message.answer(f'После оплаты нажмите кнопку оплачено!\
                          \nВаша ссылка на оплату: {invoice_url}', 
                          reply_markup=kb_cryptopay_keyboard(invoice_id, summ))
    await state.clear()


@router.callback_query(lambda c: re.match(r'paid_(\d+)_(\d+)\Z', c.data))
async def checking_crbot_pay(call: types.CallbackQuery):
    invoice_id = call.data.split('_')[1]
    sum_usr_input = call.data.split('_')[2]
    user_id = call.from_user.id
    crypto = CryptoPay()
    await crypto.initialize()
    try:
        info = await crypto.get_invoice_data(id=invoice_id)
    finally:
        await crypto.cleanup()
    for inv in info:
        if inv.status == 'paid' and inv.invoice_id == f'{int(id)}' \
            and inv.asset == 'USDT' and inv.amount == f'{int(sum_usr_input)}':
            user_bal = db.db_get_user_balance(user_id)
            new_user_bal = int(user_bal) + int(inv.amount)
            db.db_update_user_bal(user_id, new_user_bal)
            upd_bal = db.db_get_user_balance(user_id)
            await call.message.answer(f'Вы оплатили сумму: {inv.amount} \
                                      в валюте {inv.asset}\nВаш баланс теперь: {upd_bal[0]}',
                                      reply_markup=kb_go_to_main_menu())
        else:
            await call.message.answer("Что-то пошло не так, инфвойс не оплачен, \
                                      попробуйте еще и нажмите оплачено",
                                      reply_markup=kb_cryptopay_keyboard(invoice_id, sum_usr_input))
            return


@router.callback_query(lambda c: c.data == 'profile')
async def profile(call: types.CallbackQuery):
    res = db.check_ban_user(call.from_user.id)
    if res[0] == 0:
        msg = 'История покупок:\n'
        user_id = call.from_user.id
        usr_inf = db.db_get_user_info(user_id)
        user_purchase = db.db_get_user_purchase(user_id)
        for i in user_purchase:
            prod = db.db_get_product_info(i[1])
            msg += f'==========\nID: {prod[0][0]}\
            \nНазвание: {prod[0][1]}\nВес: {prod[0][2]}\
                                 \nЦена: {prod[0][4]}\nКуплено: {i[2]}\n'

        await call.message.answer(f"Ваше имя: {usr_inf[1]}\nВаш баланс: {usr_inf[2]}\
                              \nДата регистрации: {usr_inf[-1]} \n{msg}", reply_markup=kb_back_to_main())
    else:
        await call.message.answer(f'{call.from_user.username}, ты забанен')


    