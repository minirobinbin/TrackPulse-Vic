import time


async def logQLDtrain(ctx, type, number, date, line, start, end):
        await print("logging the nsw sydney train")

        savedate = date.split('/')
        if date.lower() == 'today':
            current_time = time.localtime()
            savedate = time.strftime("%Y-%m-%d", current_time)
        else:
            try:
                savedate = time.strptime(date, "%d/%m/%Y")
                savedate = time.strftime("%Y-%m-%d", savedate)
            except ValueError:
                await ctx.response.send_message(f'Invalid date: {date}\nMake sure to use a possible date.', ephemeral=True)
                return
            except TypeError:
                await ctx.response.send_message(f'Invalid date: {date}\nUse the form `dd/mm/yyyy`', ephemeral=True)
                return

        # idk how to get nsw train set numbers i cant find a list of all sets pls help
        # nvm now we have this info provided!
        set = getSydneySetNumber(number)
        if set == None:
            set = number.upper()
            
        if type == 'auto':
            type = sydneyTrainType(set)
        if set == None:
            await ctx.response.send_message(f'Invalid train number: {number.upper()}',ephemeral=True)
            return

        # Add train to the list
        id = addSydneyTrain(ctx.user.name, set, type, savedate, line, start.title(), end.title())

        embed = discord.Embed(title="Train Logged",colour=sydney_train_colour)
        
        embed.add_field(name="Number", value=f'{set} ({type})')
        embed.add_field(name="Line", value=line)
        embed.add_field(name="Date", value=savedate)
        embed.add_field(name="Trip", value=f'{start.title()} to {end.title()}')
        embed.set_footer(text=f"Log ID #{id}")

        await ctx.followup.send(embed=embed)
        
                
    # Run in a separate task