from logging import captureWarnings
from re import I
import discord
from discord import embeds
from discord import guild
from discord.ext import commands, tasks
import asyncio
import os
import json
from discord.ext.commands.converter import EmojiConverter, GuildConverter
from discord.user import Profile
from easy_pil import Editor, Canvas, font, load_image_async, Font
import random
import string
import locale
import time
from discord_buttons_plugin import *
import DiscordUtils
from discord.user import User
import urllib.request
import re



locale.setlocale(locale.LC_TIME,'')
intents = discord.Intents().all()
lvl = [50, 150, 300, 500, 750, 1000]
bot = commands.Bot(command_prefix="Volyna/", intents=intents, help_command=None)
buttons = ButtonsClient(bot)
music = DiscordUtils.Music()

with open("config.json", "r") as configjsonFile:
    configData = json.load(configjsonFile)
    TOKEN = configData["token"]
    ARRIVER=  configData["salonarriver"]
    MEMBRE= configData["rolemembre"]
    STAFF= configData["rolestaff"]
    LOG = configData["salonlog"]
    VERIF= configData["salonverifier"]
    GUILD= configData["idduserv"]
    MUTE= configData["rolemute"]
    EVEYRONE= configData["roleevey"]
    NONVERIF= configData["rolenonverif"]
    CATTICKET= configData["catticket"]

@bot.event
async def on_ready():
    print("[------------- CONECTED -------------]")
    bot.my_current_task = live_status.start()


@tasks.loop()
async def live_status(seconds=75):
    Dis = bot.get_guild(int(GUILD)) #Int


    activity = discord.Activity(type=discord.ActivityType.watching, name=f'👥 {Dis.member_count}')
    await bot.change_presence(activity=activity)
    await asyncio.sleep(15)

    activity = discord.Activity(type=discord.ActivityType.watching, name=f'Titou#1577')
    await bot.change_presence(activity=activity)
    await asyncio.sleep(15)

    activity = discord.Activity(type=discord.ActivityType.watching, name=f'Volyna RP')
    await bot.change_presence(activity=activity)
    await asyncio.sleep(15)

    activity = discord.Activity(type=discord.ActivityType.watching, name=f'Developper par Titou')
    await bot.change_presence(activity=activity)
    await asyncio.sleep(15)






@bot.event
async def on_message(message):
    if message.author.bot == False:
        with open('users.json', 'r') as f:
            users = json.load(f)

        await update_data(users, message.author)
        await add_experience(users, message.author, 5)
        await level_up(users, message.author, message)

        with open('users.json', 'w') as f:
            json.dump(users, f)

    await bot.process_commands(message)


async def update_data(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 1


async def add_experience(users, user, exp):
    users[f'{user.id}']['experience'] += exp


async def level_up(users, user, message):
    with open('levels.json', 'r') as g:
        levels = json.load(g)
    experience = users[f'{user.id}']['experience']
    lvl_start = users[f'{user.id}']['level']
    lvl_end = int(experience ** (1 / 4))
    for data in lvl:
        if experience == data:
            await message.channel.send(f'{user.mention} est passer level {lvl_end}')
            users[f'{user.id}']['level'] = lvl_end
            users[f'{user.id}']['experience'] = 0

    


        


joke = ["C'est l'histoire du ptit dej, tu la connais ? Pas de bol",
        "Que demande un footballeur à son coiffeur ? La coupe du monde s’il vous plait ",
        "C'est l'histoire d'un pingouin qui respire par les fesses Un jour il s’assoit et il meurt",
        "Pourquoi les Belges viennent-ils à la messe avec du savon ? Pour l’Ave Maria",
        "Comment s'appelle le cul de la Schtroumpfette ? Le blu-ray"]

@bot.command()
async def blague(ctx):
    embed = discord.Embed(title="**BLAGUE**", description=random.choice(joke), color=0x250079)
    embed.set_author(name=ctx.author.name)
    embed.set_footer(text="Ajoute ta prope blague en fesant !addblague ta blague")
    await ctx.send(embed=embed)


@bot.command()
async def addblague(ctx, *blague):
    joke.append(" ".join(blague))
    await ctx.channel.send("Blague ajouter fait !blague en esperant tomber dessus :)")




number_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

alphabet_lowercase = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                              't', 'u', 'v', 'w', 'x', 'y', 'z']

@bot.command()
async def sug(ctx, *texte):
    embed = discord.Embed(title="Voici la suggestion :", color=0xE0ED12)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/769485806641217539/831206278177095771/ampoule_1.png")
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed.add_field(name=" ".join(texte), value=ctx.author.name, inline=False)
    message = await ctx.send(embed=embed)
    await message.add_reaction("✅")
    await message.add_reaction("❌")
    await ctx.message.delete()


@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, raison):
    log = LOG
    role = MUTE
    await ctx.message.delete()
    await member.add_roles(int(role))
    await ctx.send(f"{member.mention} C'est fait mute", )
    embed = discord.Embed(title="Mute", description=f"{member.mention} C'est fait mute par {ctx.message.author.mention} pour {raison}", color=0xB22E00)
    await bot.get_channel(int(log)).send(embed=embed)


@bot.command()
@commands.has_permissions(manage_roles=True)
async def umute(ctx, member: discord.Member):
    await ctx.message.delete()
    log = LOG
    role = MUTE
    await member.remove_roles(role)
    await ctx.send(f"{member.mention}, c'est fait demute")
    embed = discord.Embed(title="Umute", description=f"{member.mention} C'est fait umute par {ctx.message.author.mention}", color=0x17FF00)
    await bot.get_channel(int(log)).send(embed=embed)

@bot.command()
@commands.has_guild_permissions(ban_members=True)
async def ban(ctx, user: discord.User, reason):    
    log = LOG
    await ctx.message.delete()
    reason = " ".join(reason)
    await ctx.guild.ban(user, reason=reason)
    await ctx.send(f"{user} à été ban pour")
    embed = discord.Embed(title="Ban", description=f"{user.mention} C'est fait ban par {ctx.message.author.mention} pour {reason}", color=0xFF001F)
    await bot.get_channel(int(log)).send(embed=embed)    

@bot.command()
async def invite(ctx):
	invite = "https://discord.gg/92jj8Y7VgH"
	await ctx.send(f"Voici le lien d'invitation {invite}")

@bot.command()
async def myid(ctx):
	await ctx.send(f"Ton id est {ctx.author.id}")

@bot.command()
@commands.has_guild_permissions(manage_messages=True)
async def lock(ctx):
    log = LOG
    role = STAFF
    everyone = EVEYRONE
    membre = MEMBRE
    await ctx.channel.set_permissions(int(everyone), read_messages=True, send_messages=False)
    await ctx.channel.set_permissions(int(role), send_messages=True, read_messages=True)
    await ctx.channel.set_permissions(int(membre), read_messages=True, send_messages=False)
    await ctx.channel.send("Channel Lock")
    embed = discord.Embed(title="Lock", description=f"{ctx.message.author.mention} A lock le channel {ctx.message.channel.mention}", color=0x001FFE)
    embed.set_author(name="Copyright © 2021 Volyna. Tous droits réservés")
    await bot.get_channel(int(log)).send(embed=embed)    

@bot.command(aliases= ['purge','delete'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
   if amount == None:
       await ctx.channel.purge(limit=1000000)
   else:
       await ctx.channel.purge(limit=amount)


@bot.command()
@commands.has_guild_permissions(manage_messages=True)
async def unlock(ctx):
    log = LOG
    role = STAFF
    everyone = EVEYRONE
    membre = MEMBRE
    await ctx.channel.set_permissions(int(everyone), read_messages=True, send_messages=True)
    await ctx.channel.set_permissions(int(role), send_messages=True, read_messages=True)
    await ctx.channel.set_permissions(int(membre), read_messages=True, send_messages=True)
    await ctx.channel.send("Channel Unlock")
    embed = discord.Embed(title="Unlock", description=f"{ctx.message.author.mention} A unlock le channel {ctx.message.channel.mention}", color=0xC134CD)
    embed.set_author(name="Copyright © 2021 Volyna. Tous droits réservés")
    await bot.get_channel(int(log)).send(embed=embed)   

@bot.command()
@commands.has_guild_permissions(kick_members=True)
async def kick(ctx, user: discord.User, reason):
    log = LOG
    await ctx.message.delete()
    reason = " ".join(reason)
    await ctx.guild.kick(user, reason=reason)
    await ctx.send(f"{user} à été kick .")
    embed = discord.Embed(title="Kick", description=f"{user.mention} C'est fait kick par {ctx.message.author.mention}", color=0x34CDC8)
    embed.set_author(name="Copyright © 2021 Volyna. Tous droits réservés")
    await bot.get_channel(int(log)).send(embed=embed)  

@clear.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("il faut donner un nombre.")

@ban.error
async def ban_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("il faut donner une raison")

@kick.error
async def kick_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("il faut donner une raison")


@buttons.click
async def button_one(ctx):
    role = discord.utils.get(ctx.guild.roles, id=int(STAFF))
    catticket = CATTICKET
    overwrites = {
        role: discord.PermissionOverwrite(read_messages=True),
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=True,
                                                            read_message_history=True),
        ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True),
        ctx.member : discord.PermissionOverwrite(read_messages=True, send_messages=True,
                                                        read_message_history=True),
    }
    channel = await ctx.guild.create_text_channel(name=f"Ticket-{ctx.member.name}",  category=bot.get_channel(int(catticket)), overwrites=overwrites)
    await ctx.reply(f"Votre ticket a ete cree {channel.mention}", flags = MessageFlags().EPHEMERAL)
    embed = discord.Embed(title="Ticket", description="Appuyez sur le bouton pour fermer le ticket")
    await buttons.send(
        content = None,
        embed = embed,
        channel = channel.id,
        components = [
            ActionRow([
                Button(
                    label="Close", 
                    style=ButtonType().Primary, 
                    custom_id="button_close"          
                )
            ])
        ]
    )


closemess = 0

@buttons.click
async def button_close(ctx):
     closemess = await buttons.send(
        content = f"Ete vous sur de vouloir fermer le ticket ? {ctx.member.mention}",
        channel = ctx.channel.id,
        components = [
            ActionRow([
                Button(
                    label="Oui", 
                    style=ButtonType().Danger, 
                    custom_id="button_closesur"
                    
                ), Button(
			   label="Non",
			   style=ButtonType().Primary,
			   custom_id="button_noclose"        
		 )
            ])
        ]
    )

@buttons.click
async def button_closesur(ctx):
        await ctx.channel.send("Ce ticket va s'auto detruire dans 5 secondes")
        time.sleep(1.0)
        time.sleep(1.0)
        time.sleep(1.0)
        time.sleep(1.0)
        time.sleep(1.0)
        await ctx.channel.delete()

@buttons.click
async def button_noclose(ctx):
       global closemess
       await ctx.message.delete()


embed = discord.Embed(title="Ticket", description="Appuyez sur le bouton pour ouvrir le ticket")
embed.set_author(name="Copyright © 2021 Volyna. Tous droits réservés")

@bot.command()
async def create(ctx):
 	await buttons.send(
	    content = None,
        embed = embed,
		channel = ctx.channel.id,
		components = [
			ActionRow([
				Button(
					label="Cree un Tickets", 
					style=ButtonType().Primary, 
					custom_id="button_one"          
				)
			])
		]
	)    



@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingPermissions):
		await ctx.send("Vous n'avez pas les permissions pour faire cette commande.")


@bot.event
async def on_member_join(member):



        with open('users.json', 'r') as f:
            users = json.load(f)

        await update_data(users, member)

        with open('users.json', 'w') as f:
            json.dump(users, f)

        log = LOG
        arriver = ARRIVER
        verif = VERIF
        rolemember = MEMBRE
        nnverif = NONVERIF

        
        roleverife = discord.utils.get(member.guild.roles, id=int(nnverif))
        
        embed = discord.Embed(title=f"Oh ! {member.name}, viens de rejoindre le discord ! :)", color=0x7f00ff)
        embed.set_image(
            url=f"{member.avatar_url}")
        embed.set_footer(text=f"Nous somme maintenant {member.guild.member_count}")
        embed.set_author(name="Copyright © 2021 Volyna. Tous droits réservés")
        await bot.get_channel(int(arriver)).send(embed=embed)
        await member.add_roles(roleverife)

        user = member 
        date_format = "%a, %d %b %Y %I:%M %p"
        embed=discord.Embed(color=0xFF6C00)
        embed.set_author(name=f"{member}", icon_url=member.avatar_url)
        embed.add_field(name=f"{member.mention} Vient de rejoindre le serveur", value=f"Son compte a ete cree le {user.created_at.__format__('%d/%m/%Y a %H:%M:%S')}", inline=False)
        await bot.get_channel(int(log)).send(embed=embed)

        pass_min = 6
        pass_max = 8
        all_chars = string.ascii_uppercase + string.digits

        password = "".join(random.choice(all_chars) for x in range(random.randint(pass_min, pass_min)))
        print(password)    

        poppins = Font().poppins(size=140)
        poppins_small = Font().poppins(size=50)
        background = Editor("assets/gb.png")
        background.text((200, 50), str(password), font=poppins, color="black")
        file = discord.File(fp=background.image_bytes, filename="card.png")
        await bot.get_channel(int(verif)).send(f"{member.mention} Merci de remplir le captcha pour aceder a la totaliter du serveur",file=file)
        channel = bot.get_channel(int(verif))
        def check(m: discord.Message):
            return m.author.id == member.id and m.channel.id == channel.id 

        try:
            verif = await bot.wait_for("message", check = check, timeout = 60.0)
            if verif.content == password:
                role = discord.utils.get(member.guild.roles, id=int(rolemember))
                await bot.get_channel(int(log)).send(f"{member.mention} a passer la verification !")
                roleverife = discord.utils.get(member.guild.roles, id=int(nnverif))
                await member.add_roles(role)
                await member.remove_roles(roleverife)
            else:
                await bot.get_channel(int(log)).send(f"{member.mention} a ete expluser car il a rater le captcha !")
                await member.guild.kick(member)

        except asyncio.TimeoutError:
            await bot.get_channel(int(log)).send(f"{member.mention} a trop attendu avant de completer le captcha!")
            await member.guild.kick(member)






@bot.command()
async def info(ctx, member: discord.Member = None):
    if not member:
        id = ctx.message.author.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        member = ctx.author
        xp = users[str(id)]['experience']
        name, nick, Id, status = str(member), member.display_name, str(member.id), str(member.status)
        created_at = member.created_at.strftime("%A %d\n%B %Y")
        joined_at = member.joined_at.strftime("%A %d\n%B %Y")    
        name = f"{name[:16]}.." if len(name)>16 else name
        nick = f"{nick[:17]}.." if len(nick)>17 else f"{nick}"
        poppins = Font().poppins(size=30)
        poppins_small = Font().poppins(size=20)
        profile = await load_image_async(str(ctx.author.avatar_url))
        profile = Editor(profile).resize((220, 220)).circle_image()
        background = Editor("assets/gaming1_background.png")
        base = Editor("assets/base.png")
        base.text((280,240), str(name), font = poppins, color="white")
        base.text((270,315), str(nick), font = poppins, color="white")
        base.text((65,490), str(Id), font = poppins, color="white")
        base.text((405,490), str(status), font = poppins, color="white")
        base.text((65,635), str(xp), font = poppins, color="white")
        base.text((405,635), str(lvl), font = poppins, color="white")
        base.text((65,770), str(created_at), font = poppins, color="white")
        base.text((405,770), str(joined_at), font = poppins, color="white")
        base.paste(profile.image,(56,158))
        background.paste(base.image, (0,0))
        file = discord.File(fp=background.image_bytes, filename="info.png")
        await ctx.channel.send(file=file)

    else:
        try:
            id = member.id
            with open('users.json', 'r') as f:
                users = json.load(f)
            lvl = users[str(id)]['level']
            member = member
            xp = users[str(id)]['experience']
            pseudoa =  str(member)
            pseudo = member.display_name
            Id = str(member.id) 
            status =  str(member.status)
            creation_de_compte = member.created_at.strftime("%A %d\n%B %Y")
            rejoin_le_serv = member.joined_at.strftime("%A %d\n%B %Y")    

            poppins = Font().poppins(size=30)
            poppins_small = Font().poppins(size=20)
            profile = await load_image_async(str(member.avatar_url))
            profile = Editor(profile).resize((220, 220)).circle_image()
            background = Editor("assets/gaming1_background.png")
            base = Editor("assets/base.png")
            base.text((280,240), str(pseudoa), font = poppins, color="white")
            base.text((270,315), str(pseudo), font = poppins, color="white")
            base.text((65,490), str(Id), font = poppins, color="white")
            base.text((405,490), str(status), font = poppins, color="white")
            base.text((65,635), str(xp), font = poppins, color="white")
            base.text((405,635), str(lvl), font = poppins, color="white")
            base.text((65,770), str(creation_de_compte), font = poppins, color="white")
            base.text((405,770), str(rejoin_le_serv), font = poppins, color="white")
            base.paste(profile.image,(56,158))
            background.paste(base.image, (0,0))
            file = discord.File(fp=background.image_bytes, filename="info.png")
            await ctx.channel.send(file=file)
        except KeyError:
            id = member.id

            lvl = 0
            member = member
            xp = 0
            pseudoa =  str(member)
            pseudo = member.display_name
            Id = str(member.id) 
            status =  str(member.status)
            creation_de_compte = member.created_at.strftime("%A %d\n%B %Y")
            rejoin_le_serv = member.joined_at.strftime("%A %d\n%B %Y")    

            poppins = Font().poppins(size=30)
            poppins_small = Font().poppins(size=20)
            profile = await load_image_async(str(member.avatar_url))
            profile = Editor(profile).resize((220, 220)).circle_image()
            background = Editor("assets/gaming1_background.png")
            base = Editor("assets/base.png")
            base.text((280,240), str(pseudoa), font = poppins, color="white")
            base.text((270,315), str(pseudo), font = poppins, color="white")
            base.text((65,490), str(Id), font = poppins, color="white")
            base.text((405,490), str(status), font = poppins, color="white")
            base.text((65,635), str(xp), font = poppins, color="white")
            base.text((405,635), str(lvl), font = poppins, color="white")
            base.text((65,770), str(creation_de_compte), font = poppins, color="white")
            base.text((405,770), str(rejoin_le_serv), font = poppins, color="white")
            base.paste(profile.image,(56,158))
            background.paste(base.image, (0,0))
            file = discord.File(fp=background.image_bytes, filename="info.png")
            await ctx.channel.send(file=file)


@bot.command()
async def level(ctx, member: discord.Member = None):
    if not member:
        id = ctx.message.author.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        if lvl == 1:
            endxp = 50
        elif lvl == 2:
            endxp = 150
        elif lvl == 3:
            endxp = 300
        elif lvl == 4:
            endxp = 500
        elif lvl == 5:
            endxp = 750
        elif lvl == 6:
            endxp = 1000


        
        xp = users[str(id)]['experience']
        poppins = Font().poppins(size=40)
        poppins_small = Font().poppins(size=30)
        background = Editor("assets/bg.png")
        profile = await load_image_async(str(ctx.author.avatar_url))
        profile = Editor(profile).resize((150, 150)).circle_image()
        background.paste(profile.image, (30, 30))
        background.text((200, 40), str(ctx.author), font=poppins, color="white")
        background.text((200, 40), str(ctx.author), font=poppins, color="white")
        background.rectangle((30, 220), width=650, height=40, fill="white", radius=20)  

        background.text(
            (200, 130),
            f"Level : {lvl} "
            + f" XP : {xp} / {endxp}",
            font=poppins_small,
            color="white",
        )
        file = discord.File(fp=background.image_bytes, filename="card.png")
        await ctx.send(file=file)
    else:
        id = member.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        if lvl == 1:
            endxp = 50
        elif lvl == 2:
            endxp = 150
        elif lvl == 3:
            endxp = 300
        elif lvl == 4:
            endxp = 500
        elif lvl == 5:
            endxp = 750
        elif lvl == 6:
            endxp = 1000


        
        xp = users[str(id)]['experience']
        poppins = Font().poppins(size=40)
        poppins_small = Font().poppins(size=30)
        background = Editor("assets/bg.png")
        profile = await load_image_async(str(member.avatar_url))
        profile = Editor(profile).resize((150, 150)).circle_image()
        background.paste(profile.image, (30, 30))
        background.text((200, 40), str(member), font=poppins, color="white")
        background.text((200, 40), str(member), font=poppins, color="white")
        background.rectangle((30, 220), width=650, height=40, fill="white", radius=20)  

        background.text(
            (200, 130),
            f"Level : {lvl} "
            + f" XP : {xp} / {endxp}",
            font=poppins_small,
            color="white",
        )
        file = discord.File(fp=background.image_bytes, filename="card.png")
        await ctx.send(file=file)








embed1 = discord.Embed(title="**Commande**", description ="Voici les commande disponible", color=0x34CDC8)
embed1.add_field(name="__Volyna/sug__", value=" Pemet de faire une suggestion", inline=False)
embed1.add_field(name="__Volyna/invite__", value="Permet d'avoir le lien d'invite de votre discord", inline=False)
embed1.add_field(name="__Volyna/blague__", value="Permet de voir ton id", inline=False)
embed1.add_field(name="__Volyna/addblague__", value="Permet de voir ton id", inline=False)
embed1.add_field(name="__Volyna/level__", value="Permet de voir ton rank", inline=False)
embed1.set_footer(text="Page 1/4")
embed1.set_author(name="Copyright © 2021 Volyna. Tous droits réservés")

embed2 = discord.Embed(title="Commande D'administration", description ="Voici les commande disponible", color=0xFF6C00)
embed2.add_field(name="__Volyna/clear__", value="Clear un nombre de message", inline=False)
embed2.add_field(name="__Volyna/mute__", value="Mute un membre", inline=False)
embed2.add_field(name="__Volyna/umute__", value="Umute un membre", inline=False)
embed2.add_field(name="__Volyna/ban__", value="Ban un membre", inline=False)
embed2.add_field(name="__Volyna/kick__", value="Kick un membre", inline=False)
embed2.add_field(name="__Volyna/lock__", value="lock un channel", inline=False)
embed2.add_field(name="__Volyna/unlock__", value="unlock un channel", inline=False)
embed2.set_footer(text="Page 2/4")
embed2.set_author(name="Copyright © 2021 Volyna. Tous droits réservés")


embed3 = discord.Embed(title="Commande Musique", description ="Voici les commande disponible", color=0xECFF00)
embed3.add_field(name="__Volyna/play__", value="Permet de lancer une musique", inline=False)
embed3.add_field(name="__Volyna/leave__", value="permet de deconnecter le bot", inline=False)
embed3.add_field(name="__Volyna/pause__", value="Mettre pause a la musique", inline=False)
embed3.add_field(name="__Volyna/resume__", value="Mettre play a la musique", inline=False)
embed3.add_field(name="__Volyna/skip__", value="Passer au son suivant", inline=False)
embed3.set_footer(text="Page 3/4")
embed3.set_author(name="Copyright © 2021 Volyna. Tous droits réservés")

embed4 = discord.Embed(title="Info Du bot", description ="Voici les commande disponible", color=0xECFF00)
embed4.set_author(name="Copyright © 2021 Volyna. Tous droits réservés")
embed4.add_field(name="**__Version du bot**__", value="2.0", inline=False)
embed4.add_field(name="**__Develloper par__**", value="Volyna#1647", inline=False)
embed4.set_footer(text="Page 4/4")

bot.help_pages = [embed1, embed2, embed3, embed4]

@bot.command()
async def help(ctx):
    buttons = [u"\u25C0", u"\u25B6"]
    current = 0
    message = await ctx.send(embed=bot.help_pages[current])

    for button in buttons:
        await message.add_reaction(button)


    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout = 60.0)
        except asyncio.TimeoutError:
            print("fin du temp")

        else:
            previous_page = current

            if reaction.emoji == u"\u25C0":
                if current > 0:
                    current -= 1
            elif reaction.emoji == u"\u25B6":
                if current < len(bot.help_pages)-1:
                    current += 1


            for button in buttons:
                await message.remove_reaction(button, ctx.author)
            if current !=  previous_page:
                await message.edit(embed=bot.help_pages[current])




@bot.command()
async def deco(ctx):
    mevoicetru = ctx.guild.me.voice
    if mevoicetru is None:
        return await ctx.send("Je ne suis pas dans un salon vocale")
    await ctx.reply("Deconectter!")
    client = ctx.guild.voice_client
    await client.disconnect()


@bot.command()
async def queue(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    await ctx .send(f"{''.join([song.name for song in player.current_queue()])}")



@bot.command()
async def pause(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.pause()



@bot.command()
async def resume(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.resume()

@bot.command()
async def loop(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.toggle_song_loop()
    if song.is_looping:
        return await ctx.send(f"{song.name} a ete ajouter en loop")


@bot.command()
async def skip(ctx):
    client = ctx.guild.voice_client
    client.stop()

    
@bot.command()
async def play(ctx, url = None, name = None):
    mevoice = ctx.guild.me.voice
    if mevoice is None:
        await ctx.author.voice.channel.connect()
    if not url:
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + " ".join(name))
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        url = f"https://www.youtube.com/watch?v=" + video_ids[0]
    client = ctx.guild.voice_client
    player = music.get_player(guild_id=ctx.guild.id)
    if not player:
        player = music.create_player(ctx, ffmpeg_error_betterfix=True)
    if not client.is_playing():
        await player.queue(url, search=True)
        song = await player.play()
        embed = discord.Embed(title="Musique")
        embed.add_field(name="Nom du son", value=song.name)
        await ctx.channel.send(embed=embed)
    else:
        song = await player.queue(url, search=True)
        embed = discord.Embed(title="Musique")
        embed.add_field(name=f"{song.name} A ete ajouter a la liste", value="Faite Volyna/skip pour passer a cette musique")
        await ctx.channel.send(embed=embed)

@bot.command()
async def join(ctx):
    voicetrue = ctx.author.voice
    if voicetrue is None:
        return await ctx.send("Tu n'est pas dans un salon vocale")
    await ctx.author.voice.channel.connect()








bot.run(TOKEN)
