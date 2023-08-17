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
async def grab(ctx, channel:discord.TextChannel):
    
    
    await ctx.respond(channel.last_message,ephemeral=True)

bot.run(os.getenv("BOT_TOKEN"))
