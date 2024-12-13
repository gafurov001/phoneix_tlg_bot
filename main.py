import asyncio
import datetime
import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, CallbackQuery, \
    ChatMemberUpdated, ReplyKeyboardRemove, BotCommand
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import bot_token, group_id_2, group_id_1, amalyot_group_id, platforma_group_id
from form import LessonsQuestion
from functions import validate_full_name
from models import create_table, Answer, Question, Complaint, Curator, AmalyotAnswer, PlatformaAnswer

TOKEN = bot_token
dp = Dispatcher()
admin = [5760868166]
'''Savollaringizni shu yerda yozishingiz mumkin.Kurator sizga imkon qadar tezda javob beradi.Har bir jarayon sodda va oson!
Savolingizni yuboring va javobni kuting!'''


@dp.message(F.text == '/admin')
async def admin_send_report(message: Message):
    if message.from_user.id in admin:
        d = {}
        data = await Curator.select()
        data = [i for i in data]
        text = str()
        for i in data:
            if d.get(i[1]):
                d[str(i[1])] += 1
                continue
            d[i[1]] = 1
        for id, k in enumerate(d):
            text += "".join(f'<a href="tg://user?id={int(k)}">{id + 1}</a> = {d[k]}\n')
        await message.answer(text, parse_mode=ParseMode.HTML)


@dp.message(lambda message: message.chat.id in [group_id_1, group_id_2, amalyot_group_id, platforma_group_id])
async def send_msg_group(message: Message, state: FSMContext, bot: Bot):
    await state.clear()
    await state.storage.close()
    await state.set_state(LessonsQuestion.curator)
    msg = message.reply_to_message.text.split('\n\n')
    q = await Question.filter(Question.id == int(msg[0].split('Savol id:')[1]))
    q = [i for i in q][0]
    chat_id = message.chat.id
    if message.text:
        await bot.send_message(chat_id=q[-1], text=message.text)
        await Curator.create(curator_id=message.from_user.id, answer=message.text, question_id=q[0],
                             created_at=datetime.date.today())
    elif message.audio:
        await bot.send_audio(q[-1], message.audio.file_id)
        await Curator.create(curator_id=message.from_user.id, answer="audio", question_id=q[0],
                             created_at=datetime.date.today())
    elif message.voice:
        await bot.send_voice(q[-1], message.voice.file_id)
        await Curator.create(curator_id=message.from_user.id, answer="voice", question_id=q[0],
                             created_at=datetime.date.today())
    elif message.video_note:
        await bot.send_video_note(q[-1], message.video_note.file_id)
        await Curator.create(curator_id=message.from_user.id, answer="video_note", question_id=q[0],
                             created_at=datetime.date.today())
    elif message.document:
        await bot.send_document(q[-1], message.document.file_id)
        await Curator.create(curator_id=message.from_user.id, answer="document", question_id=q[0],
                             created_at=datetime.date.today())
    elif message.photo:
        await bot.send_photo(q[-1], message.photo[-1].file_id)
        await Curator.create(curator_id=message.from_user.id, answer="photo", question_id=q[0],
                             created_at=datetime.date.today())
    elif message.video:
        await bot.send_video(q[-1], message.video.file_id)
        await Curator.create(curator_id=message.from_user.id, answer="video", question_id=q[0],
                             created_at=datetime.date.today())

    ikb = InlineKeyboardBuilder().add(
        InlineKeyboardButton(text=f"Profilga o'tish", url=f"tg://user?id={q[-1]}"))
    await bot.edit_message_text(text=f'{msg[0]}\n\n<tg-spoiler>{msg[1]}</tg-spoiler>',
                                chat_id=chat_id,
                                message_id=message.reply_to_message.message_id, reply_markup=ikb.as_markup())


@dp.my_chat_member()
async def on_chat_member_update(event: ChatMemberUpdated, bot: Bot):
    if event.new_chat_member.status == "member":
        chat = event.chat
        await bot.send_message(
            chat_id=chat.id,
            text=f"{chat.id}"
        )


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    kb = [
        [KeyboardButton(text="Dars bo'yicha savol 📚")],
        [KeyboardButton(text="Amaliyot bo‘yicha savollar📊")],
        [KeyboardButton(text="Platforma va uyga vazifalar bo‘yicha savollar📱")],
    ]
    rkb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    text = '''Assalomu alaykum! 👋
TargetPro botga xush kelibsiz! 🚀
Bu yerda siz kurs haqida barcha kerakli ma’lumotlarni topishingiz mumkin. Men sizga yordam berish va savollaringizga javob qaytarish uchun shu yerdaman. 😊
Men bilan ishlash juda oson va qulay! 😉
Qanday ma’lumot kerakligini tanlang va boshlaymiz:
1️⃣ Darslar va vazifalar haqida ma’lumot
2️⃣ Amaliyot bo’yicha savol/Kurator bilan bog’lanish
3️⃣ Uyga vazifa bo’yicha savollar
Men sizga yordam berishga doim tayyorman! 😊
'''
    await message.answer(text, reply_markup=rkb)


@dp.message(F.text == "Amaliyot bo‘yicha savollar📊")
async def amalyot_answer(message: Message):
    rkb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Amalyot bo'yicha tayyor savollar📖")],
                                        [KeyboardButton(text="Mutaxasislar bilan bog'lanish👨🏻‍💻")],
                                        [KeyboardButton(text="Ortga")]], resize_keyboard=True)
    await message.answer("Tugmalardan birini tanlang!", reply_markup=rkb)


@dp.message(F.text == "Platforma va uyga vazifalar bo‘yicha savollar📱")
async def amalyot_answer(message: Message):
    rkb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Platforma bo'yicha tayyor savollar📖")],
                                        [KeyboardButton(text="Mutaxasislarimiz bilan bog'lanish👨🏻‍💻")],
                                        [KeyboardButton(text="Ortga")]], resize_keyboard=True)
    await message.answer("Tugmalardan birini tanlang!", reply_markup=rkb)


@dp.message(F.text == "Platforma bo'yicha tayyor savollar📖")
async def tayyot_javob_amalyot(message: Message):
    res = await PlatformaAnswer.select_where_asc(2, PlatformaAnswer.id >= 1)
    markup = [[InlineKeyboardButton(text=i[1], callback_data=f"{i[0]}*platforma")] for i in [j for j in res]]
    markup.append([InlineKeyboardButton(text="➡️", callback_data="platforma_oldinga")])
    ikb = InlineKeyboardBuilder(
        markup=markup)
    await message.answer(
        "Savolardan birini tanlang, agar ozingizga kerak bo'lgan savolni topa olmasangiz keyigi sahifaga otkazib koring‼️",
        reply_markup=ikb.as_markup())


@dp.callback_query(F.data == "platforma_oldinga")
async def oldinga_amalyot(callback: CallbackQuery, bot: Bot):
    last_object_id = await PlatformaAnswer.last_id()
    inline = callback.message.reply_markup.inline_keyboard
    res = await PlatformaAnswer.select_where_asc(2, PlatformaAnswer.id > inline[-2][0].callback_data.split('*')[0])
    markup = [[InlineKeyboardButton(text=i[1], callback_data=f"{i[0]}*platforma")] for i in [j for j in res]]
    if int(markup[-1][0].callback_data.split('*')[0]) != last_object_id[0]:
        markup.append([InlineKeyboardButton(text="⬅️", callback_data="platforma_ortga"),
                       InlineKeyboardButton(text="➡️", callback_data="platforma_oldinga")])
    else:
        markup.append([InlineKeyboardButton(text="⬅️", callback_data="platforma_ortga")])
    ikb = InlineKeyboardBuilder(
        markup=markup)
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                        reply_markup=ikb.as_markup())

    await bot.edit_message_reply_markup()


@dp.callback_query(F.data == "platforma_ortga")
async def oldinga_amalyot(callback: CallbackQuery, bot: Bot):
    first_object_id = await PlatformaAnswer.first_id()
    inline = callback.message.reply_markup.inline_keyboard
    res = [i for i in
           await PlatformaAnswer.select_where_desc(2, PlatformaAnswer.id < inline[0][0].callback_data.split('*')[0])]
    markup = [[InlineKeyboardButton(text=i[1], callback_data=f"{i[0]}*platforma")] for i in res[::-1]]
    if int(markup[0][0].callback_data.split('*')[0]) != first_object_id[0]:
        markup.append([InlineKeyboardButton(text="⬅️", callback_data="platforma_ortga"),
                       InlineKeyboardButton(text="➡️", callback_data="platforma_oldinga")])
    else:
        markup.append([
            InlineKeyboardButton(text="➡️", callback_data="platforma_oldinga")])
    ikb = InlineKeyboardBuilder(
        markup=markup)
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                        reply_markup=ikb.as_markup())


@dp.callback_query(F.data.endswith('platforma'))
async def amalyot_send_answer(callback: CallbackQuery):
    answer = [i for i in await PlatformaAnswer.filter(PlatformaAnswer.id == int(callback.data.split('*')[0]))]
    await callback.message.answer(f"Savol:\n\n{answer[0][1]}\n\nJavob:\n\n{answer[0][2]}",
                                  reply_markup=InlineKeyboardBuilder(markup=[[InlineKeyboardButton(text='Tushunarli✔️',
                                                                                                   callback_data='tushunarli')]]).as_markup())


@dp.message(F.text == "Mutaxasislarimiz bilan bog'lanish👨🏻‍💻")
async def send_to_amalyot_group(message: Message, state: FSMContext):
    await message.answer("Savolingizni yozishingiz mumkin tez orada sizga mutaxasislarimiz bog'lanishadi!")
    await state.set_state(LessonsQuestion.platforma_group)


@dp.message(F.text == "Amalyot bo'yicha tayyor savollar📖")
async def tayyot_javob_amalyot(message: Message):
    res = await AmalyotAnswer.select_where_asc(2, AmalyotAnswer.id >= 1)
    markup = [[InlineKeyboardButton(text=i[1], callback_data=f"{i[0]}*amalyot")] for i in [j for j in res]]
    markup.append([InlineKeyboardButton(text="➡️", callback_data="amalyot_oldinga")])
    ikb = InlineKeyboardBuilder(
        markup=markup)
    await message.answer(
        "Savolardan birini tanlang, agar ozingizga kerak bo'lgan savolni topa olmasangiz keyigi sahifaga otkazib koring‼️",
        reply_markup=ikb.as_markup())


@dp.callback_query(F.data == "amalyot_oldinga")
async def oldinga_amalyot(callback: CallbackQuery, bot: Bot):
    last_object_id = await AmalyotAnswer.last_id()
    inline = callback.message.reply_markup.inline_keyboard
    res = await AmalyotAnswer.select_where_asc(2, AmalyotAnswer.id > inline[-2][0].callback_data.split('*')[0])
    markup = [[InlineKeyboardButton(text=i[1], callback_data=f"{i[0]}*amalyot")] for i in [j for j in res]]
    if int(markup[-1][0].callback_data.split('*')[0]) != last_object_id[0]:
        markup.append([InlineKeyboardButton(text="⬅️", callback_data="amalyot_ortga"),
                       InlineKeyboardButton(text="➡️", callback_data="amalyot_oldinga")])
    else:
        markup.append([InlineKeyboardButton(text="⬅️", callback_data="amalyot_ortga")])
    ikb = InlineKeyboardBuilder(
        markup=markup)
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                        reply_markup=ikb.as_markup())

    await bot.edit_message_reply_markup()


@dp.callback_query(F.data == "amalyot_ortga")
async def oldinga_amalyot(callback: CallbackQuery, bot: Bot):
    first_object_id = await AmalyotAnswer.first_id()
    inline = callback.message.reply_markup.inline_keyboard
    res = [i for i in
           await AmalyotAnswer.select_where_desc(2, AmalyotAnswer.id < inline[0][0].callback_data.split('*')[0])]
    markup = [[InlineKeyboardButton(text=i[1], callback_data=f"{i[0]}*amalyot")] for i in res[::-1]]
    if int(markup[0][0].callback_data.split('*')[0]) != first_object_id[0]:
        markup.append([InlineKeyboardButton(text="⬅️", callback_data="amalyot_ortga"),
                       InlineKeyboardButton(text="➡️", callback_data="amalyot_oldinga")])
    else:
        markup.append([
            InlineKeyboardButton(text="➡️", callback_data="amalyot_oldinga")])
    ikb = InlineKeyboardBuilder(
        markup=markup)
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                        reply_markup=ikb.as_markup())


@dp.callback_query(F.data.endswith('amalyot'))
async def amalyot_send_answer(callback: CallbackQuery):
    answer = [i for i in await AmalyotAnswer.filter(AmalyotAnswer.id == int(callback.data.split('*')[0]))]
    await callback.message.answer(f"Savol:\n\n{answer[0][1]}\n\nJavob:\n\n{answer[0][2]}",
                                  reply_markup=InlineKeyboardBuilder(markup=[[InlineKeyboardButton(text='Tushunarli✔️',
                                                                                                   callback_data='tushunarli')]]).as_markup())


@dp.message(F.text == "Mutaxasislar bilan bog'lanish👨🏻‍💻")
async def send_to_amalyot_group(message: Message, state: FSMContext):
    await message.answer("Savolingizni yozishingiz mumkin tez orada sizga mutaxasislarimiz bog'lanishadi!")
    await state.set_state(LessonsQuestion.amalyot_group)


@dp.message(F.text == "Ortga")
async def menyuga_otish(message: Message):
    await command_start_handler(message)


@dp.message(F.text == "Ortga ⬅️")
async def another_question(message: Message, state: FSMContext):
    await button_lesson_question(message, state)


@dp.callback_query(F.data == "ortga")
async def another_question(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await button_lesson_question(callback.message, state)


@dp.message(F.text == "Dars bo'yicha savol 📚")
async def button_lesson_question(message: Message, state: FSMContext):
    res = await Answer.order(Answer.id)
    l = set()
    for i in res:
        l.add(i[1])
    l = sorted(list(l))

    kb = []
    for i in l:
        kb.append([KeyboardButton(text=i)])
    kb.append([KeyboardButton(text="Ortga ⬅️")])
    rkb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer('Modul tanlang 🗃️', reply_markup=rkb)
    await state.update_data(user_id=message.chat.id)
    await state.set_state(LessonsQuestion.modul)


@dp.message(F.text == "Ko'p so'raladigan savollar 📖")
async def frequently_asked_question(message: Message, state: FSMContext):
    data = await state.get_data()
    questions = await Answer.filter(Answer.modul == data['modul'], Answer.lesson == data['lesson'])
    ikb = InlineKeyboardBuilder()
    for i in questions:
        ikb.row(InlineKeyboardButton(text=i[3],
                                     callback_data=f"{i[1] if i[1].count('-') == 1 else i[1].split()[0]}*{i[2] if i[2].count('-') == 1 else i[2].split()[0]}*{i[4]}* question"))
    ikb.row(InlineKeyboardButton(text='Ortga ⬅️', callback_data='ortga'))
    await message.answer('Savolni tanlang 📝', reply_markup=ikb.as_markup())


@dp.callback_query(F.data.endswith(' question'))
async def answer_to_question(callback: CallbackQuery, bot: Bot):
    data = callback.data.split('*')
    answer = await Answer.filter(Answer.modul.ilike(f"{data[0]}%"), Answer.lesson.ilike(f"{data[1]}%"),
                                 Answer.question_number == data[2])
    ans = [i for i in answer][0]
    ikb = InlineKeyboardBuilder().add(InlineKeyboardButton(text='Tushunarli✔️', callback_data='tushunarli'))
    await callback.message.answer(text=f"Savol: \n\n{ans[3]}\n\nJavob:\n\n{ans[-1]}", reply_markup=ikb.as_markup())


@dp.callback_query(F.data.endswith('tushunarli'))
async def inline_echo(callback: CallbackQuery, bot: Bot):
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)


@dp.message(F.text == "Kurator bilan bog‘lanish 📞")
async def another_question(message: Message, state: FSMContext):
    await message.answer(
        '''Savollaringizni shu yerda yozishingiz mumkin 🖊️.Kurator sizga imkon qadar tezda javob beradi.Har bir jarayon sodda va oson! Savolingizni yuboring va javobni kuting!''')
    await state.set_state(LessonsQuestion.answer)


@dp.message(F.text == "Shikoyalar 🔴")
async def complaint_info_start(message: Message, state: FSMContext):
    await message.answer(
        "Shikoyatingizni qabul qilish uchun bazi savolarga javob berishingiz kerak iltimos to'g'ri javob bering‼️\nIsm Familyangizni kiriting!",
        reply_markup=ReplyKeyboardRemove())
    await state.set_state(LessonsQuestion.full_name)


@dp.message(LessonsQuestion.platforma_group)
async def send_amalyot(message: Message, state: FSMContext, bot: Bot):
    question = await Question.create(question=message.text, user_id=message.from_user.id)
    ikb = InlineKeyboardBuilder().add(
        InlineKeyboardButton(text=f"Profilga o'tish", url=f"tg://user?id={message.from_user.id}"))
    await bot.send_message(chat_id=platforma_group_id, text=f"Savol id:{question[0]}\n\n{message.text}",
                           reply_markup=ikb.as_markup())
    await message.answer("Xabaringiz kuratorlarga yuborildi iltimos kuting tez orada siz bilan bog'lanishadi")


@dp.message(LessonsQuestion.amalyot_group)
async def send_amalyot(message: Message, state: FSMContext, bot: Bot):
    question = await Question.create(question=message.text, user_id=message.from_user.id)
    ikb = InlineKeyboardBuilder().add(
        InlineKeyboardButton(text=f"Profilga o'tish", url=f"tg://user?id={message.from_user.id}"))
    await bot.send_message(chat_id=amalyot_group_id, text=f"Savol id:{question[0]}\n\n{message.text}",
                           reply_markup=ikb.as_markup())
    await message.answer("Xabaringiz kuratorlarga yuborildi iltimos kuting tez orada siz bilan bog'lanishadi")


@dp.message(LessonsQuestion.full_name)
async def complaint_info_get_full_name(message: Message, state: FSMContext):
    if validate_full_name(message.text):
        await state.update_data(full_name=message.text)
        kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Telefon raqamni jo'natish", request_contact=True)]],
                                 resize_keyboard=True)
        await message.answer("Telefon raqamingizni kiriting, iltimos tugma orqali", reply_markup=kb)
        await state.set_state(LessonsQuestion.phone_number)
    else:
        await message.answer("Isim yoki Familya noto'g'ri,iltimos ism va familyangizni boshidan to'g'ri kiriting❗️❗️❗️")
        await state.set_state(LessonsQuestion.full_name)


@dp.message(LessonsQuestion.phone_number)
async def complaint_info_get_phone_number(message: Message, state: FSMContext):
    if message.contact:
        await state.update_data(phone_number=message.contact.phone_number)
        await message.answer("To'lovingizni chekini screenshotini yuboring!", reply_markup=ReplyKeyboardRemove())
        await state.set_state(LessonsQuestion.screenshot_check)
    else:
        await state.update_data(phone_number=message.text)
        await message.answer("To'lovingizni chekini screenshotini yuboring!")
        await state.set_state(LessonsQuestion.screenshot_check)


@dp.message(LessonsQuestion.screenshot_check)
async def complaint_info_get_screenshot_check(message: Message, state: FSMContext, bot: Bot):
    if message.content_type == 'photo' and not message.photo is None:
        photo = message.photo[-1]
        file_id = photo.file_id
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path
        file = await bot.download_file(file_path)

        save_path = f"photos/{file_id}.jpg"
        with open(save_path, 'wb') as f:
            f.write(file.read())

        await state.update_data(screenshot_check=save_path)
        await message.answer("Kursni yakunlamoqchi bo'lganingiz haqida batafsil gapirib bering!")
        await state.set_state(LessonsQuestion.reason_cancel_course)
    else:
        await message.answer(
            "Jo'natgan habaringiz talabga javob bermaydi iltimos chekni screenshot wilib rasmini yuboring‼️")
        await state.set_state(LessonsQuestion.phone_number)


@dp.message(LessonsQuestion.reason_cancel_course)
async def complaint_info_get_reason_cancel_course(message: Message, state: FSMContext):
    await state.update_data(reason_cancel_course=message.text)
    data = await state.get_data()
    await Complaint.create(full_name=data.get('full_name'), phone_number=data.get('phone_number'),
                           screenshot_check=data.get('screenshot_check'),
                           reason_cancel_course=data.get('reason_cancel_course'))
    await message.answer("Malumotlaringiz saqlandi!")
    await command_start_handler(message)


@dp.message(LessonsQuestion.modul)
async def form_modul(message: Message, state: FSMContext):
    modul = message.text
    await state.update_data(modul=modul)
    res = await Answer.filter_order(Answer.modul == modul)
    _set = set()
    for i in res:
        _set.add(i[2])
    _set = sorted(list(_set))
    kb = [[KeyboardButton(text=i)] for i in _set]
    kb.append([KeyboardButton(text=f"Ortga ⬅️")])
    rkb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer('Darsni tanlang 📝', reply_markup=rkb)
    await state.set_state(LessonsQuestion.lesson)


@dp.message(LessonsQuestion.answer)
async def send_question_group(message: Message, state: FSMContext, bot: Bot):
    await message.answer("Xabaringiz kuratorlarga yuborildi iltimos kuting tez orada siz bilan bog'lanishadi")
    if message.from_user.id % 2 == 0:
        group_id = group_id_1
    else:
        group_id = group_id_2
    await state.update_data(answer=message.text)
    question = await Question.create(question=message.text, user_id=message.from_user.id)
    ikb = InlineKeyboardBuilder().add(
        InlineKeyboardButton(text=f"Profilga o'tish", url=f"tg://user?id={message.from_user.id}"))
    await bot.send_message(chat_id=group_id, text=f"Savol id:{question[0]}\n\n{message.text}",
                           reply_markup=ikb.as_markup())


@dp.message(LessonsQuestion.lesson)
async def form_lesson(message: Message, state: FSMContext):
    await state.update_data(lesson=message.text)

    kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Ko'p so'raladigan savollar 📖")],
                                       [KeyboardButton(text="Kurator bilan bog‘lanish 📞")],
                                       [KeyboardButton(text="Shikoyalar 🔴")], [KeyboardButton(text="Ortga ⬅️")]],
                             resize_keyboard=True)
    await message.answer(
        '''Agar savolingiz kop so'raladigan turga kirsa "Ko'p so'raladigan savollar 📖" bu yerdan javob olishingiz mumkun!\nAgar kuratorlar bilan bog'lanmoqchi bo'lsangiz "Kurator bilan bog‘lanish 📞" ushbu tugmani bosing va kuratirlar siz bilan tezda bog'lanishadi.\nAgar shikoyat qilmoqchi bo'lsangiz "Shikoyalar 🔴" shu tugmani bosing!''',
        reply_markup=kb)


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    commands = [BotCommand(command='start', description="Botni boshlash")]
    await bot.set_my_commands(commands)


async def main() -> None:
    dp.startup.register(on_startup)
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    create_table()
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
