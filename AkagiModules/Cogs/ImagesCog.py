from discord.ext import commands
from discord import Embed as AkagiEmbed
from AkagiModules.Config.Config import reddit_client_id as RedditAkagiClientID
from AkagiModules.Config.Config import reddit_client_secret as RedditAkagiClientSecret
from AkagiModules.Config.Config import reddit_user_agent as RedditAkagiUserAgent
import discord
import random
import aiohttp
import datetime
import praw

reddit = praw.Reddit(client_id=RedditAkagiClientID,
                     client_secret=RedditAkagiClientSecret,
                     user_agent=RedditAkagiUserAgent, check_for_async=False)


class ImagesCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def cat(self, ctx):
		async with aiohttp.ClientSession() as cs:
			async with cs.get("http://aws.random.cat/meow") as r:
				data = await r.json()
				embed_meow = AkagiEmbed(
			    title='Cat!',
			    description=f'[*Meow~*]({data["file"]})',
			    timestamp=datetime.datetime.utcnow(),
			    color=discord.Color.red())
				embed_meow.set_image(url=data['file'])
				embed_meow.set_footer(text="{}".format(ctx.author.display_name),
			                         icon_url=ctx.author.avatar_url)
				embed_meow.set_author(name=ctx.me.display_name,
			                         icon_url=ctx.me.avatar_url)
			await ctx.send(embed=embed_meow)
	
	@commands.command()
	async def dog(self, ctx):
		async with aiohttp.ClientSession() as cs:
			async with cs.get("http://random.dog/woof.json") as r:
				data = await r.json()
				embed_woof = AkagiEmbed(
			    title='Dog!',
			    description=f'[*Woof~*]({data["url"]})',
			    timestamp=datetime.datetime.utcnow(),
			    color=discord.Color.red())
				embed_woof.set_image(url=data['url'])
				embed_woof.set_footer(text="{}".format(ctx.author.display_name),
			                         icon_url=ctx.author.avatar_url)
				embed_woof.set_author(name=ctx.me.display_name,
			                         icon_url=ctx.me.avatar_url)
			await ctx.send(embed=embed_woof)
			
	@commands.command()
	async def fox(self, ctx):
		async with aiohttp.ClientSession() as cs:
			async with cs.get("http://randomfox.ca/floof/") as r:
				data = await r.json()
				embed_floof = AkagiEmbed(
			    title='Fox!',
			    description=f'[*Floof~*]({data["image"]})',
			    timestamp=datetime.datetime.utcnow(),
			    color=discord.Color.red())
				embed_floof.set_image(url=data['image'])
				embed_floof.set_footer(text="{}".format(ctx.author.display_name),
			                         icon_url=ctx.author.avatar_url)
				embed_floof.set_author(name=ctx.me.display_name,
			                         icon_url=ctx.me.avatar_url)
			await ctx.send(embed=embed_floof)
	
	@commands.command()
	async def duck(self, ctx):
		subreddit = reddit.subreddit('duck')
		all_subs = []		
		top = subreddit.top(limit=5)
		for submission in top:
			all_subs.append(submission)			
		random_sub = random.choice(all_subs)		   
		
		name = random_sub.title		
		url = random_sub.url
		embed = AkagiEmbed(title=f"Duck!",
                               description=f'[*{name}*]({url})',
                               timestamp=datetime.datetime.utcnow(),
                               color=discord.Color.red())
		embed.set_image(url=url)
		embed.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
		embed.set_footer(text="{}".format(ctx.author.display_name),
                         icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed)
		
	@commands.command()
	async def frog(self, ctx):
		subreddit = reddit.subreddit('frogs')
		all_subs = []		
		top = subreddit.top(limit=5)
		for submission in top:
			all_subs.append(submission)			
		random_sub = random.choice(all_subs)		   
		
		name = random_sub.title		
		url = random_sub.url
		embed = AkagiEmbed(title=f"Frog!",
                               description=f'[*{name}*]({url})',
                               timestamp=datetime.datetime.utcnow(),
                               color=discord.Color.red())
		embed.set_image(url=url)
		embed.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
		embed.set_footer(text="{}".format(ctx.author.display_name),
                         icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed)
		
	@commands.command()
	async def ferret(self, ctx):
		subreddit = reddit.subreddit('ferrets')
		all_subs = []		
		top = subreddit.top(limit=5)
		for submission in top:
			all_subs.append(submission)			
		random_sub = random.choice(all_subs)		   
		
		name = random_sub.title		
		url = random_sub.url
		embed = AkagiEmbed(title=f"Ferret!",
                               description=f'[*{name}*]({url})',
                               timestamp=datetime.datetime.utcnow(),
                               color=discord.Color.red())
		embed.set_image(url=url)
		embed.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
		embed.set_footer(text="{}".format(ctx.author.display_name),
                         icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed)
	
	@commands.command()
	async def awwnime(self, ctx):
		subreddit = reddit.subreddit('awwnime')
		all_subs = []		
		top = subreddit.top(limit=5)
		for submission in top:
			all_subs.append(submission)			
		random_sub = random.choice(all_subs)		   
		
		name = random_sub.title		
		url = random_sub.url
		embed = AkagiEmbed(title=f"Moe!",
                               description=f'[*{name}*]({url})',
                               timestamp=datetime.datetime.utcnow(),
                               color=discord.Color.red())
		embed.set_image(url=url)
		embed.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
		embed.set_footer(text="{}".format(ctx.author.display_name),
                         icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed)
                
	async def on_message(self, message):
		print(message.content)


def setup(bot):
	bot.add_cog(ImagesCog(bot))
