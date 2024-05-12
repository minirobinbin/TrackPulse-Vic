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

from utils.search import *
from utils.colors import *
from utils.stats import *
from utils.pageScraper import *
from utils.trainImage import *
from utils.checktype import *
from utils.rareTrain import *
from utils.montagueAPI import *
from utils.map.map import *
from utils.game.lb import *
from utils.trainlogger.main import *
from utils.trainset import *

rareCheckerOn = False

# ENV READING
config = dotenv_values(".env")

BOT_TOKEN = config['BOT_TOKEN']
CHANNEL_ID = int(config['CHANNEL_ID']) # channel id to send the startup message
COMMAND_PREFIX = config['COMMAND_PREFIX']
USER_ID = config['USER_ID']

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=discord.Intents.all())
log_channel = bot.get_channel(CHANNEL_ID)

channel_game_status = {} #thing to store what channels are running the guessing game

def convert_to_unix_time(date: datetime) -> str:
    # Get the end date
    end_date = date

    # Get a tuple of the date attributes
    date_tuple = (end_date.year, end_date.month, end_date.day, end_date.hour, end_date.minute, end_date.second)

    # Convert to unix time
    return f'<t:{int(time.mktime(datetime(*date_tuple).timetuple()))}:R>'

@bot.event
async def on_ready():
    print("Bot started")
    channel = bot.get_channel(CHANNEL_ID)
    with open('logs.txt', 'a') as file:
        file.write(f"\n{datetime.now()} - Bot started")
    await channel.send(f"<@{USER_ID}> Bot is online! {convert_to_unix_time(datetime.now())}")
    try:
        task_loop.start()
    except:
        print("WARNING: Rare train checker is not enabled!")
        await channel.send("WARNING: Rare train checker is not enabled! <@{USER_ID}>")
        

# Threads

# Rare train finder
def check_rare_trains_in_thread():
    rare_trains = checkRareTrainsOnRoute()
    asyncio.run_coroutine_threadsafe(log_rare_trains(rare_trains), bot.loop)

async def log_rare_trains(rare_trains):
    log_channel = bot.get_channel(1227224314483576982)
    channel = bot.get_channel(1227039212553900204)

    if rare_trains:
        embed = discord.Embed(title="Trains found on lines they are not normally on!", color=0xf23f42)

        for route in rare_trains:
            parts = route.split(' - Train ')
            route_name = parts[0]
            train_type = parts[1]
            
            # Extract the train name and train info from train_type
            train_name, train_info = train_type.split('\n') if '\n' in train_type else ('Unknown train name', 'Unknown train type')

            embed.add_field(name=route_name, value=f"{train_name}\n{train_info}", inline=True)

        try:
            await channel.send(embed=embed)
            with open('logs.txt', 'a') as file:
                file.write(f"\n{datetime.now()} - Sent rare trains")
        except discord.HTTPException:
            await channel.send("Embed too big! There are many trains on the wrong line. Check ANYTRIP.")
            with open('logs.txt', 'a') as file:
                file.write(f"\n{datetime.now()} - Sent rare trains but it was too long")
        await channel.send('<@&1227171023795781694> Trains found on lines they are not normally on!\n`Due to errors in the PTV api data out of our control, some data may be inaccurate.`')
    else:
        await log_channel.send("None found")



@tasks.loop(minutes=10)
async def task_loop():
    if rareCheckerOn:
        log_channel = bot.get_channel(1227224314483576982)
        await log_channel.send("Checking for trains on lines they aren't meant for")
        with open('logs.txt', 'a') as file:
            file.write(f"\n{datetime.now()} - Checking for rare trains")

        # Create a new thread to run checkRareTrainsOnRoute
        thread = threading.Thread(target=check_rare_trains_in_thread)
        thread.start()
    else:
        print("Rare checker not enabled!")



    

    
@bot.tree.command(name="metro-line", description="Show info about a Metro line")
@app_commands.describe(line = "What Metro line to show info about?")
@app_commands.choices(line=[
        app_commands.Choice(name="Alamein", value="Alamein"),
        app_commands.Choice(name="Belgrave", value="Belgrave"),
        app_commands.Choice(name="Craigieburn", value="Craigieburn"),
        app_commands.Choice(name="Cranbourne", value="Cranbourne"),
        app_commands.Choice(name="Frankston", value="Frankston"),
        app_commands.Choice(name="Glen Waverley", value="Glen%20Waverley"),
        app_commands.Choice(name="Hurstbridge", value="Hurstbridge"),
        app_commands.Choice(name="Lilydale", value="Lilydale"),
        app_commands.Choice(name="Mernda", value="Mernda"),
        app_commands.Choice(name="Pakenham", value="Pakenham"),
        app_commands.Choice(name="Sandringham", value="Sandringham"),
        app_commands.Choice(name="Stony Point", value="Stony%20Point"),
        app_commands.Choice(name="Sunbury", value="Sunbury"),
        app_commands.Choice(name="Upfield", value="Upfield"),
        app_commands.Choice(name="Werribee", value="Werribee"),
])

async def line_info(ctx, line: str):
    json_info_str = route_api_request(line, "0")
    json_info_str = json_info_str.replace("'", "\"")  # Replace single quotes with double quotes
    json_info = json.loads(json_info_str)
    
    routes = json_info['routes']
    status = json_info['status']
    version = status['version']
    health = status['health']
    
    route = routes[0]
    route_service_status = route['route_service_status']
    description = route_service_status['description']
    timestamp = route_service_status['timestamp']
    route_type = route['route_type']
    route_id = route['route_id']
    route_name = route['route_name']
    route_number = route['route_number']
    route_gtfs_id = route['route_gtfs_id']
    geopath = route['geopath']
    
    print(f"route id: {route_id}")
    
    
    # disruption info
    disruptionDescription = ""
    try:
        # print(disruption_api_request(route_id))
        disruptions = disruption_api_request(route_id)
        print(disruptions)
        
        # Extracting title and description
        general_disruption = disruptions["disruptions"]["metro_train"][0]
        disruptionTitle = general_disruption["title"]
        disruptionDescription = general_disruption["description"]

        # print("Title:", title)
        # print("Description:", description)
        
    except Exception as e:
        # await ctx.response.send_message(f"error:\n`{e}`")
        print(e)

    color = genColor(description)
    print(f"Status color: {color}")
    
    
    embed = discord.Embed(title=f"Route Information - {route_name}", color=color)
    embed.add_field(name="Route Name", value=route_name, inline=False)
    embed.add_field(name="Status Description", value=description, inline=False)
    if disruptionDescription:
        embed.add_field(name="Disruption Info",value=disruptionDescription, inline=False)

    
    await ctx.response.send_message(embed=embed)
    with open('logs.txt', 'a') as file:
                file.write(f"\n{datetime.now()} - user sent line info command with input {line}")

# @bot.tree.command(name="vline-line", description="Show info about a V/Line line")
# @app_commands.describe(vline_line = "What V/Line line to show info about?")
# @app_commands.choices(vline_line=[
#         app_commands.Choice(name="Geelong", value="Geelong%20Melbourne"),
#         app_commands.Choice(name="Ballarat", value="Ballarat%20Melbourne"),
#         app_commands.Choice(name="Gippsland", value="Gippsland%20Melbourne"),
#         app_commands.Choice(name="Seymour", value="Seymour%20Melbourne"),

# ])

# async def vline_line_info(ctx, vline_line: str):
#     json_info_str = route_api_request(vline_line, "3")
#     json_info_str = json_info_str.replace("'", "\"")  # Replace single quotes with double quotes
#     json_info = json.loads(json_info_str)
    
#     routes = json_info['routes']
#     status = json_info['status']
#     version = status['version']
#     health = status['health']
    
#     route = routes[0]
#     route_service_status = route['route_service_status']
#     description = route_service_status['description']
#     timestamp = route_service_status['timestamp']
#     route_type = route['route_type']
#     route_id = route['route_id']
#     route_name = route['route_name']
#     route_number = route['route_number']
#     route_gtfs_id = route['route_gtfs_id']
#     geopath = route['geopath']

#     color = genColor(description)
#     print(f"Status color: {color}")
    
    
#     embed = discord.Embed(title=f"Route Information - {route_name}", color=color)
#     embed.add_field(name="Route Name", value=route_name, inline=False)
#     embed.add_field(name="Status Description", value=description, inline=False)
    
#     await ctx.response.send_message(embed=embed)


@bot.tree.command(name="run_search", description="Show runs for a route")
@app_commands.describe(runid = "route id")
async def runs(ctx, runid: str):
    
    api_response = runs_api_request(runid)
    json_response = json.dumps(api_response)
    data = json.loads(json_response)

    # Extract relevant information from runs with vehicle data
    vehicle_data = []
    for run in data['runs']:
        if run['vehicle_position']:
            vehicle_info = {
                'run_id': run['run_id'],
                'latitude': run['vehicle_position']['latitude'],
                'longitude': run['vehicle_position']['longitude'],
                'direction': run['vehicle_position']['direction'],
                'operator': run['vehicle_descriptor']['operator'],
                'description': run['vehicle_descriptor']['description']
            }
            vehicle_data.append(vehicle_info)
    for vehicle_info in vehicle_data:
        print(vehicle_info)
    
    embed = discord.Embed(title=f"Route Information - ", color=0x0e66ad)
    for vehicle_info in vehicle_data:
        embed.add_field(name="Train type:", value=vehicle_info["description"], inline=False)    
    
    await ctx.response.send_message(embed=embed)
    with open('logs.txt', 'a') as file:
                file.write(f"\n{datetime.now()} - user sent run search command with input {runid}")
    
    
 


# # commend to show route types:
# @bot.tree.command(name="route_types", description="Show numbers for each route type")
# async def route_types(ctx):
#     embed = discord.Embed(title="Route type numbers")
#     embed.add_field(name="Metro Train", value="`0`")
#     embed.add_field(name="Tram",value="`1`")
#     embed.add_field(name="Bus",value="`2`")
#     embed.add_field(name="V/line Train",value="`3`")
#     embed.add_field(name="Night Bus",value="`4`")
#     await ctx.response.send_message(embed=embed)
    

# bus route search
'''@bot.tree.command(name="bus_route", description="Show info about a bus route")
@app_commands.describe(line = "What bus route to show info about?")


async def bus_route(ctx, line: str):
    try:
        json_info_str = route_api_request(line, "2")
        json_info_str = json_info_str.replace("'", "\"")  # Replace single quotes with double quotes
        json_info = json.loads(json_info_str)
        
        channel = ctx.channel
        await ctx.response.send_message(f"Results for {line}")
        # embed = discord.Embed(title=f"Bus routes matching `{line}`:", color=0xff8200)
        counter = 0
        for route in json_info['routes']:

            routes = json_info['routes']
            status = json_info['status']
            version = status['version']
            health = status['health']
        
        
            route = routes[counter]
            route_service_status = route['route_service_status']
            description = route_service_status['description']
            timestamp = route_service_status['timestamp']
            route_type = route['route_type']
            route_id = route['route_id']
            route_name = route['route_name']
            route_number = route['route_number']
            route_gtfs_id = route['route_gtfs_id']
            geopath = route['geopath']

            embed = discord.Embed(title=f"Bus route {route_number}:", color=0xff8200)
            embed.add_field(name="Route Name", value=f"{route_number} - {route_name}", inline=False)
            embed.add_field(name="Status Description", value=description, inline=False)

            await channel.send(embed=embed)
            print(f"sent route {route_name}")
            counter = counter + 1
    except Exception as e:
        await ctx.response.send_message(f"error:\n`{e}`\nMake sure you inputted a valid bus route number, otherwise, the bot is broken.")'''


# Route Seach v2
@bot.tree.command(name="route", description="Show info about a tram or bus route")
@app_commands.describe(rtype = "What type of transport is this route?")
@app_commands.choices(rtype=[
        app_commands.Choice(name="Tram", value="1"),
        # app_commands.Choice(name="Metro Train", value="0"),
        app_commands.Choice(name="Bus", value="2"),
        # app_commands.Choice(name="VLine Train", value="3"),
        app_commands.Choice(name="Night Bus", value="4"),
])
@app_commands.describe(number = "What route number to show info about?")

async def route(ctx, rtype: str, number: int):    
    try:
        json_info_str = route_api_request(number, rtype)
        json_info_str = json_info_str.replace("'", "\"")  # Replace single quotes with double quotes
        json_info = json.loads(json_info_str)
        
        channel = ctx.channel
        await ctx.response.send_message(f"Results for {number}:")
        # embed = discord.Embed(title=f"Bus routes matching `{line}`:", color=0xff8200)
        counter = 0
        for route in json_info['routes']:

            routes = json_info['routes']
            status = json_info['status']
            version = status['version']
            health = status['health']
        
        
            route = routes[counter]
            route_service_status = route['route_service_status']
            description = route_service_status['description']
            timestamp = route_service_status['timestamp']
            route_type = route['route_type']
            route_id = route['route_id']
            route_name = route['route_name']
            route_number = route['route_number']
            route_gtfs_id = route['route_gtfs_id']
            geopath = route['geopath']
            
             # disruption info
            disruptionDescription = ""
            try:
                disruptions = disruption_api_request(route_id)
                # print(disruptions)
                
                # Extracting title and description
                general_disruption = disruptions["disruptions"]["metro_bus"][0]
                disruptionTitle = general_disruption["title"]
                disruptionDescription = general_disruption["description"]


                
            except Exception as e:
                print(e)

            
            # disruption status:

             # Check if the route number is the one you want
            if route_number == str(number):
                # Create and send the embed only for the desired route number
                embed = discord.Embed(title=f"Route {route_number}:", color=getColor(rtype))
                embed.add_field(name="Route Name", value=f"{route_number} - {route_name}", inline=False)
                embed.add_field(name="Status Description", value=description, inline=False)
                if disruptionDescription:
                    embed.add_field(name="Disruption Info",value=disruptionDescription, inline=False)
                    
                await channel.send(embed=embed)
                with open('logs.txt', 'a') as file:
                    file.write(f"\n{datetime.now()} - user sent route search command with input {rtype}, {number}")
                                
            counter = counter + 1
                
    except Exception as e:
        await ctx.response.send_message(f"error:\n`{e}`\nMake sure you inputted a valid route number, otherwise, the bot is broken.")
        with open('logs.txt', 'a') as file:
                    file.write(f"\n{datetime.now()} - ERROR with user command - user sent route search command with input {rtype}, {number}")



# Photo search
@bot.tree.command(name="train_photo", description="Search for xm9g's railway photos")
@app_commands.describe(number="Carriage number")
async def line_info(ctx, number: str):
    channel = ctx.channel
    search_query = number.upper()
    photo_url = f"https://railway-photos.xm9g.xyz/photos/{search_query}.jpg"
    await ctx.response.send_message(f"Searching for `{search_query}`...")

   

    # Make a HEAD request to check if the photo exists
    URLresponse = requests.head(photo_url)
    if URLresponse.status_code == 200:
        await channel.send(photo_url)
    else:
        mAdded = search_query+'M'
        
        
        # try with m added
        photo_url = f"https://railway-photos.xm9g.xyz/photos/{mAdded}.jpg"
        URLresponse = requests.head(photo_url)
        if URLresponse.status_code == 200:
            await channel.send(photo_url)
            for i in range(2,5):
                photo_url = f"https://railway-photos.xm9g.xyz/photos/{mAdded}-{i}.jpg"
                print(f"searching for other images for {mAdded}")
                print(f"url: {photo_url}")
                URLresponse = requests.head(photo_url)
                if URLresponse.status_code == 200:
                    await channel.send(photo_url)
                else:
                    print("no other images found")
                    await channel.send(f"Photo not in xm9g database!")
                    break

        
        
    for i in range(2,5):
        photo_url = f"https://railway-photos.xm9g.xyz/photos/{search_query}-{i}.jpg"
        print(f"searching for other images for {search_query}")
        print(f"url: {photo_url}")
        URLresponse = requests.head(photo_url)
        if URLresponse.status_code == 200:
            await channel.send(photo_url)
        else:
            print("no other images found")
            break


# Wongm search
@bot.tree.command(name="wongm", description="Search Wongm's Rail Gallery")
@app_commands.describe(search="search")
async def line_info(ctx, search: str):
    channel = ctx.channel
    print(f"removing spaces in search {search}")
    spaces_removed = search.replace(' ', '%20')
    print(spaces_removed)
    url = f"https://railgallery.wongm.com/page/search/?s={spaces_removed}"
    await ctx.response.send_message(url)



# Train search
@bot.tree.command(name="train_search", description="Find trips for a specific Metro train")
@app_commands.describe(train="train")
async def train_line(ctx, train: str):
    await ctx.response.send_message(f"Searching, trip data may take longer to send...")
    channel = ctx.channel
    type = trainType(train)
    print(f"TRAINTYPE {type}")
    if type == None:
        await channel.send("Train not found")
        
    else:
        embed = discord.Embed(title=f"Info for {train.upper()}:", color=0x0070c0)
        
        embed.add_field(name="Type:", value=type)
        if train.upper() == "7005": # Only old livery sprinter
            embed.set_thumbnail(url="https://xm9g.xyz/discord-bot-assets/MPTB/Sprinter-VLine.png")
        else:
            embed.set_thumbnail(url=getIcon(type))
        embed.set_image(url=getImage(train.upper()))
    
        # additional embed fields:
        embed.add_field(name="Source:", value=f"[TransportVic (Data)](https://vic.transportsg.me/metro/tracker/consist?consist={train.upper()})\n[XM9G (Image)](https://railway-photos.xm9g.xyz#:~:text={train.upper()})\n[MPTG (Icon)](https://melbournesptgallery.weebly.com/melbourne-train-and-tram-fronts.html)", inline=False)
        await channel.send(embed=embed)
        
        # seperated the runs to a seperate thing cause its slow
        embed = discord.Embed(title=f"Current runs for {train.upper()}:", color=0x0070c0)

        # Run transportVicSearch in a separate thread
        loop = asyncio.get_event_loop()
        task = loop.create_task(transportVicSearch_async(ctx, train.upper()))
        await task

async def transportVicSearch_async(ctx, train):
    embed = discord.Embed(title=f"Current runs for {train.upper()}:", color=0x0070c0)

    runs = await asyncio.to_thread(transportVicSearch, train)  # find runs in a separate thread
    if isinstance(runs, list):
        print("thing is a list")
        for i, run in enumerate(runs):
            embed.add_field(name=f"Trip {i+1}", value=run, inline=False)
        await ctx.channel.send(embed=embed)
    else:
        await ctx.channel.send(f"No runs currently found for {train.upper()}")



# Montague Bridge search
@bot.tree.command(name="days-since-montague-hit", description="See how many days it has been since the Montague Street bridge has been hit.")
async def train_line(ctx):
    await ctx.response.send_message(f"Checking...")
    channel = ctx.channel
    
    embed = discord.Embed(title=f"How many days since the Montague Street bridge has been hit?", color=0xd8d800)
    # embed.set_image(url=getImage(train.upper()))
    
    # Create a new thread to call the function
    days_queue = queue.Queue()
    thread = threading.Thread(target=montagueDays, args=(days_queue,))
    thread.start()

    thread.join()
    # Retrieve the result from the queue
    days = days_queue.get()
    
    api_queue = queue.Queue()
    thread = threading.Thread(target=montagueAPI, args=(api_queue,))    
    thread.start()
    thread.join()
    
    apiData = api_queue.get()
    
    # Extract individual variables from the apis data
    date = apiData["date"]
    thanks = apiData["thanks"]
    streak = apiData["streak"]
    chumps = apiData["chumps"]
    name = chumps[0]['name'] # get name from the chumps thing
    image = apiData["image"]
    thumb = apiData["thumb"]
    date_year = apiData["date_year"]
    date_week = apiData["date_week"]
    date_aus_string = apiData["date_aus_string"]
    
    embed.add_field(name=f"{days} days", value='\u200b', inline=False)

    embed.add_field(name="Current Champion:", value=name)
    embed.add_field(name="Date:", value=date)
    embed.set_image(url=f'https://howmanydayssincemontaguestreetbridgehasbeenhit.com{image}')
    
    embed.set_author(name='howmanydayssincemontaguestreetbridgehasbeenhit.com', url="https://howmanydayssincemontaguestreetbridgehasbeenhit.com")
    await ctx.channel.send(embed=embed)
    
# the map thing
# IMPORTANT: Make this a thread!
'''@bot.tree.command(name="map", description="testing")
async def map(ctx):
    channel = ctx.channel
    await ctx.response.send_message("Generating Map, please wait", ephemeral=True)

    genMap()
    file = discord.File("utils/map/gen.png", filename="gen.png")
    embed = discord.Embed(title='Metro Trains Location', color=0x5865f2)
    embed.set_image(url="attachment://gen.png")
    await channel.send(file=file, embed=embed)'''
    
@bot.tree.command(name="station-guesser", description="Play a game where you guess what train station is in the photo.")
@app_commands.describe(rounds = "The number of rounds. Defaults to 1.", ultrahard = "Ultra hard mode.")
async def game(ctx, ultrahard: bool=False, rounds: int = 1):
    
    channel = ctx.channel
    async def run_game():

        # Check if a game is already running in this channel
        if channel in channel_game_status and channel_game_status[channel]:
            await ctx.response.send_message("A game is already running in this channel.", ephemeral=True )
            return
        if rounds > 25:
            await ctx.response.send_message("You can only play a maximum of 25 rounds!", ephemeral=True )
            return

        channel_game_status[channel] = True
        
        # Define the CSV file path
        if ultrahard:
            csv_file = 'utils/game/ultrahard/images.csv'
        else:
            csv_file = 'utils/game/images.csv'

        # Read the CSV file and store rows in a list
        rows = []
        with open(csv_file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                rows.append(row)

        # Remove the header row if present
        header = rows[0]
        data = rows[1:]

        for round in range(rounds):
            # Get a random row
            random_row = random.choice(data)

            # Extract data from the random row
            url = random_row[0]
            station = random_row[1]
            difficulty = random_row[2]
            credit = random_row[3]

            if ultrahard:
                embed = discord.Embed(title=f"[ULTRARD] Guess the station!", color=0xe52727, description="Type ! before your answer. You have 30 seconds to answer.")
            else:
                embed = discord.Embed(title=f"Guess the station!", description="Type ! before your answer. You have 30 seconds to answer.")
                if difficulty == 'Very Easy':
                    embed.color = 0x89ff65
                elif difficulty == 'Easy':
                    embed.color = 0xcaff65
                elif difficulty == 'Medium':
                    embed.color = 0xffe665
                elif difficulty == 'Hard':
                    embed.color = 0xffa665
                elif difficulty == 'Very Hard':
                    embed.color = 0xff6565
            
            embed.set_image(url=url)
            embed.add_field(name='Difficulty', value=difficulty)
            embed.set_footer(text=f"Photo by {credit}. DM @xm9g to submit a photo")
            embed.set_author(name=f"Round {round+1}/{rounds}")

            # Send the embed message
            await ctx.response.send_message(embed=embed)

            # Define a check function to validate user input
            def check(m):
                return m.channel == channel and m.author != bot.user and m.content.startswith('!')

            try:
                correct = False
                if ultrahard:
                    gameType = 'ultrahard'
                else:
                    gameType = 'guesser'
                
                
                while not correct:
                    # Wait for user's response in the same channel
                    user_response = await bot.wait_for('message', check=check, timeout=30.0)
                    
                    # Check if the user's response matches the correct station
                    if user_response.content[1:].lower() == station.lower():
                        if ultrahard:
                            await ctx.channel.send(f"{user_response.author.mention} guessed it right!")
                        else:
                            await ctx.channel.send(f"{user_response.author.mention} guessed it right! {station.title()} was the correct answer!")
                        correct = True
                        if ultrahard:
                            addLb(user_response.author.id, user_response.author.name, 'ultrahard')
                        else:
                            addLb(user_response.author.id, user_response.author.name, 'guesser')
                            
                    elif user_response.content.lower() == '!skip':
                        if user_response.author.id in [ctx.user.id,707866373602148363,780303451980038165] :
                            await ctx.channel.send(f"Round {round+1} skipped.")
                            break
                        else:
                            await ctx.channel.send(f"{user_response.author.mention} you can only skip the round if you were the one who started it.")
                    elif user_response.content.lower() == '!stop':
                        if user_response.author.id in [ctx.user.id,707866373602148363,780303451980038165] :
                            await ctx.channel.send(f"Game ended.")
                            return
                        else:
                            await ctx.channel.send(f"{user_response.author.mention} you can only stop the game if you were the one who started it.")    
                    else:
                        await ctx.channel.send(f"Wrong guess {user_response.author.mention}! Try again.")
                        if ultrahard:
                            addLoss(user_response.author.id, user_response.author.name, 'ultrahard')
                        else:
                            addLoss(user_response.author.id, user_response.author.name, 'guesser')
            except asyncio.TimeoutError:
                if ultrahard:
                    await ctx.channel.send(f"Times up. Answers are not revealed in ultrahard mode.")
                else:
                    await ctx.channel.send(f"Times up. The answer was ||{station.title()}||")
            finally:
                # Reset game status after the game ends
                channel_game_status[channel] = False

    # Run the game in a separate task
    asyncio.create_task(run_game())
    

    
@bot.tree.command(name="leaderboard", description="Global leaderboards for the games",)
@app_commands.describe(game="What game's leaderboard to show?")
@app_commands.choices(game=[
        app_commands.Choice(name="Station Guesser", value="guesser"),
        app_commands.Choice(name="Ultrahard Station Guesser", value="ultrahard"),
        app_commands.Choice(name="Station order game", value="domino"),

])

async def lb(ctx, game: str='guesser'):
    channel = ctx.channel
    leaders = top5(game)
    print(leaders)
    # Create the embed
    embed = discord.Embed(title=f"Top 7 players for {game}", color=discord.Color.gold())
    
    count = 1
    for item, number, losses in leaders:
        try:
            embed.add_field(name=f'{count}: {item}', value=f'Wins: {str(number)}\nLosses: {str(losses)}\nAccuracy: {str(round((number/(number+losses))*100, 1))}%', inline=False)
        except:
            embed.add_field(name=f'{count}: {item}', value=f'Wins: {str(number)}\nLosses: {str(losses)}', inline=False)
        count = count + 1
        
    await ctx.response.send_message(embed=embed)

@bot.tree.command(name="user-stats", description="Stats for a user in the guessing game")
async def userStats(ctx, user: discord.User):
    channel = ctx.channel
    print(user.name)
    stats = fetchUserStats(user.name, 'guesser')
    hardstats = fetchUserStats(user.name, 'ultrahard')
    dominostats = fetchUserStats(user.name, 'domino')


    embed = discord.Embed(title=f"{user.name.split('#')[0]}'s stats", color=discord.Color.gold())
    if stats:
        item, wins, losses = stats
        embed.add_field(name='Station Guesser', value=f'Wins: {str(wins)}\nLosses: {str(losses)}\nAccuracy: {str(round((wins/(wins+losses))*100, 1))}%', inline=False)
    if hardstats:
        item, wins, losses = hardstats
        embed.add_field(name='Ultrahard Station Guesser', value=f'Wins: {str(wins)}\nLosses: {str(losses)}\nAccuracy: {str(round((wins/(wins+losses))*100, 1))}%', inline=False)
    if dominostats:
        item, wins, losses = dominostats
        embed.add_field(name='Station Order Guesser', value=f'Wins: {str(wins)}\nLosses: {str(losses)}\nAccuracy: {str(round((wins/(wins+losses))*100, 1))}%', inline=False)
        
    await ctx.response.send_message(embed=embed)

# Station order game made by @domino

lines_dictionary = {
    'Alamein': [['Richmond', 'East Richmond', 'Burnley', 'Hawthorn', 'Glenferrie', 'Auburn', 'Camberwell', 'Riversdale', 'Willison', 'Hartwell', 'Burwood', 'Ashburton', 'Alamein'],0x01518a],
    'Belgrave': [['Richmond', 'East Richmond', 'Burnley', 'Hawthorn', 'Glenferrie', 'Auburn', 'Camberwell', 'East Camberwell', 'Canterbury', 'Chatham', 'Union', 'Box Hill', 'Laburnum', 'Blackburn', 'Nunawading', 'Mitcham', 'Heatherdale', 'Ringwood', 'Heathmont', 'Bayswater', 'Boronia', 'Ferntree Gully', 'Upper Ferntree Gully', 'Upwey', 'Tecoma', 'Belgrave'],0x01518a],
    'Craigieburn': [['North Melbourne', 'Kensington', 'Newmarket', 'Ascot Vale', 'Moonee Ponds', 'Essendon', 'Glenbervie', 'Strathmore', 'Pascoe Vale', 'Oak Park', 'Glenroy', 'Jacana', 'Broadmeadows', 'Coolaroo', 'Roxburgh Park', 'Craigieburn'],0xfcb818],
    'Cranbourne': [['Richmond', 'South Yarra', 'Malvern', 'Caulfield', 'Carnegie', 'Murrumbeena', 'Hughesdale', 'Oakleigh', 'Huntingdale', 'Clayton', 'Westall', 'Springvale', 'Sandown Park', 'Noble Park', 'Yarraman', 'Dandenong', 'Lynbrook', 'Merinda Park', 'Cranbourne'],0x00a8e4],
    'Flemington Racecourse': [['Flemington Racecourse', 'Showgrounds', 'North Melbourne', 'Southern Cross', 'Flinders Street'],0x8a8c8f],
    'Frankston': [['Flinders Street', 'Richmond', 'South Yarra', 'Hawksburn', 'Toorak', 'Armadale', 'Malvern', 'Caulfield', 'Glen Huntly', 'Ormond', 'McKinnon', 'Bentleigh', 'Patterson', 'Moorabbin', 'Highett', 'Southland', 'Cheltenham', 'Mentone', 'Parkdale', 'Mordialloc', 'Aspendale', 'Edithvale', 'Chelsea', 'Bonbeach', 'Carrum', 'Seaford', 'Kananook', 'Frankston'],0x009645],
    'Glen Waverley': [['Richmond', 'East Richmond', 'Burnley', 'Heyington', 'Kooyong', 'Tooronga', 'Gardiner', 'Glen Iris', 'Darling', 'East Malvern', 'Holmesglen', 'Jordanville', 'Mount Waverley', 'Syndal', 'Glen Waverley'],0x01518a],
    'Hurstbridge': [['Jolimont', 'West Richmond', 'North Richmond', 'Collingwood', 'Victoria Park', 'Clifton Hill', 'Westgarth', 'Dennis', 'Fairfield', 'Alphington', 'Darebin', 'Ivanhoe', 'Eaglemont', 'Heidelberg', 'Rosanna', 'Macleod', 'Watsonia', 'Greensborough', 'Montmorency', 'Eltham', 'Diamond Creek', 'Wattle Glen', 'Hurstbridge'],0xd0202e],
    'Lilydale': [['Richmond', 'East Richmond', 'Burnley', 'Hawthorn', 'Glenferrie', 'Auburn', 'Camberwell', 'East Camberwell', 'Canterbury', 'Chatham', 'Union', 'Box Hill', 'Laburnum', 'Blackburn', 'Nunawading', 'Mitcham', 'Heatherdale', 'Ringwood', 'Ringwood East', 'Croydon', 'Mooroolbark', 'Lilydale'],0x01518a],
    'Mernda': [['Jolimont', 'West Richmond', 'North Richmond', 'Collingwood', 'Victoria Park', 'Clifton Hill', 'Rushall', 'Merri', 'Northcote', 'Croxton', 'Thornbury', 'Bell', 'Preston', 'Regent', 'Reservoir', 'Ruthven', 'Keon Park', 'Thomastown', 'Lalor', 'Epping', 'South Morang', 'Middle Gorge', 'Hawkstowe', 'Mernda'],0xd0202e],
    'Pakenham': [['Richmond', 'South Yarra', 'Malvern', 'Caulfield', 'Carnegie', 'Murrumbeena', 'Hughesdale', 'Oakleigh', 'Huntingdale', 'Clayton', 'Westall', 'Springvale', 'Sandown Park', 'Noble Park', 'Yarraman', 'Dandenong', 'Hallam', 'Narre Warren', 'Berwick', 'Beaconsfield', 'Officer', 'Cardinia Road', 'Pakenham'],0x00a8e4],
    'Sandringham': [['Flinders Street', 'Richmond', 'South Yarra', 'Prahran', 'Windsor', 'Balaclava', 'Ripponlea', 'Elsternwick', 'Gardenvale', 'North Brighton', 'Middle Brighton', 'Brighton Beach', 'Hampton', 'Sandringham'],0xf17fb1],
    'Stony Point': [['Stony Point', 'Crib Point', 'Morradoo', 'Bittern', 'Hastings', 'Tyabb', 'Somerville', 'Baxter', 'Leawarra', 'Frankston'],0x009645],
    'Sunbury': [['North Melbourne', 'Footscray', 'Middle Footscray', 'West Footscray', 'Tottenham', 'Sunshine', 'Albion', 'Ginifer', 'St Albans', 'Keilor Plains', 'Watergardens', 'Diggers Rest', 'Sunbury'],0xfcb818],
    'Upfield': [['North Melbourne', 'Macaulay', 'Flemington Bridge', 'Royal Park', 'Jewell', 'Brunswick', 'Anstey', 'Moreland', 'Coburg', 'Batman', 'Merlynston', 'Fawkner', 'Gowrie', 'Upfield'],0xfcb818],
    'Werribee': [['Flinders Street', 'Southern Cross', 'North Melbourne', 'South Kensington', 'Footscray', 'Seddon', 'Yarraville', 'Spotswood', 'Newport', 'Seaholme', 'Altona', 'Westona', 'Laverton', 'Aircraft', 'Williams Landing', 'Hoppers Crossing', 'Werribee'],0x009645],
    'Williamstown': [['Flinders Street', 'Southern Cross', 'North Melbourne', 'South Kensington', 'Footscray', 'Seddon', 'Yarraville', 'Spotswood', 'Newport', 'North Williamstown', 'Williamstown Beach', 'Williamstown'],0x009645]
}
linelist = [
    None,
    'Alamein', #1
    'Belgrave', #2
    'Craigieburn', #3
    'Cranbourne', #4
    'Mernda', #5
    'Frankston', #6
    'Glen Waverley', #7
    'Hurstbridge', #8
    'Lilydale', #9
    None,
    'Pakenham', #11
    'Sandringham', #12
    None,
    'Sunbury', #14
    'Upfield', #15
    'Werribee', #16
    'Williamstown' #17
]

@bot.tree.command(name="station-game", description="A game where you list the stations before or after a station.")
@app_commands.describe(rounds = "The number of rounds. Defaults to 1.", direction = "The directions you are listing the stations in. Defaults to Up or Down.")
@app_commands.choices(
    direction=[
        app_commands.Choice(name="Up or Down", value='updown'),
        app_commands.Choice(name="Up", value='up'),
        app_commands.Choice(name="Down", value='down')
        ],
    )

async def testthing(ctx, direction: str = 'updown', rounds: int = 1):
    channel = ctx.channel
    async def run_game():
        # Check if a game is already running in this channel
        if channel in channel_game_status and channel_game_status[channel]:
            await ctx.response.send_message("A game is already running in this channel.", ephemeral=True )
            return
        if rounds > 25:
            await ctx.response.send_message("You can only play a maximum of 25 rounds!", ephemeral=True )
            return

        channel_game_status[channel] = True

        for round in range(rounds):
            # choose random number of stations
            numdirection = random.randint(2,5)

            # choose direction
            if direction == 'updown':
                direction1 = random.choice(['up','down'])
            else:
                direction1 = direction
            if direction1 == 'up':
                numdirection = numdirection*-1
            
            # choose random line
            line = None
            while line == None:
                line = linelist[random.randint(0,len(linelist)-1)]

            # choose random station
            if line == 'Flemington Racecourse':
                if numdirection == 5 or numdirection == -5:
                    numdirection = random.choice([-4,-3,-2,2,3,4])
            station = None
            while station == None:
                station = lines_dictionary[line][0][random.randint(0,len(lines_dictionary[line][0])-1)]
                if not 0 <= lines_dictionary[line][0].index(station)+numdirection <= len(lines_dictionary[line][0]):
                    station = None

            embed = discord.Embed(
                title=f"Which __**{numdirection if numdirection > 0 else numdirection*-1}**__ stations are __**{direction1}**__ from __**{station}**__ station on the __**{line} line**__?",
                description=f"**Answers must be in the correct order!** Answer using this format:\n!<station1>, <station2>{', <station3>' if numdirection >= 3 or numdirection <= -3 else ''}{', <station4>' if numdirection >= 4 or numdirection <= -4 else ''}{', <station5>' if numdirection >= 5 or numdirection <= -5 else ''}\n\n*Use !skip to skip to the next round.*",
                colour=lines_dictionary[line][1])
            embed.set_author(name=f"Round {round+1}/{rounds}")
            if round == 0:
                await ctx.response.send_message(embed=embed)
            else:
                await ctx.channel.send(embed=embed)

            # Define a check function to validate user input
            def check(m): return m.channel == channel and m.author != bot.user and m.content.startswith('!')

            # get list of correct stations
            if numdirection > 0:
                correct_list = lines_dictionary[line][0][lines_dictionary[line][0].index(station)+1:lines_dictionary[line][0].index(station)+numdirection+1]
            else:
                correct_list = lines_dictionary[line][0][lines_dictionary[line][0].index(station)+numdirection:lines_dictionary[line][0].index(station)]
                correct_list.reverse()
            correct_list1 = [x.lower() for x in correct_list]

            # the actual input part
            try:
                correct = False
                while not correct:
                    # Wait for user's response in the same channel
                    user_response = await bot.wait_for('message', check=check, timeout=30.0)
                    try:
                        response = user_response.content[1:].lower().split(',')
                        response = [x.strip() for x in response]
                    except:
                        pass

                    # Check if the user's response matches the correct station
                    if response == correct_list1:
                        await ctx.channel.send(f"{user_response.author.mention} guessed it correctly!")
                        addLb(user_response.author.id, user_response.author.name, 'domino')
                        
                        correct = True 
                    elif user_response.content.lower() == '!skip':
                        if user_response.author.id in [ctx.user.id,707866373602148363,780303451980038165] :
                            await ctx.channel.send(f"Round {round+1} skipped. The answer was ||{correct_list[0]}, {correct_list[1]}{f', {correct_list[2]}' if len(correct_list) >=3 else ''}{f', {correct_list[3]}' if len(correct_list) >=4 else ''}{f', {correct_list[4]}' if len(correct_list) >=5 else ''}||")
                            break
                        else:
                            await ctx.channel.send(f"{user_response.author.mention} you can only skip the round if you were the one who started it.")
                    elif user_response.content.lower() == '!stop':
                        if user_response.author.id in [ctx.user.id,707866373602148363,780303451980038165] :
                            await ctx.channel.send(f"Game ended.")
                            return
                        else:
                            await ctx.channel.send(f"{user_response.author.mention} you can only stop the game if you were the one who started it.")
                    else:
                        await ctx.channel.send(f"Wrong guess {user_response.author.mention}! Try again.")
                        addLoss(user_response.author.id, user_response.author.name, 'domino')
                        
            except asyncio.TimeoutError:
                await ctx.channel.send(f"Times up. The answer was ||{correct_list[0]}, {correct_list[1]}{f', {correct_list[2]}' if len(correct_list) >=3 else ''}{f', {correct_list[3]}' if len(correct_list) >=4 else ''}{f', {correct_list[4]}' if len(correct_list) >=5 else ''}||")
            finally:
                # Reset game status down the game ends
                channel_game_status[channel] = False
            
    # Run the game in a separate task
    asyncio.create_task(run_game())


async def station_autocompletion(
        interaction: discord.Interaction,
        current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for drink_choice in [
    "Flinders Street", "Southern Cross", "Melbourne Central", "Richmond", "Flagstaff", "Parliament",
    "Box Hill", "Glenferrie", "Footscray", "North Melbourne", "Essendon", "Prahran", "Caulfield",
    "South Yarra", "Hawthorn", "South Kensington", "Collingwood", "Moorabbin", "Malvern", "St Albans",
    "Mordialloc", "Ringwood", "Pakenham", "Frankston", "Lilydale"
]:
            if current.lower() in drink_choice.lower():
                data.append(app_commands.Choice(name=drink_choice, value=drink_choice))
        return data 
@bot.tree.command(name="log-train", description="Log set you have been on")
@app_commands.describe(number = "Carrige Number", date = "Date in DD/MM/YYYY format", line = 'Train Line', start='Starting Station', end = 'Ending Station')
@app_commands.autocomplete(start=station_autocompletion)
@app_commands.autocomplete(end=station_autocompletion)
@app_commands.choices(line=[
        app_commands.Choice(name="Alamein", value="Alamein"),
        app_commands.Choice(name="Belgrave", value="Belgrave"),
        app_commands.Choice(name="Craigieburn", value="Craigieburn"),
        app_commands.Choice(name="Cranbourne", value="Cranbourne"),
        app_commands.Choice(name="Frankston", value="Frankston"),
        app_commands.Choice(name="Glen Waverley", value="Glen Waverley"),
        app_commands.Choice(name="Hurstbridge", value="Hurstbridge"),
        app_commands.Choice(name="Lilydale", value="Lilydale"),
        app_commands.Choice(name="Mernda", value="Mernda"),
        app_commands.Choice(name="Pakenham", value="Pakenham"),
        app_commands.Choice(name="Sandringham", value="Sandringham"),
        app_commands.Choice(name="Stony Point", value="Stony Point"),
        app_commands.Choice(name="Sunbury", value="Sunbury"),
        app_commands.Choice(name="Upfield", value="Upfield"),
        app_commands.Choice(name="Werribee", value="Werribee"),
])

# Train logger
async def logtrain(ctx, number: str, date:str, line:str, start:str, end:str):
    channel = ctx.channel
    async def log():
        print("logging the thing")
        set = setNumber(number.upper())
        if set == None:
            await ctx.response.send_message(f'Invalid train number : `{number}`')
            return
        type = trainType(number.upper())
        addTrain(ctx.user.name, set, type, date, line, start.title(), end.title())
        await ctx.response.send_message(f"Added {set} ({type}) on the {line} line on {date}  from {start.title()} to {end.title()} to your file")
        
                
    # Run in a separate task
    asyncio.create_task(log())
    
# train logger reader
@bot.tree.command(name="train-logs", description="View logged trips for a user")
async def userLogs(ctx, user: discord.User):
    print(user.name)
    data = readLogs(user.name)
    formatted_data = ""
    for sublist in data:
        if len(sublist) >= 6:  # Ensure the sublist has enough items
            formatted_data += "**Set:**\n{}, {}\n".format(sublist[0], sublist[1])
            formatted_data += "**Date:**\n{}\n".format(sublist[2])
            formatted_data += "**Line:**\n{}\n".format(sublist[3])
            formatted_data += "**Trip Start:**\n{}\n".format(sublist[4])
            formatted_data += "**Trip End:**\n{}\n\n".format(sublist[5])

    await ctx.response.send_message(f'# Logged trips for {user.name}:\n{formatted_data}')
    
@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

bot.run(BOT_TOKEN)