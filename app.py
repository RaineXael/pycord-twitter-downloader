import discord
import dotenv
import os
import asyncio

dotenv.load_dotenv()
bot = discord.Bot(command_prefix='xl', description='A simple bot.')


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name='grab', description='Grabs all images from embeds in a specific channel')
async def grab(ctx, channel:discord.TextChannel, limit:int):
    try:
        messages = await channel.history(limit=limit).flatten()

        message_texts = []
        for message in messages:
            #text = await channel.fetch_message(message.id)
            message_texts.append(message.embeds[0].author)
            message_texts.append(message.embeds[0].image)
        print(message_texts)
        await ctx.respond("Check log",ephemeral=True)
    except Exception as e:
        if '403' in str(e):
            await ctx.respond(f'The bot does not have access to the channel "{channel.name}".',ephemeral=True)
        else:        
            await ctx.respond(f'Something went wrong when accessing the channel: {e}',ephemeral=True)

bot.run(os.getenv("BOT_TOKEN"))
