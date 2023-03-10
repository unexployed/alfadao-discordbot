from discord.ext import commands
import discord

import logging

from cog_support.audit_utils import *

chain_ids = get_audit_chain_ids()

logger = logging.getLogger('Audit-COG')
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

class AuditCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('Audit COG loaded.')

    async def is_channel(ctx):   
        pass # return ctx.channel.id in [1080423975290687508, 1080422347594547241]
    
    @commands.group(name='audit_token')
    async def audit_token(self, ctx, chain:str, contract:str):
        if ctx.invoked_subcommand is None and chain is not None and contract is not None:
            try:
                data = ping_audit_api(chain_ids[chain], contract)
                filtered = filter_security(data)
                embed = discord.Embed(
                    title=f'Token audit for {data[contract]["token_name"]}',
                    description=f'[{contract}](https://etherscan.io/token/{contract})'
                )
                for key, value in filtered.items():
                    if key == 'lp_holders'and isinstance(value, list):
                        lp_holder = filtered['lp_holders'][0]
                        embed.add_field(
                            name='UniCrypt locked LP',
                            value=f'percentage locked: {lp_holder["percentage_locked"]}\nunlock date: {lp_holder["unlock_date"]}',
                            inline=True
                        )
                    else:
                        if key in ['creator_address', 'owner_address']:
                            value = f'[{value}](https://etherscan.io/address/{value})'
                        embed.add_field(name=key, value=value, inline=True)
                await ctx.send(embed=embed)
            except Exception as e:
                await ctx.send(f'An error occured: {e}')

async def setup(bot):
    await bot.add_cog(AuditCog(bot))