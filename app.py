import discord
import dotenv
import os
import asyncio

dotenv.load_dotenv()
bot = discord.Bot(command_prefix='xl', description='A simple bot.')


def extract_handle(title):
    print(f"Parsing {title}")
    if not isinstance(title, str):
        raise Exception(f"Expected string for title of handle extraction. Obtained {title}.")
    title = title.split('(@')[1]
    title = title[:-1]
    return title
    
       

class EmbedData():
    def __init__(self, handle):
        if not isinstance(handle, str):
            raise Exception("Expected String for handle")
        self.handle = handle
        self.image_links = []

    def __repr__(self) -> str:
        return f'@{self.handle} - {self.image_links}'


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name='grab', description='Grabs all images from embeds in a specific channel')
async def grab(ctx, channel:discord.TextChannel, limit:int):
    #try:
        messages = await channel.history(limit=limit).flatten()

        all_embed_data = []
        failed_messages = []

        for message in messages:
            #for each message in the channel...

            if len(message.embeds) <= 0:
                #if no embeds
                #should add the message to a "failed fetch" list to be added @ the last message
                failed_messages.append(message.content)
            else:
                #An embed exists at this point. TODO: Check if it's a twit, or fxtwit or vxtwit or whatever


                #make a new data object, get the handle from the first embed (which should exist with the first check)
                current_data = EmbedData(extract_handle(message.embeds[0].author.name)) # fetch twi handle (todo check if it's a twi thing)

                #if multiple embeds (> 1 image in one of em)
                if len(message.embeds) > 1:
                    for embed in message.embeds:
                        #foreach embed(image) slap its link in the current data object
                        current_data.image_links.append(message.embeds[0].image.proxy_url)
                else:
                    #just one image, just get from index 0
                    current_data.image_links.append(message.embeds[0].image.proxy_url)
                
            all_embed_data.append(current_data)    
                    
            
        print(all_embed_data)
        #then with each embed data entry, get the image and name it with the username got before.

        failed_message_response = ''
        if len(failed_messages) > 0:
            failed_message_response = '\n\nThere were some messages that failed to parse. Please look at them individually:\n'
            for message in failed_messages:
                failed_message_response += f'\n* "{message}"'

        await ctx.respond(f"Embed checking done. Please check the system's files for the output.{failed_message_response}",ephemeral=True)
    #except Exception as e:
    #    if '403' in str(e):
    #        await ctx.respond(f'The bot does not have access to the channel "{channel.name}".',ephemeral=True)
        #else:        
        #    await ctx.respond(f'Something went wrong when accessing the channel: {e}',ephemeral=True)

bot.run(os.getenv("BOT_TOKEN"))
