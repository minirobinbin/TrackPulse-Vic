import discord
import requests


async def searchTrainPhoto(ctx, number:str, search_set:bool):
    await ctx.response.defer()
    
    if search_set:
        from utils.trainset import setNumber
        set = setNumber(number)
        if set is None:
            await ctx.followup.send(f"Set {number} not found.")
            return
        else:
            carriages = set.split('-')
    else:
        carriages = [number]
        
    for carriage in carriages:
        allCredits = []

        if carriage == '':
            continue
            
        image_count = 0
        images = []
        
        # get the photo credits
        from utils.photo import getPhotoCredits
        
        # search up to 5 photos of the carriage
        for i in range(5):
            if image_count >= 5:
                break
                
            photoNumber = f"-{i+1}" if i > 0 else ""
            carriage_num = f"{carriage}{photoNumber}"
            
            credits = getPhotoCredits(carriage_num, state='VIC')
            url = f'https://victorianrailphotos.com/photos/{carriage_num}.webp'
            try:
                response = requests.head(url)
                if response.status_code == 200:
                    gallery_item = discord.MediaGalleryItem(media=url, description=f'{carriage}, Photo by {credits}')
                    images.append(gallery_item)
                    allCredits.append(credits) if credits not in allCredits else None
                    image_count += 1
                else:
                    if photoNumber == '':
                        await ctx.followup.send(f"There are no photos of `{carriage_num}`.")
                        continue
                    else:
                        print(f"Image not found for {carriage_num}.")
                        break    
            except requests.RequestException as e:
                print(f"Error fetching image for {carriage_num}: {e}")
        
        if images:
            class GalleryContainer(discord.ui.Container):
                heading = discord.ui.TextDisplay(f'## Photos of [{carriage}](https://victorianrailphotos.com?number={carriage})')
                gallery = discord.ui.MediaGallery(*images)
                credits = discord.ui.TextDisplay(f'-# Photos by: {", ".join(allCredits)}')
                    
            class GalleryView(discord.ui.LayoutView):
                    Gallery = GalleryContainer(id=1)
            
            await ctx.followup.send(view=GalleryView())
    
    