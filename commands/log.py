async def log():
        print("logging the thing")

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

        # checking if train number is valid
        if number != 'Unknown':
            set = setNumber(number.upper())
            if set == None:
                await ctx.response.send_message(f'Invalid train number: {number.upper()}',ephemeral=True)
                return
            type = trainType(number.upper())
        else:
            set = 'Unknown'
            type = 'Unknown'
            if traintype == 'auto':
                type = 'Unknown'
            else: type = traintype
        if traintype == "Tait":
            set = '381M-208T-230D-317M'

        # Add train to the list
        id = addTrain(ctx.user.name, set, type, savedate, line, start.title(), end.title())
        await ctx.response.send_message(f"Added {set} ({type}) on the {line} line on {savedate} from {start.title()} to {end.title()} to your file. (Log ID `#{id}`)")
        
                