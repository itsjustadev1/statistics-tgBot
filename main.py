import sqlite3
import threading
from update import UpdateInfo
import time
import schedule
from datetime import datetime, timezone
from sqlite import Table
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from emojis import encode
from requests import get
import json
import requests
import bs4Parsing
from addInformation import addInform
from convertToXlsx import convert
import aiogram
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

lang = "eng"
greetings = encode(
    'Ready for work! :muscle: Please select one of the buttons to tell me what you need! Or you can immediately type the channel id you are interested in to view Info or to Add a new one:innocent:\nWith this Bot you can get information about channels in xlsx tables\nAll information will be updated every 15min automatically and added to all existing tables')
s = requests.Session()

if lang == "eng":
    addChannelButton = "/addChannel"
    showStatisticsButton = "/countUsers"
if lang == "rus":
    addChannelButton = "Добавить канал"
    showStatisticsButton = "Показать число пользователей"

button1 = KeyboardButton(addChannelButton)
button2 = KeyboardButton(showStatisticsButton)
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
greet_kb.add(button1, button2)

Table().create_username_table()

thread1 = threading.Thread(target=UpdateInfo)
thread1.start()


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    Table().create_all_channels_table(message.from_user.username)
    Table().get_user_id(message.from_user.username)

    await message.reply(greetings, reply_markup=greet_kb)


@dp.message_handler(commands=['addChannel'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.from_user.id, "type public channel id without @ like in following example:\nyourchannel\nIf you've already added this channel you will receive the last statistics for it")


@dp.message_handler(commands=['countUsers'])
async def process_start_command(message: types.Message):
    addInform()
    await bot.send_message(message.from_user.id, "users counted for all added channels\nYou can view statistics for one of them by typing channel id like:\nyourchannel")


@dp.message_handler(commands=['help'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Bot will recognize only existing channels id's. If you don't receive an answer that means bot haven't found this channel in public web")


@dp.message_handler()
async def process_start_command(message: types.Message):

    now = datetime.now(timezone.utc).astimezone()
    time_format = "%H:%M/%d.%m"
    thisDate = now.strftime(time_format)

    idChannel = message.text
    number = bs4Parsing.countUsers(idChannel)[0]
    nameChannel = bs4Parsing.countUsers(idChannel)[1]
    item = (thisDate, idChannel, nameChannel, number)

    Table()
    array_channels = Table().get_channels_id(message.from_user.username)
    if array_channels == []:
        await bot.send_message(message.from_user.id, encode("channel added :white_check_mark:"))
    i = 0
    for el in array_channels:

        if idChannel in el:
            convert(idChannel)
            doc = open(f'xlsx/{idChannel}.xlsx', 'rb')
            await bot.send_document(message.chat.id, doc)
            # dfadsfagagasgg
        else:
            i += 1
            if i == len(array_channels):
                await bot.send_message(message.from_user.id, encode("channel added :white_check_mark:"))

    Table().create_table(message.from_user.username, idChannel)
    Table().insert(item, message.from_user.username, idChannel)
    Table().insert_in_all_channels_table(message.from_user.username, idChannel)
    Table().close()

    # for el in array_statistics:
    #     if idChannel in array_statistics:
    #
    #         # СДЕЛАТЬ СТАТИСТИКУ ЗДЕСЬ В ЭКСЕЛЕ!!!!!!!!!!!!!!!!
    #     else:
    #         #     answerString = str(el[4]) + ' users ' + 'on ' + \
    #         #         str(el[1]) + ' ' + str(el[2])
    #         await bot.send_message(message.from_user.id, "channel added")


if __name__ == "__main__":

    executor.start_polling(dp)
