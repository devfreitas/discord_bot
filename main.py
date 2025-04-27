import discord
from discord.ext import commands
import os
import asyncio
import random
import datetime
from sympy import sympify
from sympy.parsing.mathematica import parse_mathematica

TOKEN = '#'

PREFIX = '!'

intents = discord.Intents.default()
intents.message_content = True  
intents.members = True 

bot = commands.Bot(command_prefix=PREFIX, description='Um bot divertido e útil para o seu servidor!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logado como {bot.user.name}')
    print(f'ID do bot: {bot.user.id}')
    print('------')
    await bot.change_presence(activity=discord.Game(name='com os membros!'))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if bot.user.mentioned_in(message):
        respostas = [
            f"Olá! Fui mencionado por {message.author.mention}!",
            f"Sim? Precisa de algo, {message.author.mention}?",
            f"Estou aqui! O que posso fazer por você, {message.author.mention}?",
            f"Recebi sua menção, {message.author.mention}!",
            f"Oi! Como vai, {message.author.mention}?",
        ]
        await message.channel.send(random.choice(respostas))
    await bot.process_commands(message)

@bot.command()
async def pesquisar(ctx, *, termo):
    conhecimento = {
        "olá": "Olá! Como posso ajudar?",
        "qual o seu nome?": f"Meu nome é {bot.user.name}!",
        "que dia é hoje?": datetime.datetime.now().strftime('%d de %B de %Y'),
        "qual a hora?": datetime.datetime.now().strftime('%H:%M:%S %Z%z'),
        "pi": "O valor aproximado de pi é 3.14159.",
        "de onde você veio?": "O Rafael me sequest.... Digo, ele me contratou!",
        "qual a capital do Brasil?": "A capital do Brasil é Brasília.",
        "qual a maior floresta do mundo?": "A maior floresta tropical do mundo é a Amazônia.",
    }
    termo = termo.lower()
    if termo in conhecimento:
        await ctx.send(conhecimento[termo])
    else:
        await ctx.send(f"Desculpe, não tenho informações sobre '{termo}' no momento. Mas estou sempre aprendendo!")

@bot.command()
async def calcular(ctx, *, expressao):
    try:
        resultado = eval(expressao)
        await ctx.send(f"O resultado de `{expressao}` é: `{resultado}`")
    except (NameError, TypeError, SyntaxError):
        try:
            expr = sympify(expressao)
            resultado = expr
            await ctx.send(f"O resultado de `{expressao}` é: `{resultado}`")
        except Exception as e:
            await ctx.send(f"Desculpe, não consegui calcular `{expressao}`. Verifique a sintaxe.")

@bot.command()
async def diga(ctx, *, mensagem):
    await ctx.send(mensagem)

@bot.command()
async def sorteio(ctx, *escolhas):
    if not escolhas:
        await ctx.send("Por favor, forneça algumas opções para sortear.")
    else:
        vencedor = random.choice(escolhas)
        await ctx.send(f"E o vencedor é: **{vencedor}**!")


@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    await ctx.send(f"**Nome do Servidor:** {guild.name}")
    await ctx.send(f"**ID do Servidor:** {guild.id}")
    await ctx.send(f"**Membros:** {guild.member_count}")
    await ctx.send(f"**Dono:** {guild.owner.display_name}")
    await ctx.send(f"**Criado em:** {guild.created_at.strftime('%d/%m/%Y %H:%M:%S')}")


@bot.command()
async def ajuda(ctx):
    embed = discord.Embed(title="Comandos do Meu Bot!", description="Aqui estão todos os comandos que você pode usar:", color=0x00ff00)
    for command in bot.commands:
        embed.add_field(name=f"{PREFIX}{command.name}", value=command.help, inline=False)
    await ctx.send(embed=embed)

bot.run("#")