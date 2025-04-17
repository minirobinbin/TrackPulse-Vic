import csv

import discord

from utils.checktype import sydneyTrainType
from utils.colors import getSydneyTrainIcon

async def NSWsearchTrainCommand(ctx, number):
    await ctx.response.defer()
    with open('utils/datalists/nsw-trains.csv', 'r') as file:
        csv_reader = csv.reader(file)
        train_info = None
        for row in csv_reader:
            if row[0] == number:
                train_info = {
                    'Set Number': row[0],
                    'Carriages': row[1],
                    'Status': row[2],
                    'Livery': row[3],
                    'Note': row[4],
                }
        if not train_info:
            train_info = None
            file.seek(0)  # Reset file pointer to start
            for row in csv_reader:
                carriages = row[1].split('-')
                if number in carriages:
                    train_info = {
                        'Set Number': row[0],
                        'Carriages': row[1],
                        'Status': row[2],
                        'Livery': row[3],
                        'Note': row[4],
                    }
                    break
            if not train_info:
                await ctx.followup.send(f"No train found with number {number}")
                return
            
        # get train type name
        trainType = sydneyTrainType(train_info['Set Number'])
        
        # make the embed 4 the train info
        embed = discord.Embed(title=f"{number}:", color=0xeb6607)
        
        embed.add_field(name=f'{train_info["Set Number"]} - {trainType}', value=train_info['Carriages'], inline=False)
        embed.add_field(name='Livery:', value=train_info['Livery'], inline=False)
        info_text = f"- **Status:** {train_info['Status']}"
        if train_info['Note']:
            info_text += f"\n- **Note:** {train_info['Note']}"
        embed.add_field(name='Information', value=info_text, inline=False)
        embed.add_field(name='Source:', value='[NSW Transport Wiki](https://nswtrains.fandom.com/wiki/NSW_Railways_Wiki)\n[Icons from NSW Transport](https://transportnsw.info/travel-info/ways-to-get-around/train/fleet-facilities/sydney-intercity-train-fleet)', inline=False)
        
        embed.set_thumbnail(url="attachment://image.png")
        await ctx.followup.send(file=getSydneyTrainIcon(trainType), embed=embed)