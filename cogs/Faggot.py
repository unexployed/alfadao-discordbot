from discord.ext import commands

import logging
from art import *

logger = logging.getLogger('Faggot-COG')
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

class Faggot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('Faggot COG loaded.')

    async def is_channel(ctx):   
        return ctx.channel.id in [1011894450814996492, 1080423975290687508]
    
    @commands.command(name='faggot', description='lmao.')
    @commands.check(is_channel)
    async def faggot(self, ctx):
        gay_sex = text2art('gay_sex', font='rnd-medium')
        await ctx.send(f'```{gay_sex}```')
    

async def setup(bot):
    await bot.add_cog(Faggot(bot))
    