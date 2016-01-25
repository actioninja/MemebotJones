import sys
import discord
import json
import asyncio
import traceback
import memebotjones


# Get the config and load it as the variable config
# Also catch if there isn't one there, and generate a new one.
try:
    with open('config.json') as data:
        config = json.load(data)
except FileNotFoundError:
    print("You do not have a config file!  New one generated as config.json, exiting.")
    with open('config.json', 'w') as outfile:
        data = {'version': "0.1", 'email': "", 'password': "", 'ownerid': "", 'invoker': "$", 'voicechannel': "", 'numberofvotestoskip': 4}
        json.dump(data, outfile)
        sys.exit()


# If the config is outdated, some nasty ass shit can happen.
# Update this variable only when the config gets new parameters.
# TODO: Make it auto add the new required variables.
if config['version'] != "0.1":
    print("Your config file is outdated.  Please update your config with new values added since last patch.")
    sys.exit()


linkspool = []
client = discord.Client(max_messages=3000)
voice = None





@client.async_event
def on_ready():
    print("Logged in as:")
    print(client.user.name)
    print(client.user.id)
    print("-------------------------------")
    # Using the voice channel value from the config, the bot will immediately connect to the voice channel as soon as it
    # is running.



@client.async_event
def on_message(message):
    if message.content.startswith(config['invoker']) and message.author.id != client.user.id:
        command = message.content[1:].split(' ')[0].lower()
        if command in memebotjones.base.functions:
            yield from client.send_typing(message.channel)
            yield from memebotjones.base.functions[command](message, client)


@client.async_event
def on_typing(channel, user, when):
    # :^)
    # Bonus points if you figure out who's id this is.
    if user.id == "81216735872548864":
        print("The goy is talking")


@client.async_event
def on_error(event):
    print("Caught error, dumping queue")
    print(traceback.format_exc())
    memebotjones.music.clear_queue()



def main_task():
    try:
        yield from client.login(config['email'], config['password'])
        yield from client.connect()
    except discord.errors.LoginFailure:
        print('Invalid login credentials!  Exiting.')
        sys.exit()


# I don't really know what this does, but it's necessary
loop = asyncio.get_event_loop()
loop.run_until_complete(main_task())
loop.close()
