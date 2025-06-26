import asyncio
import datetime
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode, ContentType
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardMarkup, CallbackQuery, FSInputFile, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.methods import DeleteMessage, EditMessageText
from aiogram import F

import proverochka
import obrabotka
import id_unic
import work_with_google
import sbor_infi
import spiski_dly_knopok

# Все обработчики должны быть прикреплены к Router (или Dispatcher).
Router = Dispatcher()
logging.basicConfig(level=logging.INFO)

id_chat = -1002246431231
# -4124053389(ТЕСТ) -1002246431231(ОСНОВА) -1002203151196(ТЕСТ ТЕМЫ)
id_chat_oplat = {"АЛЬФА": [-1002143783286, 9], "САТУРН": [-1002140127774, 8], "ЯФ": [-1001724787158, 1]}
# {"АЛЬФА": [-1002143783286, 9], "САТУРН": [-1002140127774, 8], "ЯФ": [-1001724787158, 1]} (ОСНОВА)
# {"АЛЬФА": [-1002203151196, 2], "САТУРН": [-1002203151196, 4], "ЯФ": [-1002203151196, 18]} (ТЕСТ)
id_chat_oplat_dm = [-1001954702096, 41]
# [-1001954702096, 41] (ОСНОВА)
# [-1002203151196, 27] (ТЕСТ)
ADMIN_CHAT_ID = 1006018804


class Form(StatesGroup):
    summa = State()
    summa1 = State()
    summa_pol = State()
    tip_platega = State()
    proect = State()
    meneger = State()
    tim = State()
    Podrazdelenia = State()
    nomer_lida = State()
    data_lida = State()
    city = State()
    ictochnic_lida = State()
    nomer_dogovora = State()
    ur_liso = State()
    platelchic = State()
    INN = State()
    check = State()
    check1 = State()
    forma_checa = State()
    forma_checa1 = State()
    kol_vo = State()
    fio_tm = State()
    dogovor1 = State()
    dogovor2 = State()
    dogovor3 = State()
    dogovor4 = State()
    forma_dogovor1 = State()
    forma_dogovor2 = State()
    unic_id_save = State()
    unic_id_save1 = State()
    unic_id_save2 = State()
    otkuda_babosi = State()


class Form2(StatesGroup):
    tip_platega = State()
    proect = State()
    proect_page = State()


PAGE_SIZE = 50


class correc(StatesGroup):
    page_number = State()
    item_number = State()
    text = State()


def text_pozd(name_1, name_2, rgp):
    gruppa = spiski_dly_knopok.podraz(rgp)
    id_chat_pl = id_chat_oplat[gruppa][0]
    topic_id = id_chat_oplat[gruppa][1]
    foto = spiski_dly_knopok.fotog(rgp)
    if name_1 != name_2:
        text = (f'Дорогие коллеги, {name_1} и {name_2}!\n'
                f'\n'
                f'Поздравляем с оплатой. Отличная работа, ждем дальше жирных чеков!')
    else:
        text = (f'Дорогой коллега, {name_1}!\n'
                f'\n'
                f'Поздравляем с оплатой. Отличная работа, ждем дальше жирных чеков!')
    return text, id_chat_pl, foto, topic_id


@Router.message(CommandStart())
async def command_start_handler(message: Message):
    logi = [message.from_user.username, message.from_user.id, "кнопка старта", "-", "-"]
    work_with_google.del_dob4(logi)

    id_sotrudnica = str(message.from_user.id)
    otvet_proverci_and_name = proverochka.proverka_id(id_sotrudnica)

    if otvet_proverci_and_name != "Пользователь не зарегистрирован в системе" and otvet_proverci_and_name != "Должность не соответствует, критериям":
        builder = ReplyKeyboardBuilder()

        builder.add(types.KeyboardButton(text="Отправить платежку"))
        builder.add(types.KeyboardButton(text="Дополнить/скорректровать мои платежки"))
        builder.adjust(1)
        await message.reply(
            f'Приветствую, {otvet_proverci_and_name}, рад вас видеть! Как я могу помочь вам сегодня ?',
            reply_markup=builder.as_markup(resize_keyboard=True))
    elif otvet_proverci_and_name == "Должность не соответствует, критериям":
        await message.reply(
            'Приветствую, к сожалению, по моим данным вы еще не доросли до СТМ или выше, ничем вам не могу помощь.\n'
            '\n'
            'На это не повод отчаиваться, а только мотивация расти дальше к новым высотам.\n'
            '\n'
            'Хорошего вам дня☺️', reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.reply('Приветствую, к сожалению, не вижу вас в нашей системе, ничем вам не могу помощь.\n'
                            '\n'
                            'Хорошего вам дня☺️',
                            reply_markup=types.ReplyKeyboardRemove())


@Router.message(F.text == "Отправить платежку")
async def cmd_start(message: types.Message, state: FSMContext):
    logi = [message.from_user.username, message.from_user.id, "Отправить платежку", "-", "-"]
    work_with_google.del_dob4(logi)

    await state.set_state(Form.check1)
    await message.reply('Прошу скинуть чек.', reply_markup=types.ReplyKeyboardRemove())


@Router.message(F.content_type.in_({'photo', 'document'}), Form.check1)
async def process_check(message: types.Message, state: FSMContext):
    logi = [message.from_user.username, message.from_user.id, "-", "-", message.content_type]
    work_with_google.del_dob4(logi)

    if message.content_type == ContentType.PHOTO:
        await state.update_data(check1=message.photo[-1].file_id)
        await state.update_data(forma_checa1="photo")
    elif message.content_type == ContentType.DOCUMENT:
        await state.update_data(check1=message.document.file_id)
        await state.update_data(forma_checa1="document")
    await state.set_state(Form.summa1)
    await message.reply('Прошу указать сумму поступления.')


@Router.message(Form.summa1)
async def process_summa1(message: types.Message, state: FSMContext):
    logi = [message.from_user.username, message.from_user.id, "-", obrabotka.clean_phone_number(message.text), "-"]
    work_with_google.del_dob4(logi)

    await state.update_data(summa1=obrabotka.clean_phone_number(message.text))
    await state.set_state(Form.summa_pol)

    await message.reply('Прошу указать полную сумму по договору.')


@Router.message(Form.summa_pol)
async def process_summa_pol(message: types.Message, state: FSMContext):
    logi = [message.from_user.username, message.from_user.id, "-", obrabotka.clean_phone_number(message.text), "-"]
    work_with_google.del_dob4(logi)

    await state.update_data(summa_pol=obrabotka.clean_phone_number(message.text))
    await state.set_state(Form.otkuda_babosi)

    builder = InlineKeyboardBuilder()
    buttons = ["Свои", "Кредитка"]
    for btn in buttons:
        builder.button(text=btn, callback_data=f"otkuda:{btn}")
    builder.adjust(1)

    await message.reply('Прошу указать откуда деньги у клиента.', reply_markup=builder.as_markup())


@Router.callback_query(Form.otkuda_babosi)
async def process_tip_platega(callback_query: types.CallbackQuery, state: FSMContext):
    logi = [callback_query.from_user.username, callback_query.from_user.id, callback_query.data, "-", "-"]
    work_with_google.del_dob4(logi)

    await state.update_data(otkuda_babosi=callback_query.data.split("otkuda:")[1])
    await state.set_state(Form.tip_platega)

    builder = InlineKeyboardBuilder()
    indec = "Тип платежа"
    buttons = spiski_dly_knopok.spiski(indec)
    for btn in buttons:
        builder.button(text=btn, callback_data=f"tip_platega:{btn}")
    builder.adjust(1)

    await callback_query.message.reply('Прошу указать тип платежа.', reply_markup=builder.as_markup())
    await callback_query.message.delete()


@Router.callback_query(F.data.startswith("tip_platega:"), Form.tip_platega)
async def process_tip_platega(callback_query: types.CallbackQuery, state: FSMContext):
    logi = [callback_query.from_user.username, callback_query.from_user.id, callback_query.data, "-", "-"]
    work_with_google.del_dob4(logi)

    await state.update_data(tip_platega=callback_query.data.split("tip_platega:")[1])
    await state.set_state(Form2.proect_page)
    await send_project_page(callback_query.message, state, 0)
    await callback_query.message.delete()


async def send_project_page(message: types.Message, state: FSMContext, page: int):
    indec = "ПРОЕКТ"
    projects = spiski_dly_knopok.spiski(indec)
    total_pages = (len(projects) + PAGE_SIZE - 1) // PAGE_SIZE
    start = page * PAGE_SIZE
    end = start + PAGE_SIZE

    builder = InlineKeyboardBuilder()
    for project in projects[start:end]:
        builder.button(text=project, callback_data=f"proect:{project}")

    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"page:{page - 1}"))
    if page < total_pages - 1:
        navigation_buttons.append(InlineKeyboardButton(text="Вперед ➡️", callback_data=f"page:{page + 1}"))

    if navigation_buttons:
        builder.row(*navigation_buttons)
    builder.adjust(2)
    await state.update_data(current_page=page)
    await message.answer('Прошу указать проект.', reply_markup=builder.as_markup())


@Router.callback_query(F.data.startswith("page:"), Form2.proect_page)
async def process_page(callback_query: types.CallbackQuery, state: FSMContext):
    logi = [callback_query.from_user.username, callback_query.from_user.id, callback_query.data, "-", "-"]
    work_with_google.del_dob4(logi)

    page = int(callback_query.data.split("page:")[1])
    await send_project_page(callback_query.message, state, page)
    await callback_query.message.delete()


@Router.callback_query(F.data.startswith("proect:"), Form2.proect_page)
async def process_proect(callback_query: types.CallbackQuery, state: FSMContext):
    logi = [callback_query.from_user.username, callback_query.from_user.id, callback_query.data, "-", "-"]
    work_with_google.del_dob4(logi)

    await state.update_data(proect=callback_query.data.split("proect:")[1])
    await state.set_state(Form.meneger)
    await callback_query.message.answer('Прошу указать менеджера.')
    await callback_query.message.delete()


@Router.message(Form.meneger)
async def process_meneger(message: types.Message, state: FSMContext):
    logi = [message.from_user.username, message.from_user.id, "-", message.text, "-"]
    work_with_google.del_dob4(logi)

    await state.update_data(meneger=message.text)
    await state.set_state(Form.kol_vo)

    builder = InlineKeyboardBuilder()
    indec = "Кол-во касаний"
    buttons = spiski_dly_knopok.spiski(indec)
    for btn in buttons:
        builder.button(text=btn, callback_data=f"kol_vo:{btn}")
    await message.reply(
        'Прошу указать количество касаний, которые совершил менеджер (максимум 3, если вы Тим-лидер, то максимум 4)',
        reply_markup=builder.as_markup())


@Router.callback_query(F.data.startswith("kol_vo:"), Form.kol_vo)
async def process_kol_vo(callback_query: types.CallbackQuery, state: FSMContext):
    logi = [callback_query.from_user.username, callback_query.from_user.id, callback_query.data, "-", "-"]
    work_with_google.del_dob4(logi)

    await state.update_data(kol_vo=callback_query.data.split("kol_vo:")[1])
    await state.set_state(Form.tim)
    await callback_query.message.reply(
        'Прошу указать Тим-лидера (если все 4 касания совершили вы, укажите себя в обоих пунктах).')
    await callback_query.message.delete()


@Router.message(Form.tim)
async def process_tim(message: types.Message, state: FSMContext):
    logi = [message.from_user.username, message.from_user.id, "-", message.text, "-"]
    work_with_google.del_dob4(logi)

    await state.update_data(tim=message.text)
    await state.set_state(Form.Podrazdelenia)
    builder = InlineKeyboardBuilder()
    indec = "РГП"
    buttons = spiski_dly_knopok.spiski(indec)
    for btn in buttons:
        builder.button(text=btn, callback_data=f"rgp:{btn}")
    builder.adjust(3)
    await message.reply('Прошу указать руководителя.', reply_markup=builder.as_markup())


@Router.callback_query(F.data.startswith("rgp:"), Form.Podrazdelenia)
async def process_rg(callback_query: types.CallbackQuery, state: FSMContext):
    logi = [callback_query.from_user.username, callback_query.from_user.id, callback_query.data, "-", "-"]
    work_with_google.del_dob4(logi)

    await state.update_data(Podrazdelenia=callback_query.data.split("rgp:")[1])
    await state.set_state(Form.nomer_lida)
    await callback_query.message.reply('Прошу указать номер лида.')
    await callback_query.message.delete()


@Router.message(Form.nomer_lida)
async def process_nomer_lida(message: types.Message, state: FSMContext):
    logi = [message.from_user.username, message.from_user.id, "-", message.text, "-"]
    work_with_google.del_dob4(logi)

    await state.update_data(nomer_lida=message.text)
    await state.set_state(Form.data_lida)
    await message.reply('Прошу указать дату лида.')


@Router.message(Form.data_lida)
async def process_data_lida(message: types.Message, state: FSMContext):
    logi = [message.from_user.username, message.from_user.id, "-", message.text, "-"]
    work_with_google.del_dob4(logi)

    await state.update_data(data_lida=message.text)
    await state.set_state(Form.city)
    await message.reply('Прошу указать город клиента.')


@Router.message(Form.city)
async def process_city(message: types.Message, state: FSMContext):
    logi = [message.from_user.username, message.from_user.id, "-", message.text, "-"]
    work_with_google.del_dob4(logi)

    await state.update_data(city=message.text)
    await state.set_state(Form.ictochnic_lida)
    builder = InlineKeyboardBuilder()
    indec = "Откуда лид"
    buttons = spiski_dly_knopok.spiski(indec)
    for btn in buttons:
        builder.button(text=btn, callback_data=f"lid:{btn}")
    builder.adjust(3)
    await message.reply('Прошу указать источник лида.', reply_markup=builder.as_markup())


@Router.callback_query(F.data.startswith("lid:"), Form.ictochnic_lida)
async def process_ictochnic_lida(callback_query: types.CallbackQuery, state: FSMContext):
    logi = [callback_query.from_user.username, callback_query.from_user.id, callback_query.data, "-", "-"]
    work_with_google.del_dob4(logi)

    await state.update_data(ictochnic_lida=callback_query.data.split("lid:")[1])

    data = await state.get_data()
    if data['ictochnic_lida'] == "РОС" or data['ictochnic_lida'] == "ТМ":
        await state.set_state(Form.fio_tm)
        await callback_query.message.reply('Прошу указать ФИО ТМа при наличии.')
        await callback_query.message.delete()
    else:
        await state.update_data(fio_tm="")
        await state.set_state(Form.nomer_dogovora)
        await callback_query.message.reply('Прошу указать номер договора.')
        await callback_query.message.delete()


@Router.message(Form.fio_tm)
async def process_fio_tm(message: types.Message, state: FSMContext):
    logi = [message.from_user.username, message.from_user.id, "-", message.text, "-"]
    work_with_google.del_dob4(logi)

    await state.update_data(fio_tm=message.text)
    await state.set_state(Form.nomer_dogovora)
    await message.reply('Прошу указать номер договора.')


@Router.message(Form.nomer_dogovora)
async def process_nomer_dogovora(message: types.Message, state: FSMContext):
    logi = [message.from_user.username, message.from_user.id, "-", message.text, "-"]
    work_with_google.del_dob4(logi)

    await state.update_data(nomer_dogovora=message.text)
    await state.set_state(Form.ur_liso)
    await message.reply('Прошу указать юр./физ. лицо куда упала оплата.')


@Router.message(Form.ur_liso)
async def process_ur_liso(message: types.Message, state: FSMContext):
    logi = [message.from_user.username, message.from_user.id, "-", message.text, "-"]
    work_with_google.del_dob4(logi)

    await state.update_data(ur_liso=message.text)
    await state.set_state(Form.platelchic)
    await message.reply('Прошу указать ФИО плательщика.')


@Router.message(Form.platelchic)
async def process_platelchic(message: types.Message, state: FSMContext):
    logi = [message.from_user.username, message.from_user.id, "-", message.text, "-"]
    work_with_google.del_dob4(logi)

    await state.update_data(platelchic=message.text)
    await state.set_state(Form.INN)
    await message.reply('Прошу указать ИНН плательщика.')


@Router.message(Form.INN)
async def process_inn(message: types.Message, state: FSMContext):
    logi = [message.from_user.username, message.from_user.id, "-", message.text, "-"]
    work_with_google.del_dob4(logi)

    await state.update_data(INN=message.text)

    buttons = ["Скинуть договор сейчас", "Скинуть договор позже"]
    builder = InlineKeyboardBuilder()
    for btn in buttons:
        builder.button(text=btn, callback_data=btn)

    await message.reply('Прошу выбрать когда вы хотите скинуть договор.', reply_markup=builder.as_markup())


@Router.callback_query(lambda c: c.data == 'Скинуть договор сейчас')
async def process_contract_now(callback_query: types.CallbackQuery, state: FSMContext):
    logi = [callback_query.from_user.username, callback_query.from_user.id, callback_query.data, "-", "-"]
    work_with_google.del_dob4(logi)

    await callback_query.message.reply('Прошу скинуть договор.', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Form.forma_dogovor1)


@Router.message(F.content_type.in_({'photo', 'document'}), Form.forma_dogovor1)
async def process_contract_upload(message: types.Message, state: FSMContext):
    logi = [message.from_user.username, message.from_user.id, "-", "-", message.content_type]
    work_with_google.del_dob4(logi)

    await message.reply("Принял, сохраняю данные, прошу подождать.")
    if message.content_type == ContentType.PHOTO:
        await state.update_data(dogovor1=message.photo[-1].file_id)
        await state.update_data(forma_dogovor1="photo")
    elif message.content_type == ContentType.DOCUMENT:
        await state.update_data(dogovor2=message.document.file_id)
        await state.update_data(forma_dogovor1="document")

    id_sotrudnica = str(message.from_user.id)
    otvet_proverci_and_name = proverochka.proverka_id(id_sotrudnica)
    unic_id = id_unic.generate_unique_id()

    data = await state.get_data()
    proverka_zop = (f"Платежка №:\n"
                    f"#{unic_id}\n"
                    "\n"
                    f"Отправил: {otvet_proverci_and_name}\n"
                    "\n"
                    f"1. {data['summa1']} (общая {data['summa_pol']})\n"
                    f"2. {data['tip_platega']}\n"
                    f"3. {data['proect']}\n"
                    f"4.1. {data['meneger']} (количество касаний: {data['kol_vo']})\n"
                    f"4.2. {data['tim']}\n"
                    f"4.3. {data['Podrazdelenia']}\n"
                    f"5. #{data['nomer_lida']}\n"
                    f"6. {data['data_lida']}\n"
                    f"7. {data['city']}\n"
                    f"8. {data['ictochnic_lida']} {data['fio_tm']}\n"
                    f"9. {data['nomer_dogovora']}\n"
                    f"10. {data['ur_liso']}\n"
                    f"11. {data['platelchic']}\n"
                    f"12. {data['INN']}\n"
                    "\n"
                    f"{spiski_dly_knopok.hesteg(data['Podrazdelenia'])}")

    proverka_zop_1 = (f"Договор платежки №:\n"
                      f"#{unic_id}\n"
                      f"#{data['nomer_lida']}\n"
                      f"Отправил: {otvet_proverci_and_name}")

    logi = [message.from_user.username, message.from_user.id, "-", proverka_zop, "-"]
    work_with_google.del_dob4(logi)
    logi = [message.from_user.username, message.from_user.id, "-", proverka_zop_1, "-"]
    work_with_google.del_dob4(logi)

    id_chat_opl = text_pozd(data['meneger'], data['tim'], data['Podrazdelenia'])[1]
    text = text_pozd(data['meneger'], data['tim'], data['Podrazdelenia'])[0]
    foto = text_pozd(data['meneger'], data['tim'], data['Podrazdelenia'])[2]
    topic_id = text_pozd(data['meneger'], data['tim'], data['Podrazdelenia'])[3]
    if id_chat_opl != -1001724787158:
        if foto != "Таурус (Руслан Мамедалиев)":
            input_file = FSInputFile(foto)
            await bot.send_photo(chat_id=id_chat_opl, photo=input_file, caption=text, message_thread_id=topic_id)
        else:
            input_file = FSInputFile(foto)
            await bot.send_video(chat_id=id_chat_opl, photo=input_file, caption=text, message_thread_id=topic_id)
    else:
        if foto != "Таурус (Руслан Мамедалиев)":
            input_file = FSInputFile(foto)
            await bot.send_photo(chat_id=id_chat_opl, photo=input_file, caption=text)
        else:
            input_file = FSInputFile(foto)
            await bot.send_video(chat_id=id_chat_opl, photo=input_file, caption=text)

    if data['ictochnic_lida'] == 'РОС':
        input_file = FSInputFile('РОС.jpg')
        text1 = (f'Дорогой коллега, {data['fio_tm']}!\n'
                 f'\n'
                 f'Поздравляем с оплатой по твоему лиду!'
                 f'\n'
                 f'ОТЛИЧНАЯ РАБОТА! ЖДЕМ ЕЩЕ ЗАКРЫТЫХ СДЕЛОК С ТВОИХ ЛИДОВ!')

        await bot.send_photo(chat_id=id_chat_oplat_dm[0], photo=input_file, caption=text1
                             , message_thread_id=id_chat_oplat_dm[1])

    if data['ictochnic_lida'] == 'ТМ':
        kakoe_foto = spiski_dly_knopok.fio_tm(data['fio_tm'])
        if kakoe_foto == 'УПАКОВКА':
            foto1 = 'УПАКОВКА.jpg'
        elif kakoe_foto == 'Нет':
            foto1 = 'ОТМ.jpg'
        else:
            foto1 = 'БРОКЕРИДЖ.jpg'

        text1 = (f'Дорогой коллега, {data['fio_tm']}!\n'
                 f'\n'
                 f'Поздравляем с оплатой по твоему лиду!'
                 f'\n'
                 f'ОТЛИЧНАЯ РАБОТА! ЖДЕМ ЕЩЕ ЗАКРЫТЫХ СДЕЛОК С ТВОИХ ЛИДОВ!')

        input_file = FSInputFile(foto1)
        await bot.send_photo(chat_id=id_chat_oplat_dm[0], photo=input_file, caption=text1
                             , message_thread_id=id_chat_oplat_dm[1])

    if data['forma_checa1'] == "photo":
        await bot.send_photo(chat_id=id_chat, photo=data['check1'], caption=proverka_zop)
        await bot.send_photo(chat_id=-1002231119442, photo=data['check1'], caption=proverka_zop, message_thread_id=7)
        await bot.send_photo(chat_id=message.from_user.id, photo=data['check1'], caption=proverka_zop)
    elif data['forma_checa1'] == "document":
        await bot.send_document(chat_id=id_chat, document=data['check1'], caption=proverka_zop)
        await bot.send_document(chat_id=-1002231119442, document=data['check1'], caption=proverka_zop, message_thread_id=7)
        await bot.send_document(chat_id=message.from_user.id, document=data['check1'], caption=proverka_zop)

    if data['forma_dogovor1'] == "photo":
        await bot.send_photo(chat_id=id_chat, photo=data['dogovor1'], caption=proverka_zop_1)
        await bot.send_photo(chat_id=-1002231119442, photo=data['dogovor1'], caption=proverka_zop_1
                             , message_thread_id=7)
        await bot.send_photo(chat_id=message.from_user.id, photo=data['dogovor1'], caption=proverka_zop_1)
    elif data['forma_dogovor1'] == "document":
        await bot.send_document(chat_id=id_chat, document=data['dogovor2'], caption=proverka_zop_1)
        await bot.send_document(chat_id=-1002231119442, document=data['dogovor2'], caption=proverka_zop_1
                             , message_thread_id=7)
        await bot.send_document(chat_id=message.from_user.id, document=data['dogovor2'], caption=proverka_zop_1)

    list_otpr = [unic_id, str(datetime.datetime.today().strftime("%d.%m.%Y %H:%M")),
                 message.from_user.id,
                 message.from_user.username, "ДОХОД", data['nomer_lida'],
                 str(datetime.datetime.today().strftime("%d.%m.%Y")), data['data_lida'],
                 data['summa1'], data['summa_pol'], "", "", "", "", "",
                 data['tip_platega'], data['ur_liso'], data['proect'],
                 data['meneger'], data['kol_vo'], data['tim'], data['Podrazdelenia'],
                 "", data['city'], "", data['nomer_dogovora'], data['ictochnic_lida'],
                 data['fio_tm'], "", "", "Есть", data['platelchic'], data['INN'], data['otkuda_babosi']]
    await state.clear()
    indec = "добавить"
    work_with_google.del_dob(indec, list_otpr)

    builder = ReplyKeyboardBuilder()

    builder.add(types.KeyboardButton(text="Отправить платежку"))
    builder.add(types.KeyboardButton(text="Дополнить/скорректровать мои платежки"))
    builder.adjust(1)
    await message.reply('Данные сохранены, ждем дальше жирные чеки!',
                        reply_markup=builder.as_markup(resize_keyboard=True))


@Router.callback_query(lambda c: c.data == 'Скинуть договор позже')
async def process_back_button(callback_query: types.CallbackQuery, state: FSMContext):
    logi = [callback_query.from_user.username, callback_query.from_user.id, callback_query.data, "-", "-"]
    work_with_google.del_dob4(logi)

    await callback_query.message.reply("Принял, сохраняю данные, прошу подождать.")
    id_sotrudnica = str(callback_query.from_user.id)
    otvet_proverci_and_name = proverochka.proverka_id(id_sotrudnica)
    unic_id = id_unic.generate_unique_id()

    data = await state.get_data()
    proverka_zop = (f"Платежка №: #{unic_id}\n"
                    "\n"
                    f"Отправил: {otvet_proverci_and_name}\n"
                    "\n"
                    f"1. {data['summa1']} (общая {data['summa_pol']})\n"
                    f"2. {data['tip_platega']}\n"
                    f"3. {data['proect']}\n"
                    f"4.1. {data['meneger']} (количество касаний: {data['kol_vo']})\n"
                    f"4.2. {data['tim']}\n"
                    f"4.3. {data['Podrazdelenia']}\n"
                    f"5. #{data['nomer_lida']}\n"
                    f"6. {data['data_lida']}\n"
                    f"7. {data['city']}\n"
                    f"8. {data['ictochnic_lida']} {data['fio_tm']}\n"
                    f"9. {data['nomer_dogovora']}\n"
                    f"10. {data['ur_liso']}\n"
                    f"11. {data['platelchic']}\n"
                    f"12. {data['INN']}\n"
                    "\n"
                    f"{spiski_dly_knopok.hesteg(data['Podrazdelenia'])}")

    logi = [callback_query.from_user.username, callback_query.from_user.id, "-", proverka_zop, "-"]
    work_with_google.del_dob4(logi)

    if data['forma_checa1'] == "photo":
        await bot.send_photo(chat_id=id_chat, photo=data['check1'], caption=proverka_zop)
        await bot.send_photo(chat_id=-1002231119442, photo=data['check1'], caption=proverka_zop, message_thread_id=7)
        await bot.send_photo(chat_id=callback_query.from_user.id, photo=data['check1'], caption=proverka_zop)

    elif data['forma_checa1'] == "document":
        await bot.send_document(chat_id=id_chat, document=data['check1'], caption=proverka_zop)
        await bot.send_document(chat_id=-1002231119442, document=data['check1'], caption=proverka_zop, message_thread_id=7)
        await bot.send_document(chat_id=callback_query.from_user.id, document=data['check1'], caption=proverka_zop)

    id_chat_opl = text_pozd(data['meneger'], data['tim'], data['Podrazdelenia'])[1]
    text = text_pozd(data['meneger'], data['tim'], data['Podrazdelenia'])[0]
    foto = text_pozd(data['meneger'], data['tim'], data['Podrazdelenia'])[2]
    topic_id = text_pozd(data['meneger'], data['tim'], data['Podrazdelenia'])[3]
    if id_chat_opl != -1001724787158:
        if foto != "Таурус (Руслан Мамедалиев)":
            input_file = FSInputFile(foto)
            await bot.send_photo(chat_id=id_chat_opl, photo=input_file, caption=text, message_thread_id=topic_id)
        else:
            input_file = FSInputFile(foto)
            await bot.send_video(chat_id=id_chat_opl, photo=input_file, caption=text, message_thread_id=topic_id)
    else:
        if foto != "Таурус (Руслан Мамедалиев)":
            input_file = FSInputFile(foto)
            await bot.send_photo(chat_id=id_chat_opl, photo=input_file, caption=text)
        else:
            input_file = FSInputFile(foto)
            await bot.send_video(chat_id=id_chat_opl, photo=input_file, caption=text)

    if data['ictochnic_lida'] == 'РОС':
        input_file = FSInputFile('РОС.jpg')
        text1 = (f'Дорогой коллега, {data['fio_tm']}!\n'
                 f'\n'
                 f'Поздравляем с оплатой по твоему лиду!'
                 f'\n'
                 f'ОТЛИЧНАЯ РАБОТА! ЖДЕМ ЕЩЕ ЗАКРЫТЫХ СДЕЛОК С ТВОИХ ЛИДОВ!')
        await bot.send_photo(chat_id=id_chat_oplat_dm[0], photo=input_file, caption=text1
                             , message_thread_id=id_chat_oplat_dm[1])

    if data['ictochnic_lida'] == 'ТМ':
        kakoe_foto = spiski_dly_knopok.fio_tm(data['proect'])
        if kakoe_foto == 'УПАКОВКА':
            foto1 = 'УПАКОВКА.jpg'
        elif kakoe_foto == 'ОТМ':
            foto1 = 'ОТМ.jpg'
        elif kakoe_foto == 'БРОКЕРИДЖ':
            foto1 = 'БРОКЕРИДЖ.jpg'
        else:
            foto1 = 'ОТМ.jpg'

        text1 = (f'Дорогой коллега, {data['fio_tm']}!\n'
                 f'\n'
                 f'Поздравляем с оплатой по твоему лиду!'
                 f'\n'
                 f'ОТЛИЧНАЯ РАБОТА! ЖДЕМ ЕЩЕ ЗАКРЫТЫХ СДЕЛОК С ТВОИХ ЛИДОВ!')

        input_file = FSInputFile(foto1)
        await bot.send_photo(chat_id=id_chat_oplat_dm[0], photo=input_file, caption=text1
                             , message_thread_id=id_chat_oplat_dm[1])

    list_otpr = [unic_id, str(datetime.datetime.today().strftime("%d.%m.%Y %H:%M")),
                 callback_query.from_user.id,
                 callback_query.from_user.username, "ДОХОД", data['nomer_lida'],
                 str(datetime.datetime.today().strftime("%d.%m.%Y")), data['data_lida'],
                 data['summa1'], data['summa_pol'], "", "", "", "", "",
                 data['tip_platega'], data['ur_liso'], data['proect'],
                 data['meneger'], data['kol_vo'], data['tim'], data['Podrazdelenia'],
                 "", data['city'], "", data['nomer_dogovora'], data['ictochnic_lida'],
                 data['fio_tm'], "", "", "Нет", data['platelchic'], data['INN'], data['otkuda_babosi']]
    await state.clear()

    indec = "добавить"
    work_with_google.del_dob(indec, list_otpr)

    builder = ReplyKeyboardBuilder()

    builder.add(types.KeyboardButton(text="Отправить платежку"))
    builder.add(types.KeyboardButton(text="Дополнить/скорректровать мои платежки"))
    builder.adjust(1)
    await callback_query.message.reply('Данные сохранены, ждем дальше жирные чеки!',
                                       reply_markup=builder.as_markup(resize_keyboard=True))
    await callback_query.message.delete()


def create_page_keyboard(page_number: int, total_pages: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if page_number > 0:
        builder.button(text="⬅️ Назад", callback_data=f"prev:{page_number - 1}")
    if page_number < total_pages - 1:
        builder.button(text="Вперед ➡️", callback_data=f"next:{page_number + 1}")
    builder.button(text="Дополнить/скорректировать", callback_data=f"skorectirovat:{page_number}")
    builder.button(text="Добавить договор/письмо", callback_data=f"plategki_dop:{page_number}")
    builder.button(text="Вернуться в меню", callback_data="back_to_menu")
    builder.adjust(1)
    return builder.as_markup()


def format_page_content(page_content: list) -> str:
    return "\n".join(page_content)


@Router.message(F.text == "Дополнить/скорректровать мои платежки")
async def cmd_start(message: types.Message):
    logi = [message.from_user.username, message.from_user.id, "Дополнить/скорректровать мои платежки", "-", '-']
    work_with_google.del_dob4(logi)

    await message.reply('Принял, собираю данные.', reply_markup=types.ReplyKeyboardRemove())

    progress_message = await message.reply("Принял, собираю данные.\n"
                                           "\n"
                                           "Загрузка:⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️")

    async def update_progress():
        for percent in range(1, 11, 1):  # Обновляем прогресс каждые 10%
            progress_bar = "🟩" * percent + "⬛️" * (10 - percent)
            await progress_message.edit_text(f"Принял, собираю данные.\n"
                                             "\n"
                                             f"Загрузка: {progress_bar}")
            await asyncio.sleep(0.2)  # Задержка для демонстрации прогресса

    async def collect_data():
        id_sotrudnica = str(message.from_user.id)
        list_dlay_otpr = sbor_infi.sbor_infi(id_sotrudnica)
        return list_dlay_otpr

    data_task = asyncio.create_task(collect_data())
    progress_task = asyncio.create_task(update_progress())

    list_otpr = await data_task
    await progress_task

    page_number = 0
    data_key = list(list_otpr)

    if len(data_key) >= 1:

        page_content = format_page_content(list_otpr[data_key[page_number]])

        # Сохранение текущего состояния книги в память
        await message.reply(page_content, reply_markup=create_page_keyboard(page_number, len(list_otpr)))
        await message.reply("Нажмите кнопки для навигации и выберите, какую хотите платежку изменить.")

    else:

        builder = ReplyKeyboardBuilder()

        builder.add(types.KeyboardButton(text="Отправить платежку"))
        builder.add(types.KeyboardButton(text="Дополнить/скорректровать мои платежки"))
        builder.adjust(1)
        await message.reply("На данный пока что у вас нет платежек.",
                            reply_markup=builder.as_markup(resize_keyboard=True))


# Хендлер для обработки callback data
@Router.callback_query(F.data.startswith('prev:') | F.data.startswith('next:'))
async def page_callback_handler(callback_query: CallbackQuery):
    logi = [callback_query.from_user.username, callback_query.from_user.id, callback_query.data, "-", "-"]
    work_with_google.del_dob4(logi)

    action, page_number = callback_query.data.split(':')
    page_number = int(page_number)
    id_sotrudnica = str(callback_query.from_user.id)
    list_otpr = sbor_infi.sbor_infi(id_sotrudnica)
    data_key = list(list_otpr)
    page_content = format_page_content(list_otpr[data_key[page_number]])

    await bot(EditMessageText(
        text=page_content,
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=create_page_keyboard(page_number, len(list_otpr))
    ))


# Хендлер для кнопки "Назад в меню"
@Router.callback_query(lambda c: c.data == "back_to_menu")
async def back_to_menu_handler(callback_query: CallbackQuery):
    logi = [callback_query.from_user.username, callback_query.from_user.id, callback_query.data, "-", "-"]
    work_with_google.del_dob4(logi)

    builder = ReplyKeyboardBuilder()

    builder.add(types.KeyboardButton(text="Отправить платежку"))
    builder.add(types.KeyboardButton(text="Дополнить/скорректровать мои платежки"))
    builder.adjust(1)
    await callback_query.message.reply("Вы вернулись назад.", reply_markup=builder.as_markup(resize_keyboard=True))
    global bot
    await bot(DeleteMessage(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id
    ))


# Хендлер для кнопки "Скинуть платежку"
@Router.callback_query(F.data.startswith("plategki_dop:"))
async def back_to_menu_handler(callback_query: CallbackQuery, state: FSMContext):
    logi = [callback_query.from_user.username, callback_query.from_user.id, callback_query.data, "-", "-"]
    work_with_google.del_dob4(logi)

    _, page_number = callback_query.data.split(':')
    page_number = int(page_number)

    id_sotrudnica = str(callback_query.from_user.id)
    list_otpr = sbor_infi.sbor_infi(id_sotrudnica)
    data_key = list(list_otpr)
    data_pl = list_otpr[list(list_otpr)[page_number]]
    nomber_lids = data_pl[0].split('\n')[8].split('5. ')[1]

    await state.update_data(unic_id_save=data_key[page_number])
    await state.update_data(unic_id_save1=page_number)
    await state.update_data(unic_id_save2=nomber_lids)
    await state.set_state(Form.forma_dogovor2)
    await callback_query.message.reply("Прошу скинуть договор.")
    await bot(DeleteMessage(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id
    ))


@Router.message(Form.forma_dogovor2, F.content_type.in_({'photo', 'document'}))
async def process_name(message: types.Message, state: FSMContext):
    logi = [message.from_user.username, message.from_user.id, "-", "-", message.content_type]
    work_with_google.del_dob4(logi)

    await message.reply("Принял, сохраняю данные, прошу подождать.")
    if message.content_type == ContentType.PHOTO:
        await state.update_data(dogovor3=message.photo[-1].file_id)
        await state.update_data(forma_dogovor2="photo")
    elif message.content_type == ContentType.DOCUMENT:
        await state.update_data(dogovor4=message.document.file_id)
        await state.update_data(forma_dogovor2="document")

    id_sotrudnica = str(message.from_user.id)
    otvet_proverci_and_name = proverochka.proverka_id(id_sotrudnica)

    data = await state.get_data()
    item_number = "ДОГОВОР"
    text = "Есть"
    id_sotrudnica = str(message.from_user.id)
    work_with_google.clear_now(id_sotrudnica, data['unic_id_save1'], item_number, text)

    proverka_zop_1 = (f"Платежки №:\n"
                      f"#{data['unic_id_save']}\n"
                      f"#{data['unic_id_save2']}\n"
                      f"Отправил: {otvet_proverci_and_name}")

    logi = [message.from_user.username, message.from_user.id, "-", proverka_zop_1, "-"]
    work_with_google.del_dob4(logi)

    if data['forma_dogovor2'] == "photo":
        await bot.send_photo(chat_id=id_chat, photo=data['dogovor3'], caption=proverka_zop_1)
        await bot.send_photo(chat_id=-1002231119442, photo=data['dogovor3'], caption=proverka_zop_1
                             , message_thread_id=7)
        await bot.send_photo(chat_id=message.from_user.id, photo=data['dogovor3'], caption=proverka_zop_1)
    elif data['forma_dogovor2'] == "document":
        await bot.send_document(chat_id=id_chat, document=data['dogovor4'], caption=proverka_zop_1)
        await bot.send_document(chat_id=-1002231119442, document=data['dogovor4'], caption=proverka_zop_1
                             , message_thread_id=7)
        await bot.send_document(chat_id=message.from_user.id, document=data['dogovor4'], caption=proverka_zop_1)
    await state.clear()
    builder = ReplyKeyboardBuilder()

    builder.add(types.KeyboardButton(text="Отправить платежку"))
    builder.add(types.KeyboardButton(text="Дополнить/скорректровать мои платежки"))
    builder.adjust(1)
    await message.reply("Данные сохранены, удачного дня!", reply_markup=builder.as_markup(resize_keyboard=True))


# Хендлер для кнопки "Скорректировать"
@Router.callback_query(F.data.startswith("skorectirovat:"))
async def skorectirovat_handler(callback_query: CallbackQuery):
    logi = [callback_query.from_user.username, callback_query.from_user.id, callback_query.data, "-", "-"]
    work_with_google.del_dob4(logi)

    _, page_number = callback_query.data.split(':')
    page_number = int(page_number)

    id_sotrudnica = str(callback_query.from_user.id)
    list_otpr = sbor_infi.sbor_infi(id_sotrudnica)
    data_key = list(list_otpr)
    page_content = format_page_content(list_otpr[data_key[page_number]])

    correction_keyboard = InlineKeyboardBuilder()
    list_dla_pravki = ["СУММА", "ОБЩАЯ СУММА", "ТИП ПЛАТЕЖА", "ПРОЕКТ", "МЕНЕДЖЕР", "КАСАНИЯ", "ТИМ-ЛИДЕР", "РГП",
                       "НОМЕР ЛИДА", "ДАТА ЛИДА", "ГОРОД", "ИСТОЧНИК ЛИДА", "ФИО ТМа (при наличии)", "НОМЕР ДОГОВОРА",
                       "ЮР ЛИЦО, КУДА ПОСТУПИЛА ОПЛАТА", "ФИО ПЛАТЕЛЬЩИКА", "ИНН ПЛАТЕЛЬЩИКА"]
    for i in range(len(list_dla_pravki)):
        correction_keyboard.button(text=f"{list_dla_pravki[i]}",
                                   callback_data=f"cor:{page_number}:{list_dla_pravki[i]}")
    correction_keyboard.button(text=f"НАЗАД",
                               callback_data=f"nazad")
    correction_keyboard.adjust(2)
    await callback_query.message.reply(
        f"Корректируем страницу {page_number + 1}. Пожалуйста, выберите пункт для корректировки\n\n{page_content}",
        reply_markup=correction_keyboard.as_markup())
    await bot(DeleteMessage(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id
    ))


# Хендлер для выбора пункта корректировки
@Router.callback_query(F.data.startswith("cor:"))
async def correct_item_handler(callback_query: CallbackQuery, state: FSMContext):
    logi = [callback_query.from_user.username, callback_query.from_user.id, callback_query.data, "-", "-"]
    work_with_google.del_dob4(logi)

    _, page_number, item_number = callback_query.data.split(':')
    page_number = int(page_number)
    item_number = item_number

    await state.set_state(correc.text)

    await state.update_data(page_number=page_number)
    await state.update_data(item_number=item_number)
    # Здесь можно добавить логику для корректировки конкретного пункта
    await callback_query.message.reply(
        f"Корректируем пункт {item_number} на странице {page_number + 1}. Пожалуйста, внесите изменения.")
    await bot(DeleteMessage(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id
    ))


@Router.message(correc.text)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    await state.update_data(text=message.text)
    page_number = data['page_number']
    item_number = data['item_number']
    text = data['text']
    id_sotrudnica = str(message.from_user.id)
    work_with_google.clear_now(id_sotrudnica, page_number, item_number, text)

    what_correct = (f"Кто:{id_sotrudnica}"
                    f"Что1:{page_number}"
                    f"Что2:{item_number}"
                    f"На что:{text}")

    logi = [message.from_user.username, message.from_user.id, "-", what_correct, "-"]
    work_with_google.del_dob4(logi)

    await state.clear()

    builder = ReplyKeyboardBuilder()

    builder.add(types.KeyboardButton(text="Отправить платежку"))
    builder.add(types.KeyboardButton(text="Дополнить/скорректровать мои платежки"))
    builder.adjust(1)
    await message.reply("Корректировки внесены, хорошего дня.", reply_markup=builder.as_markup(resize_keyboard=True))


# Хендлер для выбора пункта назад
@Router.callback_query(lambda c: c.data == "nazad")
async def correct_item_handler(callback_query: CallbackQuery, state: FSMContext):
    logi = [callback_query.from_user.username, callback_query.from_user.id, callback_query.data, "-", "-"]
    work_with_google.del_dob4(logi)

    await callback_query.message.reply('Принял, собираю данные.', reply_markup=types.ReplyKeyboardRemove())

    progress_message = await callback_query.message.reply("Принял, собираю данные.\n"
                                                          "\n"
                                                          "Загрузка:⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️")

    async def update_progress():
        for percent in range(1, 11, 1):  # Обновляем прогресс каждые 10%
            progress_bar = "🟩" * percent + "⬛️" * (10 - percent)
            await progress_message.edit_text(f"Принял, собираю данные.\n"
                                             "\n"
                                             f"Загрузка: {progress_bar}")
            await asyncio.sleep(0.2)  # Задержка для демонстрации прогресса

    async def collect_data():
        id_sotrudnica = str(callback_query.from_user.id)
        list_dlay_otpr = sbor_infi.sbor_infi(id_sotrudnica)
        return list_dlay_otpr

    data_task = asyncio.create_task(collect_data())
    progress_task = asyncio.create_task(update_progress())

    list_otpr = await data_task
    await progress_task

    page_number = 0
    data_key = list(list_otpr)

    if len(data_key) >= 1:

        page_content = format_page_content(list_otpr[data_key[page_number]])

        # Сохранение текущего состояния книги в память
        await callback_query.message.reply(page_content, reply_markup=create_page_keyboard(page_number, len(list_otpr)))
        await callback_query.message.reply("Нажмите кнопки для навигации и выберите, какую хотите платежку изменить.")

    else:

        builder = ReplyKeyboardBuilder()

        builder.add(types.KeyboardButton(text="Отправить платежку"))
        builder.add(types.KeyboardButton(text="Дополнить/скорректровать мои платежки"))
        builder.adjust(1)
        await callback_query.message.reply("На данный пока что у вас нет платежек.",
                                           reply_markup=builder.as_markup(resize_keyboard=True))
    await bot(DeleteMessage(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id
    ))


@Router.message(F.text == "Назад")
async def cmd_start(message: types.Message):
    logi = [message.from_user.username, message.from_user.id, "Назад", "-", "-"]
    work_with_google.del_dob4(logi)

    builder = ReplyKeyboardBuilder()

    builder.add(types.KeyboardButton(text="Отправить платежку"))
    builder.add(types.KeyboardButton(text="Дополнить/скорректровать мои платежки"))
    builder.adjust(1)
    await message.reply("Вы вернулись назад.", reply_markup=builder.as_markup())


@Router.message()
async def log_text_message(message: types.Message):
    logi = [message.from_user.username, message.from_user.id, "-", message.text, "-"]
    work_with_google.del_dob4(logi)


async def main() -> None:
    global bot

    TOKENS = "6495758232:AAFSkFuUggXQKTF6WmrG69lyQAXJtIiSxSo"
    # 7275897561:AAGeR7N4Jl9gWQNsBBALeiowdqnF8VcDiNg(ТЕСТ) 6495758232:AAFSkFuUggXQKTF6WmrG69lyQAXJtIiSxSo(ОСНОВА)
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKENS, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await Router.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
