import discord
from discord.ext import commands
from discord import Embed as AkagiEmbed
import datetime
import asyncio
import itertools
import sys
import traceback
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL


ytdlopts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # ipv6 addresses cause issues sometimes
}

ffmpegopts = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = YoutubeDL(ytdlopts)


class VoiceConnectionError(commands.CommandError):
	"""Custom Exception class for connection errors."""

class InvalidVoiceChannel(VoiceConnectionError):
	"""Exception for cases of invalid Voice Channels."""

class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get('title')
        self.web_url = data.get('webpage_url')

        # YTDL info dicts (data) have other useful information you might want
        # https://github.com/rg3/youtube-dl/blob/master/README.md

    def __getitem__(self, item: str):
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        embed_added = AkagiEmbed(title='Added', description=f'*Added {data["title"]} to the Queue!*', timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
        embed_added.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
        embed_added.set_footer(text="{}".format(ctx.author.display_name), icon_url =ctx.author.avatar_url)
        await ctx.send(embed=embed_added)

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}

        return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url']), data=data, requester=requester)


class MusicPlayer:
    __slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'next', 'current', 'np', 'volume')

    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.np = None  # Now playing message
        self.volume = .5
        self.current = None

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:
                # Wait for the next song. If we timeout cancel the player and disconnect...
                async with timeout(300):  # 5 minutes...
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                return self.destroy(self._guild)

            if not isinstance(source, YTDLSource):
                # Source was probably a stream (not downloaded)
                # So we should regather to prevent stream expiration
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception as e:
                    embed_error = AkagiEmbed(title='Error', description=f'*There was an error processing your song! {e}*', timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
                    embed_error.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar_url)
                    await self._channel.send(embed=embed_error)
                    
                    continue

            source.volume = self.volume
            self.current = source

            self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            embed_np = AkagiEmbed(title='Now Playing', description=f'*{source.title} Requested by {source.requester}!*', timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed_np.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar_url)
            self.np = await self._channel.send(embed=embed_np)
            await self.next.wait()

            # Make sure the FFmpeg process is cleaned up.
            source.cleanup()
            self.current = None

            try:
                # We are no longer playing this song...
                await self.np.delete()
            except discord.HTTPException:
                pass

    def destroy(self, guild):
        """Disconnect and cleanup the player."""
        return self.bot.loop.create_task(self._cog.cleanup(guild))


class Music(commands.Cog):
    __slots__ = ('bot', 'players')

    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    async def __local_check(self, ctx):
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

    async def __error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return
            except discord.HTTPException:
                pass
        elif isinstance(error, InvalidVoiceChannel):
            await ctx.send('Error connecting to Voice Channel. '
                           'Please make sure you are in a valid channel or provide me with one')

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    def get_player(self, ctx):
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player

    @commands.command(name='connect', aliases=['join'])
    async def connect_(self, ctx, *, channel: discord.VoiceChannel=None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                # await ctx.send(embed=embed_novc)
                embed_novc = AkagiEmbed(title='Error', description='*No channel to join. Please specify valid one!*', timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
                embed_novc.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
                embed_novc.set_footer(text="{}".format(ctx.author.display_name), icon_url =ctx.author.avatar_url)
                await ctx.send(embed=embed_novc)

        vc = ctx.voice_client

        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                embed_mtm = AkagiEmbed(title='Moving', description=f'*Moving to channel {channel} timed out!*', timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
                embed_mtm.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
                embed_mtm.set_footer(text="{}".format(ctx.author.display_name), icon_url =ctx.author.avatar_url)
                await ctx.send(embed=embed_mtm)
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                embed_cc = AkagiEmbed(title='Connecting', description=f'*Connecting to channel {channel} timed out!*', timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
                embed_cc.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
                embed_cc.set_footer(text="{}".format(ctx.author.display_name), icon_url =ctx.author.avatar_url)
                await ctx.send(embed=embed_cc)

        embed_ccc = AkagiEmbed(title='Connected', description=f'*Connected to {channel}!*', timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
        embed_ccc.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
        embed_ccc.set_footer(text="{}".format(ctx.author.display_name), icon_url =ctx.author.avatar_url)
        await ctx.send(embed=embed_ccc)

    @commands.command(name='play', aliases=['sing'])
    async def play_(self, ctx, *, search: str):
        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.connect_)

        player = self.get_player(ctx)

        # If download is False, source will be a dict which will be used later to regather the stream.
        # If download is True, source will be a discord.FFmpegPCMAudio with a VolumeTransformer.
        source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)

        await player.queue.put(source)

    @commands.command(name='pause')
    async def pause_(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            embed_errornp = AkagiEmbed(title='Error', description=f'*I am not currently playing anything!*', timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed_errornp.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
            embed_errornp.set_footer(text="{}".format(ctx.author.display_name), icon_url =ctx.author.avatar_url)
            return await ctx.send(embed=embed_errornp)
        elif vc.is_paused():
            return

        vc.pause()
        embed_paused = AkagiEmbed(title='Paused', description=f'*Song paused by {ctx.author}!*', timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
        embed_paused.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
        embed_paused.set_footer(text="{}".format(ctx.author.display_name), icon_url =ctx.author.avatar_url)
        await ctx.send(embed=embed_paused)

    @commands.command(name='resume')
    async def resume_(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed_errnp = AkagiEmbed(title='Error', description=f'*I am not currently playing anything!*', timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed_errnp.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
            embed_errnp.set_footer(text="{}".format(ctx.author.display_name), icon_url =ctx.author.avatar_url)
            return await ctx.send(embed=embed_errnp)
        elif not vc.is_paused():
            return

        vc.resume()
        embed_resumed = AkagiEmbed(title='Resumed', description=f'*Song resumed by {ctx.author}!*', timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
        embed_resumed.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
        embed_resumed.set_footer(text="{}".format(ctx.author.display_name), icon_url =ctx.author.avatar_url)
        await ctx.send(embed=embed_resumed)

    @commands.command(name='skip')
    async def skip_(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed_enp = AkagiEmbed(title='Error', description=f'*I am not currently playing anything!*', timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed_enp.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
            embed_enp.set_footer(text="{}".format(ctx.author.display_name), icon_url =ctx.author.avatar_url)
            return await ctx.send(embed=embed_enp)

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return

        vc.stop()
        embed_skipped = AkagiEmbed(title='Skipped', description=f'*Song skipped by {ctx.author}!*', timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
        embed_skipped.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
        embed_skipped.set_footer(text="{}".format(ctx.author.display_name), icon_url =ctx.author.avatar_url)
        await ctx.send(embed=embed_skipped)

    @commands.command(name='queue', aliases=['q', 'playlist'])
    async def queue_info(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed_qnp = AkagiEmbed(title='Error', description=f'*I am not currently playing anything!*', timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed_qnp.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
            embed_qnp.set_footer(text="{}".format(ctx.author.display_name), icon_url =ctx.author.avatar_url)
            return await ctx.send(embed=embed_qnp)

        player = self.get_player(ctx)
        if player.queue.empty():
            embed_errqueue = AkagiEmbed(title='Error', description=f'*There are currently no more queued songs!*', timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed_errqueue.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
            embed_errqueue.set_footer(text="{}".format(ctx.author.display_name), icon_url =ctx.author.avatar_url)
            return await ctx.send(embed=embed_errqueue)

        # Grab up to 5 entries from the queue...
        upcoming = list(itertools.islice(player.queue._queue, 0, 5))

        fmt = '\n'.join(f'*{_["title"]}*' for _ in upcoming)
        embed_queue = AkagiEmbed(title=f'Upcoming next - {len(upcoming)}', description=fmt, timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
        embed_queue.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
        embed_queue.set_footer(text="{}".format(ctx.author.display_name), icon_url =ctx.author.avatar_url)

        await ctx.send(embed=embed_queue)

    @commands.command(name='nowplaying', aliases=['np', 'current', 'currentsong', 'playing'])
    async def now_playing_(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed_npnp = AkagiEmbed(title='Error', description='*I am not currently playing anything!*', timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed_npnp.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
            embed_npnp.set_footer(text="{}".format(ctx.author.display_name), icon_url =ctx.author.avatar_url)
            return await ctx.send(embed=embed_npnp)

        player = self.get_player(ctx)
        if not player.current:
            embed_npnp = AkagiEmbed(title='Error', description='*I am not currently playing anything!*', timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed_npnp.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
            embed_npnp.set_footer(text="{}".format(ctx.author.display_name), icon_url =ctx.author.avatar_url)
            return await ctx.send(embed=embed_npnp)

        try:
            # Remove our previous now_playing message.
            await player.np.delete()
        except discord.HTTPException:
            pass
            
        embed_np = AkagiEmbed(title='Now Playing', description=f'*{vc.source.title} Requested by {vc.soirce.requester}!*', timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
        embed_np.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
        embed_np.set_footer(text="{}".format(ctx.author.display_name), icon_url =ctx.author.avatar_url)

        player.np = await ctx.send(embed=embed_np)

    @commands.command(name='volume', aliases=['vol'])
    async def change_volume(self, ctx, *, vol: float):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed_nvc = AkagiEmbed(title='Error', description='*I am not currently connected to voice channel!*', timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed_nvc.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
            embed_nvc.set_footer(text="{}".format(ctx.author.display_name), icon_url =ctx.author.avatar_url)
            return await ctx.send(embed=embed_nvc)

        if not 0 < vol < 101:
            embed_errint = AkagiEmbed(title='Error', description='*Please specify a value between 1 and 100!*', timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed_errint.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
            embed_errint.set_footer(text="{}".format(ctx.author.display_name), icon_url =ctx.author.avatar_url)
            return await ctx.send(embed=embed_errint)

        player = self.get_player(ctx)

        if vc.source:
            vc.source.volume = vol / 100

        player.volume = vol / 100
        embed_vol = AkagiEmbed(title='Setted', description=f'*Set the volume to {vol}%!*', timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
        embed_vol.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
        embed_vol.set_footer(text="{}".format(ctx.author.display_name), icon_url =ctx.author.avatar_url)
        await ctx.send(embed=embed_vol)

    @commands.command(name='stop')
    async def stop_(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed_snp = AkagiEmbed(title='Error', description='*I am not currently playing anything!*', timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed_snp.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
            embed_snp.set_footer(text="{}".format(ctx.author.display_name), icon_url =ctx.author.avatar_url)
            return await ctx.send(embed=embed_snp)

        await self.cleanup(ctx.guild)
       		

def setup(bot):
    bot.add_cog(Music(bot))