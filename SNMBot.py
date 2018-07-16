import asyncio
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import time
from random import choice
from blib import *
try: from BotResources import *
except ModuleNotFoundError: from DiscordBots.BotResources import *


Client = discord.Client()
client = commands.Bot(command_prefix="")
botName = "SNMBot#8413"

print(eval("datetime.datetime(2018, 7, 15, 17, 25, 47, 427412)"))

users = {}
wordFilter = {
    "communist": "capitalist",
    "communism": "capitalism",
    "capitalist": "communist",
    "capitalism": "communism"
}
try:    # Tries to extract existing user data from storage and insert it into the 'users' dict
    with open("users.txt") as f:
        userdict = eval(f.read())
        for x in userdict.values():
            users[x["_User__userID"]] = User(
                x["_User__userID"],
                x["_User__rps_games"],
                x["_User__rps_wins"],
                x["_User__rps_losses"],
                RPSGame(
                    x["_User__userID"],
                    x["_User__rps_game"]["_RPSGame__round"],
                    x["_User__rps_game"]["_RPSGame__winner"],
                    x["_User__rps_game"]["_RPSGame__comp_wins"],
                    x["_User__rps_game"]["_RPSGame__user_wins"]
                ) if x["_User__rps_game"] is not None else None,
                x["_User__snm_points"],
                x["_User__last_snm_point_update"],
                x["_User__bet_games"],
                x["_User__bet_wins"],
                x["_User__bet_losses"],
                Bet(
                    x["_User__userID"],
                    x["_User__bet_game"]["_Bet__opts"]
                ) if x["_User__bet_game"] is not None else None,
                x["_User__ongoing_bets"]
            )
except FileNotFoundError: print("file not found")

print(users)

@client.event
async def on_ready():
    print("SNMBot has connected to its servers!")

@client.event
async def on_message(mes):
    if str(mes.author) != botName: #str(mes.channel.server) == "Bot Test Realm": # for debuggin
        try:    # Tries to print the users id, name and message contents in a manner where if the user has not been created by the bot it will cause an error and get caught by the except statement
            print(users[mes.author.id].userID + "\n" + str(mes.author) + ": " + mes.content + "\nResponse:")
        except KeyError:    # Creates a new user
            users[mes.author.id] = User(mes.author.id, last_snm_point_update=datetime.now())
            print(mes.author.id + "\n" + str(mes.author) + ": " + mes.content + "\nResponse:\nCreated new user")
        user = users[mes.author.id]
        '''     Filters and other higher priority checks      '''

        '''     Commands and other lower priority checks      '''
        if mes.content.lower().startswith("!rpsrank"):  # Returns the players rank in rock paper scissors
            print("Showed user their rps rank")
            ranks = sorted(list(users.values()), key=lambda x: x.rps_kd, reverse=True)
            await client.send_message(
                mes.channel,
                "<@" + user.userID + "> RPS rank is #" + str([x.userID for x in ranks].index(user.userID) + 1) + "\n" + str(user.rps_kd)
            )
        if mes.content.lower().startswith("!playrps"):
            if user.rps_game is not None:
                print("Informed user of existing rps game")
                await client.send_message(
                    mes.channel,
                    "We're already playing a game <@" + mes.author.id + ">!\nHere's the status:\n" + user.rps_game.status(True)
                )
            else:
                user.play_rps()
                print("Started rps game")
                await client.send_message(
                    mes.channel,
                    "Alright <@" + mes.author.id + ">, let's play 3 rounds of Rock Paper Scissors!\n" +
                    "To pick type '!pick <your pick> in chat! (Example: !pick rock)"
                )
        elif mes.content.lower().startswith("!pick"):
            if user.rps_game is not None:
                result = user.rps_game.play_round((mes.content.split() + [""])[1])
                print("Played rps with user")
                if user.rps_game.winner is not None:
                    result += "\n\n The winner is " + user.rps_game.winner + "!\n Thanks for playing!"
                    user.game_over_rps()
                    print("Displayed winner")
                await client.send_message(mes.channel, result)
            else:
                print("Informed user that they have not started a rps game")
                await client.send_message(mes.channel, "You first have to start a game by typing *!playrps* <@" + mes.author.id + ">!")
        elif mes.content.lower().startswith("!decide "):
            print("Decided for user")
            await client.send_message(
                mes.channel,
                "Hmmmm... Ok <@" + user.userID + ">, let's go for:\n" + choice(mes.content[len("!decide "):].split(","))
            )
        elif mes.content.lower().startswith("!snmp"):
            print("Displayed users snmp")
            await client.send_message(mes.author, "You have " + str(user.snm_points) + "SNM Points <@" + user.userID + ">!")
        elif mes.content.lower().startswith("!startbet "):
            if user.bet_game is not None:
                print("Told use to end their ongiong bet first")
                await client.send_message(mes.channel, "You first have to end your other bet <@" + user.userID + ">!\nTo end a bet just type '!endbet [winning_option]' (Example !endbet 4)\n" + "".join([str(x) + ": " + elem + "\n" for x, elem in enumerate(user.bet_game.opts)]))
            else:
                print("Started bet for user")
                user.start_bet(mes.content[len("!startbet "):].split(","))
                await client.send_message(mes.channel, "Alright <@" + user.userID + ">, I just started a bet. Everybody join in by betting your SNM Points!\nTo bet your points just type: '!bet @[user] [option] [amount]' (Example: !bet @SNMBot 2 69)\nTo find out how many SNM Points you have just type !snmp\nTo end a bet just type '!endbet [winning_option]' (Example !endbet 4)\nThe options are:\n" + "".join([str(x) + ": " + elem + "\n" for x, elem in enumerate(user.bet_game.opts)]))
        elif mes.content.lower().startswith("!bet "):
            try:
                bet_user = mes.mentions[0].id
                if user == bet_user:
                    print("Alerted user that they can not bet on they're own bets")
                    await client.send_message(mes.author, "You cannot bet on your own bets <@" + user.userID + ">!")
                elif users[bet_user].bet_game is None:
                    print("Alert user that the bet user has no ongoing bets")
                    await client.send_message(mes.author, "<@" + bet_user + "> has no ongoing bets!")
                else:
                    if int(mes.content.split()[3]) <= user.snm_points:
                        print("Betted for the user")
                        user.choose_bet(bet_user, int(mes.content.split()[2]), int(mes.content.split()[3]))
                        await client.send_message(mes.author, "Your bet went through and you now have " + str(user.snm_points) + "SNMP left until the bet ends!")
                    else:
                        print("Alerted user that they don't have enough snmp")
                        await client.send_message(mes.author, "You can't afford to bet " + mes.content.split()[3] + " <@" + user.userID + ", you broke ass fuck!")
            except KeyError:
                print("Alerted user that bet user does not exit")
                await client.send_message(mes.author, "User <@" + bet_user + "> does not exist!")
        elif "no u" in mes.content.lower():
            print("Corrected users pubescent insult")
            await client.send_message(
                mes.channel,
                "No U has never been an original insult <@" + user.userID + ">, you're simply stealing it from Anti-Uranium political groups!\nsum(Silicon, Carbon, Potassium), sum(Baron, Uranium, Radon)\nsum(Germanium, Tantalum), sum(Rhenium, Potassium, Tellurium)"
            )


        print()
        with open("users.txt", "w") as f:
            f.write(str(users))


client.run("NDY2NzE4MzIyMTY0MTA1MjE2.DilKtQ.OIUu-fTBigSfM8DvdhXU0pTkiS8")