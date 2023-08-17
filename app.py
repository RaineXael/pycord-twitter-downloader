import discord
import dotenv
import os
import asyncio

dotenv.load_dotenv()
bot = discord.Bot(command_prefix='xl', description='A simple bot.')


def extract_handle(title):
    print(type(title))
    if not isinstance(title, str):
        raise Exception(f"Expected string for title of handle extraction. Obtained {title}.")
    title = title.split('(@')[1]
    title = title[:-1]
    return title

class EmbedData():
    def __init__(self, handle, image_links):
        if not isinstance(handle, str):
            raise Exception("Expected String for handle")
        for link in image_links:
            if not isinstance(link,str):
                raise Exception("Expected string for all image_link elements")
        self.handle = handle
        self.image_links = image_links



@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name='grab', description='Grabs all images from embeds in a specific channel')
async def grab(ctx, channel:discord.TextChannel, limit:int):
    #try:
        messages = await channel.history(limit=limit).flatten()

        embed_data = []
        failed_messages = []

        for message in messages:
            #text = await channel.fetch_message(message.id)
            if len(message.embeds) <= 0:
                #should add the message to a "failed fetch" list to be added @ the last message but for now do nothing
                print(message.content)
                failed_messages.append(message.content)
            else:
                #this will work with one embed with multiple images, but how about multiple embeds (twi links) in one message??
                
                
                
                #if multiple embeds (> 1 image in one of em)
                if len(message.embeds) > 1:
                    print("big boi")
                
                #if one embed (one image)
                for embed in message.embeds:
                    #maybe should have a twi detector if there's other sources of embeds
                    print(f'{message.content} - {embed.author}')
                    
                    embed_data.append(extract_handle(embed.author.name))
                    embed_data.append(embed.image.proxy_url)
            
        print(embed_data)
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
