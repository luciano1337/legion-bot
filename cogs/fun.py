import random
import discord
import urllib
import secrets
import asyncio
import youtube_dl
import aiohttp
import re
import datetime
import time

from io import BytesIO
from discord.ext import commands
from utils import lists, permissions, http, default, argparser

players = {}

class Fun_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.config()
        self.alex_api_token = self.config["alexflipnote_api"]

    @commands.command()
    async def adunare(self, ctx, a: int, b: int):
        """ Fac si eu adunari ca nu sunt prost. """
        await ctx.send(a+b)

    @commands.command()
    async def scadere(self, ctx, a: int, b: int):
        """ Fac si eu scaderi sa arat ca sunt olimpic. """
        await ctx.send(a-b)

    @commands.command()
    async def inmultire(self, ctx, a: int, b: int):
        """ Fac si inmultiri ba nebunule. """
        await ctx.send(a*b)

    @commands.command()
    async def impartire(self, ctx, a: int, b: int):
        """ Fac si impartiri ce stii tu. """
        await ctx.send(a/b)

    @commands.command(aliases=['intrebare'])
    async def question(self, ctx, *, question: commands.clean_content):
        """ Pui o intrebare. """
        answer = random.choice(lists.raspunsuri)
        await ctx.send(f"❓ **Intrebarea:** {question}\n✔️**Raspunsul:** {answer}")

    @commands.command()
    async def bulangiu(self, ctx, *, user: discord.Member = None):
        """ Vezi cat de bulangiu este prietenul tau. """
        if user is None:
            user = ctx.author

        num = random.randint(0, 100)
        deci = random.randint(0, 9)

        if num == 100:
            deci = 0

        await ctx.send(f"Cat de bulangiu este {user.name} = **{num}.{deci}% / 100%**")

    @commands.command()
    async def gay(self, ctx, *, user: discord.Member = None):
        """ Vezi cat de gay este prietenul tau. """
        if user is None:
            user = ctx.author

        num = random.randint(0, 100)
        deci = random.randint(0, 9)

        if num == 100:
            deci = 0

        await ctx.send(f"Cat de gay este {user.mention} = **{num}.{deci}% / 100%**")

    @commands.command()
    async def fuck(self, ctx, *, user: discord.Member = None):
        """ Vezi care este sansa sa te futi si tu cu cineva ca esti virgin """
        if user is None:
            user = ctx.author

        num = random.randint(0, 100)
        deci = random.randint(0, 9)

        if num == 100:
            deci = 0

        await ctx.send(f"Sansele de a te fute cu {user.mention} = sunt de **{num}.{deci}% / 100%**")

    @commands.command()
    async def hot(self, ctx, *, user: discord.Member = None):
        """ Vezi cat de fierbinte este, mrrr. """
        if user is None:
            user = ctx.author

        num = random.randint(0, 100)
        deci = random.randint(0, 9)

        if num == 100:
            deci = 0

        await ctx.send(f"{user.mention} este : **{num}.{deci}% fierbintee 🤤😏 **")

    @commands.command()
    async def kill(self, ctx, *, user: discord.Member = None):
        """ Vezi care este sansa sa mori efectiv. """
        if user is None:
            user = ctx.author

        num = random.randint(0, 100)
        deci = random.randint(0, 9)

        if num == 100:
            deci = 0

        await ctx.send(f"{user.mention} Sansele tale de a murii sunt de **{num}.{deci}% / 100%**")


    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def cat(self, ctx):
        """ Posts a random cat """
        chosen_image = random.choice(lists.pisica)
        if not permissions.can_handle(ctx, "attach_files"):
            return await ctx.send("Nu pot sa trimit imagini aici bagami-as pula :(.")
        
        embed = discord.Embed(color=0xff69b4, timestamp=datetime.datetime.utcnow())
        embed.set_image(url=chosen_image)
        embed.set_footer(text=f"Requested by: {ctx.author.name}")

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def dog(self, ctx):
        """ Posts a random dog """
        chosen_image = random.choice(lists.caini)
        if not permissions.can_handle(ctx, "attach_files"):
            return await ctx.send("Nu pot sa trimit imagini aici bagami-as pula :(.")
        
        embed = discord.Embed(color=0xff69b4, timestamp=datetime.datetime.utcnow())
        embed.set_image(url=chosen_image)
        embed.set_footer(text=f"Requested by: {ctx.author.name}")

        await ctx.send(embed=embed)

    @commands.command()
    async def coin(self, ctx):
        """ Cap si pajura. """
        coinsides = ['Cap', 'Pajura']
        await ctx.send(f"**{ctx.author.name}** a aruncat cu banu si a picat **{random.choice(coinsides)}**!")

    @commands.command()
    async def f(self, ctx, *, text: commands.clean_content = None):
        """ Press F to pay respect """
        hearts = ['❤', '💛', '💚', '💙', '💜']
        reason = f"for **{text}** " if text else ""
        await ctx.send(f"**{ctx.author.name}** has paid their respect {reason}{random.choice(hearts)}")

    @commands.command()
    async def supreme(self, ctx, *, text: commands.clean_content(fix_channel_mentions=True)):
        """ Make a fake Supreme logo

        Arguments:
            --dark | Make the background to dark colour
            --light | Make background to light and text to dark colour
        """
        parser = argparser.Arguments()
        parser.add_argument('input', nargs="+", default=None)
        parser.add_argument('-d', '--dark', action='store_true')
        parser.add_argument('-l', '--light', action='store_true')

        args, valid_check = parser.parse_args(text)
        if not valid_check:
            return await ctx.send(args)

        inputText = urllib.parse.quote(' '.join(args.input))
        if len(inputText) > 500:
            return await ctx.send(f"**{ctx.author.name}**, the Supreme API is limited to 500 characters, sorry.")

        darkorlight = ""
        if args.dark:
            darkorlight = "dark=true"
        if args.light:
            darkorlight = "light=true"
        if args.dark and args.light:
            return await ctx.send(f"**{ctx.author.name}**, you can't define both --dark and --light, sorry..")

        await self.api_img_creator(ctx, f"https://api.alexflipnote.dev/supreme?text={inputText}&{darkorlight}", "supreme.png", token=self.alex_api_token)

    @commands.command(aliases=['color'])
    @commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
    async def colour(self, ctx, colour: str):
        """ View the colour HEX details """
        async with ctx.channel.typing():
            if not permissions.can_handle(ctx, "embed_links"):
                return await ctx.send("I can't embed in this channel ;-;")

            if colour == "random":
                colour = "%06x" % random.randint(0, 0xFFFFFF)

            if colour[:1] == "#":
                colour = colour[1:]

            if not re.search(r'^(?:[0-9a-fA-F]{3}){1,2}$', colour):
                return await ctx.send("You're only allowed to enter HEX (0-9 & A-F)")

            try:
                r = await http.get(
                    f"https://api.alexflipnote.dev/colour/{colour}", res_method="json",
                    no_cache=True, headers={"Authorization": self.alex_api_token}
                )
            except aiohttp.ClientConnectorError:
                return await ctx.send("The API seems to be down...")
            except aiohttp.ContentTypeError:
                return await ctx.send("The API returned an error or didn't return JSON...")

            embed = discord.Embed(colour=r["int"])
            embed.set_thumbnail(url=r["image"])
            embed.set_image(url=r["image_gradient"])

            embed.add_field(name="HEX", value=r['hex'], inline=True)
            embed.add_field(name="RGB", value=r['rgb'], inline=True)
            embed.add_field(name="Int", value=r['int'], inline=True)
            embed.add_field(name="Brightness", value=r['brightness'], inline=True)

            await ctx.send(embed=embed, content=f"{ctx.invoked_with.title()} name: **{r['name']}**")

    @commands.command()
    async def invers(self, ctx, *, text: str):
        """ Scriu si invers mai nou
        """
        t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        await ctx.send(f"🔁 {t_rev}")

    @commands.command()
    async def password(self, ctx, nbytes: int = 18):
        """ Iti generez o parola puternica pentru tine

        Aceasta returnează un șir de text aleatoriu pentru adresele URL aleatorii, conținând nbytes aleator octeți.
        Textul este codificat Base64, deci în medie fiecare octet are aproximativ 1,3 caractere.
        """
        if nbytes not in range(3, 1401):
            return await ctx.send("Accept doar numere intre 3-1400")
        if hasattr(ctx, 'guild') and ctx.guild is not None:
            await ctx.send(f"Ti-am trimis mesaj in privat cu o parola random. **{ctx.author.name}**")
        await ctx.author.send(f"🎁 **Ia ma parola sarakule:**\n{secrets.token_urlsafe(nbytes)}")

    @commands.command()
    async def bere(self, ctx, user: discord.Member = None, *, reason: commands.clean_content = ""):
        """ Cinsteste cu o bere sarakule! 🍻 """
        if not user or user.id == ctx.author.id:
            return await ctx.send(f"**{ctx.author.name}**: paaaarty!🎉🍺")
        if user.id == self.bot.user.id:
            return await ctx.send("*bea o bere cu mine* 🍻")
        if user.bot:
            return await ctx.send(f"Mi-ar placea sa ii dau o bere botului **{ctx.author.name}**, dar ma gandesc ca nu poate accepta :/")

        beer_offer = f"**{user.name}**, ai o primit o oferta de 🍺 de la **{ctx.author.name}**"
        beer_offer = beer_offer + f"\n\n**Motiv:** {reason}" if reason else beer_offer
        msg = await ctx.send(beer_offer)

        def reaction_check(m):
            if m.message_id == msg.id and m.user_id == user.id and str(m.emoji) == "🍻":
                return True
            return False

        try:
            await msg.add_reaction("🍻")
            await self.bot.wait_for('raw_reaction_add', timeout=30.0, check=reaction_check)
            await msg.edit(content=f"**{user.name}** si **{ctx.author.name}** savureaza o bere blonda impreuna. 🍻")
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send(f"well, **{ctx.author.mention}** se pare ca **{user.mention}** nu vrea sa bea o bere cu tine , al drq virgin. ;-;")
        except discord.Forbidden:
            # Yeah so, bot doesn't have reaction permission, drop the "offer" word
            beer_offer = f"**{user.name}**, ai o primit o oferta de 🍺 de la **{ctx.author.name}**"
            beer_offer = beer_offer + f"\n\n**Motiv:** {reason}" if reason else beer_offe
            await msg.edit(content=beer_offer)

    @commands.command()
    async def pupic(self, ctx, user: discord.Member = None, *, reason: commands.clean_content = ""):
        """ Dai cuiva un pupic uwu! 😘 """
        chosen_image = random.choice(lists.pozekiss)
        if not user or user.id == ctx.author.id:
            return await ctx.send(f"**{ctx.author.mention}**: 😘❤️")
        if user.id == self.bot.user.id:
            return await ctx.send("*vrea un pupic de la tine* 😘")
        if user.bot:
            return await ctx.send(f"Mi-ar placea sa ii dau botului un pupic **{ctx.author.mention}**, dar nu o sa imi raspunda :/")

        kiss_offer = f"**{ctx.author.mention}**, ai primit un 😘 de la **{user.mention}**"
        kiss_offer = kiss_offer + f"\n\n**Motiv:** {reason}" if reason else kiss_offer
        msg = await ctx.send(kiss_offer)

        def reaction_check(m):
            if m.message_id == msg.id and m.user_id == user.id and str(m.emoji) == "😘":
                return True
            return False

        try:
            await msg.add_reaction("😘")
            await self.bot.wait_for('raw_reaction_add', timeout=30.0, check=reaction_check)
            await msg.edit(content=f"**{ctx.author.mention}** si **{user.mention}** se iubesc 🥰")
            embed = discord.Embed(color=0xff69b4, timestamp=datetime.datetime.utcnow())
            embed.set_image(url=chosen_image)
            embed.set_footer(text=f"Requested by: {ctx.author.name}")

            await ctx.send(embed=embed)
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send(f"well, **{ctx.author.mention}** se pare ca **{user.mention}** nu vrea un pupic de la tine 😢")
        except discord.Forbidden:
            # Yeah so, bot doesn't have reaction permission, drop the "offer" word
            kiss_offer = f"**{ctx.author.mention}**, ai primit un 😘 de la **{user.mention}**"
            kiss_offer = kiss_offer + f"\n\n**Motiv:** {reason}" if reason else kiss_offer
            await msg.edit(content=kiss_offer)

    @commands.command()
    async def hug(self, ctx, user: discord.Member = None, *, reason: commands.clean_content = ""):
        """ Da o imbreatisare cuiva! 🤗 """
        chosen_image = random.choice(lists.pozehug)
        if not user or user.id == ctx.author.id:
            return await ctx.send(f"**{ctx.author.mention}**: 🤗❤️")
        if user.id == self.bot.user.id:
            return await ctx.send("*vrea o imbratisare de la tine* ❤️")
        if user.bot:
            return await ctx.send(f"Mi-ar placea sa ii dau botului o imbratisare **{ctx.author.mention}**, dar nu o sa imi raspunda :/")

        kiss_offer = f"**{ctx.author.mention}**, ai primit o 🤗 de la **{user.mention}**"
        kiss_offer = kiss_offer + f"\n\n**Motiv:** {reason}" if reason else kiss_offer
        msg = await ctx.send(kiss_offer)

        def reaction_check(m):
            if m.message_id == msg.id and m.user_id == user.id and str(m.emoji) == "🤗":
                return True
            return False

        try:
            await msg.add_reaction("🤗")
            await self.bot.wait_for('raw_reaction_add', timeout=30.0, check=reaction_check)
            await msg.edit(content=f"**{ctx.author.mention}** si **{user.mention}** se imbratiseaza 🥰")
            embed = discord.Embed(color=0xff69b4, timestamp=datetime.datetime.utcnow())
            embed.set_image(url=chosen_image)
            embed.set_footer(text=f"Requested by: {ctx.author.name}")

            await ctx.send(embed=embed)
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send(f"well, **{ctx.author.mention}** se pare ca **{user.mention}** nu vrea o imbratisare de la tine 😢")
        except discord.Forbidden:
            # Yeah so, bot doesn't have reaction permission, drop the "offer" word
            kiss_offer = f"**{ctx.author.mention}**, ai primit o 🤗 de la **{user.mention}**"
            kiss_offer = kiss_offer + f"\n\n**Motiv:** {reason}" if reason else kiss_offer
            await msg.edit(content=kiss_offer)

    @commands.command(aliases=['noticemesenpai'])
    async def noticeme(self, ctx, user: discord.Member = None):
        """ Notice me senpai! owo """
        if user is None:
            user = ctx.author
        chosen_image = random.choice(lists.pozehentai)
        if not permissions.can_handle(ctx, "attach_files"):
            return await ctx.send("Nu pot sa trimit imagini aici bagami-as pula :(.")
        
        await ctx.send(f"{ctx.message.author.mention} NOTICE ME SENPAIIII... UWU")
        embed = discord.Embed(color=0xff69b4, timestamp=datetime.datetime.utcnow())
        embed.set_image(url=chosen_image)
        embed.set_footer(text=f"Requested by: {ctx.author.name}")

        await ctx.send(embed=embed)

    @commands.command()
    async def nigga(self, ctx):
        """ NIGGA NO. """
        if not permissions.can_handle(ctx, "attach_files"):
            return await ctx.send("Nu pot sa trimit imagini aici bagami-as pula :(.")

        bio = BytesIO(await http.get("https://media1.tenor.com/images/274d834b6dffaf7229ff14577ca76a84/tenor.gif?itemid=5521492", res_method="read"))
        await ctx.send(file=discord.File(bio, filename="tenor.gif"))

    @commands.command()
    async def stayinalive(self, ctx):
        await ctx.send(f"https://www.youtube.com/watch?v=fNFzfwLM72c&ab_channel=BeeGeesVEVO")

    @commands.command()
    @commands.check(permissions.is_owner)
    async def juan(self, ctx, user_id: int):
        """ JUAN FRATE """
        user = self.bot.get_user(user_id)
        if not permissions.can_handle(ctx, "attach_files"):
            return await ctx.send("Nu pot trimite poze aici bagamias pulicica")

        bio = BytesIO(await http.get("https://i.redd.it/jacj1y21iuj51.jpg", res_method="read"))
        await user.send(file=discord.File(bio, filename="juan.jpg"))
        await ctx.send(f"✉️ L-am trimis pe Juan acasa la id-ul asta **{user_id}**")


    @commands.command()
    @commands.check(permissions.is_owner)
    async def gilbert(self, ctx, user_id: int):
        """ GILBERT FRATE """
        user = self.bot.get_user(user_id)
        if not permissions.can_handle(ctx, "attach_files"):
            return await ctx.send("Nu pot trimite poze aici bagamias pulicica")

        bio = BytesIO(await http.get("https://i.imgur.com/9x18D5m.png", res_method="read"))
        await user.send(file=discord.File(bio, filename="gilbert.png"))
        await ctx.send(f"✉️ L-am trimis pe Gilbert acasa la id-ul asta **{user_id}**")     

    @commands.command()
    async def slap(self, ctx, user: discord.Member = None):
        """ Fute o palma. """
        if user is None:
            user = ctx.author
        chosen_image = random.choice(lists.lovitura)
        if not permissions.can_handle(ctx, "attach_files"):
            return await ctx.send("Nu pot sa trimit imagini aici bagami-as pula :(.")
        
        await ctx.send(f"{ctx.message.author.mention} i-a futut una lu {user.mention}")
        embed = discord.Embed(color=0xff69b4, timestamp=datetime.datetime.utcnow())
        embed.set_image(url=chosen_image)
        embed.set_footer(text=f"Requested by: {ctx.author.name}")

        await ctx.send(embed=embed)

    @commands.command()
    async def ham(self, ctx):
        """ PENTRU REBEL FOMISTU. """
        if not permissions.can_handle(ctx, "attach_files"):
            return await ctx.send("Nu pot sa trimit imagini aici bagami-as pula :(.")

        bio = BytesIO(await http.get("https://media1.tenor.com/images/43a0e917f28b5f27369f707eea3d7cbf/tenor.gif?itemid=11375339", res_method="read"))
        await ctx.send(file=discord.File(bio, filename="tenor.gif"))

    @commands.command()
    @commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
    async def pacanele(self, ctx):
        """ Dai la pacanele. """
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

        if (a == b == c):
            await ctx.send(f"{slotmachine} All matching, Ai castigat! 🎉")
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(f"{slotmachine} 2 dintr-o lovitura, Ai castigat! 🎉")
        else:
            await ctx.send(f"{slotmachine} N-ai luat nimic, Ai pierdut 😢")

def setup(bot):
    bot.add_cog(Fun_Commands(bot))
