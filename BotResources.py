from random import randint
from BTYPE import cNum
import datetime


'''     Class that handles Rock Paper Scissor games     '''
class RPSGame:

    opts = ["rock", "scissors", "paper"]

    def __init__(self, userID, rounds=0, winner=None, comp_wins=0, user_wins=0):
        self.__userID = userID
        self.__round = rounds
        self.__winner = winner
        self.__comp_wins = comp_wins
        self.__user_wins = user_wins

    @property
    def userID(self):
        return self.__userID

    @property
    def round(self):
        return self.__round

    @property
    def winner(self):
        return self.__winner

    @property
    def user_wins(self):
        return self.__user_wins

    @property
    def comp_wins(self):
        return self.__comp_wins

    def status(self, rounds=False):     # Returns information about the game in a readable manner
        return "SNMBot wins: " + str(self.__comp_wins) +\
               "\n<@" + self.__userID + "> wins: " + str(self.__user_wins) +\
               (("\nRounds Completed: " + str(self.__round)) if rounds else "")

    def play_round(self, word):     #Initiates a round of rock paper scissors where the bot chooses at random and returns the result
        if word.lower() in ("", " "):
            return "You have to chose at least one option <@" + self.__userID + ">!\nThe options are: " + str(self.opts) + ".\nTry again!"
        elif word.lower() not in self.opts:
            return "*" + word + "* is not an option <@" + self.__userID + ">!\nThe options are: " + str(self.opts) + ".\nTry again!"
        else:
            comp_pick = cNum(0, 2, randint(0,2))
            user_pick = cNum(0, 2, self.opts.index(word.lower()))
            mes = "I pick " + self.opts[int(comp_pick)] + " <@" + self.__userID + ">!\n"
            if comp_pick - 1 == user_pick:
                self.__user_wins += 1
                mes += "Aww Shucks, I lost!"
            elif comp_pick + 1 == user_pick:
                self.__comp_wins += 1
                mes += "Yes, I win!"
            else:
                mes += "Damn, a tie!"
            if self.__comp_wins == 3:
                self.__winner = "SNMBot"
            elif self.__user_wins == 3:
                self.__winner = "<@" + self.__userID + ">"
            self.__round += 1
            return mes + "\n\nResults after round " + str(self.__round) + ":\n" + self.status()

    def __str__(self):
        return str(vars(self))

    __repr__ = __str__



'''     Class that handles betting      '''
class Bet:
    def __init__(self, userID, opts):
        self.__userID = userID
        self.__opts = opts

    @property
    def userID(self):
        return self.__userID

    @property
    def opts(self):
        return self.__opts

    def __str__(self):
        return str(vars(self))

    __repr__ = __str__


'''     Class that handles information about users that use the bot     '''
class User:
    def __init__(self, userID, rps_games=0, rps_wins=0, rps_losses=0, rps_game=None, snm_points=0, last_snm_point_update=None, bet_games=0, bet_wins=0, bet_losses=0, bet_game=None, ongoing_bets={}):
        self.__userID = userID
        self.__rps_games = rps_games
        self.__rps_wins = rps_wins
        self.__rps_losses = rps_losses
        self.__rps_game = rps_game
        self.__snm_points = snm_points
        self.__last_snm_point_update = last_snm_point_update
        self.__bet_games = bet_games
        self.__bet_wins = bet_wins
        self.__bet_losses = bet_losses
        self.__bet_game = bet_game
        self.__ongoing_bets = ongoing_bets

    @property
    def userID(self):
        return self.__userID

    @property
    def rps_games(self):
        return self.__rps_games

    @property
    def rps_wins(self):
        return self.__rps_wins

    @property
    def rps_losses(self):
        return self.__rps_losses

    @property
    def rps_game(self):
        return self.__rps_game

    @property
    def rps_kd(self):   # Returns the users rock paper scissors win/loss ratio
        return self.__rps_wins / (self.__rps_losses if self.__rps_losses != 0 else 1)

    @property
    def snm_points(self):
        self.update_snm_points()
        return self.__snm_points

    @property
    def last_snm_point_update(self):
        return self.__last_snm_point_update

    @property
    def bet_games(self):
        return self.__bet_games

    @property
    def bet_wins(self):
        return self.__bet_wins

    @property
    def bet_losses(self):
        return self.__bet_losses

    @property
    def bet_game(self):
        return self.__bet_game

    @property
    def ongoing_bets(self):
        return self.__ongoing_bets

    def update_snm_points(self):
        date = datetime.datetime.now()
        print(date, " ::: ",self.__last_snm_point_update)
        self.__snm_points += int((date - self.__last_snm_point_update).total_seconds() / 60)
        self.__last_snm_point_update = date

    def play_rps(self):     # Creates a rock paper scissors game and stores it
        self.__rps_game = RPSGame(self.__userID)

    def game_over_rps(self):    # Extracts info from rock paper scissors game then deletes it
        if self.__rps_game.winner == self.__userID:
            self.__rps_wins += 1
        else:
            self.__rps_losses += 1
        self.__rps_games += 1
        self.__rps_game = None

    def start_bet(self, opts):
        self.__bet_game = Bet(self.__userID, opts)

    def end_own_bet(self):
        self.__bet_game = None

    def end_bet(self, betID, winning_opt, client):
        try:
            win = False
            if self.__ongoing_bets[betID][0] == winning_opt:
                self.__bet_wins += 1
                self.__amount += 2 * self.__ongoing_bets[betID][1]
                win = True
            else:
                self.__bet_losses += 1
            self.__bet_games += 1
            self.__ongoing_bets.pop(betID)
            return win
        except KeyError:
            return None

    def choose_bet(self, betID, opt, amount):
        self.update_snm_points()
        self.__ongoing_bets[betID] = [opt, amount]
        self.__snm_points -= amount

    def __str__(self):
        return str(vars(self))

    __repr__ = __str__
