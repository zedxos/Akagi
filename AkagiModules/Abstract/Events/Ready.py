async def AkagiReady(Akagibot, discord):
  print('Akagi Ready!')
  await Akagibot.change_presence(status=discord.Status.dnd, activity=discord.Game(name=".help or @{}#{}".format(Akagibot.user.display_name, Akagibot.user.discriminator)))