# Discord bot with whitelist system and extra commands
# Requires: Python 3.10+
# Libraries: discord.py

import discord
from discord.ext import commands
from discord import app_commands

# VUL HIER JE BOT TOKEN IN
TOKEN = "DISCORD_TOKEN"  # <-- hier komt je Discord bot token

# Jouw Discord ID (owner)
OWNER_ID = 1260264286614196326

# Jouw main Discord server link
MAIN_DISCORD_LINK = "https://discord.gg/q6X4ceFW"

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


# 1️⃣ Owner-only whitelist command
@bot.tree.command(name="whitelist", description="Whitelist a user (owner only)")
@app_commands.describe(member="The member to whitelist")
async def whitelist_user(interaction: discord.Interaction, member: discord.Member):

    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("you are not owner", ephemeral=True)
        return

    whitelist.add(member.id)
    await interaction.response.send_message("succesful added whitelist")


# 2️⃣ Paid insta steal command
@bot.tree.command(name="paid-insta-steal", description="Get the paid insta steal script")
async def paid_insta_steal(interaction: discord.Interaction):

    if interaction.user.id not in whitelist:
        await interaction.response.send_message("You are not whitelisted.")
        return

    message = 'Here is your insta steal: loadstring(game:HttpGet("https://api.jnkie.com/api/v1/luascripts/public/155c6ad769510879d83fa70b213f172dd79aac4b94fb591dd2075460d28a54df/download"))().'

    try:
        await interaction.user.send(message)
        await interaction.response.send_message("Check your DMs.", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message(
            "I cannot send you a DM. Please enable DMs from server members.",
            ephemeral=True,
        )


# 3️⃣ Stats command (servers count)
@bot.tree.command(name="stats", description="Show how many servers the bot is in")
async def stats(interaction: discord.Interaction):
    server_count = len(bot.guilds)
    await interaction.response.send_message(f"I am currently in {server_count} servers.")


# 4️⃣ Main Discord link command
@bot.tree.command(name="main-dc", description="Get the main Discord server link")
async def main_dc(interaction: discord.Interaction):
    await interaction.response.send_message(f"Join our main Discord here: {MAIN_DISCORD_LINK}")


if __name__ == "__main__":
    if TOKEN == "":
        raise ValueError("You must paste your Discord bot token in the code.")

    bot.run(TOKEN)
