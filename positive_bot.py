''''
import discord
import requests
import json
import random

client = discord.Client()

sad_words = ['sad', 'depressed', 'unhappy', 'miserable', 'depressing']
pog_words = ['pog', 'poggers', 'pogchamp']
starter_encouragements = [
  'You got this!',
  "Hang in there!",
  'Don\'t get sad, get glad!'
  'Get better soon!'
]
pog_responses = [
  'pog',
  'pogchamp',
  'poggers'
]

def get_quote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + ' -' + json_data[0]['a']
  return(quote)

@client.event
async def on_message(message):
    if message.author == client.user: #if message is from bot, bot will not respond
      return
    msg = message.content

    if msg.startswith('-quote'): #random quote when -quote command is sent
      quote = get_quote()
      await message.channel.send(quote)
    
    if msg.startswith('-yo'):
      await message.channel.send('yo boi')
    
    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(starter_encouragements))
    
    if any(word in msg for word in pog_words):
      await message.channel.send(random.choice(pog_responses))








import os
import discord
from keep_alive import keep_alive
from discord.ext import commands
from youtube_dl import YoutubeDL


bot = commands.Bot(command_prefix='-')


#/p music
class music_cog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

    #all the music related stuff
    self.is_playing = False

    #2d array containing [song, channel]
    self.music_queue = []
    self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    self.vc = ""
  
  def search_yt(self, item):
    with YoutubeDL(self.YDL_OPTIONS) as ydl:
      try:
        info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
      except Exception:
        return False
    return {'source': info['formats'][0]['url'], 'title': info['title']}

  def play_next(self):
    if len(self.music_queue) > 0:
      self.is_playing = True

      #gets the first url
      m_url = self.music_queue[0][0]['source']

      #remove the first element as you are currently playing it
      self.music_queue.pop(0)

      self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
    else:
      self.is_playing = False

  async def play_music(self):
    if len(self.music_queue) > 0:
      self.is_playing = True

      m_url = self.music_queue[0][0]['source']

      #try to connect to voice channel if you are not already connected
      if self.vc =="" or not self.vc.is_connected():
        self.vc = await self.music_queue[0][1].connect()
      else:
        self.vc = await self.bot.move_to(self.music_queue[0][1])
      
      print(self.music_queue)
      #remove first element as you are currently playing it
      self.music_queue.pop(0)
      self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
    else:
      self.is_playing = False
  
  @commands.command()
  async def p(self, ctx, *args):
    query = " ".join(args)

    voice_channel = ctx.author.voice.channel
    if voice_channel is None:
      #you need to be connceted so that the bot knows where to go
      await ctx.send("Must be connected to a voice channel!")
    else:
      song = self.search_yt(query)
      if type(song) == type(True):
        await ctx.send("Could not play song. Incorrect format, try another keyword. This could be due to a playlist or livestream format")
      else:
        await ctx.send("Song has been added to the queue!")
        self.music_queue.append([song, voice_channel])

        if self.playing == False:
          await self.play_music()
  
  @commands.command()
  async def q(self, ctx):
    retval = ""
    for i in range(0, len(self.music_queue)):
      retval += self.music_queue[i][0]['title'] + "\n"

    print(retval)
    if retval != "":
      await ctx.send(retval)
    else:
      await ctx.send("There is currently no music in the queue.")

  @commands.command()
  async def skip(self, ctx):
    if self.vc != "":
      self.vc.stop()
      #try to play next song in queue
      await self.play_music()


