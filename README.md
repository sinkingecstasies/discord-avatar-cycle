# Before you start
Discord selfbot are against ToS, using any selfbot will likely get your account banned. I'm not responsible for any problem caused by this.

**Use this at your own risk**

The selfbot is here just either for fun or for education purposes

### Backwards compability
This was written on python 3.8.2 64 bit using [discord.py](https://github.com/Rapptz/discord.py) 1.5.0. You might encounters error if you're using older version

## Requirements
- [python](https://www.python.org/) 3.6+
- [discord.py](https://github.com/Rapptz/discord.py)
- [humanize](https://pypi.org/project/humanize/) (optional)

# Setup
- All you have to do is just set up configuration files inside config folder, you need to put your token, password. You can add avatar links by directly edit them or add them later afterwards
- Run main.py. You can use any IDE, or run straight from command prompt by doing `python main.py` at the current folder

# Hosting
Pretty sure it's compatible with most VPS like [galaxygate](https://www.galaxygate.net/), [linode](https://www.linode.com/), or [vultr](https://www.vultr.com/) for like 3/5$.

Or free ones like [heroku](https://www.heroku.com/), [repl.it](https://repl.it/) (these are not really good but it's your choice).

# repl.it
There also [repl.it project](https://repl.it/@Tris07/Avatar-cycle), all you have to do is set up [.env](https://docs.repl.it/repls/secret-keys) to store your credentials.
It should look like this:
```
TOKEN=your_token
PASSWORD=your_password
```

## Features
- This bot will changes your discord avatar with custom interval, so you could set it for like daily, hourly, etc.
- You can also append, change configuration/avatar files straight from commands or edit them manually
- This bot has 2 cycle style, random and cycle

### Random
It will randomly picks avatar inside config

### Cycle
It will cycle avatar by ascending order

# Commands
Default prefix is `!!!`, you can change it on main.py into whatever you like
| Command name | Alias | Description | Usage |
| ------ | ------ | ------ | ------ |
| avatar | avatar / av / pfp | Get user avatar in maximum resolution, able to fetch avatar even if you're not mutual server by using ID | !!!av \<user ID\>
| append | append / add | Appends an anther avatar into json, please use direct image url only. Accepts bulk links, separate them by space | !!!append \<link1\> \<link2\> ... |
| config | config / setting / settings | Changes configuration files. Available options are config and interval, config setting only accepts either `cycle` or `random`, interval only accepts time format in 0d0h0m0s, for example: 1d6h for  1 day and 6 hours | !!!config \<cycle\|interval\> \<setting\> |
| jump | jump / jumpto / skipto | Change avatar to specified index on list | !!!jump \<index\> |
| list | list / avatars / link / links | Show list of all links inside pfp.json | !!!list |
| remove | remove / rem / r  | Remove a specific url inside json by using their index number shown on 'list' command. Accepts `l`/`latest` as an argumet, also accepts bulk delete | !!!remove \<index1\> \<index2\> ... |
| skip | skip / next | Change your avatar, this command  will either cycle or picks random depending on your config | !!!skip |
| steal | steal / copy | Copy someone else pfp and make it yours. You can also steal someone else avatar outside server by using their user ID | !!!steal \<username\|user ID\>
| help | N/A | Display the defualt help command, you can also get a help from specific command | !!!help \[command_name\]
> Values in \<\> are required

> Values in \[\] are optional

# Changelogs
### 18 October 2020
- Added new command `!!!steal`/`!!!copy`
- Changing pfp manually (from either `steal` or `jump` command) will also change `bot.variables_last_link` variable
- Reloading `pfp` cog will no longer duplicate `@task.loop` tasks
- Whenever you failed to change avatar (due to ratelimit or something), `bot.variables_last_link` will not change

### 8 January 2021
- Added new command `!!!avatar`
- Added paginator to `list` and some new aliases
- Small fixes

## Notes
If `!!!steal` returns error like `this command is only for bot account`, try changing [line 51](https://github.com/Tris07/discord-avatar-cycle/blob/master/cogs/pfp.py#L51) into
```
                u = self.bot.get_user(int(u))
```

If the bot doesn't change avatar, that's probably because you hit the ratelimit or url is invalid

For whatever reason, user accounts are required to use password, bot accounts doesn't require password though

Not recommended if you're hosting the bot on [heroku](https://www.heroku.com/) due to [ephemeral file system](https://devcenter.heroku.com/articles/how-heroku-works#dyno-manager)
