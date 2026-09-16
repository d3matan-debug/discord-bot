import os
import discord
from discord.ext import commands, tasks

TOKEN = os.getenv("DISCORD_TOKEN")
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run():
 app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()




import datetime
import random
import asyncio
from twilio.rest import Client  # ספריית טוויליו לשליחת SMS

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

STAFF_ROLE_ID = 1549355771664277644
MANAGEMENT_ROLE_ID = 1549565301677367376

welcome_channels = {}
user_xp = {}
user_messages_count = {} # מעקב הודעות להגרלות

# משתנה גלובלי שמנהל האם "מצב רובוט" מופעל עבורך
robot_mode_users = set()

def get_xp(user_id):
    return user_xp.get(user_id, 0)

def add_xp(user_id, amount):
    user_xp[user_id] = get_xp(user_id) + amount


# === פקודה לשליחת SMS דרך Twilio ===
@bot.command(name="sendsms")
async def sendsms(ctx, phone_number: str = None, *, message_text: str = None):
    if str(ctx.author.id) != "1530201401710346370":
        await ctx.send("❌ אין לך הרשאה להשתמש בפקודה זו!", delete_after=5)
        try:
            await ctx.message.delete()
        except:
            pass
        return

    try:
        await ctx.message.delete()
    except:
        pass

    if not phone_number or not message_text:
        await ctx.send("❌ שימוש שגוי! יש לכתוב: `!sendsms +972500000000 תוכן ההודעה`", delete_after=10)
        return

    # החלף בפרטי ה-Twilio האמיתיים שלך
    account_sid = 'ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    auth_token = 'your_actual_auth_token_here'
    twilio_number = '+15551234567'

    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=message_text,
            from_=twilio_number,
            to=phone_number
        )
        await ctx.send(f"✅ הודעת ה-SMS נשלחה בהצלחה למספר {phone_number}! (SID: `{message.sid}`)", delete_after=10)
    except Exception as e:
        await ctx.send(f"❌ שגיאה בשליחת ה-SMS: {e}", delete_after=10)


@bot.command(name="xpshop")
async def xpshop(ctx):
    embed = discord.Embed(
        title="🛒 חנות XP",
        description="🚧 **בשיפוצים!**\n\nקניות בקרוב זה יצא לאור... **Coming Soon....** 🚀",
        color=discord.Color.gold()
    )
    embed.set_footer(text="MasterOhad Server System")
    await ctx.send(embed=embed)


@bot.command(name="setwelcome")
async def setwelcome(ctx):
    if str(ctx.author.id) != "1530201401710346370":
        await ctx.send("❌ אין לך הרשאה להפעיל פקודה זו!", delete_after=5)
        try:
            await ctx.message.delete()
        except:
            pass
        return

    try:
        await ctx.message.delete()
    except:
        pass

    welcome_channels[ctx.guild.id] = ctx.channel.id
    embed = discord.Embed(
        title="✅ ערוץ הברכות הוגדר בהצלחה!",
        description=f"מעכשיו הודעות ה-Welcome יישלחו לכאן: {ctx.channel.mention}",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed, delete_after=10)


@bot.command(name="lockdown")
async def lockdown(ctx):
    if str(ctx.author.id) != "1530201401710346370":
        await ctx.send("❌ אין לך הרשאה להפעיל פקודה זו!", delete_after=5)
        try:
            await ctx.message.delete()
        except:
            pass
        return

    try:
        await ctx.message.delete()
    except:
        pass

    guild = ctx.guild
    owner_member = guild.get_member(1530201401710346370)
    
    for channel in guild.channels:
        try:
            await channel.set_permissions(guild.default_role, read_messages=False)
            if owner_member:
                await channel.set_permissions(owner_member, read_messages=True, send_messages=True, manage_channels=True)
        except:
            pass

    target_channel = ctx.channel
    for ch in guild.text_channels:
        if "general" in ch.name.lower() or "כללי" in ch.name:
            target_channel = ch
            break

    try:
        await target_channel.set_permissions(guild.default_role, read_messages=True, send_messages=False)
        if owner_member:
            await target_channel.set_permissions(owner_member, read_messages=True, send_messages=True)
    except:
        pass

    embed = discord.Embed(
        title="🚨 **מצב חירום עליון — סגירת שרת** 🚨",
        description=(
            "**איתן ניסים בשורה הראשונה תוקף את השרת!**\n\n"
            "מלחמת העולם השלישית התחילה!\n"
            "היטלר שולט על ישראל, אנחנו במתקפה חמורה!\n"
            "אנה פרנק זה רק עניין של זמן, הארון זה רק מסווה קטן!\n\n"
            "⚠️ **כולם להיכנס לממ״ד מיד!** ⚠️"
        ),
        color=discord.Color.dark_red()
    )
    await target_channel.send(embed=embed)


@bot.command(name="unlockdown")
async def unlockdown(ctx):
    if str(ctx.author.id) != "1530201401710346370":
        await ctx.send("❌ אין לך הרשאה להפעיל פקודה זו!", delete_after=5)
        try:
            await ctx.message.delete()
        except:
            pass
        return

    try:
        await ctx.message.delete()
    except:
        pass

    guild = ctx.guild
    for channel in guild.channels:
        try:
            await channel.set_permissions(guild.default_role, read_messages=None, send_messages=None)
        except:
            pass

    target_channel = ctx.channel
    for ch in guild.text_channels:
        if "general" in ch.name.lower() or "כללי" in ch.name:
            target_channel = ch
            break

    embed = discord.Embed(
        title="🎉 **הניצחון הגיע — השרת נפתח מחדש!** 🎉",
        description=(
            "**היטלר ואיתן ניסים נכבשו על ידי רונן גיגי!**\n\n"
            "המלחמה נגמרה בהצלחה אדירה!\n\n"
            "🚪 **אפשר לצאת מהממ״ד!** 🚪"
        ),
        color=discord.Color.green()
    )
    await target_channel.send(embed=embed)


@bot.command(name="say")
async def say(ctx, *, message: str = None):
    if str(ctx.author.id) != "1530201401710346370":
        await ctx.send("❌ אין לך הרשאה להשתמש בפקודה זו!", delete_after=5)
        try:
            await ctx.message.delete()
        except:
            pass
        return

    if not message:
        await ctx.send("❌ שכחת לכתוב את ההודעה אחרי !say", delete_after=5)
        try:
            await ctx.message.delete()
        except:
            pass
        return

    try:
        await ctx.message.delete()
    except:
        pass

    await ctx.send(message)


@bot.event
async def on_member_join(member):
    target_channel = None
    if member.guild.id in welcome_channels:
        target_channel = member.guild.get_channel(welcome_channels[member.guild.id])
    
    if not target_channel:
        for ch in member.guild.text_channels:
            if "welcome" in ch.name.lower() or "ברוכים" in ch.name or "join" in ch.name:
                target_channel = ch
                break
    
    if not target_channel and member.guild.text_channels:
        target_channel = member.guild.text_channels[0]

    if not target_channel:
        return

    embed = discord.Embed(
        title=f"ברוכים הבאים — {member.guild.name}",
        description=f"היי {member.mention} , ברוכים הבאים לשרת!\nאנו מקווים שתהנה בשרת, לא לשכוח לקרוא את החוקים!",
        color=discord.Color.blurple()
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text=f"{member.guild.member_count} Members")
    await target_channel.send(embed=embed)


# === פונקציית יצירת ה-Embed לטיקט ===
def create_ticket_embed(member):
    embed = discord.Embed(
        title="טיקט בחינה לצוות",
        description=f"היי {member.mention} , תודה שפתחת טיקט בחינה לצוות.",
        color=discord.Color.from_rgb(47, 49, 54)
    )
    embed.add_field(
        name="⚠️ בזמן שאתה מחכה:",
        value="• אל תתייג את הצוות! חכה למענה שלהם.\n• אם חסר משהו, זה הזמן לשלוח: צילומי מסך, סרטונים, קבצים או כל דבר שיעזור להבין מהר.",
        inline=False
    )
    embed.set_footer(text="במידה ותטרילו בטיקט, תקבלו הרחקה תמידית מפתיחת טיקטים.")
    return embed


def create_questions_message(member):
    return (
        f"📋 **שאלות הבחינה בכתב עבור {member.mention} (10 שאלות):**\n\n"
        f"1. **מה הגיל שלך ומה הרקע הקודם שלך בניהול שרתי דיסקורד?**\n"
        f"2. **כיצד תפעל במקרה של ספאם מתמשך או קללות חריפות בצאט הציבורי?**\n"
        f"3. **מה הוביל אותך לרצות להצטרף דווקא לצוות הניהול שלנו בשרת?**\n"
        f"4. **כמה שעות פעילות אתה יכול להשקיע ביום בשרת ובמענה לטיקטים?**\n"
        f"5. **איך תגיב אם שחקן או משתמש יתחיל לתייג אותך בלי הפסקה ולהציק לך בפרטי?**\n"
        f"6. **תן דוגמה למקרה שבו נדרשת לקבל החלטה מהירה וקשה תחת לחץ – איך התמודדת?**\n"
        f"7. **שאלה על החיים:** מה תחביב העיקרי שלך כשאתה לא נמצא בדיסקורד (ספורט, מחשב, גיטרות וכו')?\n"
        f"8. **שאלה על החיים:** מה הסדרה, האנימה או המשחק האهובים עליך ביותר כרגע?\n"
        f"9. **שאלה קלילה:** אם היה לך כוח על אחד ליום אחד בלבד, מה היית בוחר לעשות איתו?\n"
        f"10. **למה לדעתך מגיע דווקא לך ולא לאחרים לקבל את התפקיד בצוות?**"
    )


class RobotTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(style=discord.ButtonStyle.secondary, emoji="🎫", custom_id="robot_open_ticket_btn")
    async def open_ticket_from_robot(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        member = interaction.user
        staff_role = guild.get_role(STAFF_ROLE_ID)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            member: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            staff_role: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True, manage_channels=True)
        }

        category = interaction.channel.category
        ticket_channel = await guild.create_text_channel(
            name=f"apply-{member.name}",
            category=category,
            overwrites=overwrites
        )
        
        view = TicketControlView()
        embed = create_ticket_embed(member)
        
        await ticket_channel.send(embed=embed, view=view)
        await ticket_channel.send(create_questions_message(member))
        
        await interaction.response.send_message(f"✅ טיקט הבחינה שלך נפתח כאן: {ticket_channel.mention}", ephemeral=True)


# === פאנל הגרלות מטורף ומתקדם (Giveaway System) ===

class GiveawayModal(discord.ui.Modal, title="🎉 יצירת הגרלה חדשה מטורפת"):
    prize = discord.ui.TextInput(label="🎁 מה הפרס בהגרלה?", placeholder="למשל: Nitro Boost / 100K XP / משחק לבחירה", required=True)
    winners_count = discord.ui.TextInput(label="🏆 כמה מנצחים?", placeholder="למשל: 1", default="1", required=True)
    duration_minutes = discord.ui.TextInput(label="⏳ משך ההגרלה (בדקות)", placeholder="למשל: 5 (או 60 לשעה)", default="5", required=True)
    
    min_msg = discord.ui.TextInput(label="💬 מינימום הודעות בשרת", placeholder="0 בשביל בלי הגבלה", default="0", required=False)
    min_voice_hours = discord.ui.TextInput(label="🎧 מינימום שעות בוויס", placeholder="0 בשביל בלי הגבלה", default="0", required=False)
    must_be_in_voice = discord.ui.TextInput(label="🎙️ חייב להיות עכשיו בוויס? (כן / לא)", placeholder="לא", default="לא", required=False)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        try:
            w_count = int(self.winners_count.value)
            duration = int(self.duration_minutes.value)
            m_msg = int(self.min_msg.value or 0)
            m_voice = float(self.min_voice_hours.value or 0)
        except:
            await interaction.followup.send("❌ שגיאה במספרים שהוזנו! נא לוודא ששדות המספרים מכילים ספרות בלבד.", ephemeral=True)
            return

        in_voice_req = self.must_be_in_voice.value.strip().lower() in ["כן", "yes", "true", "1"]
        end_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=duration)
        end_timestamp = int(end_time.timestamp())

        # בניית דרישות לתצוגה בהודעה
        requirements_list = []
        if m_msg > 0:
            requirements_list.append(f"• מינימום **{m_msg} הודעות** בשרת")
        if m_voice > 0:
            requirements_list.append(f"• מינימום **{m_voice} שעות** בחדרי קול")
        if in_voice_req:
            requirements_list.append(f"• חייב להיות **מחובר לחדר קול (Voice)** כרגע!")
        
        req_text = "\n".join(requirements_list) if requirements_list else "• אין דרישות מיוחדות! כולם יכולים להשתתף 🚀"

        embed = discord.Embed(
            title="🎉 **הגרלת ענק נוצצת בשרת!** 🎉",
            description=(
                f"### 🎁 פרס שווה במיוחד:\n"
                f"✨ **{self.prize.value}** ✨\n\n"
                f"🏆 **מספר זוכים מאושרים:** `{w_count}`\n"
                f"⏳ **מסתיימת בעוד:** <t:{end_timestamp}:R> (<t:{end_timestamp}:f>)\n\n"
                f"📌 **תנאי השתתפות בהגרלה:**\n"
                f"{req_text}\n\n"
                f"👇 **לחץ על הכפתור למטה כדי להיכנס להגרלה!**"
            ),
            color=discord.Color.from_rgb(255, 0, 128)
        )
        embed.set_footer(text=f"מומלץ על ידי Admin Adolf | נוצר על ידי {interaction.user.name}", icon_url=interaction.user.display_avatar.url)

        view = GiveawayView(prize=self.prize.value, winners=w_count, min_msg=m_msg, min_voice=m_voice, in_voice=in_voice_req, end_timestamp=end_timestamp)
        
        msg = await interaction.channel.send(embed=embed, view=view)
        await interaction.followup.send(f"✅ ההגרלה הופעלה בהצלחה בחדר {interaction.channel.mention}!", ephemeral=True)

        # טיימר להפעלת תוצאות ההגרלה בסיום הזמן
        bot.loop.create_task(run_giveaway_timer(msg, duration, self.prize.value, w_count, m_msg, m_voice, in_voice_req))


class GiveawayView(discord.ui.View):
    def __init__(self, prize, winners, min_msg, min_voice, in_voice, end_timestamp):
        super().__init__(timeout=None)
        self.prize = prize
        self.winners = winners
        self.min_msg = min_msg
        self.min_voice = min_voice
        self.in_voice = in_voice
        self.end_timestamp = end_timestamp
        self.participants = set()

    @discord.ui.button(label="השתתף בהגרלה 🎁", style=discord.ButtonStyle.success, custom_id="join_giveaway_btn")
    async def join_giveaway(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        if user.bot:
            return

        # בדיקת עמידה בתנאים
        user_id = user.id
        msg_count = user_messages_count.get(user_id, 0)
        user_minutes_in_voice = get_xp(user_id) / 4 # כל 4 XP = דקה בוויס לפי מערכת הקול שלנו
        user_hours_in_voice = user_minutes_in_voice / 60

        # בדיקת הימצאות בוויס כרגע
        currently_in_voice = bool(user.voice and user.voice.channel and not user.voice.self_deaf)

        errors = []
        if msg_count < self.min_msg:
            errors.append(f"• חסרות לך עוד {self.min_msg - msg_count} הודעות (יש לך {msg_count})")
        if user_hours_in_voice < self.min_voice:
            errors.append(f"• נדרשות עוד {round(self.min_voice - user_hours_in_voice, 1)} שעות בוויס")
        if self.in_voice and not currently_in_voice:
            errors.append(f"• אתה חייב להיות מחובר לחדר קול (Voice) כרגע כדי להשתתף!")

        if errors:
            err_msg = "❌ **אינך עומד בתנאי ההגרלה הבאים:**\n" + "\n".join(errors)
            await interaction.response.send_message(err_msg, ephemeral=True)
            return

        if user_id in self.participants:
            self.participants.remove(user_id)
            await interaction.response.send_message("❌ יצאת מההגרלה בהצלחה.", ephemeral=True)
        else:
            self.participants.add(user_id)
            await interaction.response.send_message(f"✅ **נרשמת בהצלחה להגרלה!** בהצלחה בזיכייה ב-{self.prize} 🍀", ephemeral=True)


async def run_giveaway_timer(message, duration_minutes, prize, winners_count, min_msg, min_voice, in_voice_req):
    await asyncio.sleep(duration_minutes * 60)
    
    # שליפת המשתתפים מהוויו של ההודעה אם קיים
    participants = []
    for component in message.components:
        for child in component.children:
            if hasattr(child, "view") and hasattr(child.view, "participants"):
                participants = list(child.view.participants)

    guild = message.guild
    valid_winners = []

    # סינון נוסף לוודא שעדיין עומדים בתנאים
    for uid in participants:
        member = guild.get_member(uid)
        if member:
            valid_winners.append(member)

    if valid_winners:
        actual_winners_count = min(winners_count, len(valid_winners))
        winners = random.sample(valid_winners, actual_winners_count)
        winners_mention = ", ".join([w.mention for w in winners])

        end_embed = discord.Embed(
            title="🎉 **ההגרלה הסתיימה!** 🎉",
            description=(
                f"🎁 **הפרס:** {prize}\n\n"
                f"🏆 **הזוכים המאושרים:**\n{winners_mention}\n\n"
                f"כל הכבוד לזוכים! תודה לכל השאר שהשתתפו 🚀"
            ),
            color=discord.Color.gold()
        )
    else:
        end_embed = discord.Embed(
            title="🎉 **ההגרלה הסתיימה!** 🎉",
            description=f"🎁 **הפרס:** {prize}\n\n❌ **לצערנו אף אחד לא נרשם או עמד בתנאים, אין זוכה בהגרלה זו.**",
            color=discord.Color.dark_red()
        )

    try:
        await message.edit(embed=end_embed, view=None)
        if valid_winners:
            await message.channel.send(f"🎊 כל הכבוד ל-{winners_mention} שזכו ב-**{prize}**! תפתחו טיקט כדי לאסוף את הפרס.")
    except:
        pass


# === מודל מחיקת הודעות מהירה מהפאנל ===
class PurgeMessagesModal(discord.ui.Modal, title="מחיקת הודעות מרוכזת (Purge)"):
    amount = discord.ui.TextInput(label="כמה הודעות למחוק?", placeholder="מספר בין 1 ל-100", default="10", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        try:
            limit = int(self.amount.value)
            limit = max(1, min(limit, 100))
            deleted = await interaction.channel.purge(limit=limit)
            await interaction.followup.send(f"🗑️ נמחקו בהצלחה **{len(deleted)}** הודעות מהחדר!", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ שגיאה במחיקת הודעות: {e}", ephemeral=True)


# === פאנל הניהול Admin Adolf ===

class EmojiSelect(discord.ui.Select):
    def __init__(self, guild):
        options = []
        for emoji in guild.emojis[:25]:
            options.append(discord.SelectOption(label=emoji.name[:25], value=str(emoji.id), description=f":{emoji.name}:", emoji=emoji))
        if not options:
            options.append(discord.SelectOption(label="אין אמוג'ים בשרת", value="none"))
        super().__init__(placeholder="😀 בחר אמוג'י מהשרת להעתקה...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "none":
            await interaction.response.send_message("❌ אין אמוג'ים מותאמים אישית בשרת זה.", ephemeral=True)
            return
        
        emoji_id = int(self.values[0])
        emoji_obj = interaction.guild.get_emoji(emoji_id)
        if emoji_obj:
            await interaction.response.send_message(f"הנה האמוג'י שבחרת: {emoji_obj} (`{str(emoji_obj)}`)", ephemeral=True)
        else:
            await interaction.response.send_message("❌ האמוג'י לא נמצא.", ephemeral=True)

class EmojiSelectView(discord.ui.View):
    def __init__(self, guild):
        super().__init__(timeout=60)
        self.add_item(EmojiSelect(guild))


class SendDMModal(discord.ui.Modal, title="שליחת הודעה בפרטי (DM / Spam)"):
    user_id = discord.ui.TextInput(label="ID של המשתמש", placeholder="הזן מזהה משתמש...", required=True)
    dm_text = discord.ui.TextInput(label="תוכן ההודעה", style=discord.TextStyle.paragraph, placeholder="תוכן ההודעה...", required=True, max_length=4000)
    is_spam = discord.ui.TextInput(label="מצב ספאם? (כן / לא)", placeholder="רשום 'כן' או 'לא'", default="לא", required=False)
    spam_count = discord.ui.TextInput(label="כמה פעמים לשלוח?", placeholder="למשל: 5", default="1", required=False)
    spam_delay = discord.ui.TextInput(label="השהייה בשניות בין הודעות", placeholder="למשל: 1", default="1", required=False)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        try:
            target_user = await interaction.client.fetch_user(int(self.user_id.value))
            text = f"💬 **הודעה מהנהלת השרת:**\n{self.dm_text.value}"
            spam_mode = self.is_spam.value.strip().lower() in ["כן", "yes", "true", "1"]
            
            if not spam_mode:
                await target_user.send(text)
                await interaction.followup.send(f"✅ ההודעה נשלחה ל-DM של {target_user.name}!", ephemeral=True)
            else:
                try:
                    count = int(self.spam_count.value)
                except:
                    count = 3
                try:
                    delay = float(self.spam_delay.value)
                except:
                    delay = 1.0

                count = max(1, min(count, 30))
                delay = max(0.2, min(delay, 10.0))

                await interaction.followup.send(f"🚀 מתחיל לשלוח ספאם ({count} פעמים) ל-{target_user.name}...", ephemeral=True)
                for i in range(count):
                    try:
                        await target_user.send(f"{text} `[{i+1}/{count}]`")
                    except:
                        pass
                    if i < count - 1:
                        await asyncio.sleep(delay)
        except Exception as e:
            await interaction.followup.send(f"❌ שגיאה: {e}", ephemeral=True)


class ManageUserModal(discord.ui.Modal, title="ניהול משתמש בשרת"):
    user_id = discord.ui.TextInput(label="ID של המשתמש", placeholder="הזן מזהה משתמש...", required=True)
    action = discord.ui.TextInput(label="פעולה (ban / timeout / kick)", placeholder="ban או timeout או kick", required=True)
    reason = discord.ui.TextInput(label="סיבה", placeholder="סיבה לעונש...", required=False, max_length=500)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        try:
            uid = int(self.user_id.value)
            member = interaction.guild.get_member(uid)
            act = self.action.value.lower()
            res = self.reason.value or "ללא סיבה"

            if act == "ban":
                await interaction.guild.ban(discord.Object(id=uid), reason=res)
                await interaction.followup.send("⛔ המשתמש הורחק (Ban) בהצלחה!", ephemeral=True)
            elif act == "kick" and member:
                await member.kick(reason=res)
                await interaction.followup.send(f"👞 המשתמש {member.name} הוצא (Kick) מהשרת!", ephemeral=True)
            elif act == "timeout" and member:
                await member.timeout(datetime.timedelta(minutes=60), reason=res)
                await interaction.followup.send(f"⏰ המשתמש {member.name} קיבל Timeout לשעה!", ephemeral=True)
            else:
                await interaction.followup.send("❌ פעולה לא תקינה או משתמש לא נמצא.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ שגיאה בביצוע הפעולה: {e}", ephemeral=True)


class DeleteChannelSelect(discord.ui.Select):
    def __init__(self, channels):
        options = []
        for ch in channels[:25]:
            options.append(discord.SelectOption(label=ch.name[:25], value=str(ch.id), description=f"סוג: {ch.type}"))
        super().__init__(placeholder="🗑️ בחר חדר למחיקה...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        ch_id = int(self.values[0])
        channel = interaction.guild.get_channel(ch_id)
        if channel:
            c_name = channel.name
            await channel.delete()
            await interaction.response.send_message(f"🗑️ החדר **{c_name}** נמחק בהצלחה!", ephemeral=True)
        else:
            await interaction.response.send_message("❌ החדר לא נמצא.", ephemeral=True)

class DeleteChannelView(discord.ui.View):
    def __init__(self, guild):
        super().__init__(timeout=None)
        self.add_item(DeleteChannelSelect(guild.channels))


class GetRoleSelect(discord.ui.Select):
    def __init__(self, roles):
        options = []
        for r in roles[:25]:
            if not r.is_default():
                options.append(discord.SelectOption(label=r.name[:25], value=str(r.id)))
        super().__init__(placeholder="👑 בחר רול שברצונך לקבל...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        r_id = int(self.values[0])
        role = interaction.guild.get_role(r_id)
        if role:
            try:
                await interaction.user.add_roles(role)
                await interaction.response.send_message(f"✅ קיבלת את הרול **{role.name}**!", ephemeral=True)
            except Exception as e:
                await interaction.response.send_message(f"❌ שגיאה: {e}", ephemeral=True)

class GetRoleView(discord.ui.View):
    def __init__(self, guild):
        super().__init__(timeout=None)
        self.add_item(GetRoleSelect(guild.roles))


class AdminAdolfView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="מחק חדר", style=discord.ButtonStyle.danger, emoji="🗑️", custom_id="admin_del_ch_btn", row=0)
    async def delete_channel_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("בחר מתוך התפריט את החדר שברצונך למחוק:", view=DeleteChannelView(interaction.guild), ephemeral=True)

    @discord.ui.button(label="מחיקת הודעות", style=discord.ButtonStyle.danger, emoji="🧹", custom_id="admin_purge_msg_btn", row=0)
    async def purge_msg_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(PurgeMessagesModal())

    @discord.ui.button(label="קבל רול בשרת", style=discord.ButtonStyle.success, emoji="👑", custom_id="admin_get_role_btn", row=0)
    async def get_any_role_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("בחר איזה רול תרצה לקבל:", view=GetRoleView(interaction.guild), ephemeral=True)

    @discord.ui.button(label="צור הגרלה חדשה 🎉", style=discord.ButtonStyle.primary, emoji="🎁", custom_id="admin_create_giveaway_btn", row=1)
    async def create_giveaway_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(GiveawayModal())

    @discord.ui.button(label="בחר אמוג'י מהשרת", style=discord.ButtonStyle.primary, emoji="😀", custom_id="admin_get_emoji_btn", row=1)
    async def get_emoji_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("בחר אמוג'י מהרשימה כדי לקבל אותו:", view=EmojiSelectView(interaction.guild), ephemeral=True)

    @discord.ui.button(label="מצב רובוט: כבוי", style=discord.ButtonStyle.secondary, emoji="🤖", custom_id="toggle_robot_mode_btn", row=2)
    async def toggle_robot_mode(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = str(interaction.user.id)
        if user_id in robot_mode_users:
            robot_mode_users.remove(user_id)
            button.label = "מצב רובוט: כבוי"
            button.style = discord.ButtonStyle.secondary
            await interaction.response.edit_message(view=self)
            await interaction.followup.send("🔴 מצב רובוט כובה בהצלחה.", ephemeral=True)
        else:
            robot_mode_users.add(user_id)
            button.label = "מצב רובוט: מופעל"
            button.style = discord.ButtonStyle.success
            await interaction.response.edit_message(view=self)
            await interaction.followup.send("🟢 מצב רובוט הופעל! מעכשיו כל הודעה שתכתוב תשלח על ידי הבוט עם כפתור טיקט קטן.", ephemeral=True)

    @discord.ui.button(label="שלח הודעה בפרטי (DM)", style=discord.ButtonStyle.secondary, emoji="✉️", custom_id="admin_send_dm_btn", row=2)
    async def send_dm_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(SendDMModal())

    @discord.ui.button(label="ניהול משתמשים (Ban/Timeout)", style=discord.ButtonStyle.danger, emoji="🔨", custom_id="admin_manage_user_btn", row=3)
    async def manage_user_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ManageUserModal())

    @discord.ui.button(label="הוסף 100K XP", style=discord.ButtonStyle.green, emoji="💰", custom_id="admin_add_xp_btn", row=3)
    async def add_money(self, interaction: discord.Interaction, button: discord.ui.Button):
        add_xp(interaction.user.id, 100000)
        await interaction.response.send_message(f"💰 נוספו לך 100,000 XP! המאזן: **{get_xp(interaction.user.id):,} XP**", ephemeral=True)


@bot.command(name="admin_adolf")
async def admin_adolf(ctx):
    if str(ctx.author.id) != "1530201401710346370":
        await ctx.send("❌ אין לך הרשאה להשתמש בפקודה הזו!", delete_after=5)
        try:
            await ctx.message.delete()
        except:
            pass
        return

    try:
        await ctx.message.delete()
    except:
        pass

    embed = discord.Embed(
        title="👑 Admin Adolf — פאנל שליטה ראשי",
        description="ברוך הבא לפאנל הניהול הבלעדי שלך! לחץ על הלחצנים למטה לביצוע כל פעולה בשרת:",
        color=discord.Color.dark_red()
    )
    embed.add_field(name="💰 מאזן XP אישי", value=f"**{get_xp(ctx.author.id):,} XP**", inline=False)
    embed.set_footer(text="Master Control Panel")

    await ctx.send(embed=embed, view=AdminAdolfView(), delete_after=120)


# === מערכת הטיקטים לבחינה ===

class TicketControlView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="לקחת", style=discord.ButtonStyle.primary, custom_id="claim_ticket_btn", row=0)
    async def claim_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        staff_role = interaction.guild.get_role(STAFF_ROLE_ID)
        if staff_role not in interaction.user.roles:
            await interaction.response.send_message("רק אנשי צוות יכולים לקחת טיקט!", ephemeral=True)
            return
        button.disabled = True
        button.label = "נלקח על ידי " + interaction.user.name
        button.style = discord.ButtonStyle.secondary
        await interaction.message.edit(view=self)
        await interaction.response.send_message(f"✅ הטיקט נלקח על ידי {interaction.user.mention}.")

    @discord.ui.button(label="סגור", style=discord.ButtonStyle.danger, custom_id="close_ticket_btn", row=0)
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        staff_role = interaction.guild.get_role(STAFF_ROLE_ID)
        if staff_role not in interaction.user.roles:
            await interaction.response.send_message("רק אנשי צוות יכולים לסגור טיקט!", ephemeral=True)
            return
        await interaction.response.send_message("🔒 הטיקט ייסגר בעוד 5 שניות...")
        await asyncio.sleep(5)
        try:
            await interaction.channel.delete()
        except:
            pass

    @discord.ui.button(label="בקשת סגירה", style=discord.ButtonStyle.secondary, custom_id="req_close_btn", row=0)
    async def request_close(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("📌 הוגשה בקשת סגירה לטיקט זה. ממתין לאישור צוות.", ephemeral=True)

    @discord.ui.button(label="קריאה להנהלה", style=discord.ButtonStyle.danger, custom_id="call_management_btn", row=1)
    async def call_management(self, interaction: discord.Interaction, button: discord.ui.Button):
        staff_role = interaction.guild.get_role(STAFF_ROLE_ID)
        if staff_role not in interaction.user.roles:
            await interaction.response.send_message("רק אנשי צוות יכולים להשתמש בכפתור זה!", ephemeral=True)
            return
        mgmt_role = interaction.guild.get_role(MANAGEMENT_ROLE_ID)
        mgmt_mention = mgmt_role.mention if mgmt_role else "@הנהלה"
        await interaction.response.send_message(f"🚨 {mgmt_mention} — חבר צוות קרא להנהלה לטיקט זה!")

    @discord.ui.button(label="עבר את הבחינה בכתב", style=discord.ButtonStyle.success, custom_id="passed_written_exam_btn", row=1)
    async def passed_written_exam(self, interaction: discord.Interaction, button: discord.ui.Button):
        staff_role = interaction.guild.get_role(STAFF_ROLE_ID)
        if staff_role not in interaction.user.roles:
            await interaction.response.send_message("רק אנשי צוות יכולים לאשר מעבר שלב!", ephemeral=True)
            return
            
        success_text = (
            f"✅ **המשתמש עבר בהצלחה את שלב הבחינה בכתב!**\n\n"
            f"📌 שימו לב: **הרול טרם הוענק.** מעכשיו על המועמד לעבור את **הבחינה הקולית בווייס** מול חבר הנהלה/אחראי.\n"
            f"⏳ אנא המתינו בסבלנות לקריאה לחדר הדיבורים."
        )
        await interaction.response.send_message(success_text)


class TicketSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Staff Application | בחינה לצוות", description="פתיחת טיקט להגשת מועמדות ובחינה לצוות", value="staff_apply")
        ]
        super().__init__(placeholder="בחר את נושא הפנייה שלך...", min_values=1, max_values=1, options=options, custom_id="arcade_ticket_select")

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user
        staff_role = guild.get_role(STAFF_ROLE_ID)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            member: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            staff_role: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True, manage_channels=True)
        }

        category = interaction.channel.category
        ticket_channel = await guild.create_text_channel(
            name=f"apply-{member.name}",
            category=category,
            overwrites=overwrites
        )
        view = TicketControlView()
        embed = create_ticket_embed(member)
        
        await ticket_channel.send(embed=embed, view=view)
        await ticket_channel.send(create_questions_message(member))
        
        await interaction.response.send_message(f"הטיקט נפתח כאן: {ticket_channel.mention}", ephemeral=True)

class TicketView(discord.ui.View):
    def __init__(self, guild=None):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())

@bot.command(name="ticket")
async def ticket_cmd(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    
    guild = ctx.guild
    member = ctx.author
    staff_role = guild.get_role(STAFF_ROLE_ID)

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        member: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
        staff_role: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True, manage_channels=True)
    }

    category = ctx.channel.category
    ticket_channel = await guild.create_text_channel(
        name=f"apply-{member.name}",
        category=category,
        overwrites=overwrites
    )
    view = TicketControlView()
    embed = create_ticket_embed(member)
    
    await ticket_channel.send(embed=embed, view=view)
    await ticket_channel.send(create_questions_message(member))
    
    await ctx.send(f"✅ טיקט הבחינה שלך נפתח כאן: {ticket_channel.mention}", delete_after=5)


@bot.event
async def on_ready():
    bot.add_view(TicketView())
    bot.add_view(AdminAdolfView())
    if not give_voice_xp.is_running():
        give_voice_xp.start()
    print(f"Logged in as bot {bot.user}")

@tasks.loop(minutes=1)
async def give_voice_xp():
    for guild in bot.guilds:
        for member in guild.members:
            if not member.bot and member.voice and member.voice.channel and not member.voice.self_deaf:
                add_xp(member.id, 4)

# === מעקב הודעות למתן XP, ספירת הודעות ומצב רובוט ===
@bot.event
async def on_message(message):
    if message.guild and not message.author.bot:
        add_xp(message.author.id, 1)
        
        # ספירת הודעות לצורך דרישות הגרלות
        user_messages_count[message.author.id] = user_messages_count.get(message.author.id, 0) + 1

        # בדיקה האם מצב רובוט פעיל עבורך
        if str(message.author.id) == "1530201401710346370" and str(message.author.id) in robot_mode_users:
            if not message.content.startswith("!"):
                user_text = message.content
                try:
                    await message.delete()
                except:
                    pass



                await message.channel.send(user_text, view=RobotTicketView())          
# keep_alive() צריך להיות מופעל ממש לפני הרצת הבוט או ממש בהתחלה
bot.run(TOKEN)
