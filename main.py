import discord
from discord.ext import commands
import os
from keep_alive import keep_alive

#import all of the cogs
from main_cog import main_cog
from music_cog import music_cog



bot = commands.Bot(command_prefix='-')
#remove the default help command so that we can write out own
bot.remove_command('help')

#register the class with the bot
bot.add_cog(main_cog(bot))
bot.add_cog(music_cog(bot))


keep_alive()
bot.run(os.getenv('TOKEN')) #activates discord bot


