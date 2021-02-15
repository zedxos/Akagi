from discord import Embed as AkagiEmbed
from discord.ext import commands
import datetime
import discord

async def AkagiCommandError(Akagibot, CommandNotFound, MissingPermissions, CommandInvokeError, NoPrivateMessage):
	
  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
   if isinstance(error, CommandNotFound):
       return
   raise error
   
  @Akagibot.event
  async def on_command_error(ctx, error):
   if isinstance(error, NoPrivateMessage):
       embed_errguild = AkagiEmbed(title='Error', description='*This Command is only available on Servers!*', timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
       embed_errguild.set_footer(text="{}".format(ctx.author.display_name),icon_url=ctx.author.avatar_url)
       embed_errguild.set_author(name=ctx.me.display_name, icon_url = ctx.me.avatar_url)
       await ctx.send(embed=embed_errguild)
    
  @Akagibot.event
  async def on_command_error(ctx, error):
   if isinstance(error, MissingPermissions):
       embed_errperms = AkagiEmbed(title='Error', description='*You‘re lack of permissions to use this command!*', timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
       embed_errperms.set_footer(text="{}".format(ctx.author.display_name),icon_url=ctx.author.avatar_url)
       embed_errperms.set_author(name=ctx.me.display_name, icon_url = ctx.me.avatar_url)
       await ctx.send(embed=embed_errperms)
    