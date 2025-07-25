import discord
from discord.ext import commands, tasks
import datetime
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

last_active = {}

@bot.event
async def on_ready():
    print(f"Zalogowano jako {bot.user}")
    check_inactive.start()

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    last_active[message.author.id] = datetime.datetime.utcnow()
    await bot.process_commands(message)

@tasks.loop(hours=24)
async def check_inactive():
    channel_id = int(os.getenv("CHANNEL_ID"))
    channel = bot.get_channel(channel_id)
    if not channel:
        print("Nie znaleziono kanału.")
        return

    now = datetime.datetime.utcnow()
    threshold = datetime.timedelta(days=60)

    for member in channel.guild.members:
        if member.bot:
            continue
        last = last_active.get(member.id)
        if not last or (now - last > threshold):
            try:
                await channel.send(f"{member.mention}, nie pisałeś nic od ponad 2 miesięcy! Odezwij się! 😊")
            except Exception as e:
                print(f"Błąd: {e}")

bot.run(os.getenv("DISCORD_TOKEN"))
