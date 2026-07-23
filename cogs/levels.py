import discord
from discord.ext import commands, tasks
from ..database import get_user, update_user

LEVEL_CHANNEL_ID = 1529001439123210240


class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_xp.start()

    def cog_unload(self):
        self.voice_xp.cancel()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        user_id = message.author.id

        old_xp, old_level = get_user(user_id)

        new_xp = old_xp + 1
        new_level = new_xp // 100 + 1

        update_user(user_id, new_xp, new_level)

        if new_level > old_level:
            channel = self.bot.get_channel(LEVEL_CHANNEL_ID)

            if channel:
                await channel.send(
                    f"🎉 مبروك {message.author.mention} وصلت لفل **{new_level}**!"
                )

        await self.bot.process_commands(message)


    @tasks.loop(minutes=1)
    async def voice_xp(self):
        for guild in self.bot.guilds:
            for member in guild.members:

                if member.bot:
                    continue

                if member.voice and member.voice.channel:

                    user_id = member.id

                    old_xp, old_level = get_user(user_id)

                    new_xp = old_xp + 2
                    new_level = new_xp // 100 + 1

                    update_user(
                        user_id,
                        new_xp,
                        new_level
                    )

                    if new_level > old_level:
                        channel = self.bot.get_channel(LEVEL_CHANNEL_ID)

                        if channel:
                            await channel.send(
                                f"🎉 مبروك {member.mention} وصلت لفل **{new_level}**!"
                            )


    @commands.command()
    async def level(self, ctx, member: discord.Member = None):

        member = member or ctx.author

        xp, level = get_user(member.id)

        await ctx.send(
            f"⭐ {member.mention}\n"
            f"المستوى: **{level}**\n"
            f"XP: **{xp}/{level * 100}**"
        )


async def setup(bot):
    await bot.add_cog(Levels(bot))
