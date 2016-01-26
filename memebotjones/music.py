import memebotjones.base as base
import discord
import asyncio
import json
import pickle
from random import choice

# set up some needed globals
with open("config.json") as data:
    config = json.load(data)

queue_list = []
skip_list = []
player = None
shutdown_flag = False
snark_list = [
    "is not in the sudoers file.  This incident will be reported.",
    "doesn't have permission to use admin commands, but tried to anyways",
    "is a massive wanglord",
    "wants to tell everybody about his massive erection",
    "is a very naughty boy",
    "thinks he's above the law",
    "is gay for moleman"
]


@base.memefunc
def join(message, client):
    try:
        channel = discord.utils.get(client.get_all_channels(), name=config['voicechannel'])
    except discord.errors.InvalidArgument:
        print("The configured voice channel in the config does not exist.")
    global queue_list
    try:
        with open("queue.txt") as readfile:
            queue_list = pickle.load(readfile)
    except FileNotFoundError:
        print("No previous queue, running anyways")
    global voice
    voice = yield from client.join_voice_channel(channel)
    if len(queue_list) != 0:
        play_next()

# Define some utility functions first


# This is an internally used function that advances the play queue,
# then plays the next in the queue if there is something in the queue.
def move_queue():
    if shutdown_flag:
        with open("queue.txt", "w") as writefile:
            pickle.dump(queue_list, writefile)
            print("It is now safe to shut down")
    else:
        print("Advancing the queue")
        global skip_list
        skip_list = []
        player.stop()
        queue_list.pop(0)
        if len(queue_list) != 0:
            play_next()


# Plays the next entry in the queue.  Pretty straight forward
def play_next():
    try:
        global player
        player = voice.create_ytdl_player(queue_list[0], options="--ignore-errors --no-playlist", after=move_queue)
        # Also moves queue after finished
        print("now playing: {}".format(queue_list[0]))
        player.start()
    # This except doesn't seem to work right.  Not sure about it.
    except discord.ClientException:
        print('invalid link, skipping..')
        move_queue() 

'''
def skip_current_track():
    player.stop()
    move_queue()
'''


@base.memefunc
def add(message, client):
    link = message.content.split(" ")[1]
    # validate the link and make sure it's a youtube link first.
    if link.startswith("https://www.youtube.com")\
            or link.startswith("http://www.youtube.com")\
            or link.startswith("https://youtu.be") \
            or link.startswith("http://youtu.be"):
        queue_list.append(link)
        yield from client.send_message(message.channel, "Successfully added link to queue")
        if len(queue_list) == 1:
            play_next()
    else:
        yield from client.send_message(message.channel, "{} is not a valid youtube link".format(link))


@base.memefunc
def skip(message, client):
    if message.author.id not in skip_list or message.author.id != "98900092924215296":
        skip_list.append(message.author.id)
        yield from client.send_message(message.channel, "{} has voted to skip the currently playing track. \n {}/{}"
                                       .format(message.author.name, len(skip_list), config['numberofvotestoskip']))
    else:
        yield from client.send_message(message.channel, "{} has already voted to skip.".format(message.author.name))
    # max skips is equal to the percent configured in the Config converted to a decimal
    # times the number of users in the channel memebot is in, rounded to the nearest whole number.
    max_skips = round(config['percenttoskip'] / 100 * len(voice.channel.voice_members))
    if len(skip_list) >= max_skips:
        move_queue()
        yield from client.send_message(message.channel, "Skipping current track...")


@base.memefunc
def next(message, client):
    if message.author.id == config['ownerid']:
        yield from client.send_message(message.channel, "Forcing skip by admin...")
        move_queue()
    else:
        yield from client.send_message(message.channel, "{} {}".format(message.author.name, choice(snark_list)))


@base.memefunc
def queue(message, client):
    string_send = "The current queue is:\n"
    for entry in queue_list:
        string_send += "{}. {} \n".format(queue_list.index(entry) + 1, entry)
    string_send += "Add a new song to the queue with $add"
    yield from client.send_message(message.channel, string_send)


@base.memefunc
def nowplaying(message, client):
    yield from client.send_message(message.channel, "Now playing: \n {}".format(queue_list[0]))


@base.memefunc
def shutdown(message, client):
    if message.author.id == config['ownerid']:
        global shutdown_flag
        shutdown_flag = True
        yield from client.send_message(message.channel,
                                       "Shutdown initialized.  Will commence once the currently playing track ends.")


@base.memefunc
def killitohgod(message, client):
    if message.author.id == config['ownerid']:
        clear_queue()
        player.stop()
        yield from client.send_message(message.channel,
                                       "Queue dumped and playing stopped.  Don't break it again assholes")


def clear_queue():
    global queue_list
    queue_list = []
