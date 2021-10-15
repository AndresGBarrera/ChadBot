import discord
from discord.ext import commands
import os
import discord
from keep_alive import keep_alive
import requests
4	- import json
5	- import random
65	 
6	+ #import all of the cogs
7	+ from main_cog import main_cog
8	+ from music_cog import music_cog
79	 
10	+ bot = commands.Bot(command_prefix='-')
11	+
812	  client = discord.Client()
13	+ @client.event
14	+ async def on_ready():
15	+   print('ChadBot has logged in as {0.user}'.format(client))
916	 
10	- sad_words = ['sad', 'depressed', 'unhappy', 'angry', 'miserable', 'depressing']
11	- pog_words = ['pog', 'poggers', 'pogchamp']
17	+ #remove the default help command so that we can write out own
18	+ bot.remove_command('help')
1219	 
13	- starter_encouragements = [
14	-   'You got this!',
15	-   "Hang in there!",
20	+ #register the class with the bot
21	+ bot.add_cog(main_cog(bot))
22	+ bot.add_cog(music_cog(bot))
16	-   'Don\'t get sad, get glad!'
17	-   'Get better soon!'
18	- ]
19	- pog_responses = [
20	-   'pog',
21	-   'pogchamp',
22	-   'poggers'
23	- ]
2423	 
25	- def get_quote():
26	-   response = requests.get('https://zenquotes.io/api/random')
27	-   json_data = json.loads(response.text)
28	-   quote = json_data[0]['q'] + ' -' + json_data[0]['a']
29	-   return(quote)
3024	 
31	- @client.event
32	- async def on_ready():
33	-   print('Positive bot has logged in as {0.user}'.format(client))
3425	 
26	+ keep_alive()
27	+ bot.run(os.getenv('TOKEN')) #activates discord bot
3528	 
3629	 
37	- @client.event
38	- async def on_message(message):
39	-     if message.author == client.user: #if message is from bot, bot will not respond
40	-       return
41	-     msg = message.content
42	-
43	-     if msg.startswith('-quote'): #random quote when -quote command is sent
44	-       quote = get_quote()
45	-       await message.channel.send(quote)
46	-     
47	-     if msg.startswith('-yo'):
48	-       await message.channel.send('yo boi')
49	-     
50	-     if any(word in msg for word in sad_words):
51	-       await message.channel.send(random.choice(starter_encouragements))
52	-     
53	-     if any(word in msg for word in pog_words):
54	-       await message.channel.send(random.choice(pog_responses))
55	-
56	- client.run(os.getenv('TOKEN')) #activates discord bot