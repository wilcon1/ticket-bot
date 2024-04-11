from nextcord import Interaction,SlashOption
import nextcord 
from nextcord.ext import commands
import asyncio
import config
intents = nextcord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

class Buttony(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="ticket", style=nextcord.ButtonStyle.blurple, emoji="🎉", custom_id="ticket")
    async def ticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer(ephemeral=True)
        category = nextcord.utils.get(interaction.guild.categories, id=config.catgory_id)
        if category:
            for ch in category.text_channels:
                if ch.topic == f"{interaction.user.id} DO NOT CHANGE THE TOPIC OF THIS CHANNEL!":
                    await interaction.followup.send(f"You already have a ticket in {ch.mention}", ephemeral=True)
                    return

      
        if not interaction.guild.get_role(config.ticket_role_id): 
            await interaction.followup.send("Ticket creation failed. Please contact an administrator.", ephemeral=True)
            return

        r1 = interaction.guild.get_role(config.ticket_role_id)  
        overwrites = {
            interaction.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            r1: nextcord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True),
            interaction.guild.me: nextcord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True)
        }
        channel = await category.create_text_channel(
            name=f"{interaction.user.name}-ticket",
            topic=f"{interaction.user.id} DO NOT CHANGE THE TOPIC OF THIS CHANNEL!",
            overwrites=overwrites
        )
        embed=nextcord.Embed(
                title="Ticket created",
                description="Don't ping a staff member, they will be here now",
                color=nextcord.Color.dark_red()
            )
        await channel.send(embed=embed, view=Closeticket())

class Closeticket(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="close the button", emoji="❌", custom_id="close", style=nextcord.ButtonStyle.blurple)
    async def closeticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        await interaction.channel.send("closing ticket in 3 seconds!")
        await asyncio.sleep(3)
        await interaction.channel.delete()
class TicketCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="ticket", description="Create a ticket")
    async def ticket(self, interaction: nextcord.Interaction):
        view=Buttony()
        await interaction.response.send_message(
            embed=nextcord.Embed(
                description="Tap the button to create a ticket."
            ),
            view=view
        )


def setup(bot):
    bot.add_cog(TicketCog(bot))




