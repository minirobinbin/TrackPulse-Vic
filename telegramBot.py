from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters, InlineQueryHandler
from dotenv import dotenv_values

from tracemalloc import stop
from discord.ext import commands, tasks
from discord import app_commands
import discord
import json
import requests
import re
import asyncio
import threading
import queue
from datetime import datetime
import time
import csv
import random
import pandas as pd
from typing import Literal, Optional
import typing
import enum
from re import A
from io import StringIO

from utils.search import *
from utils.colors import *
from utils.stats.stats import *
from utils.pageScraper import *
from utils.trainImage import *
from utils.checktype import *
from utils.rareTrain import *
from utils.montagueAPI import *
from utils.map.map import *
from utils.game.lb import *
from utils.trainlogger.main import *
from utils.trainset import *
from utils.trainlogger.stats import *
from utils.trainlogger.ids import *
from utils.unixtime import *
from utils.pastTime import *
from utils.routeName import *
from utils.trainlogger.graph import *
import zipfile

# ENV READING
config = dotenv_values(".env")

TELEGRAM_TOKEN = config['TELEGRAM_TOKEN']


# station autocompleat
file = open('utils\\stations.txt','r')
stations_list = []
for line in file:
    line = line.strip()
    stations_list.append(line)
file.close()

# Define command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! Welcome to the bot.')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)
    
# Command handler for adding train logs
async def logtrain(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Please provide the required parameters: <number> <line> Optional: <start> <end> <date>")
        return

    number = args[0]
    line = args[1]
    start = args[2] if len(args) > 2 else 'N/A'
    end = args[3] if len(args) > 3 else 'N/A'
    date = args[4] if len(args) > 4 else 'today'


    current_time = time.localtime()
    if date.lower() == 'today':
        savedate = time.strftime("%Y-%m-%d", current_time)
    else:
        try:
            savedate = time.strptime(date, "%d/%m/%Y")
            savedate = time.strftime("%Y-%m-%d", savedate)
        except ValueError:
            await update.message.reply_text(f'Invalid date: {date}\nMake sure to use a possible date.')
            return
        except TypeError:
            await update.message.reply_text(f'Invalid date: {date}\nUse the form `dd/mm/yyyy`')
            return
        
    # replace - with a space
    start = start.replace("-", " ").title()
    end = end.replace("-", " ").title()
    line = line.replace("-", " ").title()
        
    # Checking if train number is valid
    set = setNumber(number.upper())
    if set is None:
        await update.message.reply_text(f'Invalid train number: {number.upper()}')
        return
    type = trainType(number.upper())

    # Add train to the list
    id = addTrain(update.message.from_user.username, set, type, savedate, line, start.title(), end.title())
    await update.message.reply_text(f"Added {set} ({type}) on the {line} line on {savedate} from {start.title()} to {end.title()} to your file. (Log ID `#{id}`)")

# train logger reader
vLineLines = ['Geelong/Warrnambool', 'Ballarat/Maryborough/Ararat', 'Bendigo/Echuca/Swan Hill','Albury', 'Seymour/Shepparton', 'Traralgon/Bairnsdale']

async def viewlogs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    async def sendLogs():
        args = context.args
        mode = args[0] if len(args) > 0 else 'train'
        # for train  
        if mode == 'train': 
            try:
                with open(f'utils/trainlogger/userdata/{update.message.from_user.username}.csv', 'rb') as file:
                    await update.message.reply_document(document=file, caption=f"{update.message.from_user.username}'s Trip Logs", filename=f"{update.message.from_user.username}_logs.csv")
            except FileNotFoundError:

                await update.message.reply_text("This user has no trains logged!")
                return
            print(update.message.from_user.username)
            data = readLogs(update.message.from_user.username)
            if data == 'no data':
                await update.message.reply_text("You have no trains logged!")
                return
            
            formatted_data = ""
            for sublist in data:
                if len(sublist) >= 7:  # Ensure the sublist has enough items
                    image = None
                    
                    # thing to find image:
                    hyphen_index = sublist[1].find("-")
                    if hyphen_index != -1:
                        first_car = sublist[1][:hyphen_index]
                        print(f'First car: {first_car}')
                        image = getImage(first_car)
                        if image == None:
                            last_hyphen = sublist[1].rfind("-")
                            if last_hyphen != -1:
                                last_car = sublist[1][last_hyphen + 1 :]  # Use last_hyphen instead of hyphen_index
                                print(f'Last car: {last_car}')
                                image = getImage(last_car)
                                if image == None:
                                    image = getImage(sublist[2])
                                    print(f'the loco number is: {sublist[1]}')
                                    
                    message = f"Log {sublist[0]}\n"
                    message += f'Set: {sublist[1]} ({sublist[2]})\n'
                    message += f'Line: {sublist[4]}\n'
                    message += f'Date: {sublist[3]}\n'
                    message += f'Trip Start: {sublist[5]}\n'
                    message += f'Trip End: {sublist[6]}'
                    if sublist[4] not in vLineLines and sublist[5] != 'N/A' and sublist[6] != 'N/A':
                        try:
                            message +=  f'\nDistance: {round(getStationDistance(load_station_data("utils/trainlogger/stationDistances.csv"), sublist[5], sublist[6]))}km'
                        except:
                            pass
                    if image != None:
                        message += f'\n{image}'

                    await update.message.reply_text(message, disable_notification=True)
                    time.sleep(0.5)

        # for tram:
        if mode == 'tram':
            try:
                with open(f'utils/trainlogger/userdata/tram/{update.message.from_user.username}.csv', 'rb') as file:
                    await update.message.reply_document(document=file, caption=f"{update.message.from_user.username}'s Tram Logs", filename=f"{update.message.from_user.username}_tramlogs.csv")
            except FileNotFoundError:
                await update.message.reply_text("This user has no trams logged!")
                return
            print(update.message.from_user.username)
            data = readTramLogs(update.message.from_user.username)
            if data == 'no data':
                await update.message.reply_text("You have no trains logged!")
                return
            
            formatted_data = ""
            for sublist in data:
                if len(sublist) >= 7:  # Ensure the sublist has enough items
                    image = None
                    
                    # thing to find image:
                    hyphen_index = sublist[1].find("-")
                    # if hyphen_index != -1:
                    #     first_car = sublist[1][:hyphen_index]
                    #     print(f'First car: {first_car}')
                    #     image = getImage(first_car)
                    #     if image == None:
                    #         last_hyphen = sublist[1].rfind("-")
                    #         if last_hyphen != -1:
                    #             last_car = sublist[1][last_hyphen + 1 :]  # Use last_hyphen instead of hyphen_index
                    #             print(f'Last car: {last_car}')
                    #             image = getImage(last_car)
                    #             if image == None:
                    #                 image = getImage(sublist[2])
                    #                 print(f'the loco number is: {sublist[1]}')
                                    
                    message = f"Log {sublist[0]}\n"
                    message += f'Set: {sublist[1]} ({sublist[2]})\n'
                    message += f'Line: {sublist[4]}\n'
                    message += f'Date: {sublist[3]}\n'
                    message += f'Trip Start: {sublist[5]}\n'
                    message += f'Trip End: {sublist[6]}'
                    if sublist[4] not in vLineLines and sublist[5] != 'N/A' and sublist[6] != 'N/A':
                        try:
                            message +=  f'\nDistance: {round(getStationDistance(load_station_data("utils/trainlogger/stationDistances.csv"), sublist[5], sublist[6]))}km'
                        except:
                            pass
                    if image != None:
                        message += f'\n{image}'

                    await update.message.reply_text(message, disable_notification=True)
                    time.sleep(0.5)

            
            
            # for nsw train:
        if mode == 'nswtrain':
            try:
                with open(f'utils/trainlogger/userdata/sydney-trains/{update.message.from_user.username}.csv', 'rb') as file:
                    await update.message.reply_document(document=file, caption=f"{update.message.from_user.username}'s NSW Train Logs", filename=f"{update.message.from_user.username}_tramlogs.csv")
            except FileNotFoundError:
                await update.message.reply_text("This user has no trams logged!")
                return
            print(update.message.from_user.username)
            data = readSydneyTrainLogs(update.message.from_user.username)
            if data == 'no data':
                await update.message.reply_text("You have no trains logged!")
                return
            
            formatted_data = ""
            for sublist in data:
                if len(sublist) >= 7:  # Ensure the sublist has enough items
                    image = None
                    
                    # thing to find image:
                    hyphen_index = sublist[1].find("-")
                    # if hyphen_index != -1:
                    #     first_car = sublist[1][:hyphen_index]
                    #     print(f'First car: {first_car}')
                    #     image = getImage(first_car)
                    #     if image == None:
                    #         last_hyphen = sublist[1].rfind("-")
                    #         if last_hyphen != -1:
                    #             last_car = sublist[1][last_hyphen + 1 :]  # Use last_hyphen instead of hyphen_index
                    #             print(f'Last car: {last_car}')
                    #             image = getImage(last_car)
                    #             if image == None:
                    #                 image = getImage(sublist[2])
                    #                 print(f'the loco number is: {sublist[1]}')
                                    
                    message = f"Log {sublist[0]}\n"
                    message += f'Set: {sublist[1]} ({sublist[2]})\n'
                    message += f'Line: {sublist[4]}\n'
                    message += f'Date: {sublist[3]}\n'
                    message += f'Trip Start: {sublist[5]}\n'
                    message += f'Trip End: {sublist[6]}'
                    if sublist[4] not in vLineLines and sublist[5] != 'N/A' and sublist[6] != 'N/A':
                        try:
                            message +=  f'\nDistance: {round(getStationDistance(load_station_data("utils/trainlogger/stationDistances.csv"), sublist[5], sublist[6]))}km'
                        except:
                            pass
                    if image != None:
                        message += f'\n{image}'

                    await update.message.reply_text(message, disable_notification=True)
                    time.sleep(0.5) 
    asyncio.create_task(sendLogs())



def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("logtrain", logtrain))
    app.add_handler(CommandHandler("viewlogs", viewlogs))

    # Start the bot
    app.run_polling()

if __name__ == '__main__':
    main()
