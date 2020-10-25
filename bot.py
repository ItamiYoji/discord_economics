import discord
from discord.ext import commands
import datetime
import sqlite3
from discord.utils import get
import asyncio
import tracemalloc

PREFIX = '!'
client = commands.Bot(command_prefix = PREFIX)
client.remove_command('help')

connection = sqlite3.connect('summoners.db')
cursor = connection.cursor()


@client.event

async def on_ready():
    print('Bot connected')

# @client.event
# async def on_member_join(member):
#     channel = client.get_channel(769260889244434462)
#     role = member.guild.get_role(769237514065149982)
#     await member.add_roles(role)
#     await channel.send(embed = discord.Embed(description=f'Hi {member.name} !'))


@client.command(pass_context = True)
@commands.has_permissions(administrator = True)

async def clear(ctx, amount = 100):
    await ctx.channel.purge(limit = amount)

#--------------------------------------------------------------------------------------------------------------------

@client.command(pass_context = True)
async def name(ctx, nickname,amount: int = None):
    cursor.execute(f"INSERT INTO users VALUES({ctx.author.id},'{nickname}',0,0,0,'No')")
    connection.commit()

    await ctx.channel.purge(limit = 1)

    Role = discord.utils.get(ctx.guild.roles, id= 769237514065149982)
    await ctx.author.add_roles(Role)

    emb = discord.Embed(title = 'Новый игрок',description = 'К нам сегодня присоединился еще один призыватель', colour = discord.Colour.blue())
    emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)
    emb.add_field(name = f'{nickname}', value = 'Welcome to the club, buddy!')
    await ctx.send(embed = emb)

#--------------------------------------------------------------------------------------------------------------------

@client.command(pass_context = True)
async def my_rate(ctx):
    await ctx.channel.purge(limit = 1)
    rate = cursor.execute(f"SELECT lol_rate FROM users WHERE dis_id = {ctx.author.id}").fetchone()[0]
    ment = cursor.execute(f"SELECT lol_nick FROM users WHERE dis_id = {ctx.author.id}").fetchone()[0]
    emb = discord.Embed(title = f'Рейтинг {ment}',description = f'На данный момент ваш рейтинг составляет {rate}', colour = discord.Colour.blue())
    await ctx.send(embed = emb)

#--------------------------------------------------------------------------------------------------------------------

@client.command(pass_context = True)
@commands.has_permissions(administrator = True)

async def ru_lol(ctx, member: discord.Member = None ,amount: int = None):
    await ctx.channel.purge(limit=1)
    cursor.execute(f"UPDATE users SET lol_rate = lol_rate + {amount} WHERE dis_id = {member.id}")
    connection.commit()
    ment = cursor.execute(f"SELECT lol_nick FROM users WHERE dis_id = {member.id}").fetchone()[0]
    emb = discord.Embed(title=f'Рейтинг {ment}', description=f'Рейтинг {ment} повышен на {amount}',
                        colour=discord.Colour.blue())
    await ctx.send(embed=emb)

    rate_check = cursor.execute(f"SELECT lol_rate FROM users WHERE dis_id = {member.id}").fetchone()[0]

    if rate_check >= 16 and rate_check <= 30 :
        Role = discord.utils.get(ctx.guild.roles, id=769237495145168916)
        await ctx.author.add_roles(Role)
        emb = discord.Embed(title=f'Рейтинг {ment}', description=f'{ment} получил 1 ранг',
                            colour=discord.Colour.blue())
        await ctx.send(embed=emb)

    elif rate_check >= 31 and rate_check <= 40 :
        Role = discord.utils.get(ctx.guild.roles, id=769237445991596082)
        await ctx.author.add_roles(Role)
        emb = discord.Embed(title=f'Рейтинг {ment}', description=f'{ment} получил 2 ранг',
                            colour=discord.Colour.blue())
        await ctx.send(embed=emb)

    elif rate_check >= 41 and rate_check <= 50 :
        Role = discord.utils.get(ctx.guild.roles, id=769237416212561930)
        await ctx.author.add_roles(Role)
        emb = discord.Embed(title=f'Рейтинг {ment}', description=f'{ment} получил 3 ранг',
                            colour=discord.Colour.blue())
        await ctx.send(embed=emb)

    elif rate_check >= 51 and rate_check <= 60 :
        Role = discord.utils.get(ctx.guild.roles, id=769237410194128926)
        await ctx.author.add_roles(Role)
        emb = discord.Embed(title=f'Рейтинг {ment}', description=f'{ment} получил 4 ранг',
                            colour=discord.Colour.blue())
        await ctx.send(embed=emb)

#--------------------------------------------------------------------------------------------------------------------

@client.command(pass_context = True)
@commands.has_permissions(administrator = True)

async def rd_lol(ctx, member: discord.Member = None ,amount: int = None):
    await ctx.channel.purge(limit=1)
    cursor.execute(f"UPDATE users SET lol_rate = lol_rate - {amount} WHERE dis_id = {member.id}")
    connection.commit()
    ment = cursor.execute(f"SELECT lol_nick FROM users WHERE dis_id = {member.id}").fetchone()[0]
    emb = discord.Embed(title = f'Рейтинг {ment}',description = f'Рейтинг {ment} уменьшен на {amount}', colour = discord.Colour.red())
    await ctx.send(embed = emb)


#--------------------------------------------------------------------------------------------------------------------

@client.command(pass_context = True)
#@commands.has_permissions(administrator = True)

async def teamcreate(ctx, name):

    await ctx.channel.purge(limit = 1)


    cap_test = cursor.execute(f"SELECT team_cap FROM users WHERE dis_id = {ctx.author.id}").fetchone()[0]
    mentov = cursor.execute(f"SELECT lol_nick FROM users WHERE dis_id = {ctx.author.id}").fetchone()[0]
    if cap_test == 0:

        cursor.execute(f"INSERT INTO teams_rates VALUES ('{name}', 0, {ctx.author.id})")
        cursor.execute(f"UPDATE users SET team_cap = team_cap + 1 WHERE dis_id = {ctx.author.id}")
        cursor.execute(f"UPDATE users SET team_index = '{name}' WHERE dis_id = {ctx.author.id}")
        connection.commit()

        guild = client.get_guild(766594088526151680) # <-- insert yor guild id here

        # guild = ctx.guild
        # member = ctx.author
        # team_role = discord.utils.get(ctx.guild.roles, name=f"{name}")


        category = await ctx.guild.create_category(f"{name}", overwrites=None, reason=None)
        await ctx.guild.create_voice_channel(f"{name}", overwrites=None, category=category, reason=None)
        await ctx.guild.create_text_channel(f"{name}", overwrites=None, category=category, reason=None)

        emb = discord.Embed(title=f'{name}', description=f'Каналы команды {name} созданы, пора побеждать!',colour=discord.Colour.blue())
        await ctx.send(embed=emb)

        Role = discord.utils.get(ctx.guild.roles, id=769237676616056872)
        await ctx.author.add_roles(Role)
        guild = ctx.guild
        await guild.create_role(name=name)

        role_to_add = discord.utils.get(ctx.guild.roles, name = f"{name}")
        await ctx.author.add_roles(role_to_add)




    else:
        emb = discord.Embed(title=f'{mentov}', description=f'ОТКАЗАНО В ДОСТУПЕ \n ВЫ УЖЕ КАПИТАН ОДНОЙ КОМАНДЫ \n ЧТОБЫ СОЗДАТЬ НОВУЮ КОМАНДУ НЕОБХОДИМО РАСПУСТИТЬ НЫНЕШНЮЮ',colour=discord.Colour.red())
        await ctx.send(embed=emb)

#--------------------------------------------------------------------------------------------------------------------

@client.command(pass_context = True)
async def teamclose(ctx, category: discord.CategoryChannel):

    #await ctx.channel.purge(limit=1)

    team_index = cursor.execute(f"SELECT team_index FROM users WHERE dis_id = {ctx.author.id}").fetchone()[0]



    if str(category).lower() == str(team_index).lower():
        for channel in category.channels:
            await channel.delete()

        cursor.execute(f"UPDATE users SET team_cap = team_cap - 1 WHERE dis_id = {ctx.author.id}")
        cursor.execute(f"UPDATE users SET team_index = 'No' WHERE dis_id = {ctx.author.id}")
        connection.commit()
        await category.delete()

        role_to_delete = discord.utils.get(ctx.guild.roles, name=f"{category}")
        await discord.Role.delete(role_to_delete)

        role_to_take = discord.utils.get(ctx.guild.roles, name = "Капитан")
        await ctx.author.remove_roles(role_to_take)

        emb = discord.Embed(title=f'{category}',description=f'Каналы команды {category} удалены, спасибо что были с нами! Мы всегда рады видеть вас снова!', colour = discord.Colour.red())
        await ctx.send(embed = emb)
        cursor.execute(f"DELETE FROM teams_rates WHERE cap_id = {ctx.author.id}")
        connection.commit()

    else:
        emb = discord.Embed(title=f'{category}', description=f'Вы не имеете права удалять каналы команды {category}, так как вы не её капитан',colour=discord.Colour.red())
        await ctx.send(embed=emb)

#--------------------------------------------------------------------------------------------------------------------

@client.command(pass_context = True)

async def teamadd(ctx, member: discord.Member):
    author_team = cursor.execute(f"SELECT team_index FROM users WHERE dis_id = {ctx.author.id}").fetchone()[0]
    await member.send(f"{ctx.author.name} хочет добавить тебя в свою команду {author_team}, хочешь?\n Для согласия пропиши !teamaccept {author_team} в текстовом канале TEAMS")
    await member.send("Если вы еще не проходили регистрацию, то убедительно просим вас пройти её \n Прописав в канале ``registration`` команду !name {ваш ник в лиге}")


#--------------------------------------------------------------------------------------------------------------------

@client.command(pass_context = True)

async def teamaccept(ctx, name):

    team_check = cursor.execute(f"SELECT team_index FROM users WHERE dis_id = {ctx.author.id}").fetchone()[0]
    if str(team_check).lower() == str('No').lower() or str(team_check).lower() == str(name).lower():
        role_to_add = discord.utils.get(ctx.guild.roles, name=f"{name}")
        await ctx.author.add_roles(role_to_add)

        cursor.execute(f"UPDATE users SET team_index = '{name}' WHERE dis_id = {ctx.author.id}")
        connection.commit()

        emb = discord.Embed(title=f'{ctx.author.name}', description=f'Приветствуем вас в команде {name}',colour=discord.Colour.blue())
        await ctx.send(embed=emb)

    else:
        emb = discord.Embed(title=f'{ctx.author.name}', description=f'Извините, но вы уже в чей-то команде',colour=discord.Colour.red())
        await ctx.send(embed=emb)

#--------------------------------------------------------------------------------------------------------------------

@client.command(pass_context = True)
@commands.has_permissions(administrator = True)

async def teamwin(ctx, name, amount: int = None):
    cursor.execute(f"UPDATE teams_rates SET team_rate = team_rate + {amount} WHERE team_name = '{name}'")
    connection.commit()
    emb = discord.Embed(title=f'{name}', description=f'За победу, увеличивается рейтинг команды {name} на: {amount}',colour=discord.Colour.green())
    await ctx.send(embed=emb)

#--------------------------------------------------------------------------------------------------------------------

@client.command(pass_context = True)
@commands.has_permissions(administrator = True)

async def teamlose(ctx, name, amount: int = None):
    cursor.execute(f"UPDATE teams_rates SET team_rate = team_rate - {amount} WHERE team_name = '{name}'")
    connection.commit()
    emb = discord.Embed(title=f'{name}', description=f'За проигрыш, уменьшается рейтинг команды {name} на: {amount}',colour=discord.Colour.magenta())
    await ctx.send(embed=emb)

#--------------------------------------------------------------------------------------------------------------------

@client.command(pass_context = True)

async def team_ratings(ctx):
    cursor.execute("SELECT team_name, team_rate FROM teams_rates")
    ratings_to_show= cursor.fetchall()
    emb = discord.Embed(title=f'Рейтинги команд', description=f'На ваших экранах самая свежая сводка о рейтингах команд',colour=discord.Colour.lighter_grey())
    await ctx.send(embed=emb)
    for row in ratings_to_show:
        await ctx.send(row)

#--------------------------------------------------------------------------------------------------------------------

@client.command(pass_context = True)
async def teamregroup_to(ctx, member : discord.Member, name):
    cap_check = cursor.execute(f"SELECT team_cap FROM users WHERE dis_id = {ctx.author.id}").fetchone()[0]


    if cap_check == 1:
        cursor.execute(f"UPDATE users SET team_cap = 0 WHERE dis_id = {ctx.author.id}")
        #cursor.execute(f"UPDATE users SET team_index = 'No' WHERE dis_id = {ctx.author.id}")
        cursor.execute(f"UPDATE users SET team_cap = 1 WHERE dis_id = '{member.id}'")
        cursor.execute(f"UPDATE teams_rates SET cap_id = {member.id} WHERE team_name = '{name}'")
        connection.commit()

        old_cap=cursor.execute(f"SELECT team_cap FROM users WHERE dis_id = {ctx.author.id}").fetchone()[0]
        new_cap = cursor.execute(f"SELECT team_cap FROM users WHERE dis_id = {member.id}").fetchone()[0]


        role_to_take = discord.utils.get(ctx.guild.roles, id=769237676616056872)
        await ctx.author.remove_roles(role_to_take)


        Role = discord.utils.get(ctx.guild.roles, id=769237676616056872)
        await member.add_roles(Role)

        emb = discord.Embed(title=f'Смена капитана команды {name}', description=f'{member.name} стал капитаном команды {name}', colour=discord.Colour.lighter_grey())
        await ctx.send(embed=emb)

    else:

        emb = discord.Embed(title=f'Нельзя передать', description=f'вы не кэп',colour=discord.Colour.lighter_grey())
        await ctx.send(embed=emb)

#--------------------------------------------------------------------------------------------------------------------

@client.command(pass_contex = True)

async def teamremove(ctx, member: discord.Member, name):
    cap_check = cursor.execute(f"SELECT team_cap FROM users WHERE dis_id = {ctx.author.id}").fetchone()[0]
    cap_team = cursor.execute(f"SELECT team_index FROM users WHERE dis_id = {ctx.author.id}").fetchone()[0]
    # await ctx.send(cap_team)
    # await ctx.send(cap_check)

    if str(cap_team).lower() == str(name).lower() and cap_check == 1:
        role_to_take = discord.utils.get(ctx.guild.roles, name=f"{name}")
        await member.remove_roles(role_to_take)
        team_member = cursor.execute(f"SELECT lol_nick FROM users WHERE dis_id = {member.id}").fetchone()[0]
        cursor.execute(f"UPDATE users SET team_index = 'No' WHERE dis_id = {member.id}")
        connection.commit()

        emb = discord.Embed(title=f"{name}", description=f"Игрок {member.name} ('{team_member}') покинул команду {name}", colour=discord.Colour.magenta())
        await ctx.send(embed=emb)
    else:
        emb = discord.Embed(title=f"{name}", description=f"Вы не являетесь капитаном команды {name}",colour=discord.Colour.magenta())
        await ctx.send(embed=emb)

#--------------------------------------------------------------------------------------------------------------------

@client.command(pass_contex = True)

async def teamleave(ctx, team_name):
    role_to_take = discord.utils.get(ctx.guild.roles, name=f"{team_name}")
    await ctx.author.remove_roles(role_to_take)
    cursor.execute(f"UPDATE users SET team_index = 'No' WHERE dis_id = {ctx.author.id}")
    cursor.execute(f"UPDATE users SET team_cap = 0 WHERE dis_id = {ctx.author.id}")
    connection.commit()
    #team_member = cursor.execute(f"SELECT team_cap FROM users WHERE dis_id = {ctx.author.id}")


    emb = discord.Embed(title=f'{ctx.author.name}', description=f"Игрок {ctx.author.name} покинул команду {team_name}", colour=discord.Colour.magenta())
    await ctx.send(embed=emb)


TOKEN = 'NzY2NjQ5ODY1MjY1NDc5NzIw.X4mcUw.8CpvNDDVbqL00X2IX3a-dmNXm8k'
client.run(TOKEN)
