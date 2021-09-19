import discord
from discord import embeds
from discord.ext import commands
from bs4 import BeautifulSoup
from datetime import datetime
from utils import Config
import json
import requests
import re

class Server(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def server(self, ctx, username):
        def EnviarRequestGet(url: str):
            return requests.get(url)

        def RemoverEspacos(valor):
            return re.sub("^ +|\b +", "", valor).replace("  ", "")

        def RetoranrInformacoesDoServidor(infoDoServidor):
            try:
                return infoDoServidor["info"]["clean"]
            except:
                return infoDoServidor["motd"]["clean"]

        def CriarEmbed(ip, playersOnline, playersMaximo, icon, descricao, version, online):
            mensagemJogadores = "Online: ``%s``" % str(playersOnline) + "\nOfline: ``%s``" % str(playersMaximo)
            
            embed = discord.Embed(colour=discord.Colour(0x9013fe))
            embed.set_author(name="Status do servidor: %s" % username, icon_url=icon)
            embed.set_thumbnail(url=icon)
            embed.add_field(name="Descrição", value='``%s``' % descricao, inline=False)
            embed.add_field(name="Players", value=mensagemJogadores, inline=True)
            embed.add_field(name="Version", value="Versão: ``%s``" % version + "\nOnline: ``%s``" % online)

            return embed

        try:
            infoDoServidor = json.loads(EnviarRequestGet("https://api.mcsrvstat.us/2/%s" % username).text)

            descricao = ""

            ip = infoDoServidor["ip"] + ":" + str(infoDoServidor["port"])
            playersOnline = infoDoServidor["players"]["online"]
            playersMaximo = infoDoServidor["players"]["max"]
            icon = "https://api.mcsrvstat.us/icon/%s" % username
            version = RemoverEspacos(infoDoServidor["version"])
            online = "Sim" if infoDoServidor["online"] else "Não"

            for info in RetoranrInformacoesDoServidor(infoDoServidor):
                if(RetoranrInformacoesDoServidor(infoDoServidor).index(info) != 0):
                    descricao += "\n%s" %  RemoverEspacos(info)
                else:
                    descricao += RemoverEspacos(info)            

            embed = CriarEmbed(ip, playersOnline, playersMaximo, icon, descricao, version, online)
            await ctx.message.reply(embed=embed)
        except Exception:
            await ctx.message.reply("Não foi possível consultar o servidor %s" % username)

def setup(client):
    client.add_cog(Server(client))