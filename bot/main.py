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


# ----------------------- KICK ------------------------ #
@bot.command(name="kick")
@commands.has_permissions(ban_members=False)
async def kick(ctx, *, reason=None):
    member = ctx.guild.get_member(ctx.message.author.id)
    await member.kick(reason=reason)
# ----------------------- KICK ------------------------ #


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
    api = 'https://evilinsult.com/generate_insult.php?lang=frsb amp;type=json'
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


# ----------------------- MEMES ----------------------- #
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
# ----------------------- MEMES ----------------------- #


# ----------------------- HELP ------------------------ #
@bot.remove_command("help")
@bot.command(name="help")
async def help(ctx):
    # création d'une nouvelle embed
    embed = discord.Embed(title="All commands")
    # création du champ d'administration
    embed.add_field(name="Administration",
                    value="Mute : sb mute {user} \n"
                          "Kick : sb kick {user} \n"
                          "Rename : sb rename {user} [name]",
                    inline=False)
    # création du champ des images d'API
    embed.add_field(name="Random pics",
                    value="Dog : sb dog [breed] \n"
                          "Meme : sb meme \n"
                          "Raccoon : sb raccoon",
                    inline=False)
    # création du champ des commandes troll
    embed.add_field(name="Others",
                    value="Trash : sb trash {user}",
                    inline=False)
    # ajout du thumbnail
    embed.set_thumbnail(url="https://i.imgur.com/KvjcO01.jpg")
    embed.set_footer(text="Informations requested by {}".format(ctx.author.display_name))
    # envoi du message
    await ctx.send(embed=embed)
# ----------------------- HELP ------------------------ #


if __name__ == '__main__':
    bot.run(os.getenv('DISCORD_TOKEN'))
