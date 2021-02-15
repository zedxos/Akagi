from discord.ext import commands
from discord import Embed as AkagiEmbed
import discord
import random
import aiohttp
import datetime

class RoleplayCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
			
	@commands.command()
	async def hug(self, ctx, member : discord.Member = None):
		if member is None:
			member = ctx.author
		async with aiohttp.ClientSession() as cs:
			async with cs.get("https://nekos.life/api/v2/img/hug") as r:
				data = await r.json()
				embed_hug = AkagiEmbed(
			    title='Hug!',
			    description=f'*{ctx.author.display_name} hugs {member.display_name}~*',
			    timestamp=datetime.datetime.utcnow(),
			    color=discord.Color.red())
				embed_hug.set_image(url=data['url'])
				embed_hug.set_footer(text="{}".format(ctx.author.display_name),
			                         icon_url=ctx.author.avatar_url)
				embed_hug.set_author(name=ctx.me.display_name,
			                         icon_url=ctx.me.avatar_url)
			await ctx.send(embed=embed_hug)
	
	@commands.command()
	async def tickle(self, ctx, member : discord.Member = None):
		if member is None:
			member = ctx.author
		async with aiohttp.ClientSession() as cs:
			async with cs.get("https://nekos.life/api/v2/img/tickle") as r:
				data = await r.json()
				embed_tickle = AkagiEmbed(
			    title='Tickle!',
			    description=f'*{ctx.author.display_name} tickles {member.display_name}~*',
			    timestamp=datetime.datetime.utcnow(),
			    color=discord.Color.red())
				embed_tickle.set_image(url=data['url'])
				embed_tickle.set_footer(text="{}".format(ctx.author.display_name),
			                         icon_url=ctx.author.avatar_url)
				embed_tickle.set_author(name=ctx.me.display_name,
			                         icon_url=ctx.me.avatar_url)
			await ctx.send(embed=embed_tickle)
	
	@commands.command()
	async def feed(self, ctx, member : discord.Member = None):
		if member is None:
			member = ctx.author
		async with aiohttp.ClientSession() as cs:
			async with cs.get("https://nekos.life/api/v2/img/feed") as r:
				data = await r.json()
				embed_feed = AkagiEmbed(
			    title='Feed!',
			    description=f'*{ctx.author.display_name} feeds {member.display_name}~*',
			    timestamp=datetime.datetime.utcnow(),
			    color=discord.Color.red())
				embed_feed.set_image(url=data['url'])
				embed_feed.set_footer(text="{}".format(ctx.author.display_name),
			                         icon_url=ctx.author.avatar_url)
				embed_feed.set_author(name=ctx.me.display_name,
			                         icon_url=ctx.me.avatar_url)
			await ctx.send(embed=embed_feed)

	@commands.command()
	async def cuddle(self, ctx, member : discord.Member = None):
		if member is None:
			member = ctx.author
		async with aiohttp.ClientSession() as cs:
			async with cs.get("https://nekos.life/api/v2/img/cuddle") as r:
				data = await r.json()
				embed_cuddle = AkagiEmbed(
			    title='Cuddle!',
			    description=f'*{ctx.author.display_name} cuddles {member.display_name}~*',
			    timestamp=datetime.datetime.utcnow(),
			    color=discord.Color.red())
				embed_cuddle.set_image(url=data['url'])
				embed_cuddle.set_footer(text="{}".format(ctx.author.display_name),
			                         icon_url=ctx.author.avatar_url)
				embed_cuddle.set_author(name=ctx.me.display_name,
			                         icon_url=ctx.me.avatar_url)
			await ctx.send(embed=embed_cuddle)
	
	@commands.command()
	async def pat(self, ctx, member : discord.Member = None):
		if member is None:
			member = ctx.author
		async with aiohttp.ClientSession() as cs:
			async with cs.get("https://nekos.life/api/v2/img/pat") as r:
				data = await r.json()
				embed_pat = AkagiEmbed(
			    title='Pat!',
			    description=f'*{ctx.author.display_name} pats {member.display_name}~*',
			    timestamp=datetime.datetime.utcnow(),
			    color=discord.Color.red())
				embed_pat.set_image(url=data['url'])
				embed_pat.set_footer(text="{}".format(ctx.author.display_name),
			                         icon_url=ctx.author.avatar_url)
				embed_pat.set_author(name=ctx.me.display_name,
			                         icon_url=ctx.me.avatar_url)
			await ctx.send(embed=embed_pat)

	@commands.command()
	async def kiss(self, ctx, member : discord.Member = None):
		if member is None:
			member = ctx.author
		async with aiohttp.ClientSession() as cs:
			async with cs.get("https://nekos.life/api/v2/img/kiss") as r:
				data = await r.json()
				embed_kiss = AkagiEmbed(
			    title='Kiss!',
			    description=f'*{ctx.author.display_name} kisses {member.display_name}~*',
			    timestamp=datetime.datetime.utcnow(),
			    color=discord.Color.red())
				embed_kiss.set_image(url=data['url'])
				embed_kiss.set_footer(text="{}".format(ctx.author.display_name),
			                         icon_url=ctx.author.avatar_url)
				embed_kiss.set_author(name=ctx.me.display_name,
			                         icon_url=ctx.me.avatar_url)
			await ctx.send(embed=embed_kiss)
	
	@commands.command()
	async def smug(self, ctx, member : discord.Member = None):
		if member is None:
			member = ctx.author
		async with aiohttp.ClientSession() as cs:
			async with cs.get("https://nekos.life/api/v2/img/smug") as r:
				data = await r.json()
				embed_smug = AkagiEmbed(
			    title='Smug!',
			    description=f'*{ctx.author.display_name} smugs at {member.display_name}~*',
			    timestamp=datetime.datetime.utcnow(),
			    color=discord.Color.red())
				embed_smug.set_image(url=data['url'])
				embed_smug.set_footer(text="{}".format(ctx.author.display_name),
			                         icon_url=ctx.author.avatar_url)
				embed_smug.set_author(name=ctx.me.display_name,
			                         icon_url=ctx.me.avatar_url)
			await ctx.send(embed=embed_smug)

	@commands.command()
	async def poke(self, ctx, member : discord.Member = None):
		if member is None:
			member = ctx.author
		async with aiohttp.ClientSession() as cs:
			async with cs.get("https://nekos.life/api/v2/img/poke") as r:
				data = await r.json()
				embed_poke = AkagiEmbed(
			    title='Poke!',
			    description=f'*{ctx.author.display_name} pokes {member.display_name}~*',
			    timestamp=datetime.datetime.utcnow(),
			    color=discord.Color.red())
				embed_poke.set_image(url=data['url'])
				embed_poke.set_footer(text="{}".format(ctx.author.display_name),
			                         icon_url=ctx.author.avatar_url)
				embed_poke.set_author(name=ctx.me.display_name,
			                         icon_url=ctx.me.avatar_url)
			await ctx.send(embed=embed_poke)
                
	async def on_message(self, message):
		print(message.content)


def setup(bot):
	bot.add_cog(RoleplayCog(bot))
