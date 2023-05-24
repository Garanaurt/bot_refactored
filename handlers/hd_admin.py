from aiogram import Router, Bot
from aiogram import types
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup
from keyboards.kb_admin_m import kb_get_add_location_button, kb_get_main_menu, kb_get_main_products_menu 
from keyboards.kb_admin_m import kb_delete_button, kb_go_to_products, kb_cancel_but, kb_ban_button
from keyboards.kb_admin_m import kb_unban_button, kb_go_to_start, kb_location_del
from user_data import ADMIN_LIST
from dbss import db
from aiogram.fsm.context import FSMContext
from aiogram import F
from money.cryptobot import CryptoPay
import re
import uuid

router = Router()

class AddLocationStates(StatesGroup):
    LOCA = State()

class AddProductStates(StatesGroup):
    NAME = State()
    WEIGHT = State()
    LOCATION = State()
    PRICE = State()
    IMAGE1 = State()
    IMAGE2 = State()


def yes_no(i):
    if i == 1:
        return "Да"
    else:
        return "Нет"

@router.callback_query(lambda c: c.data == "cancel_adding")
async def cancel_adding(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await get_products(call)


@router.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer('Наш прекрасный магазин рад приветствовать тебя')
    await cmd_star(message)

#hi menu, check admin
@router.callback_query(F.data == "star")
async def cmd_star(call: types.CallbackQuery):
    admin_id = call.from_user.id
    admin_username = call.from_user.username
    if not str(admin_id) in ADMIN_LIST:
        await call.answer(f'У вас нет сюда доступа! Напишите владельцу! Ваш айди: {admin_id}')
    else:
        await call.answer(f'Привет {admin_username}!', reply_markup=kb_get_main_menu())

#menu
@router.callback_query(lambda c: c.data == "get_products")
async def get_products(call: types.CallbackQuery):
    await call.message.answer(f'Что будем делать?\n*При добавлении товаров добавьте сначала локации',
                               reply_markup=kb_get_main_products_menu())


#info about products lite
@router.callback_query(lambda c: c.data == "product_list_lite")
async def get_lite_list(call: types.CallbackQuery):
    msg = ''
    count = db.db_get_count_productions()
    distr = db.db_get_loc_where_product_now_count()
    for key, val in distr.items():
        msg += f'{key[0]} - {val[0]} шт\n'
    await call.message.edit_text(f"Всего записей: {count[0]} \nРайоны: \n{msg}", reply_markup=kb_go_to_products())


#info about product
@router.callback_query(lambda c: c.data == "prod_list")
async def product_list(call: types.CallbackQuery):
    res = db.db_get_all_products()
    for i in res:
        loc = db.db_get_location_name(i[0])
        await call.message.answer(f'-----start-----\nID: {i[0]}\nНазвание: {i[1]} \
                                  \nВес: {i[2]}\nЛокация: {loc[0]}\nЦена: {i[4]} \
                                  \nДата добавления: {i[-1]}')
        await call.message.answer_photo(types.FSInputFile(i[5]))
        await call.message.answer_photo(types.FSInputFile(i[6]))
        await call.message.answer('Удалить из базы:', reply_markup=kb_delete_button(i[0]))
    await call.message.answer('Вернуться', reply_markup=kb_go_to_products())


#delete product
@router.callback_query(lambda c: re.match(r'^del_prod_\d+$', c.data))
async def del_product(call: types.CallbackQuery):
    i = call.data.split('_')[2]
    result = db.db_delete_product(i)
    if result == True:
        await call.answer(f"Запись успешно удалена")
        await product_list(call=call)



@router.callback_query(F.data == 'locations')
async def locations_list(call: types.CallbackQuery):
    locations = db.db_get_full_list_location()
    msg = ''
    for l in locations:
        msg += f'{l[1]}, '
    await call.message.answer(f"Добавленные локации: {msg}", reply_markup=kb_location_del(locations))
    await call.message.answer('Вернуться', reply_markup=kb_go_to_products())


@router.callback_query(lambda c: re.match(r'^del_loc_\d+$', c.data))
async def buy_product(call: types.CallbackQuery):
    id = call.data.split('_')[2]
    prod_in_loc = db.db_get_all_products_where_location(id)
    if prod_in_loc:
        await call.message.answer("В этой локации есть товары, удаление невозможно")
    else:
        db.db_delete_location(id)
        await call.answer("Удалено")
        await locations_list(call)
    await call.message.answer('Вернуться', reply_markup=kb_go_to_products())



#Adding location
@router.callback_query(lambda c: c.data == "add_location")
async def add_location(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(AddLocationStates.LOCA)
    msg = ''
    locations = db.db_get_full_list_location()
    for l in locations:
        msg += f'{l[1]}, '
    await call.message.answer(f"Уже добавленные: {msg} \nВведите название локации:", reply_markup=kb_cancel_but())


@router.message(AddLocationStates.LOCA, F.text)
async def process_add_location(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    location = await state.get_data()
    result = db.db_add_location(location['name'])
    if result == True:
        await message.answer(f"Локация {location['name']} успешно добавлена", reply_markup=kb_get_main_products_menu())
        await state.clear()
    else:
        await message.answer('Такая локация уже есть введите еще раз:', reply_markup=kb_cancel_but())
        return



#adding product
@router.callback_query(lambda c: c.data == "add_prod")
async def add_product(message: types.Message, state: FSMContext):
    await state.set_state(AddProductStates.NAME)
    await message.message.answer("Введите название товара:", reply_markup=kb_cancel_but())

@router.message(AddProductStates.NAME, F.text)
async def process_weight(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddProductStates.WEIGHT)
    await message.answer("Введите вес товара:", reply_markup=kb_cancel_but())

@router.message(AddProductStates.WEIGHT, F.text)
async def process_weight(message: types.Message, state: FSMContext):
    weight = message.text
    mess = ''
    if not weight.isdigit():
        await message.answer("Введите вес товара числом. Пожалуйста, попробуйте еще раз:", reply_markup=kb_cancel_but())
        return
    await state.update_data(weight=int(weight))
    await state.set_state(AddProductStates.LOCATION)
    locations = db.db_get_full_list_location()
    for i in locations:
        mess += f'{i[0]} - {i[1]}\n'
    await message.answer(f'Список названий локаций и их айди:\n{mess} Укажите айди!', reply_markup=kb_get_add_location_button())

@router.message(AddProductStates.LOCATION, F.text)
async def process_weight(message: types.Message, state: FSMContext):
    check = []
    location_id = message.text
    locations = db.db_location_ids_list()
    for loc in locations:
        check.append(loc[0])
    try:
        int(location_id)
    except ValueError:
        await message.answer('Укажите существующий айди!', reply_markup=kb_cancel_but())
        return
    if int(location_id) not in check or not location_id.isdigit():
        await message.answer('Укажите существующий айди!', reply_markup=kb_cancel_but())
        return
    await state.update_data(location_id=message.text)
    await state.set_state(AddProductStates.PRICE)
    await message.answer("Введите цену товара:", reply_markup=kb_cancel_but())

@router.message(AddProductStates.PRICE, F.text)
async def process_weight(message: types.Message, state: FSMContext):
    price = message.text
    if not price.isdigit() or int(price) <= 0:
        await message.answer("Цена должна быть числом больше 0, попробуйте еще раз:", reply_markup=kb_cancel_but())
        return
    await state.update_data(price=message.text)
    await state.set_state(AddProductStates.IMAGE1)
    await message.answer("Добавьте одну картинку:", reply_markup=kb_cancel_but())

@router.message(AddProductStates.IMAGE1)
async def process_image(message: types.Message, state: FSMContext, bot: Bot):
    photo = message.photo[-1].file_id
    file_path = f"images/{uuid.uuid4()}.jpg"
    await bot.download(photo, destination=file_path)
    await state.update_data(image_path1=file_path)
    await state.set_state(AddProductStates.IMAGE2)
    await message.answer("Добавь вторую картинку", reply_markup=kb_cancel_but())

@router.message(AddProductStates.IMAGE2)
async def process_image(message: types.Message, state: FSMContext, bot: Bot):
    photo = message.photo[-1].file_id
    file_path = f"images/{uuid.uuid4()}.jpg" 
    await bot.download(photo, destination=file_path)
    await state.update_data(image_path2=file_path)
    print('data')
    product_data = await state.get_data()
    print(product_data)
    res = db.db_add_product_to_db(product_data)
    if res == True:
        await message.answer("Товар успешно добавлен", reply_markup=kb_go_to_products())


#balance
@router.callback_query(lambda c: c.data == "balance")
async def balance(call: types.CallbackQuery):
    crypto = CryptoPay()
    await crypto.initialize()
    try:
        my_info = await crypto.get_my_info()
        my_bal = await crypto.get_my_balance()
        usdt = my_bal[0]
        await call.message.answer(f'Инфо о тебе в криптоботе: {my_info}, Баланс: {usdt}')
    finally:
        await crypto.cleanup()


#history
@router.callback_query(lambda c: c.data == "history")
async def history_purchases(call: types.CallbackQuery):
    mess = f'Список покупок:\n'
    result  = db.db_get_purchases()
    for i in result:
        user_name = db.db_get_user_info(i[0])
        prod = db.db_get_product_info(i[1])
        loc = db.db_get_location_name(prod[0][3])
        mess += f'Пользователь {user_name[1]} купил {prod[0][2]}гр {prod[0][1]} в {loc[0]}, дата - {i[2]}\n'
    await call.message.answer(text=mess, reply_markup=kb_go_to_products())

@router.callback_query(lambda c: c.data == "users")
async def user_menu(call: types.CallbackQuery):
    users  = db.db_get_all_users()
    print(users)
    for user in users:
        if user[4] == 0:
            await call.message.answer(f'Имя - {user[1]}\
                                      \nБаланс - {user[2]}\nРегистрация - {user[3]}\
                                      \nЗабанен - {yes_no(user[4])} ', 
                                      reply_markup=kb_ban_button(user[0]))
        else:
            await call.message.answer(f'Имя - {user[1]}\nБаланс - {user[2]}\nРегистрация - {user[3]}\
                                      \nЗабанен - {yes_no(user[4])} ', 
                                      reply_markup=kb_unban_button(user[0]))
    await call.message.answer('Назад', reply_markup= kb_go_to_products())

@router.callback_query(lambda c: re.match(r'^ban_\d+$', c.data))
async def ban_user(call: types.CallbackQuery):
    id = call.data.split('_')[1]
    db.db_ban_user(id)
    name = db.db_get_user_info(id)
    await call.message.answer(f'Пользователь {name[1]} был забанен')
    await user_menu(call)

@router.callback_query(lambda c: re.match(r'^unban_\d+$', c.data))
async def unban_user(call: types.CallbackQuery):
    id = call.data.split('_')[1]
    db.db_unban_user(id)
    name = db.db_get_user_info(id)
    await call.message.answer(f'Пользователь {name[1]} был разбанен')
    await user_menu(call)

    

    

    

