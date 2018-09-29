from pyrez.api import *
from pyrez.enumerations import *

from decouple import config, Csv

from flask import Flask, jsonify, request

app = Flask(__name__)

try:
    PYREZ_AUTH_ID = config("PYREZ_AUTH_ID")
    PYREZ_DEV_ID = config("PYREZ_DEV_ID")
except:
    PYREZ_AUTH_ID = os.environ("PYREZ_AUTH_ID")
    PYREZ_DEV_ID = os.environ("PYREZ_DEV_ID")

paladinsPC = PaladinsAPI(devId=PYREZ_DEV_ID, authKey=PYREZ_AUTH_ID)
paladinsPS4 = PaladinsAPI(devId=PYREZ_DEV_ID, authKey=PYREZ_AUTH_ID, platform=Platform.PS4)
paladinsXBOX = PaladinsAPI(devId=PYREZ_DEV_ID, authKey=PYREZ_AUTH_ID, platform=Platform.XBOX)

CURRENT_MATCH_STRINGS = {
    "pt" : "Partida atual: {0} | VS | {1}",
    "en" : "Current match: {0} | VS | {1}",
}
CURRENT_MATCH_PLAYER_STRINGS = {
    "pt" : "{0}: {1} ({2}){3}",
    "en" : "{0} as {1} ({2}){3}",
}
PLAYER_NULL_STRINGS = {
    "pt" : "Player not specified!",
    "en" : "Player not specified!",
}
PLAYER_NOT_FOUND_STRINGS = {
    "pt" : "Jogador inválido!",
    "en" : "Player not found!",
}
PLAYER_NOT_MATCH_STRINGS = {
    "pt" : "Player isn't in a match!",
    "en" : "Jogador não está em partida!",
}
PLAYER_RANK_STRINGS = {
    "pt" : "{0} (Nível {1}) é {2}{3} com {4} vitórias e {5} derrotas.{6}",
    "en" : "{0} (Level {1}) is {2}{3} with {4} wins and {5} losses.{6}",
}
#Arrumar
CHAMP_WINRATE_STRINGS = {
    "pt" : "{0} (Nível {1}): Vitórias: {2}, derrotas: {3} (Kills: {5} / Deaths: {6} / Assists: {7} - {8} KDA) - Winrate: {4}%",
    "en" : "{0} (Level {1}): {2} Wins, {3} Losses (Kills: {5} / Deaths: {6} / Assists: {7} - {8} KDA) - Winrate: {4}%",
}
GAME_VERSION_STRINGS = {
    "pt" : "{0} {1} está {2} - Versão atual: {3} ({4})",
    "en" : "{0} {1} is {2} - Current version: {3} ({4})",
}

@app.route('/api/version', methods=['GET'])
def getGameVersion():
    platform = request.args.get("platform") if request.args.get("platform") else "pc"
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"
    
    hiRezServerStatus = paladinsXBOX.getHiRezServerStatus() if platform.lower() == "xb" or platform.lower() == "xbox" or platform.lower() == "switch" else paladinsPS4.getHiRezServerStatus() if platform.lower() == "ps" or platform.lower() == "ps4" else paladinsPC.getHiRezServerStatus()
    patchInfo = paladinsXBOX.getPatchInfo() if platform.lower() == "xb" or platform.lower() == "xbox" or platform.lower() == "switch" else paladinsPS4.getPatchInfo() if platform.lower() == "ps" or platform.lower() == "ps4" else paladinsPC.getPatchInfo()
    return GAME_VERSION_STRINGS[language].format("Paladins", "PC" if platform.lower() == "pc" else "PS4" if platform.lower() == "ps" or platform.lower() == "ps4" else "Nintendo switch" if platform.lower() == "switch" else "Xbox One", "UP" if hiRezServerStatus.status else "DOWN", patchInfo.gameVersion, hiRezServerStatus.version)

@app.route('/api/stalk', methods=['GET'])
def getStalk():
    platform = request.args.get("platform") if request.args.get("platform") else "pc"
    player = request.args.get("player")
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"

    if not player:
        return PLAYER_NULL_STRINGS[language]
    playerStalkRequest = paladinsXBOX.getPlayerStatus(player) if platform.lower() == "xb" or platform.lower() == "xbox" or platform.lower() == "switch" else paladinsPS4.getPlayerStatus(player) if platform.lower() == "ps" or platform.lower() == "ps4" else paladinsPC.getPlayerStatus(player)
    return "{0} is {1}.".format(player.capitalize(), (playerStalkRequest.playerStatusString.replace("God", "Champion").replace("_", " ") if playerStalkRequest.playerStatus != 3 else "currently in a match (Match ID: {0})".format(playerStalkRequest.currentMatchID)))

@app.route('/api/lastmatch', methods=['GET'])
def getLastMatch():
    platform = request.args.get("platform") if request.args.get("platform") else "pc"
    player = request.args.get("player")
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"

    if not player:
        return PLAYER_NULL_STRINGS[language]
    lastMatchRequest = paladinsXBOX.getMatchHistory(player.lower()) if platform.lower() == "xb" or platform.lower() == "xbox" or platform.lower() == "switch" else paladinsPS4.getMatchHistory(player.lower()) if platform.lower() == "ps" or platform.lower() == "ps4" else paladinsPC.getMatchHistory(player.lower())
    kda = ((lastMatchRequest[0].assists / 2) + lastMatchRequest[0].kills) / lastMatchRequest[0].deaths if lastMatchRequest[0].deaths > 1 else 1
    kda = int(kda) if kda % 2 == 0 else round(kda, 2)
    return "{0} - Match ID: {1}, Duration: {10}m, Region: {11}: {2} ({3}/{4}/{5} - {6} KDA) Killing spree: {7}, Damage: {8}, Credits: {9} - {12} (Score: {13})".format(lastMatchRequest[0].mapGame, lastMatchRequest[0].matchID, lastMatchRequest[0].championName, lastMatchRequest[0].kills, lastMatchRequest[0].deaths, lastMatchRequest[0].assists, kda, lastMatchRequest[0].killingSpree, format(lastMatchRequest[0].damage, ',d'), format(lastMatchRequest[0].credits, ',d'), lastMatchRequest[0].matchMinutes, lastMatchRequest[0].matchRegion, lastMatchRequest[0].winStatus, "{0}/{1}".format(lastMatchRequest[0].team1Score, lastMatchRequest[0].team2Score) if lastMatchRequest[0].taskForce == 1 else "{0}/{1}".format(lastMatchRequest[0].team2Score, lastMatchRequest[0].team1Score))

@app.route('/api/currentmatch', methods=['GET'])
def getCurrentMatch():
    platform = request.args.get("platform") if request.args.get("platform") else "pc"
    player = request.args.get("player")
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"
    
    if not player:
        return PLAYER_NULL_STRINGS[language]
    playerStatusRequest = paladinsXBOX.getPlayerStatus(player) if platform.lower() == "xb" or platform.lower() == "xbox" or platform.lower() == "switch" else paladinsPS4.getPlayerStatus(player) if platform.lower() == "ps" or platform.lower() == "ps4" else paladinsPC.getPlayerStatus(player)
    if playerStatusRequest.playerStatus != 3:
        return PLAYER_NOT_MATCH_STRINGS[language]
    else:
        tim1 = ""
        tim1Aux = 1
        tim2Aux = 1
        tim2 = ""
        players = paladinsXBOX.getMatchPlayerDetails(playerStatusRequest.currentMatchID) if platform.lower() == "xb" or platform.lower() == "xbox" or platform.lower() == "switch" else paladinsPS4.getMatchPlayerDetails(playerStatusRequest.currentMatchID) if platform.lower() == "ps" or platform.lower() == "ps4" else paladinsPC.getMatchPlayerDetails(playerStatusRequest.currentMatchID)
        for player in players:
            rank = paladinsXBOX.getPlayer(player.playerName) if platform.lower() == "xb" or platform.lower() == "xbox" or platform.lower () == "switch" else paladinsPS4.getPlayer(player.playerName) if platform.lower() == "ps" or platform.lower() == "ps4" else paladinsPC.getPlayer(player.playerName)
            if player.taskForce == 1:
                tim1 += CURRENT_MATCH_PLAYER_STRINGS[language].format(player.playerName, player.championName, rank.playerElo, "{0}".format(", " if tim1Aux <= 4 else ""))
                tim1Aux += 1
            else:
                tim2 += CURRENT_MATCH_PLAYER_STRINGS[language].format(player.playerName, player.championName, rank.playerElo, "{0}".format(", " if tim2Aux <= 4 else ""))
                tim2Aux += 1
        return CURRENT_MATCH_STRINGS[language].format(tim1, tim2)

@app.route('/api/rank', methods=['GET'])
def getRank():
    platform = request.args.get("platform") if request.args.get("platform") else "pc"
    player = request.args.get("player")
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"

    if not player:
        return PLAYER_NULL_STRINGS[language]
    try:
        playerRank = paladinsXBOX.getPlayer(player) if platform.lower() == "xb" or platform.lower() == "xbox" or platform.lower() == "switch" else paladinsPS4.getPlayer(player) if platform.lower() == "ps" or platform.lower() == "ps4" else paladinsPC.getPlayer(player)
    except:
        return PLAYER_NOT_FOUND_STRINGS[language]
    return PLAYER_RANK_STRINGS[language].format(playerRank.playerName, playerRank.accountLevel, playerRank.rankedConquest.currentElo,
                                                "" if playerRank.rankedConquest.currentElo == Tier.Unranked else " ({0} TP{1})".format(format(playerRank.rankedConquest.currentTrumpPoints, ',d'),
                                                ", {0} on the leaderboard".format(playerRank.rankedConquest.leaderboardIndex) if playerRank.rankedConquest.leaderboardIndex > 0 else ""),
                                                format(playerRank.rankedConquest.wins, ',d'), format(playerRank.rankedConquest.losses, ',d'), " (Winrate Global: {0}% & Ranked: {1}%)".format(playerRank.getWinratio(), playerRank.rankedConquest.getWinratio()))

@app.route('/api/winrate', methods=['GET'])
def getWinrate():
    platform = request.args.get("platform") if request.args.get("platform") else "pc"
    player = request.args.get("player")
    champion = str(request.args.get("champion")).lower ().replace (" ", "").replace("'", "") if request.args.get("champion") else None
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"

    if not player:
        return PLAYER_NULL_STRINGS[language]
    if len(str(champion)) <= 0 or champion is None:
        try:
            playerGlobalWinrate = paladinsXBOX.getPlayer(player) if platform.lower() == "xb" or platform.lower() == "xbox" or platform.lower() == "switch" else paladinsPS4.getPlayer(player) if platform.lower() == "ps" or platform.lower() == "ps4" else paladinsPC.getPlayer(player)
            playerGlobalKDA = paladinsXBOX.getChampionRanks(player) if platform.lower() == "xb" or platform.lower() == "xbox" or platform.lower() == "switch" else paladinsPS4.getChampionRanks(player) if platform.lower() == "ps" or platform.lower() == "ps4" else paladinsPC.getChampionRanks(player)
            
            deaths = 0
            kills = 0
            assists = 0
            for i in range(0, len(playerGlobalKDA)):
                kills += playerGlobalKDA[i].kills
                deaths += playerGlobalKDA[i].deaths
                assists += playerGlobalKDA[i].assists
            kda = ((assists / 2) + kills) / deaths if deaths > 1 else 1
            return CHAMP_WINRATE_STRINGS[language].format(playerGlobalWinrate.playerName, playerGlobalWinrate.accountLevel,
                                                          format(playerGlobalWinrate.wins, ',d'), format(playerGlobalWinrate.losses, ',d'),
                                                          playerGlobalWinrate.getWinratio(), format(kills, ',d'), format(deaths, ',d'),
                                                          format(assists, ',d'), int(kda) if kda % 2 == 0 else round(kda, 2))
        except:
            return PLAYER_NOT_FOUND_STRINGS[language]
    else:
        try:
            playerChampionWinrate = paladinsXBOX.getChampionRanks(player) if platform.lower() == "xb" or platform.lower() == "xbox" or platform.lower() == "switch" else paladinsPS4.getChampionRanks(player) if platform.lower() == "ps" or platform.lower() == "ps4" else paladinsPC.getChampionRanks(player)
            
            for i in range(0, len(playerChampionWinrate)):
                if (playerChampionWinrate[i].godName.lower().replace(" ", "").replace("'", "") == champion):
                    return CHAMP_WINRATE_STRINGS[language].format(playerChampionWinrate[i].godName.replace("'", " "), playerChampionWinrate[i].wins,
                                                                  playerChampionWinrate[i].losses, playerChampionWinrate[i].getWinratio(),
                                                                  format(playerChampionWinrate[i].kills, ',d'), format(playerChampionWinrate[i].deaths, ',d'),
                                                                  format(playerChampionWinrate[i].assists, ',d'), playerChampionWinrate[i].getKDA(),
                                                                  playerChampionWinrate[i].godLevel)
        except:
            return PLAYER_NOT_FOUND_STRINGS[language]

if __name__ == "__main__":
    app.run(debug=False)
