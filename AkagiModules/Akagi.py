def akagi():
	from discord.ext import commands
	from discord import Embed as AkagiEmbed
	from discord.ext.commands import CommandNotFound
	from discord.ext.commands import MissingPermissions
	from discord.ext.commands import CommandInvokeError
	from discord.ext.commands import NoPrivateMessage
	from AkagiModules.Config.Config import token as AkagiToken
	from AkagiModules.Config.Config import default_prefix as AkagiPrefix
	from AkagiModules.Config.Config import description as AkagiDescription
	from AkagiModules.Abstract.Events.Ready import AkagiReady
	from AkagiModules.Abstract.Events.CommandError import AkagiCommandError
	import os
	import json
	import discord
	import datetime
	def get_prefix(Akagibot, message):
	  if not message.guild:
	  	return AkagiPrefix
	  with open("AkagiModules/Abstract/Database/Prefixes.json", "r") as f:
	    Prefixes = json.load(f)
	    
	  return Prefixes[str(message.guild.id)]

	Akagibot = commands.Bot(command_prefix=get_prefix, case_insensitive=True, description=AkagiDescription)

	Akagibot.remove_command('help')
        
	@Akagibot.event
	async def on_guild_join(guild):
	  with open("AkagiModules/Abstract/Database/Prefixes.json", "r") as f:
	    Prefixes = json.load(f)
	    
	  Prefixes[str(guild.id)] = AkagiPrefix
	  
	  with open('AkagiModules/Abstract/Database/Prefixes.json', 'w') as f:
	    json.dump(Prefixes, f, indent=4)
	
	@Akagibot.event
	async def on_guild_remove(guild):
	  with open("AkagiModules/Abstract/Database/Prefixes.json", "r") as f:
	    Prefixes = json.load(f)
	    
	  Prefixes.pop(str(guild.id))
	  
	  with open('AkagiModules/Abstract/Database/Prefixes.json', 'w') as f:
	    json.dump(Prefixes, f, indent=4)
	
	for f in os.listdir('./AkagiModules/Cogs'):
		if f.endswith('.py'):
			Akagibot.load_extension(f'AkagiModules.Cogs.{f[:-3]}')
	
	@Akagibot.event
	async def on_message(message):
	 await Akagibot.process_commands(message)
	 try:
	  if message.mentions[0] == Akagibot.user:
	    with open("AkagiModules/Abstract/Database/Prefixes.json", "r") as f:
	      Prefixes = json.load(f)
	   
	    pre = Prefixes[str(message.guild.id)]
	    
	    embed=AkagiEmbed(title='Prefix', description=f'*My prefix for this guild is {pre}*', timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
	    embed.set_footer(text="{}".format(message.author.display_name), icon_url=message.author.avatar_url)
	    embed.set_author(name=message.guild.me.display_name, icon_url=message.guild.me.avatar_url)
	    await message.channel.send(embed=embed)
	 except:
	   return
            
	@Akagibot.event
	async def on_ready():
		await AkagiCommandError(Akagibot, CommandNotFound, MissingPermissions, CommandInvokeError, NoPrivateMessage)
		await AkagiReady(Akagibot, discord)
	Akagibot.run(AkagiToken)


