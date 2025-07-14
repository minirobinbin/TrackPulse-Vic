"this will be run every so oftern like 10 minutes to see when the train is"

import os

import discord
from commands.searchtrain import addmap
from utils.checktype import trainType
from utils.locationFromNumber import convertTrainLocationToGoogle, getTrainLocation, makeMapv2
from utils.routeName import get_route_name
from utils.stoppingpattern import getStoppingPatternFromCar
from utils.trainset import setNumber
import sqlite3
import asyncio

async def trainTimleyFetcherAdd(ctx, train, channel, frequency):
    conn = sqlite3.connect('utils/schedule/channels.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS train_timely (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel TEXT,
            train TEXT,
            frequency TEXT
        )
    ''')
    cursor.execute('''
        INSERT INTO train_timely (channel, train, frequency)
        VALUES (?, ?, ?)
    ''', (channel.id, train, frequency))
    conn.commit()
    conn.close()
    embed = discord.Embed(title="Train added to tracking", description=f"The current run for {train} will be sent in {channel.mention} every {frequency} minutes.") 
    await ctx.followup.send(embed=embed)

async def trainTimleyFetcherRemove(ctx, train, channel):
    conn = sqlite3.connect('utils/schedule/channels.db')
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM train_timely WHERE channel = ? AND train = ?
    ''', (channel.id, train))
    conn.commit()
    conn.close()
    embed = discord.Embed(title="Train removed from tracking", description=f"The current run for {train} will no longer be sent in {channel.mention}.") 
    await ctx.followup.send(embed=embed)
    
async def trainTimleyFetcherList(ctx, channel):
    conn = sqlite3.connect('utils/schedule/channels.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT train, frequency FROM train_timely WHERE channel = ?
    ''', (channel.id,))
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        await ctx.followup.send("No trains are currently being tracked in this channel.")
        return
    
    embed = discord.Embed(title="Tracked Trains", description=f"Trains being tracked in {channel.mention}:")
    for row in rows:
        embed.add_field(name=row[0], value=f"Frequency: {row[1]} minutes", inline=False)
    
    await ctx.followup.send(embed=embed)
    
def getchannelstocheck():
    conn = sqlite3.connect('utils/schedule/channels.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT channel, train, frequency FROM train_timely
    ''')
    rows = cursor.fetchall()
    conn.close()
    
    return rows
    
       
async def getinfo(train):
    try:
        type = trainType(train)
        set = setNumber(train.upper())
        # Generate the map asynchronously
        # After map generation, send it
        if type == "HCMT": # because ptv api lists hcmts like "9005M-9905M" for some fucking reason
            hcmtcar1 = set.split('-')
            location = getTrainLocation(hcmtcar1[0]+'M')
        else:
            location = getTrainLocation(set)
        line = ""
        print(f"Location: {location}")
        url = convertTrainLocationToGoogle(location)
        try:
            stoppingPattern = getStoppingPatternFromCar(location)
        except Exception as e:
            return f'An error has occurred while searching for this trains run.'
        print(f"STOPPING PATTERN: {stoppingPattern}")
        
        # get final stop
        if stoppingPattern is None:
            stoppingPattern = "No stopping pattern found"
            lastStop = None
        else:
            lastStop = list(reversed(stoppingPattern))[0][0]

        try:
            if location is not None:
                for item in location:
                    latitude = item['vehicle_position']['latitude']
                    longitude = item['vehicle_position']['longitude']
                    line = get_route_name(item['route_id'])

                await makeMapv2(latitude,longitude, train, '') 
        except Exception as e:
            return train, f'No trip data available\n{e}'

        file_path = f"temp/{train}-map.png"
        if os.path.exists(file_path):
                file = f"{train}-map.png"
                
                return file, line, url, stoppingPattern, train, lastStop, latitude , longitude
        else:
            return(f"Error: Map file '{file_path}' not found.")
    except Exception as e:
        return(f'There was an error generating the map:\n```{e}```')

import concurrent.futures

async def seeWhereTrainsAre(trains:list):
    locations = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        
        futures = [
            loop.run_in_executor(
                executor, 
                lambda train=train: asyncio.run(getinfo(train)) # calling async function in thread requires this
            )
            for train in trains
        ]
        
        for result in await asyncio.gather(*futures):
            locations.append(result)
    return locations