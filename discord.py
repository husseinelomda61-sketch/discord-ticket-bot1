import discord
from discord.ext import commands
from discord.ui import Button, View, Select

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)


class TicketSelect(Select):

  def __init__(self):
    options = [
        discord.SelectOption(
            label="توثيق", description="اضغط هنا لطلب التوثيق", emoji="✅"
        ),
        discord.SelectOption(
            label="شكوى على إداري",
            description="لتقديم شكوى ضد إداري",
            emoji="⚠️",
        ),
        discord.SelectOption(
            label="شكوى", description="لتقديم شكوى عامة", emoji="📌"
        ),
        discord.SelectOption(
            label="تقديم إدارة",
            description="للتقديم على رتبة الإدارة",
            emoji="💼",
        ),
    ]
    super().__init__(
        placeholder="...اختر نوع التذكرة",
        min_values=1,
        max_values=1,
        options=options,
    )

  async def callback(self, interaction: discord.Interaction):
    guild = interaction.guild
    category = discord.utils.get(guild.categories, name="تذاكر الدعم")
    if not category:
      category = await guild.create_category("تذاكر الدعم")

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        interaction.user: discord.PermissionOverwrite(
            read_messages=True, send_messages=True
        ),
        guild.me: discord.PermissionOverwrite(
            read_messages=True, send_messages=True
        ),
    }

    # إنشاء روم خاصة بالتذكرة
    channel = await guild.create_text_channel(
        f"ticket-{interaction.user.name}-{self.values[0]}",
        category=category,
        overwrites=overwrites,
    )

    await interaction.response.send_message(
        f"تم فتح التذكرة بنجاح في الروم: {channel.mention}", ephemeral=True
    )
    await channel.send(
        f"مرحباً {interaction.user.mention}! لقد اخترت قسم: **{self.values[0]}**. سيتم الرد عليك قريباً من قبل الإدارة."
    )


class TicketView(View):

  def __init__(self):
    super().__init__(timeout=None)
    self.add_item(TicketSelect())


@bot.event
async def on_ready():
  print(f"Logged in as {bot.user.name}")


@bot.command()
async def ticket(ctx):
  embed = discord.Embed(
      title="تذاكر الدعم",
      description="اختر نوع التذكرة من القائمة بالأسفل لفتح تذكرة.",
      color=0x2F3136,
  )
  await ctx.send(embed=embed, view=TicketView())


# حط هنا توكن البوت بتاعك
bot.run("YOUR_BOT_TOKEN")