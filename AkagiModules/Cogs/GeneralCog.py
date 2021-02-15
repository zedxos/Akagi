from discord.ext import commands
from discord import Embed as AkagiEmbed
from AkagiModules.Config.Config import akagi_yes as AkagiYes
from AkagiModules.Config.Config import cerberus_neko as CerberusNeko
from AkagiModules.Config.Config import chika_pout as ChikaPout
from AkagiModules.Config.Config import comfy as Comfy
from AkagiModules.Config.Config import mae as Mae
from AkagiModules.Config.Config import disappointed as Disappointed
from AkagiModules.Config.Config import rem as Rem
from AkagiModules.Config.Config import patreon as Patreon
from AkagiModules.Config.Config import invite_link as InviteLink
import discord
import datetime

class GeneralCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(no_pm=True)
	async def serverinfo(self, ctx):
		if not ctx.guild:
			embed_errordm = AkagiEmbed(
			    title='Error',
			    description='*This command can only be used in servers!*',
			    timestamp=datetime.datetime.utcnow(),
			    color=discord.Color.red())
			embed_errordm.set_author(name=ctx.me.display_name,
			                         icon_url=ctx.me.avatar_url)
			embed_errordm.set_footer(text="{}".format(ctx.author.display_name),
			                         icon_url=ctx.author.avatar_url)
			await ctx.author.send(embed=embed_errordm)
		else:
			embed = AkagiEmbed(title=f"{ctx.guild.name}",
			                   timestamp=datetime.datetime.utcnow(),
			                   color=discord.Color.red())
			embed.add_field(name="Server created at",
			                value=f"*{ctx.guild.created_at}*")
			embed.add_field(name="Server Owner", value=f"*{ctx.guild.owner}*")
			embed.add_field(name="Server Region",
			                value=f"*{ctx.guild.region}*")
			embed.add_field(name="Server ID", value=f"*{ctx.guild.id}*")
			embed.set_author(name=ctx.me.display_name,
			                 icon_url=ctx.me.avatar_url)
			embed.set_footer(text="{}".format(ctx.author.display_name),
			                 icon_url=ctx.author.avatar_url)
			await ctx.send(embed=embed)

	@commands.command()
	async def userinfo(self, ctx, user: discord.Member = None):
		if user is None:
			user = ctx.author
		if user.activity is not None:
			game = user.activity.name
		else:
			game = None
		voice_state = None if not user.voice else user.voice.channel
		embed = discord.Embed(timestamp=ctx.message.created_at,
		                      colour=discord.Color.red())
		embed_values = {
		    "User ID":
		    f'*{user.id}*',
		    "Nick":
		    f'*{user.nick}*',
		    "Status":
		    f'*{user.status}*',
		    "On Mobile":
		    f'*{user.is_on_mobile()}*',
		    "In Voice":
		    f'*{voice_state}*',
		    "Game":
		    f'*{game}*',
		    "Highest Role":
		    f'*{user.top_role.name}*',
		    "Account Created":
		    f"*{user.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S')}*",
		    "Join Date":
		    f"*{user.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S')}*"
		}
		for n, v in embed_values.items():
			embed.add_field(name=n, value=v)
		embed.set_thumbnail(url=user.avatar_url)
		embed.set_author(name=ctx.me.display_name,
			                         icon_url=ctx.me.avatar_url)
		embed.set_footer(text="{}".format(ctx.author.display_name),
			                         icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed)
	
	@commands.group(pass_context=True, invoke_without_command=True, case_insensitive=True)
	async def help(self, ctx):
		embed_help = AkagiEmbed(
			    title=f'{AkagiYes}Help',
			    description=f'*{ctx.prefix}help [Command Category] to get the commands!\n[Invite me~]({InviteLink}), [Support me~]({Patreon})*',
			    timestamp=datetime.datetime.utcnow(),
			    color=discord.Color.red())
		embed_help.add_field(name=f'{Rem}Config', value=f'*{ctx.prefix}help config*')
		embed_help.add_field(name=f'{Disappointed}General', value=f'*{ctx.prefix}help general*')
		embed_help.add_field(name=f'{CerberusNeko}Images', value=f'*{ctx.prefix}help images*')
		embed_help.add_field(name=f'{Comfy}Music', value=f'*{ctx.prefix}help music*')
		embed_help.add_field(name=f'{Mae}Roleplay', value=f'*{ctx.prefix}help roleplay*')
		embed_help.add_field(name=f'{ChikaPout}Nsfw', value=f'*{ctx.prefix}help nsfw*')
		embed_help.set_author(name=ctx.me.display_name,
			                         icon_url=ctx.me.avatar_url)
		embed_help.set_footer(text="{}".format(ctx.author.display_name),
			                         icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed_help)
	
	@help.group()
	async def config(self, ctx):
		embed_help = AkagiEmbed(
			    title=f'{Rem}Config Commands',
			    description='*changeprefix.*',
			    timestamp=datetime.datetime.utcnow(),
			    color=discord.Color.red())
		embed_help.set_author(name=ctx.me.display_name,
			                         icon_url=ctx.me.avatar_url)
		embed_help.set_footer(text="{}".format(ctx.author.display_name),
			                         icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed_help)
		
	@help.group()
	async def general(self, ctx):
		embed_help = AkagiEmbed(
			    title=f'{Disappointed}General Commands',
			    description='*donate, help, info, serverinfo, userinfo.*',
			    timestamp=datetime.datetime.utcnow(),
			    color=discord.Color.red())
		embed_help.set_author(name=ctx.me.display_name,
			                         icon_url=ctx.me.avatar_url)
		embed_help.set_footer(text="{}".format(ctx.author.display_name),
			                         icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed_help)
	
	@help.group()
	async def images(self, ctx):
		embed_help = AkagiEmbed(
			    title=f'{CerberusNeko}Images Commands',
			    description='*awwnime, cat, dog, duck, ferret, fox, frog.*',
			    timestamp=datetime.datetime.utcnow(),
			    color=discord.Color.red())
		embed_help.set_author(name=ctx.me.display_name,
			                         icon_url=ctx.me.avatar_url)
		embed_help.set_footer(text="{}".format(ctx.author.display_name),
			                         icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed_help)
	
	@help.group()
	async def music(self, ctx):
		embed_help = AkagiEmbed(
			    title=f'{Comfy}Music Commands',
			    description='*connect, play, pause, resume, skip, queue, nowplaying, volume, stop.*',
			    timestamp=datetime.datetime.utcnow(),
			    color=discord.Color.red())
		embed_help.set_author(name=ctx.me.display_name,
			                         icon_url=ctx.me.avatar_url)
		embed_help.set_footer(text="{}".format(ctx.author.display_name),
			                         icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed_help)
		
	@help.group()
	async def roleplay(self, ctx):
		embed_help = AkagiEmbed(
			    title=f'{Mae}Roleplay Commands',
			    description='*cuddle, kiss, hug, feed, pat, poke, smug, tickle.*',
			    timestamp=datetime.datetime.utcnow(),
			    color=discord.Color.red())
		embed_help.set_author(name=ctx.me.display_name,
			                         icon_url=ctx.me.avatar_url)
		embed_help.set_footer(text="{}".format(ctx.author.display_name),
			                         icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed_help)
		
	@help.group()
	async def nsfw(self, ctx):
		if not ctx.channel.nsfw:
			embed_help = AkagiEmbed(
			    title=f'{ChikaPout}Nsfw Commands',
			    description='*Only Available in NSFW Channels!*',
			    timestamp=datetime.datetime.utcnow(),
			    color=discord.Color.red())
			embed_help.set_author(name=ctx.me.display_name,
			                         icon_url=ctx.me.avatar_url)
			embed_help.set_footer(text="{}".format(ctx.author.display_name),
			                         icon_url=ctx.author.avatar_url)
			await ctx.send(embed=embed_help)
		else:
			embed_help = AkagiEmbed(
			    title=f'{ChikaPout}Nsfw Commands',
			    description='*ass, boobs, bdsm, bottomless, dick, chubby, collared, hentai, nsfw, kinky, pawg, pussy, redhead.*',
			    timestamp=datetime.datetime.utcnow(),
			    color=discord.Color.red())
			embed_help.set_author(name=ctx.me.display_name,
			                         icon_url=ctx.me.avatar_url)
			embed_help.set_footer(text="{}".format(ctx.author.display_name),
			                         icon_url=ctx.author.avatar_url)
			await ctx.send(embed=embed_help)
			
	@commands.command()
	async def info(self, ctx):
		file = discord.File("AkagiModules/Abstract/Akagi.png", filename="akagi.png")
		serverCount = len(self.bot.guilds)
		memberCount = len(set(self.bot.get_all_members()))
		embed_info = AkagiEmbed(
			    title='Info',
			    description='*Akagi is one of the main Antagonist of Azur lane the Animation, an aircraft carrier of Sakura.*',
			    timestamp=datetime.datetime.utcnow(),
			    color=discord.Color.red())
		embed_info.set_image(url='attachment://akagi.png')
		embed_info.add_field(name='Servers', value=f'*{serverCount}*')
		embed_info.add_field(name='Members', value=f'*{memberCount}*')
		embed_info.set_author(name=ctx.me.display_name,
			                         icon_url=ctx.me.avatar_url)
		embed_info.set_footer(text="{}".format(ctx.author.display_name),
			                         icon_url=ctx.author.avatar_url)
		await ctx.send(file=file, embed=embed_info)
		
	@commands.command()
	async def donate(self, ctx):
		embed_donate = AkagiEmbed(
			    title='Donate!',
			    description=f'*You can support me by being a [Patron]({Patreon})!*',
			    timestamp=datetime.datetime.utcnow(),
			    color=discord.Color.red())
		embed_donate.set_author(name=ctx.me.display_name,
			                         icon_url=ctx.me.avatar_url)
		embed_donate.set_footer(text="{}".format(ctx.author.display_name),
			                         icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed_donate)
			
		
	async def on_message(self, message):
		print(message.content)


def setup(bot):
	bot.add_cog(GeneralCog(bot))
