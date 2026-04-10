import os
import json
from datetime import datetime, timedelta, timezone

import discord
from discord.ext import commands
from discord import app_commands

TOKEN = os.getenv("DISCORD_TOKEN")
TIMER_CHANNEL_ID = int(os.getenv("TIMER_CHANNEL_ID"))
DATA_FILE = "boss_timers.json"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

BOSSES = {
    "croms manikin": {
        "display": "Crom's Manikin",
        "group": "ENDGAME",
        "respawn_minutes": 96 * 60,
        "aliases": ["manikin", "crom", "croms", "crom's manikin"],
    },
    "dhiothu": {
        "display": "Dhiothu",
        "group": "ENDGAME",
        "respawn_minutes": 34 * 60,
        "aliases": ["dino", "dhio", "d2", "dhiothu"],
    },
    "bloodthorn": {
        "display": "Bloodthorn",
        "group": "ENDGAME",
        "respawn_minutes": 34 * 60,
        "aliases": ["bt", "bloodthorn"],
    },
    "gelebron": {
        "display": "Gelebron",
        "group": "ENDGAME",
        "respawn_minutes": 32 * 60,
        "aliases": ["gele", "gelebron"],
    },
    "proteus": {
        "display": "Proteus",
        "group": "ENDGAME",
        "respawn_minutes": 18 * 60,
        "aliases": ["prot", "base", "prime", "proteus"],
    },
    "necromancer": {
        "display": "Necromancer",
        "group": "MIDRAID",
        "respawn_minutes": 22 * 60,
        "aliases": ["necro", "necromancer"],
    },
    "mordris": {
        "display": "Mordris",
        "group": "MIDRAID",
        "respawn_minutes": 20 * 60,
        "aliases": ["mord", "mordy", "mordris"],
    },
    "hrungnir": {
        "display": "Hrungnir",
        "group": "MIDRAID",
        "respawn_minutes": 22 * 60,
        "aliases": ["hrung", "muk", "hrungnir"],
    },
    "aggragoth": {
        "display": "Aggragoth",
        "group": "MIDRAID",
        "respawn_minutes": 20 * 60,
        "aliases": ["aggy", "aggragoth"],
    },
    "215": {
        "display": "215",
        "group": "EDL",
        "respawn_minutes": 2 * 60 + 14,
        "aliases": ["215", "unox"],
    },
    "210": {
        "display": "210",
        "group": "EDL",
        "respawn_minutes": 2 * 60 + 5,
        "aliases": ["210"],
    },
    "205": {
        "display": "205",
        "group": "EDL",
        "respawn_minutes": 1 * 60 + 57,
        "aliases": ["205"],
    },
    "200": {
        "display": "200",
        "group": "EDL",
        "respawn_minutes": 1 * 60 + 48,
        "aliases": ["200"],
    },
    "195": {
        "display": "195",
        "group": "EDL",
        "respawn_minutes": 1 * 60 + 29,
        "aliases": ["195"],
    },
    "190": {
        "display": "190",
        "group": "EDL",
        "respawn_minutes": 1 * 60 + 21,
        "aliases": ["190"],
    },
    "185": {
        "display": "185",
        "group": "EDL",
        "respawn_minutes": 1 * 60 + 12,
        "aliases": ["185"],
    },
    "180": {
        "display": "180",
        "group": "DL",
        "respawn_minutes": 1 * 60 + 28,
        "aliases": ["180", "snorri"],
    },
    "170": {
        "display": "170",
        "group": "DL",
        "respawn_minutes": 1 * 60 + 18,
        "aliases": ["170"],
    },
    "165": {
        "display": "165",
        "group": "DL",
        "respawn_minutes": 1 * 60 + 13,
        "aliases": ["165"],
    },
    "160": {
        "display": "160",
        "group": "DL",
        "respawn_minutes": 1 * 60 + 8,
        "aliases": ["160"],
    },
    "155": {
        "display": "155",
        "group": "DL",
        "respawn_minutes": 1 * 60 + 3,
        "aliases": ["155"],
    },
    "pyrus": {
        "display": "Pyrus",
        "group": "FROZEN",
        "respawn_minutes": 58,
        "aliases": ["py", "pyrus"],
    },
    "grom": {
        "display": "Grom",
        "group": "FROZEN",
        "respawn_minutes": 48,
        "aliases": ["grom"],
    },
    "chained": {
        "display": "Chained",
        "group": "FROZEN",
        "respawn_minutes": 43,
        "aliases": ["chain", "chained"],
    },
    "woody": {
        "display": "Woody",
        "group": "FROZEN",
        "respawn_minutes": 38,
        "aliases": ["woody"],
    },
    "swampie": {
        "display": "Swampie",
        "group": "FROZEN",
        "respawn_minutes": 33,
        "aliases": ["swampy", "swampie"],
    },
    "eye": {
        "display": "Eye",
        "group": "FROZEN",
        "respawn_minutes": 28,
        "aliases": ["eye"],
    },
    "redbane": {
        "display": "Redbane",
        "group": "FROZEN",
        "respawn_minutes": 20,
        "aliases": ["redbane"],
    },
    "coppinger": {
        "display": "Coppinger",
        "group": "METEORIC",
        "respawn_minutes": 20,
        "aliases": ["copp", "coppinger"],
    },
    "rockbelly": {
        "display": "Rockbelly",
        "group": "METEORIC",
        "respawn_minutes": 15,
        "aliases": ["rockbelly"],
    },
    "goretusk": {
        "display": "Goretusk",
        "group": "METEORIC",
        "respawn_minutes": 20,
        "aliases": ["goretusk"],
    },
    "bonehead": {
        "display": "Bonehad",
        "group": "METEORIC",
        "respawn_minutes": 15,
        "aliases": ["bonehad", "bonehead"],
    },
    "doomclaw": {
        "display": "Doomclaw",
        "group": "METEORIC",
        "respawn_minutes": 7,
        "aliases": ["doomclaw"],
    },
    "falgren": {
        "display": "Falgren",
        "group": "WARDEN",
        "respawn_minutes": 45,
        "aliases": ["falg", "falgren"],
    },
}

GROUP_ORDER = ["ENDGAME", "MIDRAID", "EDL", "DL", "FROZEN", "METEORIC", "WARDEN"]
boss_timers = {}

def now_utc():
    return datetime.now(timezone.utc)

def save_timers():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(boss_timers, f, indent=2)

def load_timers():
    global boss_timers
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            boss_timers = json.load(f)
    except FileNotFoundError:
        boss_timers = {}

def find_boss_key(user_input: str):
    cleaned = user_input.lower().strip()
    for key, boss in BOSSES.items():
        if cleaned == key or cleaned in boss["aliases"]:
            return key
    return None

def set_boss_timer(boss_key: str):
    due = now_utc() + timedelta(minutes=BOSSES[boss_key]["respawn_minutes"])
    boss_timers[boss_key] = due.isoformat()
    save_timers()
    return due

def human_remaining(due: datetime):
    delta = due - now_utc()
    total_seconds = int(delta.total_seconds())
    if total_seconds <= 0:
        return "Due now"
    hours, rem = divmod(total_seconds, 3600)
    minutes = rem // 60
    if hours > 0:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"

def build_active_embed():
    embed = discord.Embed(title="⏳ Active Boss Times ⏳", color=discord.Color.teal())
    grouped = {group: [] for group in GROUP_ORDER}

    for boss_key, due_str in boss_timers.items():
        due = datetime.fromisoformat(due_str)
        boss = BOSSES[boss_key]
        grouped[boss["group"]].append(f"{boss['display']} • {human_remaining(due)}")

    for group in GROUP_ORDER:
        if grouped[group]:
            grouped[group].sort()
            embed.add_field(
                name=f"✧ {group}",
                value="```" + "\n".join(grouped[group]) + "```",
                inline=False
            )

    if not any(grouped.values()):
        embed.description = "No active boss timers."

    return embed

@bot.event
async def on_ready():
    load_timers()
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if message.channel.id != TIMER_CHANNEL_ID:
        return

    content = message.content.strip().lower()

    if content == ".":
        await message.channel.send(embed=build_active_embed())
        return

    boss_key = find_boss_key(content)
    if boss_key:
        due = set_boss_timer(boss_key)
        boss_name = BOSSES[boss_key]["display"]
        await message.channel.send(f"{boss_name} due {human_remaining(due)}")

@bot.tree.command(name="bosses", description="Show active boss timers")
async def bosses(interaction: discord.Interaction):
    await interaction.response.send_message(embed=build_active_embed())

@bot.tree.command(name="clearboss", description="Clear a boss timer")
@app_commands.describe(boss="Boss name or alias")
async def clearboss(interaction: discord.Interaction, boss: str):
    boss_key = find_boss_key(boss)
    if not boss_key:
        await interaction.response.send_message("Boss not found.", ephemeral=True)
        return
    if boss_key in boss_timers:
        del boss_timers[boss_key]
        save_timers()
        await interaction.response.send_message(f"Cleared {BOSSES[boss_key]['display']}.")
    else:
        await interaction.response.send_message("That boss does not currently have an active timer.", ephemeral=True)

bot.run(TOKEN)
