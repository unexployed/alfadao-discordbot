from discord.ext import commands

from tabulate import tabulate
import logging

from cog_support.chain_tvl_utils import *


logger = logging.getLogger('ChainTVL-COG')
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

class ChainTVL(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('ChainTVL COG loaded.')

    async def is_channel(ctx):   
        return ctx.channel.id in [1080423975290687508, 1080422347594547241]
    
    @commands.command(name='chain_tvl', description='Output formatted tables with TVL.')
    @commands.check(is_channel)
    async def chain_tvl(self, ctx):
        try:
            data = get_chain_tvl()
            splitted_data = split_df(data)
            
            # Generate table strings using list comprehension
            table_strs = [f'```{tabulate(splitted_data[i].values.tolist(), headers=splitted_data[i].columns.tolist())}```\n' for i in range(len(splitted_data))]
            
            # Send two tables per message
            for i in range(0, len(table_strs), 2):
                table_str = table_strs[i]
                if i+1 < len(table_strs):
                    table_str += table_strs[i+1]
                await ctx.send(table_str)
                
        except Exception as e:
            await ctx.send(f'An error occurred: {e}')

    
async def setup(bot):
    await bot.add_cog(ChainTVL(bot))
