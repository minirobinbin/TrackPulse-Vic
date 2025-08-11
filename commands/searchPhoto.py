import time
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
        
        # Fetch photos from new API
        url = f'https://victorianrailphotos.com/api/photos/{carriage}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            print(f"Error fetching images for {carriage}: {e}")
            data = {"photos": []}

        # Loop through up to 5 photos
        for photo in data.get("photos", [])[:5]:
            photographer = photo.get("photographer", "Unknown")
            photo_url = photo.get("url")
            credits = photographer
            
            if not photo_url:
                continue
            
            gallery_item = discord.MediaGalleryItem(
                media=photo_url,
                description=f'{carriage}, Photo by {credits}'
            )
            images.append(gallery_item)
            
            if credits not in allCredits:
                allCredits.append(credits)
            
            image_count += 1

        if image_count == 0:
            await ctx.followup.send(f"There are no photos of `{carriage}`.")
        
        if images:
            class GalleryContainer(discord.ui.Container):
                heading = discord.ui.TextDisplay(f'## Photos of [{carriage}](https://victorianrailphotos.com?number={carriage})')
                gallery = discord.ui.MediaGallery(*images)
                credits = discord.ui.TextDisplay(f'-# Photos by: {", ".join(allCredits)}')
                    
            class GalleryView(discord.ui.LayoutView):
                    Gallery = GalleryContainer(id=1)
            
            await ctx.followup.send(view=GalleryView())
    time.sleep(0.3)
    
    