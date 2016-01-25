import memebotjones.base as base


@base.memefunc
def help(message, client):
    yield from client.send_message(message.author, "Memebot jones is a automated music bot for the /g/ server. \nCommands are preceded with an invoker(By default \"$\") \nThis means to use a command you type \"$[command]\"\nCurrent commands are:\nadd [youtube link]: Adds a new song to the play queue\nnext: Votes to skip the current playing song and skip to the next one")