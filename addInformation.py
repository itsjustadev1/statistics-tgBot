import sqlite3
import time
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
import collections.abc


def addInform():

    now = datetime.now(timezone.utc).astimezone()
    time_format = "%H:%M/%d.%m"
    thisDate = now.strftime(time_format)
    Table().create_username_table()
    username = Table().user()

    idChannelArray = Table().get_channels_id(username)
    if idChannelArray and isinstance(idChannelArray, collections.abc.Sequence):
        for idChannel in idChannelArray:
            number = bs4Parsing.countUsers(idChannel[0])[0]
            nameChannel = bs4Parsing.countUsers(idChannel[0])[1]
            item = (thisDate, idChannel[0], nameChannel, number)
            Table().create_table(username, idChannel[0])
            Table().insert(item, username, idChannel[0])
            Table().insert_in_all_channels_table(username, idChannel[0])
            Table().close()

    print("information updated")
    return 0


addInform()
