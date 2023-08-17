import discord
import dotenv
import os
import asyncio

dotenv.load_dotenv()
bot = discord.Bot(command_prefix='xl', description='A simple bot.')


def extract_handle(title):
    print(f"Parsing {title}")
    try:
        if not isinstance(title, str):
            raise Exception(f"Expected string for title of handle extraction. Obtained {title}.")
        title = title.split('(@')[1]
        title = title[:-1]
        return title
    except Exception as e:
        print(f"{e}, continuing without appending a handle.")
        return ''
    
       

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


#creates an EmbedData for a normal twitter.com link
def create_data_normal(message):
    print(f"Parsing link{message.content}")
    current_data = EmbedData(extract_handle(message.embeds[0].author.name)) # fetch twi handle (todo check if it's a twi thing)
    #if multiple embeds (> 1 image in one of em)
    if len(message.embeds) > 1:
        for embed in message.embeds:
            #foreach embed(image) slap its link in the current data object
            current_data.image_links.append(embed.image.proxy_url)
    else:
        #just one image, just get from index 0
        current_data.image_links.append(message.embeds[0].image.proxy_url)
    return current_data


def create_data_fx(message):
    print(f"Parsing link{message.content}")
    current_data = EmbedData(extract_handle(message.embeds[0].title)) # fetch twi handle (todo check if it's a twi thing)
    #if multiple embeds (> 1 image in one of em)
    if len(message.embeds) > 1:
        for embed in message.embeds:
            #foreach embed(image) slap its link in the current data object
            current_data.image_links.append(embed.thumbnail.proxy_url)
    else:
        #just one image, just get from index 0
        current_data.image_links.append(message.embeds[0].thumbnail.proxy_url)


    return current_data




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
                if '/fxtwitter.com/' in message.content or '/vxtwitter.com/' in message.content:
                    all_embed_data.append(create_data_fx(message))
                elif '/twitter.com/' in message.content:
                    all_embed_data.append(create_data_normal(message))
                else:
                    failed_messages.append(message.content) #should just try anyways but having this here for now

        print(all_embed_data)
        #then with each embed data entry, get the image and name it with the username got before.

        failed_message_response = ''
        if len(failed_messages) > 0:
            failed_message_response = '\n\nThere were some messages that failed to parse. Please look at them individually:\n'
            
            for message in failed_messages:
                
                if 'https://' in message and len(failed_message_response + message) < 2000:
                    failed_message_response += f'\n* "{message}"'  
                
        print('--------------------------------------------------------------------------------')
        print(failed_message_response)
        await ctx.respond(f"Embed checking done. Please check the system's files for the output.{failed_message_response}",ephemeral=True)
        #await ctx.respond(f"Embed checking done. Please check the system's files for the output.",ephemeral=True)
    #except Exception as e:
    #    if '403' in str(e):
    #        await ctx.respond(f'The bot does not have access to the channel "{channel.name}".',ephemeral=True)
        #else:        
        #    await ctx.respond(f'Something went wrong when accessing the channel: {e}',ephemeral=True)

bot.run(os.getenv("BOT_TOKEN"))
