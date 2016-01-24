import sys, discord, json,  asyncio


try:
    with open('config.json') as data:
        config = json.load(data)
except FileNotFoundError:
    print("You do not have a config file!  New one generated as config.json, exiting.")
    with open('config.json', 'w') as outfile:
        data = {'version': "0.1", 'email': "", 'password': "", 'ownerid': "", 'invoker': "$", 'voicechannel': ""}
        json.dump(data, outfile)
        sys.exit()


if config['version'] != "0.1":
    print("Your config file is outdated.  Please update your config with new values added since last patch.")
    sys.exit()


linkspool = []
client = discord.Client(max_messages=3000)
voice = None


def move_queue():
    linkspool.pop(0)
    if linkspool[0] != "":
        play_next()


def play_next():
    try:
        player = voice.create_ytdl_player(linkspool[0], after=move_queue())
        player.start()
    except discord.ClientException:
        print('invalid link, skipping..')
        play_next()


@client.async_event
def on_ready():
    print("Logged in as:")
    print(client.user.name)
    print(client.user.id)
    print("-------------------------------")
    channel = discord.utils.get(client.get_all_channels(), name=config['voicechannel'])
    global voice
    voice = yield from client.join_voice_channel(channel)


@client.async_event
def on_message(message):
    if message.content.startswith(config['invoker']):
        print(message.content[1:].split(' ')[0])
        linkspool.append(message.content[1:].split(' ')[0])
        print(linkspool)
        if len(linkspool) == 1:

            play_next()


@client.async_event
def on_typing(channel, user, when):
    if user.id == "81216735872548864":
        print("The goy is talking")


def main_task():
    try:
        yield from client.login(config['email'], config['password'])
        yield from client.connect()
    except discord.errors.LoginFailure:
        print('Invalid login credentials!  Exiting.')
        sys.exit()


loop = asyncio.get_event_loop()
loop.run_until_complete(main_task())
loop.close()
