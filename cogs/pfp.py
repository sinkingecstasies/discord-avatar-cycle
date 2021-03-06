import discord
from discord.ext import commands, tasks
from discord.ext.commands import Cog as cog
from discord.ext.commands import command as cmd
import json
import random
import asyncio
import aiohttp
import re
import datetime as dt

try:
    import humanize
except ImportError:
    humanize = None

class avatar_rotator(cog):
    def __init__(self, bot):
        self.bot = bot
        self.pfp_rotator.start()
        print("pfp.py has been loaded")

    def cog_unload(self):
        self.pfp_rotator.cancel()

    @cmd(aliases=['copy'])
    async def steal(self, ctx, u: str = None):
        """
        Copy someone else pfp and make it yours. You can also steal someone else avatar outside server by using their user ID

        You can use either their username#discrim, username, or nickname. You must be in same server as the target in for this to work. Using user ID is more recommended

        This command is case sensitive. If you mistyped one case letter, this will return error
        """
        def get_password():
            with open('config/password', 'r') as f:
                password = f.readline()

            return password

        if not u:
            return await ctx.send("No target, try use username or user ID")
			
        # This will check if you're using either user ID or by their username/nickname
        regex = re.match(r"[0-9]{18}", u)
        
        if not regex:
            # Try search member by using either username, or nickname otherwise return error NotFound
            try:
                u = await commands.MemberConverter().convert(ctx, u)
            except commands.BadArgument:
                return await ctx.send("member not found")
        else:
            try:
                u = await self.bot.fetch_user(int(u))
            except discord.NotFound:
                return await ctx.send("user not found, perhaps you're using wrong ID?")
        
        async with aiohttp.ClientSession() as cs: 
            async with cs.get(str(u.avatar_url)) as r:
                av = await r.read()
                await self.bot.user.edit(avatar=av, password=get_password())
                self.bot.variables_last_link = av

        await ctx.message.add_reaction('☑️')

    @cmd(aliases=['setting', 'settings'])
    async def config(self, ctx: commands.Context, option,  *, setting):
        """
        Changes configuration files
        Available options
        cycle    : change cycling style
        interval : how often it should change

        Settings format
        cycle    : random | cycle
        interval : time format is 0d0h0m0s. For example, 6h for 6 hours
        """

        # a simple time converter by using str.split to get and calculate the number
        def time_converter(time_string):
            if time_string.isdigit() == True:
                return time_string

            the_time = time_string
            total_seconds = 0

            if str(the_time).lower().find("d") != -1:
                split, original_time = str(the_time).split("d")
                days_to_seconds = int(split) * 86400
                total_seconds = total_seconds + int(days_to_seconds)
                the_time = original_time

            if str(the_time).lower().find("h") != -1:
                split, original_time = str(the_time).split("h")
                hours_to_seconds = int(split) * 3600
                total_seconds = total_seconds + int(hours_to_seconds)
                the_time = original_time

            if str(the_time).lower().find("m") != -1:
                split, original_time = str(the_time).split("m")
                minute_to_seconds = int(split) * 60
                total_seconds = total_seconds + int(minute_to_seconds)
                the_time = original_time

            if str(the_time).lower().find("s") != -1:
                split, original_time = str(the_time).split("s")
                seconds_to_second_lol = int(split) * 1
                total_seconds = total_seconds + int(seconds_to_second_lol)
                the_time = original_time

            return total_seconds

        # check if setting has available options, otherwise success return false
        def cycle_set(setting):
            success = False

            with open('config/config.json', 'r') as f:
                config = json.load(f)

            if setting.lower() == "random":
                config['cycling style'] = setting

                with open('config/config.json', 'w') as f:
                    json.dump(config, f, indent=4)

                success = True
                return success

            elif setting.lower() == "cycle":
                config['cycling style'] = setting

                with open('config/config.json', 'w') as f:
                    json.dump(config, f, indent=4)

                success = True
                return success

            else:
                return success

        def interval_set(time_string):
            seconds = time_converter(time_string)

            if seconds == 0:
                return seconds

            with open('config/config.json', 'r') as f:
                config = json.load(f)

            config['interval'] = seconds

            with open('config/config.json', 'w') as f:
                json.dump(config, f, indent=4)

            return seconds

        if option.lower() == 'cycle':
            success = cycle_set(setting)
            if success == False:
                await ctx.send("Invalid setting provided, this setting only accept `random` or `cycle`")
            else:
                await ctx.send(f"☑️")
        elif option.lower() == 'interval':
            seconds = interval_set(setting)

            if seconds == 0:
                await ctx.send("you can't set interval at 0 second")
                return

            if humanize:
                delta = dt.timedelta(seconds=seconds)
                await ctx.send(f"successfully changed interval to {humanize.precisedelta(delta)}")
            else:
                await ctx.send(f"successfully changed interval")
        else:
            await ctx.send("There is no such option, available options: `cycle` `interval`")

    @config.error
    async def config_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(error)

    @cmd(aliases=['av', 'pfp'])
    async def avatar(self, ctx, *, target = ""):
        """Obtain someone else avatar in maximum resolution, also works if user didn't share mutual servers with the bot but ID is required for this to work
        For mass avatar, use multiple IDs, separate by space
        """
        def to_jpg(user):
            url = user.avatar_url_as(format="jpg", size=4096)
            return url

        def to_png(user):
            url = user.avatar_url_as(format="png", size=4096)
            return url

        def to_webp(user):
            url = user.avatar_url_as(format="webp", size=4096)
            return url

        def to_gif(user):
            if user.is_avatar_animated() == True:
                url = user.avatar_url_as(format="gif", size=4096)
                text = f"   |   [GIF]({url})"
                return text
            else:
                not_animated = ""
                return not_animated

        def to_default(user):
            url = user.avatar_url_as(size=4096)
            return url

        try:
            tempvalue = target.replace(" ", "")
            if target == "":
                embed = discord.Embed(color=discord.Color.green(), title=f"{ctx.author.name}#{ctx.author.discriminator}'s avatar", description=(f'[JPG]({to_jpg(ctx.author)})   |   [PNG]({to_png(ctx.author)})   |   [WebP]({to_webp(ctx.author)}){to_gif(ctx.author)}')) 

                embed.set_image(url=to_default(ctx.author))
                await ctx.send(embed=embed)

            elif tempvalue.isdigit() == False: # if not using ID, search from get_user
                target_member = await commands.MemberConverter().convert(ctx, target) # convert it into user either based on mention, name, or name#discrim

                embed = discord.Embed(color=discord.Color.green(), title=f"{target_member.name}#{target_member.discriminator}'s avatar", description=(f'[JPG]({to_jpg(target_member)})   |   [PNG]({to_png(target_member)})   |   [WebP]({to_webp(target_member)}){to_gif(target_member)}')) 

                embed.set_image(url=to_default(target_member))
                await ctx.send(embed=embed)

            elif tempvalue.isdigit() == True: # if using ID, use fetch_user
                target = target.split(" ")
                for each in target:
                    target_user = await self.bot.fetch_user(each)

                    embed = discord.Embed(color=discord.Color.green(), title=f"{target_user.name}#{target_user.discriminator}'s avatar", description=(f'[JPG]({to_jpg(target_user)})   |   [PNG]({to_png(target_user)})   |   [WebP]({to_webp(target_user)}){to_gif(target_user)}')) 

                    embed.set_image(url=to_default(target_user))
                    await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(e)

    @cmd(aliases=['next'])
    async def skip(self, ctx: commands.Context):
        """
        Change your avatar, this command will either cycle or picks random avatar depending on your config
        """
        await self.rotator()
        await ctx.message.add_reaction('☑️')

    @cmd(aliases=['skipto', 'jumpto'])
    async def jump(self, ctx, index: int):
        """
        Change avatar to specified index on list
        """
        def get_password():
            with open('config/password', 'r') as f:
                password = f.readline()

            return password

        with open('config/pfp.json', 'r') as f:
            pfp = json.load(f)

        try:
            avatar = pfp['links'][index - 1]
        except IndexError:
            return await ctx.send("index out of range")

        try:
            async with aiohttp.ClientSession() as cs: 
                async with cs.get(avatar) as r:
                    av = await r.read()
                    await self.bot.user.edit(avatar=av, password=get_password())
                    self.bot.variables_last_link = av
            await ctx.send('☑️')
        except Exception as e:
            # this will raise if url is not an image or when you're hitting the ratelimit
            await ctx.send(e)
    
    @jump.error
    async def jump_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(error)
        if isinstance(error, commands.BadArgument):
            await ctx.send("index should be an integer")

    @cmd(aliases=['avatars', 'links', 'link'])
    async def list(self, ctx: commands.Context, page_number: int = 1):
        """
        Show list of all links inside pfp.json
        """
        counter = 1

        with open("config/pfp.json", 'r') as f:
            pfp = json.load(f)

        links = pfp["links"]

        p = commands.Paginator(prefix='', suffix='')

        for link in links:
            p.add_line(line=f"{str(counter)}. {link}")
            counter += 1

        pages = p.pages
        total_pages = len(pages)

        if page_number <= 0:
            page_number = 1
            offset = 0
        elif page_number > total_pages:
            page_number = total_pages
            offset = -1
        else:
            offset = page_number - 1

        embed = discord.Embed(color=ctx.author.color, title='List of links', description=pages[offset])
        embed.set_footer(text=f"Page {page_number}/{total_pages}")

        await ctx.send(embed=embed)

    @cmd(aliases=['rem', 'r'])
    async def remove(self, ctx: commands.Context, *, index: str):
        """
        Remove a specific url inside json by using their index number shown at list/avatars command
        Accepts latest/l as an argument, this will delete most recent link
        Accepts bulk delete, separate numbers by space
        """
        with open("config/pfp.json", 'r') as f:
            pfp = json.load(f)
        links = pfp['links']

        counter = 0
        msg = ""

        index = index.split(" ")
        index.sort(reverse=True) # reversed because after you delete an element, the list index will also updates. You'll get the idea
        for num in index:
            try:
                if num.lower() == 'l' or num.lower() == 'latest':
                    num = -1
                else:
                    num = int(num) -1
                result = links.pop(num)
                msg += result + "\n"
                counter += 1
            except Exception:
                pass

        pfp['links'] = links
        with open("config/pfp.json", 'w') as f:
            json.dump(pfp, f, indent=4)

        embed = discord.Embed(
            color=discord.Color.green(),
            title=f"Successfully removed {counter} link{'s' if counter != 1 else ''}",
            description=msg
            )

        await ctx.send(embed=embed)

    @remove.error
    async def remove_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"You need to specify index number, you can view index number of each link by using `{ctx.prefix}list`")

    @cmd(aliases=['add'])
    async def append(self, ctx, *, links: str):
        """
        Appends an anther avatar into json, please use direct image url only
        Supports bulk links, separate them by space
        """
        success = 0
        fails = 0
        fails_result = ""
        
        links = links.split(" ")
        for link in links:
            # to ensure the ones you append is a link
            # regex stolen from geeksforgeeks.org lol
            regex_match = re.search(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))", link)
            if regex_match == None:
                link += "\n"
                fails_result += link
                fails += 1
            else:
                with open("config/pfp.json", 'r') as f:
                    j = json.load(f)

                j_links: list = j['links']
                j_links.append(link)

                j['links'] = j_links

                with open("config/pfp.json", 'w') as f:
                    json.dump(j, f, indent=4)
                
                success += 1

        # will pick either green or red depending if there any success
        def green_or_red():
            if success == 0:
                color = discord.Color.red()
                return color
            else:
                color = discord.Color.green()
                return color

        embed = discord.Embed(color=green_or_red(), description=f"{success} link{'s' if success != 1 and success != 0 else ''} has been appended\n{fails} is not a link")
        embed.add_field(name=f"Invalid link{'s' if fails != 1 and fails != 0 else ''}", value=fails_result) if fails != 0 else None

        await ctx.send(embed=embed)
    
    @append.error
    async def append_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(error)

    @tasks.loop()
    async def pfp_rotator(self):
        def get_interval_setting():
            with open('config/config.json', 'r') as f:
                config = json.load(f)
            
            interval = config['interval']

            return interval

        await self.rotator()

        seconds = get_interval_setting()
        await asyncio.sleep(seconds)

    # the main rotator/cycle system
    async def rotator(self):
        # It need to wait for some time to connect it, without this bot.user will always return None
        if self.bot.variables_first_run == True:
            await asyncio.sleep(15)
            self.bot.variables_first_run = False

        def get_password():
            with open('config/password', 'r') as f:
                password = f.readline()

            return password

        def get_cycle_setting():
            with open('config/config.json', 'r') as f:
                config = json.load(f)
                
            setting = config['cycling style']

            return setting
        
        # cycle links inside pfp.json, it uses variable that will keep increasing by 1 until an index error raised
        def get_cycle_avatar(links):
            index = self.bot.variables_index
            while True:
                try:
                    av = links[index]
                    index += 1
                    break
                except IndexError:
                    index = 0

            # to ensure dupe avatar will not be used
            while self.bot.variables_last_link == av:
                try:
                    index += 1
                    av = links[index]
                except IndexError:
                    index = 0

            self.bot.variables_index = index

            return av
            
        def get_random_avatar(links):
            av = random.choice(links)

            # to ensure dupe avatar will not be used
            while self.bot.variables_last_link == av:
                av = random.choice(links)

            return av

        try:
            with open("config/pfp.json", 'r') as f:
                pfp = json.load(f)

            links = pfp["links"]

            cycle = get_cycle_setting()

            if cycle == "cycle":
                avatar = get_cycle_avatar(links)

            else:
                avatar = get_random_avatar(links)

            async with aiohttp.ClientSession() as cs: 
                async with cs.get(avatar) as r:
                    av = await r.read()
                    # password is required for user accounts for whatever reason, unnecessary for bot accounts
                    await self.bot.user.edit(avatar=av, password=get_password())
                    self.bot.variables_last_link = av
        except Exception as e:
            # this will usually raised when url is invalid, config/pfp json get messed up, or when you're hitting the ratelimit
            print(e)

def setup(bot):
    bot.add_cog(avatar_rotator(bot))