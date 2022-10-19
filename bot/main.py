import discord
import os
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='titi ', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}({bot.user.id})')


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command(name="coucou")
async def coucou(ctx):
    reponse = f"Ça va, {ctx.message.author.name} ?"
    await ctx.reply(reponse)
    print(f"Réponse à message {ctx.message.id} : {reponse}")


if __name__ == '__main__':
    bot.run(os.getenv('DISCORD_TOKEN'))
