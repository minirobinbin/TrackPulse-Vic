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
import csv
import random
import pandas as pd

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

rareCheckerOn = True

# ENV READING
config = dotenv_values(".env")

BOT_TOKEN = config['TOKEN']
CHANNEL_ID = 1227224314483576982 # channel id to send the startup message
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
log_channel = bot.get_channel(1227224314483576982)


@bot.event
async def on_ready():
    print("Bot started")
    channel = bot.get_channel(CHANNEL_ID)
    with open('logs.txt', 'a') as file:
        file.write(f"\n{datetime.now()} - Bot started")
    await channel.send("Bot is online <@780303451980038165>")
    await bot.tree.sync()
    try:
        task_loop.start()
    except:
        print("WARNING: Rare train checker is not enabled!")
        await channel.send("WARNING: Rare train checker is not enabled! <@780303451980038165>")


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
async def game(ctx):
    channel = ctx.channel

    # Define the CSV file path
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

    # Get a random row
    random_row = random.choice(data)

    # Extract data from the random row
    url = random_row[0]
    station = random_row[1]
    difficulty = random_row[2]

    embed = discord.Embed(title=f"Guess the station!", color=0xd8d500, description="Type ! before your answer. You have 30 Seconds")
    embed.set_image(url=url)
    embed.add_field(name='Difficulty', value=difficulty)
    embed.set_footer(text="DM @xm9g to submit a photo")


    # Send the embed message
    await ctx.response.send_message(embed=embed)

    # Define a check function to validate user input
    def check(m):
        return m.channel == channel and m.author != bot.user and m.content.startswith('!')

    async def run_game():
        try:
            correct = False
            while not correct:
                # Wait for user's response in the same channel
                user_response = await bot.wait_for('message', check=check, timeout=30.0)
                
                # Check if the user's response matches the correct station
                if user_response.content[1:].lower() == station.lower():
                    await ctx.channel.send(f"{user_response.author.mention} guessed it right! {station.title()} was the correct answer!")
                    addLb(user_response.author.id, user_response.author.name)
                    correct = True
                else:
                    await ctx.channel.send("Wrong guess! Try again.")
        except asyncio.TimeoutError:
            await ctx.channel.send(f"Times up. The answer was ||{station}||")

    # Run the game in a separate task
    asyncio.create_task(run_game())
    
@bot.tree.command(name="station-guesser-leaderboard", description="Leaderboard for station guesser")
async def lb(ctx):
    channel = ctx.channel
    leaders = top5()
    print(leaders)
    # Create the embed
    embed = discord.Embed(title="Top 5 Station Guessers", color=discord.Color.gold())
    
    for item, number in leaders:
        embed.add_field(name=item, value=str(number), inline=False)

    await ctx.response.send_message(embed=embed)

bot.run(BOT_TOKEN)