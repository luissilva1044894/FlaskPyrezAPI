from pyrez.api import *
from pyrez.enumerations import *
from langs import *

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

@app.route('/api/version', methods=['GET'])
def getGameVersion():
    platform = str(request.args.get("platform")).lower() if request.args.get("platform") else "pc"
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"
    
    hiRezServerStatus = paladinsXBOX.getHiRezServerStatus() if platform.startswith("xb") or platform == "switch" else paladinsPS4.getHiRezServerStatus() if platform.startswith("ps") else paladinsPC.getHiRezServerStatus()
    patchInfo = paladinsXBOX.getPatchInfo() if platform.startswith("xb") or platform == "switch" else paladinsPS4.getPatchInfo() if platform.startswith("ps") else paladinsPC.getPatchInfo()
    return GAME_VERSION_STRINGS[language].format("Paladins", "PC" if platform == "pc" else "PS4" if platform.startswith("ps") else "Nintendo Switch" if platform == "switch" else "Xbox One",
                                                PALADINS_UP_STRINGS[language] if hiRezServerStatus.status else PALADINS_DOWN_STRINGS[language],
                                                patchInfo.gameVersion, hiRezServerStatus.version)

@app.route('/api/stalk', methods=['GET'])
def getStalk():
    platform = str(request.args.get("platform")).lower() if request.args.get("platform") else "pc"
    player = str(request.args.get("player")).lower()
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"

    if not player:
        return PLAYER_NULL_STRINGS[language]
    try:
        playerStalkRequest = paladinsXBOX.getPlayerStatus(player) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getPlayerStatus(player) if platform.startswith("ps") else paladinsPC.getPlayerStatus(player)
    except:
        return PLAYER_NOT_FOUND_STRINGS[language]
    return "{0} is {1}.".format(player.capitalize(), (playerStalkRequest.playerStatusString.replace("God", "Champion").replace("_", " ") if playerStalkRequest.playerStatus != 3 else CURRENTLY_MATCH_STRINGS[language].format(playerStalkRequest.currentMatchID)))

@app.route('/api/lastmatch', methods=['GET'])
def getLastMatch():
    platform = str(request.args.get("platform")).lower() if request.args.get("platform") else "pc"
    player = str(request.args.get("player")).lower()
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"

    if not player:
        return PLAYER_NULL_STRINGS[language]
    try:
        lastMatchRequest = paladinsXBOX.getMatchHistory(player) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getMatchHistory(player) if platform.startswith("ps") else paladinsPC.getMatchHistory(player)
    except:
        return PLAYER_NOT_FOUND_STRINGS[language]
    kda = ((lastMatchRequest[0].assists / 2) + lastMatchRequest[0].kills) / lastMatchRequest[0].deaths if lastMatchRequest[0].deaths > 1 else 1
    kda = int(kda) if kda % 2 == 0 else round(kda, 2)
    return LAST_MATCH_STRINGS[language].format(lastMatchRequest[0].mapGame, lastMatchRequest[0].matchID, lastMatchRequest[0].championName.capitalize(),
                                            lastMatchRequest[0].kills, lastMatchRequest[0].deaths, lastMatchRequest[0].assists, kda, lastMatchRequest[0].killingSpree,
                                            format(lastMatchRequest[0].damage, ',d'), format(lastMatchRequest[0].credits, ',d'), lastMatchRequest[0].matchMinutes,
                                            lastMatchRequest[0].matchRegion, lastMatchRequest[0].winStatus, "{0}/{1}".format(lastMatchRequest[0].team1Score,
                                            lastMatchRequest[0].team2Score) if lastMatchRequest[0].taskForce == 1 else "{0}/{1}".format(lastMatchRequest[0].team2Score, lastMatchRequest[0].team1Score))

@app.route('/api/currentmatch', methods=['GET'])
def getCurrentMatch():
    platform = str(request.args.get("platform")).lower() if request.args.get("platform") else "pc"
    player = str(request.args.get("player")).lower()
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"
    
    if not player:
        return PLAYER_NULL_STRINGS[language]
    try:
        playerStatusRequest = paladinsXBOX.getPlayerStatus(player) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getPlayerStatus(player) if platform.startswith("ps") else paladinsPC.getPlayerStatus(player)
    except:
        return PLAYER_NOT_FOUND_STRINGS[language]
    if playerStatusRequest.playerStatus != 3:
        return PLAYER_NOT_MATCH_STRINGS[language]
    else:
        tim1 = ""
        tim1Aux = 1
        tim2Aux = 1
        tim2 = ""
        players = paladinsXBOX.getMatchPlayerDetails(playerStatusRequest.currentMatchID) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getMatchPlayerDetails(playerStatusRequest.currentMatchID) if platform.startswith("ps") else paladinsPC.getMatchPlayerDetails(playerStatusRequest.currentMatchID)
        for player in players:
            rank = paladinsXBOX.getPlayer(player.playerId) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getPlayer(player.playerId) if platform.startswith("ps") else paladinsPC.getPlayer(player.playerId)
            if player.taskForce == 1:
                tim1 += CURRENT_MATCH_PLAYER_STRINGS[language].format(player.playerName.capitalize(), player.championName.capitalize(), PLAYER_RANK_STRINGS[language][rank.playerElo.value], "{0}".format(", " if tim1Aux <= 4 else ""))
                tim1Aux += 1
            else:
                tim2 += CURRENT_MATCH_PLAYER_STRINGS[language].format(player.playerName.capitalize(), player.championName.capitalize(), PLAYER_RANK_STRINGS[language][rank.playerElo.value], "{0}".format(", " if tim2Aux <= 4 else ""))
                tim2Aux += 1
        return CURRENT_MATCH_STRINGS[language].format(tim1, tim2)
    
@app.route('/api/rank', methods=['GET'])
def getRank():
    platform = str(request.args.get("platform")).lower() if request.args.get("platform") else "pc"
    player = str(request.args.get("player")).lower()
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"

    if not player:
        return PLAYER_NULL_STRINGS[language]
    try:
        playerRank = paladinsXBOX.getPlayer(player) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getPlayer(player) if platform.startswith("ps") else paladinsPC.getPlayer(player)
    except:
        return PLAYER_NOT_FOUND_STRINGS[language]
    return PLAYER_GET_RANK_STRINGS[language].format(playerRank.playerName.capitalize(), playerRank.accountLevel, PLAYER_RANK_STRINGS[language][playerRank.rankedConquest.currentElo.value],
                                                "" if playerRank.rankedConquest.currentElo == Tier.Unranked else " ({0} TP{1})".format(format(playerRank.rankedConquest.currentTrumpPoints, ',d'),
                                                ON_LEADERBOARD_STRINGS[language].format(playerRank.rankedConquest.leaderboardIndex) if playerRank.rankedConquest.leaderboardIndex > 0 else ""),
                                                format(playerRank.rankedConquest.wins, ',d'), format(playerRank.rankedConquest.losses, ',d'), " (Winrate Global: {0}% & Ranked: {1}%)".format(playerRank.getWinratio(), playerRank.rankedConquest.getWinratio()))

@app.route('/api/winrate', methods=['GET'])
def getWinrate():
    platform = str(request.args.get("platform")).lower() if request.args.get("platform") else "pc"
    player = str(request.args.get("player")).lower()
    champion = str(request.args.get("champion")).lower().replace(" ", "").replace("'", "") if request.args.get("champion") and str(request.args.get("champion")).lower() != "null" else None
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"

    if not player:
        return PLAYER_NULL_STRINGS[language]
    if champion is None:
        try:
            playerGlobalWinrate = paladinsXBOX.getPlayer(player) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getPlayer(player) if platform.startswith("ps") else paladinsPC.getPlayer(player)
            playerGlobalKDA = paladinsXBOX.getChampionRanks(player) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getChampionRanks(player) if platform.startswith("ps") else paladinsPC.getChampionRanks(player)
        except:
            return PLAYER_NOT_FOUND_STRINGS[language]
        deaths = 0
        kills = 0
        assists = 0
        for i in range(0, len(playerGlobalKDA)):
            kills += playerGlobalKDA[i].kills
            deaths += playerGlobalKDA[i].deaths
            assists += playerGlobalKDA[i].assists
        kda = ((assists / 2) + kills) / deaths if deaths > 1 else 1
        return CHAMP_WINRATE_STRINGS[language].format(playerGlobalWinrate.playerName.capitalize(), playerGlobalWinrate.accountLevel, playerGlobalWinrate.wins,
                                                      playerGlobalWinrate.losses, format(kills, ',d'), format(deaths, ',d'),
                                                      format(assists, ',d'), int(kda) if kda % 2 == 0 else round(kda, 2), playerGlobalWinrate.getWinratio())
    else:
        try:
            playerChampionWinrate = paladinsXBOX.getChampionRanks(player) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getChampionRanks(player) if platform.startswith("ps") else paladinsPC.getChampionRanks(player)
        except:
            return PLAYER_NOT_FOUND_STRINGS[language]
        for i in range(0, len(playerChampionWinrate)):
            if playerChampionWinrate[i].godName.lower().replace(" ", "").replace("'", "") == champion:
                return CHAMP_WINRATE_STRINGS[language].format(playerChampionWinrate[i].godName.replace("'", " ").capitalize(), playerChampionWinrate[i].godLevel, playerChampionWinrate[i].wins,
                                                              playerChampionWinrate[i].losses, format(playerChampionWinrate[i].kills, ',d'), format(playerChampionWinrate[i].deaths, ',d'),
                                                              format(playerChampionWinrate[i].assists, ',d'), playerChampionWinrate[i].getKDA(), playerChampionWinrate[i].getWinratio())

if __name__ == "__main__":
    app.run(debug=False)


