from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument
from discord import Embed as AkagiEmbed
import discord
import json
import datetime

class ConfigCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
		
    @commands.command(no_pm=True)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def changeprefix(self, ctx, prefix):
      if not ctx.guild:
        embed_errordm = AkagiEmbed(title='Error', description='*This command can only be used in servers!*', timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
        embed_errordm.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
        embed_errordm.set_footer(text="{}".format(ctx.author.display_name), icon_url =ctx.author.avatar_url)
        await ctx.author.send(embed=embed_errordm)
      else:
       with open('AkagiModules/Abstract/Database/Prefixes.json', 'r') as f:
         Prefixes = json.load(f)
         
      Prefixes[str(ctx.guild.id)] = prefix
        
      with open('AkagiModules/Abstract/Database/Prefixes.json', 'w') as f:
          json.dump(Prefixes, f, indent=4)
          
      embed_prefixchange = AkagiEmbed(title='Changed', description=f'*Prefix changed to {prefix}*', timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
      embed_prefixchange.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
      embed_prefixchange.set_footer(text="{}".format(ctx.author.display_name), icon_url =ctx.author.avatar_url)
      await ctx.send(embed=embed_prefixchange)

    @changeprefix.error
    async def changeprefix_error_handler(self, ctx, error):
    	if isinstance(error, MissingRequiredArgument):
    		if error.param.name == 'prefix':
    			embed_errargs = AkagiEmbed(title='Error', description='*Please specify the new prefix!*', timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
    			embed_errargs.set_footer(text="{}".format(ctx.author.display_name),icon_url=ctx.author.avatar_url)
    			embed_errargs.set_author(name=ctx.me.display_name, icon_url = ctx.me.avatar_url)
    			await ctx.send(embed=embed_errargs)
    
    async def on_message(self, message):
        print(message.content)

def setup(bot):
    bot.add_cog(ConfigCog(bot))