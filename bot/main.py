import discord
import os

import requests
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='sb ', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name}({bot.user.id}) est prêt à foutre le bordel !')


# ----------------------- ERROR ----------------------- #
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply("Vérifiez votre commande !")
    else:
        raise error
# ----------------------- ERROR ----------------------- #


# ------------------------- BAN ----------------------- #
@bot.command()
@commands.has_permissions(ban_members=False)
async def ban(ctx, *, reason=None):
    member = ctx.guild.get_member(ctx.message.author.id)
    await member.ban(reason=reason)
# ------------------------- BAN ----------------------- #


# ------------------------ MUTE ----------------------- #
@bot.command(name="mute")
async def mute(ctx):
    # récupération de l'utilisateur qui a déclenché la commande
    member = ctx.guild.get_member(ctx.message.author.id)
    # ajout du rôle muted à l'utilisateur
    await member.edit(mute=True)
# ------------------------ MUTE ----------------------- #


# ---------------------- DOG PIC ---------------------- #
@bot.command(name="dog")
async def dog(ctx, breed=""):
    # si l'utilisateur fourni une race
    if breed:
        api = 'https://dog.ceo/api/breed/' + breed + '/images/random'
    else:
        api = 'https://dog.ceo/api/breeds/image/random'
    # récupération de la réponse
    response = requests.get(f"{api}")
    if response.status_code == 200:
        await ctx.reply(response.json()["message"])
    else:
        response = "Pas de chien trouvé !"
        await ctx.reply(response)
# ---------------------- DOG PIC ---------------------- #


# ----------------------- TRASH ----------------------- #
@bot.command(name="trash")
async def trash(ctx, member: discord.Member):
    # lien vers l'API d'insultes
    api = 'https://evilinsult.com/generate_insult.php?lang=fr&amp;type=json'
    # création d'une insulte
    response = requests.get(f"{api}")
    if response.status_code == 200:
        await ctx.reply(f'<@!{member.id}>, ' + response.text)
    else:
        response = "Aucune insulte trouvée !"
        await ctx.reply(response)
# ----------------------- TRASH ----------------------- #


# ---------------------- RENAME ----------------------- #
@bot.command(name="rename")
async def rename(ctx, member: discord.Member, nickname):
    # modification du nom de l'utilisateur
    # par le nickname à l'envers (slice pos. -1)
    await member.edit(nick=nickname[::-1])
# ---------------------- RENAME ----------------------- #


# -------------------- RACCOON PIC -------------------- #
@bot.command(name="raccoon")
async def raccoon(ctx):
    api = "https://some-random-api.ml/animal/raccoon"
    # récupération de la réponse
    response = requests.get(f"{api}")
    if response.status_code == 200:
        await ctx.reply(response.json()['image'])
    else:
        response = "Pas de blaireau trouvé !"
        await ctx.reply(response)
# -------------------- RACCOON PIC -------------------- #


@bot.command(name="meme")
async def meme(ctx):
    api = "https://api.humorapi.com/memes/random?api-key=5389761c3d1740da98c0cfcdc7fc7a7e"
    # récupération de la réponse
    response = requests.get(f"{api}")
    if response.status_code == 200:
        await ctx.reply(response.json()['url'])
    elif response.status_code == 402:
        response = "Limite de memes mensuelle atteinte ! C'est de ta faute !"
        await ctx.reply(response)


if __name__ == '__main__':
    bot.run(os.getenv('DISCORD_TOKEN'))
