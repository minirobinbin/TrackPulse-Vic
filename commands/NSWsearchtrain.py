import csv

import discord

from utils.checktype import sydneyTrainType
from utils.colors import getSydneyTrainIcon
from utils.photo import getPhotoCredits
from utils.trainImage import getNSWImage

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
                    'Operator': row[5],
                    'EnteredService': row[6],
                    'Gauge': row[7],
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
                        'Operator': row[5],
                        'EnteredService': row[6],
                        'Gauge': row[7],
                    }
                    break
            if not train_info:
                await ctx.followup.send(f"No train found with number {number}")
                return
            
        # get train type name
        trainType = sydneyTrainType(train_info['Set Number'])
        
       
            
        
        # make the embed 4 the train info
        class InfoContainer(discord.ui.Container):
            upperheading = discord.ui.TextDisplay(f'-# Result for {number.upper()}')
            heading = discord.ui.TextDisplay(f'# {trainType} `{train_info["Set Number"]}`\n`{train_info["Carriages"]}`')

            liveryDisplay = discord.ui.TextDisplay(f'Livery: {train_info["Livery"]}')
            info_text = f"- **Status:** {train_info['Status']}"
            if train_info['Note']:
                info_text += f"\n- **Note:** {train_info['Note']}"
            if train_info['Operator']:
                info_text += f"\n- **Operator:** {train_info['Operator']}"
            if train_info['EnteredService']:
                info_text += f"\n- **Entered Service:** {train_info['EnteredService']}"
            if train_info['Gauge']:
                info_text += f"\n- **Gauge:** {train_info['Gauge']}"
            infoDisplay = discord.ui.TextDisplay(f'## Information:\n{info_text}')
        
            # get train image
            url = getNSWImage(train_info['Set Number'])
            if url != None:
                credits = getPhotoCredits(train_info['Set Number'], 'NSW')
                galleryPic1 = discord.MediaGalleryItem(url)
                gallery = discord.ui.MediaGallery(galleryPic1)
                seperator1 = discord.ui.Separator()
                sources = discord.ui.TextDisplay(f'-# **Sources:** {credits} (Photo), [NSW Transport Wiki](https://nswtrains.fandom.com/wiki/NSW_Railways_Wiki), [Icons from NSW Transport](https://transportnsw.info/travel-info/ways-to-get-around/train/fleet-facilities/sydney-intercity-train-fleet)')
            else:
                seperator1 = discord.ui.Separator()
                sources = discord.ui.TextDisplay(f'-# **Sources:** [NSW Transport Wiki](https://nswtrains.fandom.com/wiki/NSW_Railways_Wiki), [Icons from NSW Transport](https://transportnsw.info/travel-info/ways-to-get-around/train/fleet-facilities/sydney-intercity-train-fleet)')
            
            
        class infoView(discord.ui.LayoutView):
            if train_info['Operator'] == 'Sydney Metro':
                colour = 0x0e8489
            else:
                colour = 0xeb6607
            container = InfoContainer(id=1, accent_color=colour)
        await ctx.followup.send(view=infoView())
