# NEXUS HUB - Python 3.11.0 - BOT STOREFRONT - FINAL + ALL FEATURES - REAL LIST
import os, json, threading
import discord
from discord.ext import commands
from discord import app_commands
from flask import Flask
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
@app.route('/')
def home(): return "NEXUS HUB is online!", 200
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.getenv('PORT', 10000))), daemon=True).start()

OWNER_ID = os.getenv('OWNER_ID', '')
OWNER_USERNAME = os.getenv('OWNER_USERNAME', '@starrlightz12')
RECOVERY_KEY = os.getenv('RECOVERY_KEY', 'change-me')
SUPPORT_CHANNEL_ID = int(os.getenv('SUPPORT_CHANNEL_ID', '0'))

DB_FILE = 'hub_db.json'
DEFAULT_BOTS = {
    "NEXUS V1": {"emoji": "👑", "desc": "The original NEXUS. All-in-one.", "invite": "https://discord.com/oauth2/authorize?client_id=YOUR_ID_V1&permissions=8&scope=bot%20applications.commands", "premium": "Free", "premium_price": "Free", "category": "Main"},
    "NEXUS-BUILD": {"emoji": "🛠️", "desc": "Build servers in seconds. Templates, channels, roles.", "invite": "https://discord.com/oauth2/authorize?client_id=YOUR_ID_BUILD&permissions=8&scope=bot%20applications.commands", "premium": "Free", "premium_price": "Free", "category": "Tools"},
    "NEXUS CAL": {"emoji": "📅", "desc": "Calendar, reminders, events.", "invite": "https://discord.com/oauth2/authorize?client_id=YOUR_ID_CAL&permissions=8&scope=bot%20applications.commands", "premium": "Free", "premium_price": "Free", "category": "Tools"},
    "NEXUS FORM": {"emoji": "📝", "desc": "Applications with Accept/Deny + auto Candidate role.", "invite": "https://discord.com/oauth2/authorize?client_id=YOUR_ID_FORM&permissions=8&scope=bot%20applications.commands", "premium": "Free", "premium_price": "Free", "category": "Tools"},
    "NEXUS MEDIA": {"emoji": "📣", "desc": "YouTube / Twitch / TikTok / Insta notifier.", "invite": "https://discord.com/oauth2/authorize?client_id=YOUR_ID_MEDIA&permissions=8&scope=bot%20applications.commands", "premium": "Free / Premium", "premium_price": "$5/mo", "category": "Notifier"},
    "NEXUS REACT": {"emoji": "⚡", "desc": "Reaction roles - react to get roles.", "invite": "https://discord.com/oauth2/authorize?client_id=YOUR_ID_REACT&permissions=8&scope=bot%20applications.commands", "premium": "Free", "premium_price": "Free", "category": "Tools"},
    "NEXUS MARKET": {"emoji": "🛒", "desc": "Market / Shop - buy, sell, trade in Discord.", "invite": "https://discord.com/oauth2/authorize?client_id=YOUR_ID_MARKET&permissions=8&scope=bot%20applications.commands", "premium": "Free", "premium_price": "Free", "category": "Fun"},
    "NEXUS PING": {"emoji": "📶", "desc": "Ping, uptime, status - check if bots are alive.", "invite": "https://discord.com/oauth2/authorize?client_id=YOUR_ID_PING&permissions=8&scope=bot%20applications.commands", "premium": "Free", "premium_price": "Free", "category": "Tools"},
    "NEXUS HUB": {"emoji": "🌐", "desc": "Showcase for ALL NEXUS bots. Vote, Premium, Support.", "invite": "https://discord.com/oauth2/authorize?client_id=YOUR_ID_HUB&permissions=8&scope=bot%20applications.commands", "premium": "Free", "premium_price": "Free", "category": "Main"},
}

db = {"bots": DEFAULT_BOTS, "featured": "NEXUS HUB", "votes": {}, "voters": {}}
if os.path.exists(DB_FILE):
    try:
        loaded = json.load(open(DB_FILE))
        if loaded.get("bots"):
            db.update(loaded)
            for k, v in db["bots"].items():
                v.setdefault("premium_price", v.get("premium", "Free"))
                v.setdefault("votes", db.get("votes", {}).get(k, 0))
            db.setdefault("votes", {})
            db.setdefault("voters", {})
        else:
            db["bots"] = DEFAULT_BOTS
    except:
        pass

def save(): json.dump(db, open(DB_FILE, 'w'), indent=2)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ---------- HELPERS ----------
def find_bot(name: str):
    for k in db["bots"]:
        if k.lower() == name.lower() or name.lower() in k.lower():
            return k
    return None

def get_status_emoji(name: str, guild=None):
    if guild:
        for m in guild.members:
            if m.bot and (name.lower() in m.name.lower()):
                return "🟢" if str(m.status) != "offline" else "🔴"
    return "🟢"

def build_hub_embed(guild=None, category: str = None, sort_by_votes: bool = False):
    bots = list(db["bots"].items())
    if category:
        bots = [(n, d) for n, d in bots if d.get("category", "").lower() == category.lower()]
    if sort_by_votes:
        bots.sort(key=lambda x: db.get("votes", {}).get(x[0], 0), reverse=True)
    title = "👑 NEXUS HUB - All NEXUS Bots"
    if category: title += f" - {category}"
    if sort_by_votes: title += " - Top Voted 🏆"
    embed = discord.Embed(title=title, description=f"**Owner:** {OWNER_USERNAME}\n**Total Bots:** {len(bots)}\n**⭐ Featured:** {db.get('featured', 'NEXUS HUB')}\n\n`/hub-info name: NEXUS MEDIA` for invite + premium\n`/hub-premium` for prices • `/hub-top` for most voted", color=0x8B5CF6, timestamp=datetime.now())
    cats = {}
    for name, data in bots:
        cats.setdefault(data.get("category", "Other"), []).append((name, data))
    for cat, items in cats.items():
        txt = ""
        for name, data in items:
            star = "⭐ " if name == db.get("featured") else ""
            status = get_status_emoji(name, guild)
            votes = db.get("votes", {}).get(name, 0)
            vote_txt = f" • 👍 {votes}" if votes > 0 else ""
            txt += f"{star}{status} {data.get('emoji','🤖')} **{name}** - {data.get('desc','')}{vote_txt}\n"
        embed.add_field(name=f"📁 {cat}", value=txt, inline=False)
    if not bots:
        embed.add_field(name="No bots", value="No bots in this category!", inline=False)
    embed.set_footer(text="NEXUS HUB • Use /hub-info to see invite + premium")
    return embed

def build_premium_embed():
    embed = discord.Embed(title="💎 NEXUS HUB - Premium Prices", description=f"Owner: {OWNER_USERNAME}\nDM {OWNER_USERNAME} to buy Premium. Click **Buy Premium** on any bot.", color=0xFFD700, timestamp=datetime.now())
    for name, data in db["bots"].items():
        price = data.get("premium_price", data.get("premium", "Free"))
        embed.add_field(name=f"{data.get('emoji','🤖')} {name}", value=f"**Price:** {price}\n**Plan:** {data.get('premium','Free')}\n{data.get('desc','')}", inline=False)
    embed.set_footer(text="NEXUS HUB • Premium = More features, instant, unlimited")
    return embed

# ---------- VIEWS ----------
class HubView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="👑 View All Bots", style=discord.ButtonStyle.blurple, custom_id="hub_view")
    async def view_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=build_hub_embed(interaction.guild), ephemeral=True)
    @discord.ui.button(label="⭐ Featured Bot", style=discord.ButtonStyle.green, custom_id="hub_featured")
    async def featured_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        fname = db.get("featured", "")
        data = db["bots"].get(fname)
        if not data: return await interaction.response.send_message("❌ No featured bot set!", ephemeral=True)
        embed = discord.Embed(title=f"⭐ Featured - {fname}", description=data.get("desc",""), color=0xFFD700)
        embed.add_field(name="Premium", value=data.get("premium_price", data.get("premium","Free")), inline=True)
        embed.add_field(name="Category", value=data.get("category","Other"), inline=True)
        embed.add_field(name="Invite", value=f"[Click to Invite]({data.get('invite','#')})", inline=False)
        await interaction.response.send_message(embed=embed, view=BotActionView(fname), ephemeral=True)
    @discord.ui.button(label="💎 Premium", style=discord.ButtonStyle.gray, custom_id="hub_premium_btn")
    async def premium_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=build_premium_embed(), ephemeral=True)
    @discord.ui.button(label="🏆 Top Voted", style=discord.ButtonStyle.gray, custom_id="hub_top_btn")
    async def top_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=build_hub_embed(interaction.guild, sort_by_votes=True), ephemeral=True)

class BotActionView(discord.ui.View):
    def __init__(self, bot_name):
        super().__init__(timeout=None)
        self.bot_name = bot_name
    @discord.ui.button(label="👍 Vote", style=discord.ButtonStyle.green, custom_id="hub_vote_btn")
    async def vote_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        uid = str(interaction.user.id)
        if db.get("voters", {}).get(uid, []) and self.bot_name in db["voters"][uid]:
            return await interaction.response.send_message(f"❌ You already voted for **{self.bot_name}**!", ephemeral=True)
        db.setdefault("votes", {})[self.bot_name] = db.get("votes", {}).get(self.bot_name, 0) + 1
        db.setdefault("voters", {}).setdefault(uid, []).append(self.bot_name)
        save()
        await interaction.response.send_message(f"✅ Voted for **{self.bot_name}**! Total votes: {db['votes'][self.bot_name]} 👍", ephemeral=True)
    @discord.ui.button(label="💎 Buy Premium", style=discord.ButtonStyle.blurple, custom_id="hub_buy_btn")
    async def buy_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = db["bots"].get(self.bot_name, {})
        price = data.get("premium_price", "Free")
        await interaction.response.send_message(f"💎 **Buy Premium for {self.bot_name}**\nPrice: **{price}**\nDM {OWNER_USERNAME} with: `I want Premium for {self.bot_name}`\nOr click Support below!", ephemeral=True)
    @discord.ui.button(label="🎫 Get Support", style=discord.ButtonStyle.gray, custom_id="hub_support_btn")
    async def support_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            owner = await bot.fetch_user(int(OWNER_ID)) if OWNER_ID else None
            if owner:
                await owner.send(f"🎫 **Support Request**\nFrom: {interaction.user} ({interaction.user.id})\nServer: {interaction.guild.name if interaction.guild else 'DM'}\nBot: {self.bot_name}\nUser needs help with {self.bot_name}!")
        except: pass
        if SUPPORT_CHANNEL_ID:
            ch = bot.get_channel(SUPPORT_CHANNEL_ID)
            if ch:
                await ch.send(f"🎫 **Support** - {interaction.user.mention} needs help with **{self.bot_name}** in {interaction.guild.name if interaction.guild else 'DM'} - Please DM them!")
        await interaction.response.send_message(f"✅ Support request sent for **{self.bot_name}**! {OWNER_USERNAME} will DM you soon 🎫", ephemeral=True)

@bot.event
async def on_ready():
    try: await bot.tree.sync()
    except Exception as e: print("SYNC FAIL:", e)
    print(f"✅ NEXUS HUB logged in as {bot.user}")

@bot.event
async def on_member_join(member: discord.Member):
    if not member.bot: return
    name = member.name.upper()
    if "NEXUS" not in name and "EVIL" not in name: return
    if find_bot(member.name): return
    db["bots"][member.name.upper()] = {"emoji": "🤖", "desc": f"Auto-synced on join - {member.name}", "invite": f"https://discord.com/oauth2/authorize?client_id={member.id}&permissions=8&scope=bot%20applications.commands", "premium": "Free", "premium_price": "Free", "category": "Auto-Synced"}
    save()
    print(f"🔄 AUTO-SYNCED: {member.name}")

@bot.event
async def on_guild_join(guild: discord.Guild):
    for m in guild.members:
        if m.bot and ("NEXUS" in m.name.upper() or "EVIL" in m.name.upper()):
            if not find_bot(m.name):
                db["bots"][m.name.upper()] = {"emoji": "🤖", "desc": f"Auto-synced - {m.name}", "invite": f"https://discord.com/oauth2/authorize?client_id={m.id}&permissions=8&scope=bot%20applications.commands", "premium": "Free", "premium_price": "Free", "category": "Auto-Synced"}
    save()

@bot.tree.command(name="hub", description="Show all NEXUS bots")
async def hub_slash(interaction: discord.Interaction, category: str = None):
    await interaction.response.send_message(embed=build_hub_embed(interaction.guild, category=category), view=HubView())

@bot.tree.command(name="hub-search", description="Search for a bot")
async def hub_search(interaction: discord.Interaction, query: str):
    results = [(n, d) for n, d in db["bots"].items() if query.lower() in n.lower() or query.lower() in d.get("desc","").lower() or query.lower() in d.get("category","").lower()]
    if not results: return await interaction.response.send_message(f"❌ No bots found for `{query}`", ephemeral=True)
    embed = discord.Embed(title=f"🔍 Search: {query} - {len(results)} found", color=0x8B5CF6)
    for n, d in results:
        embed.add_field(name=f"{d.get('emoji','🤖')} {n}", value=f"{d.get('desc','')}\nVotes: 👍 {db.get('votes',{}).get(n,0)} | Price: {d.get('premium_price','Free')}\n[Invite]({d.get('invite','#')})", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="hub-info", description="Info + invite for one bot")
async def hub_info(interaction: discord.Interaction, name: str):
    found = find_bot(name)
    if not found: return await interaction.response.send_message(f"❌ Bot `{name}` not found! Do `/hub` to see list.", ephemeral=True)
    data = db["bots"][found]
    embed = discord.Embed(title=f"{data.get('emoji','🤖')} {found}", description=data.get("desc",""), color=0x8B5CF6)
    embed.add_field(name="⭐ Featured", value="Yes" if found == db.get("featured") else "No", inline=True)
    embed.add_field(name="💎 Premium", value=data.get("premium_price", data.get("premium","Free")), inline=True)
    embed.add_field(name="📁 Category", value=data.get("category","Other"), inline=True)
    embed.add_field(name="👍 Votes", value=str(db.get("votes", {}).get(found, 0)), inline=True)
    embed.add_field(name="🟢 Status", value=get_status_emoji(found, interaction.guild), inline=True)
    embed.add_field(name="🔗 Invite", value=f"[Click to Invite {found}]({data.get('invite','#')})", inline=False)
    await interaction.response.send_message(embed=embed, view=BotActionView(found))

@bot.tree.command(name="hub-premium", description="Show all Premium prices")
async def hub_premium(interaction: discord.Interaction):
    await interaction.response.send_message(embed=build_premium_embed(), ephemeral=True)

@bot.tree.command(name="hub-vote", description="Vote for a bot")
async def hub_vote(interaction: discord.Interaction, name: str):
    found = find_bot(name)
    if not found: return await interaction.response.send_message("❌ Not found!", ephemeral=True)
    uid = str(interaction.user.id)
    if found in db.get("voters", {}).get(uid, []):
        return await interaction.response.send_message(f"❌ You already voted for **{found}**!", ephemeral=True)
    db.setdefault("votes", {})[found] = db.get("votes", {}).get(found, 0) + 1
    db.setdefault("voters", {}).setdefault(uid, []).append(found)
    save()
    await interaction.response.send_message(f"✅ Voted for **{found}**! Total: 👍 {db['votes'][found]}", ephemeral=True)

@bot.tree.command(name="hub-top", description="Most voted bots")
async def hub_top(interaction: discord.Interaction):
    await interaction.response.send_message(embed=build_hub_embed(interaction.guild, sort_by_votes=True), ephemeral=True)

@bot.tree.command(name="hub-status", description="Live status of all bots")
async def hub_status(interaction: discord.Interaction):
    embed = discord.Embed(title="📡 NEXUS HUB - Live Status", description="🟢 = Online / 🔴 = Offline (if bot is in this server, real status - else assumed 🟢)", color=0x22C55E)
    for name, data in db["bots"].items():
        status = get_status_emoji(name, interaction.guild)
        embed.add_field(name=f"{status} {name}", value=f"{data.get('emoji','🤖')} Votes: {db.get('votes',{}).get(name,0)}", inline=True)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="hub-add", description="Add or update a bot in HUB (Staff)")
async def hub_add(interaction: discord.Interaction, name: str, description: str, invite: str, category: str = "Other", premium: str = "Free", premium_price: str = None, emoji: str = "🤖"):
    if not interaction.user.guild_permissions.manage_messages: return await interaction.response.send_message("❌ Need Manage Messages!", ephemeral=True)
    db["bots"][name.upper()] = {"emoji": emoji, "desc": description, "invite": invite, "premium": premium, "premium_price": premium_price or premium, "category": category}
    save()
    await interaction.response.send_message(f"✅ Added/Updated **{name.upper()}** to HUB!", ephemeral=True)

@bot.tree.command(name="hub-remove", description="Remove a bot from HUB (Staff)")
async def hub_remove(interaction: discord.Interaction, name: str):
    if not interaction.user.guild_permissions.manage_messages: return await interaction.response.send_message("❌ Need Manage Messages!", ephemeral=True)
    found = find_bot(name)
    if not found: return await interaction.response.send_message("❌ Not found!", ephemeral=True)
    del db["bots"][found]
    if found in db.get("votes", {}): del db["votes"][found]
    save()
    await interaction.response.send_message(f"✅ Removed **{found}** from HUB", ephemeral=True)

@bot.tree.command(name="hub-featured", description="Set featured bot (Staff)")
async def hub_featured(interaction: discord.Interaction, name: str):
    if not interaction.user.guild_permissions.manage_messages: return await interaction.response.send_message("❌ Need Manage Messages!", ephemeral=True)
    found = find_bot(name)
    if not found: return await interaction.response.send_message("❌ Not found!", ephemeral=True)
    db["featured"] = found; save()
    await interaction.response.send_message(f"⭐ Featured bot is now **{found}**!", ephemeral=True)

@bot.tree.command(name="hub-post", description="Post HUB embed in a channel (Staff)")
async def hub_post(interaction: discord.Interaction, channel: discord.TextChannel, title: str = None):
    if not interaction.user.guild_permissions.manage_messages: return await interaction.response.send_message("❌ Need Manage Messages!", ephemeral=True)
    embed = build_hub_embed(channel.guild)
    if title: embed.title = title
    await channel.send(embed=embed, view=HubView())
    await interaction.response.send_message(f"✅ HUB posted to {channel.mention}!", ephemeral=True)

@bot.tree.command(name="hub-help", description="Show HUB commands")
async def hub_help(interaction: discord.Interaction):
    embed = discord.Embed(title="👑 NEXUS HUB - Commands", description=f"Owner: {OWNER_USERNAME}", color=0x8B5CF6)
    embed.add_field(name="Everyone", value="`/hub` - See all bots\n`/hub category: Music` - Filter by category\n`/hub-search query: media` - Search\n`/hub-info name: NEXUS MEDIA` - Details + Invite + Vote/Buy/Support buttons\n`/hub-premium` - Prices\n`/hub-vote name: ...` - Vote\n`/hub-top` - Most voted\n`/hub-status` - Live status\n`!hub` / `!bots` / `!showcase` - Same as /hub", inline=False)
    embed.add_field(name="Staff", value="`/hub-add` - Add bot\n`/hub-remove` - Remove bot\n`/hub-featured` - Set featured\n`/hub-post channel: #bots` - Post embed", inline=False)
    embed.add_field(name="Auto", value="When a NEXUS/EVIL bot joins a server with HUB, HUB auto-adds it!", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.command(name="hub")
async def hub_prefix(ctx):
    await ctx.send(embed=build_hub_embed(ctx.guild), view=HubView())

@bot.command(name="bots", aliases=["showcase"])
async def bots_prefix(ctx):
    await ctx.send(embed=build_hub_embed(ctx.guild), view=HubView())

@bot.command(name="help")
async def help_prefix(ctx):
    embed = discord.Embed(title="👑 NEXUS HUB - Commands", description=f"Owner: {OWNER_USERNAME}", color=0x8B5CF6)
    embed.add_field(name="Everyone", value="`/hub` - See all bots\n`/hub category: Tools` - Filter by category\n`/hub-search query: media` - Search\n`/hub-info name: NEXUS MEDIA` - Details + Invite + Vote/Buy/Support buttons\n`/hub-premium` - Prices\n`/hub-vote name: ...` - Vote\n`/hub-top` - Most voted\n`/hub-status` - Live status\n`!hub` / `!bots` / `!showcase` / `!help` - Prefix commands", inline=False)
    embed.add_field(name="Staff", value="`/hub-add` - Add bot\n`/hub-remove` - Remove bot\n`/hub-featured` - Set featured\n`/hub-post channel: #bots` - Post embed", inline=False)
    embed.add_field(name="Auto", value="When a NEXUS bot joins a server with HUB, HUB auto-adds it!", inline=False)
    await ctx.send(embed=embed)

@bot.tree.command(name="claim-owner", description="Claim owner")
async def claim_owner(interaction: discord.Interaction, key: str):
    global OWNER_ID
    if key == RECOVERY_KEY:
        OWNER_ID = str(interaction.user.id)
        await interaction.response.send_message("✅ You are now Owner!", ephemeral=True)
    else:
        await interaction.response.send_message("❌ Wrong key", ephemeral=True)

TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN.strip() if TOKEN else '')
            
