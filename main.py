import discord
from discord.ext import commands
import youtube_dl
import os

client = commands.Bot(command_prefix="ar-")



url = {
    "kolchi_msigner": "https://youtu.be/lC5fFbXUeyI",
    "sefra_w_ke7la": "https://www.youtube.com/watch?v=H8J7A6YKA6c",
    "disk_sghir": "https://www.youtube.com/watch?v=dYykpGxJMMs"
}

@client.command()
async def join(ctx):
    voice_state = ctx.author.voice
    if voice_state is None:
        # Exiting if the user is not in a voice channel
        return await ctx.send('You need to be in a voice channel to use this command')
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice_client:
        await voice_client.disconnect()
    voiceChannel = ctx.author.voice.channel
    await voiceChannel.connect()

@client.command()
async def play(ctx, songname: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command !")
        return

    await join.invoke(ctx)
    # voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url[songname]])

        # songurl = str(url.get(songname))
        # ydl.download([songurl])

    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()


client.run('OTYwMTcyNDIyODUyNjQ4OTgw.YkmkQA.VSCwCkXPpaiW4rHZA32ktxctbO4')
