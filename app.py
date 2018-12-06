# -*- coding: utf-8 -*-

from pyrez.api import *
from pyrez.enumerations import *
from langs import *

from decouple import config, Csv

from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

try:
    DEBUG = config("DEBUG", default=False, cast=bool)
    PYREZ_AUTH_ID = config("PYREZ_AUTH_ID")
    PYREZ_DEV_ID = config("PYREZ_DEV_ID")
except:
    DEBUG = os.environ["DEBUG"] if os.environ["DEBUG"] else False
    PYREZ_AUTH_ID = os.environ("PYREZ_AUTH_ID")
    PYREZ_DEV_ID = os.environ("PYREZ_DEV_ID")

paladinsPC = PaladinsAPI(devId=PYREZ_DEV_ID, authKey=PYREZ_AUTH_ID)
paladinsPS4 = PaladinsAPI(devId=PYREZ_DEV_ID, authKey=PYREZ_AUTH_ID, platform=Platform.PS4)
paladinsXBOX = PaladinsAPI(devId=PYREZ_DEV_ID, authKey=PYREZ_AUTH_ID, platform=Platform.XBOX)

@app.errorhandler(404)
def not_found_error(error):
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"
    return INTERNAL_ERROR_404_STRINGS[language], 200 #return render_template("404.html"), 404 #return INTERNAL_ERROR_404_STRINGS[language], 404

@app.errorhandler(500)
def internal_error(error):
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"
    return INTERNAL_ERROR_500_STRINGS[language], 200 #return render_template("500.html"), 500 #return INTERNAL_ERROR_500_STRINGS[language], 500

@app.route('/', methods=["GET"])
@app.route("/api", methods=["GET"])
@app.route("/index", methods=["GET"])
@app.route("/index.html", methods=["GET"])
def index():#ip = request.remote_addr
    return render_template("index.html") #redirect(url_for("index"))

@app.route("/api/version", methods=["GET"])
def getGameVersion():
    platform = str(request.args.get("platform")).lower() if request.args.get("platform") else "pc"
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"
    
    try:
        hiRezServerStatus = paladinsXBOX.getHiRezServerStatus() if platform.startswith("xb") or platform == "switch" else paladinsPS4.getHiRezServerStatus() if platform.startswith("ps") else paladinsPC.getHiRezServerStatus()
        patchInfo = paladinsXBOX.getPatchInfo() if platform.startswith("xb") or platform == "switch" else paladinsPS4.getPatchInfo() if platform.startswith("ps") else paladinsPC.getPatchInfo()
    except:
        return UNABLE_TO_CONNECT_STRINGS[language]
    return GAME_VERSION_STRINGS[language].format("Paladins", "PC" if platform == "pc" else "PS4" if platform.startswith("ps") else "Nintendo Switch" if platform == "switch" else "Xbox One",
                                                PALADINS_UP_STRINGS[language] if hiRezServerStatus.status else PALADINS_DOWN_STRINGS[language],
                                                patchInfo.gameVersion, hiRezServerStatus.version)

@app.route("/api/stalk", methods=["GET"])
def getStalk():
    platform = str(request.args.get("platform")).lower() if request.args.get("platform") else "pc"
    player = str(request.args.get("player")).lower()
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"

    if not player or str(player).lower() == "none" or str(player).lower() == "null":
        return PLAYER_NULL_STRINGS[language]
    try:
        #Se der Player not found, retornar só "Nonsocial is not found"?!
        getPlayerRequest = paladinsXBOX.getPlayer(player) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getPlayer(player) if platform.startswith("ps") else paladinsPC.getPlayer(player)
        #if not getPlayerRequest:
            #return PLAYER_NOT_FOUND_STRINGS[language]
        playerStalkRequest = paladinsXBOX.getPlayerStatus(getPlayerRequest.playerId) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getPlayerStatus(getPlayerRequest.playerId) if platform.startswith("ps") else paladinsPC.getPlayerStatus(getPlayerRequest.playerId)
    except:
        return PLAYER_NOT_FOUND_STRINGS[language]
    #return "{0} is {1}.".format(player.capitalize(), (playerStalkRequest.playerStatusString.replace("God", "Champion").replace("_", " ") if playerStalkRequest.playerStatus != 3 else CURRENTLY_MATCH_STRINGS[language].format(playerStalkRequest.currentMatchID)))
    return PLAYER_STALK_STRINGS[language].format(PLAYER_LEVEL_STRINGS[language].format(getPlayerRequest.playerName, getPlayerRequest.accountLevel),
                    playerStalkRequest.playerStatusString.replace("God", "Champion").replace("_", " ") if playerStalkRequest.playerStatus != 3 else CURRENTLY_MATCH_STRINGS[language].format(playerStalkRequest.currentMatchId),
                    getPlayerRequest.createdDatetime.strptime(HOUR_FORMAT_STRINGS[language]), getPlayerRequest.lastLoginDatetime.strptime(HOUR_FORMAT_STRINGS[language]), getPlayerRequest.hoursPlayed, getPlayerRequest.platform, getPlayerRequest.playerRegion)

@app.route("/api/lastmatch", methods=["GET"])
def getLastMatch():
    platform = str(request.args.get("platform")).lower() if request.args.get("platform") else "pc"
    player = str(request.args.get("player")).lower()
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"

    if not player or str(player).lower() == "none" or str(player).lower() == "null":
        return PLAYER_NULL_STRINGS[language]
    try:
        getPlayerRequest = paladinsXBOX.getPlayer(player) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getPlayer(player) if platform.startswith("ps") else paladinsPC.getPlayer(player)
        lastMatchRequest = paladinsXBOX.getMatchHistory(getPlayerRequest.playerId) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getMatchHistory(getPlayerRequest.playerId) if platform.startswith("ps") else paladinsPC.getMatchHistory(getPlayerRequest.playerId)
    except:
        return PLAYER_NOT_FOUND_STRINGS[language]
    kda = ((lastMatchRequest[0].assists / 2) + lastMatchRequest[0].kills) / lastMatchRequest[0].deaths if lastMatchRequest[0].deaths > 1 else 1
    kda = int(kda) if kda % 2 == 0 else round(kda, 2)
    return LAST_MATCH_STRINGS[language].format(lastMatchRequest[0].mapGame, lastMatchRequest[0].matchId, lastMatchRequest[0].championName,
                                            lastMatchRequest[0].kills, lastMatchRequest[0].deaths, lastMatchRequest[0].assists, kda, lastMatchRequest[0].killingSpree,
                                            format(lastMatchRequest[0].damage, ',d'), format(lastMatchRequest[0].credits, ',d'), lastMatchRequest[0].matchMinutes,
                                            lastMatchRequest[0].matchRegion, lastMatchRequest[0].winStatus, "{0}/{1}".format(lastMatchRequest[0].team1Score,
                                            lastMatchRequest[0].team2Score) if lastMatchRequest[0].taskForce == 1 else "{0}/{1}".format(lastMatchRequest[0].team2Score, lastMatchRequest[0].team1Score))

@app.route("/api/currentmatch", methods=["GET"])
def getCurrentMatch():
    platform = str(request.args.get("platform")).lower() if request.args.get("platform") else "pc"
    player = str(request.args.get("player")).lower()
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"

    if not player or str(player).lower() == "none" or str(player).lower() == "null":
        return PLAYER_NULL_STRINGS[language]
    try:
        getPlayerRequest = paladinsXBOX.getPlayer(player) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getPlayer(player) if platform.startswith("ps") else paladinsPC.getPlayer(player)
        playerStatusRequest = paladinsXBOX.getPlayerStatus(getPlayerRequest.playerId) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getPlayerStatus(getPlayerRequest.playerId) if platform.startswith("ps") else paladinsPC.getPlayerStatus(getPlayerRequest.playerId)
    except:
        return PLAYER_NOT_FOUND_STRINGS[language]
    if playerStatusRequest.playerStatus != 3:#Olhar o id da fila 424, 428, 445, 452
        return PLAYER_NOT_MATCH_STRINGS[language].format(player.capitalize())
        # Posso mostrar se o cara tá off, jogando outra coisa ou algo assim
    else:
        tim1 = ""
        tim1Aux = 1
        tim2Aux = 1
        tim2 = ""
        players = paladinsXBOX.getMatchPlayerDetails(playerStatusRequest.currentMatchId) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getMatchPlayerDetails(playerStatusRequest.currentMatchId) if platform.startswith("ps") else paladinsPC.getMatchPlayerDetails(playerStatusRequest.currentMatchId)
        if players:
            for player in players:
                if playerStatusRequest.currentMatchQueueId == 428:
                    rank = player.tier
                else:
                    if play.playerName.lower() == player.lower():
                        rank = getPlayerRequest.playerRank.value
                    else:#rank.playerRank.value
                        rank = paladinsXBOX.getPlayer(play.playerId) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getPlayer(play.playerId) if platform.startswith("ps") else paladinsPC.getPlayer(play.playerId)
                        rank = rank.playerRank.value
                if play.taskForce == 1:
                    tim1 += CURRENT_MATCH_PLAYER_STRINGS[language].format(play.playerName, play.championName, PLAYER_RANK_STRINGS[language][rank], "{0}".format(", " if tim1Aux <= 4 else ""))
                    tim1Aux += 1
                else:
                    tim2 += CURRENT_MATCH_PLAYER_STRINGS[language].format(play.playerName, play.championName, PLAYER_RANK_STRINGS[language][rank], "{0}".format(", " if tim2Aux <= 4 else ""))
                    tim2Aux += 1
            return CURRENT_MATCH_STRINGS[language].format(tim1, tim2)
        else:
            return PLAYER_NOT_MATCH_STRINGS[language]
    
@app.route("/api/rank", methods=["GET"])
def getRank():
    platform = str(request.args.get("platform")).lower() if request.args.get("platform") else "pc"
    player = str(request.args.get("player")).lower()
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"

    if not player or str(player).lower() == "none" or str(player).lower() == "null":
        return PLAYER_NULL_STRINGS[language]
    try:
        playerRank = paladinsXBOX.getPlayer(player) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getPlayer(player) if platform.startswith("ps") else paladinsPC.getPlayer(player)
    except:
        return PLAYER_NOT_FOUND_STRINGS[language]
    return PLAYER_GET_RANK_STRINGS[language].format(PLAYER_LEVEL_STRINGS[language].format(playerRank.playerName, playerRank.accountLevel),
                                                PLAYER_RANK_STRINGS[language][playerRank.rankedConquest.currentRank.value] if playerRank.rankedConquest.currentRank != Tier.Unranked else UNRANKED_STRINGS[language] if playerRank.rankedConquest.wins + playerRank.rankedConquest.losses == 0 else QUALIFYING_STRINGS[language],
                                                "" if playerRank.rankedConquest.currentRank == Tier.Unranked else " ({0} TP{1})".format(format(playerRank.rankedConquest.currentTrumpPoints, ',d'), ON_LEADERBOARD_STRINGS[language].format(playerRank.rankedConquest.leaderboardIndex) if playerRank.rankedConquest.leaderboardIndex > 0 else ""),
                                                "" if playerRank.rankedConquest.currentRank == Tier.Unranked and playerRank.rankedConquest.wins + playerRank.rankedConquest.losses == 0 else WINS_LOSSES_STRINGS[language].format(format(playerRank.rankedConquest.wins, ',d'), format(playerRank.rankedConquest.losses, ',d')),
                                                " (Winrate Global: {0}%{1})".format (playerRank.getWinratio(), "" if playerRank.rankedConquest.wins + playerRank.rankedConquest.losses == 0 else " & Ranked: {0}%".format(playerRank.rankedConquest.getWinratio())))

@app.route("/api/winrate", methods=["GET"])
def getWinrate():
    platform = str(request.args.get("platform")).lower() if request.args.get("platform") else "pc"
    player = str(request.args.get("player")).lower()
    champion = str(request.args.get("champion")).lower().replace(" ", "").replace("'", "") if request.args.get("champion") and str(request.args.get("champion")).lower() != "null" else None
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"

    if not player or str(player).lower() == "none" or str(player).lower() == "null":
        return PLAYER_NULL_STRINGS[language]
    if champion is None:
        try:
            playerGlobalWinrate = paladinsXBOX.getPlayer(player) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getPlayer(player) if platform.startswith("ps") else paladinsPC.getPlayer(player)
            playerGlobalKDA = paladinsXBOX.getChampionRanks(playerGlobalWinrate.playerId) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getChampionRanks(playerGlobalWinrate.playerId) if platform.startswith("ps") else paladinsPC.getChampionRanks(playerGlobalWinrate.playerId)
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
        return CHAMP_WINRATE_STRINGS[language].format(PLAYER_LEVEL_STRINGS[language].format(playerGlobalWinrate.playerName, playerGlobalWinrate.accountLevel), playerGlobalWinrate.wins,
                                                      playerGlobalWinrate.losses, format(kills, ',d'), format(deaths, ',d'),
                                                      format(assists, ',d'), int(kda) if kda % 2 == 0 else round(kda, 2), playerGlobalWinrate.getWinratio())
    else:
        try:
            playerGlobalWinrate = paladinsXBOX.getPlayer(player) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getPlayer(player) if platform.startswith("ps") else paladinsPC.getPlayer(player)
            playerChampionWinrate = paladinsXBOX.getChampionRanks(playerGlobalWinrate.playerId) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getChampionRanks(playerGlobalWinrate.playerId) if platform.startswith("ps") else paladinsPC.getChampionRanks(playerGlobalWinrate.playerId)
        except:
            return PLAYER_NOT_FOUND_STRINGS[language]
        for i in range(0, len(playerChampionWinrate)):
            if playerChampionWinrate[i].godName.lower().replace(" ", "").replace("'", "") == champion:
                return CHAMP_WINRATE_STRINGS[language].format(PLAYER_LEVEL_STRINGS[language].format(playerChampionWinrate[i].godName.replace("'", " "), playerChampionWinrate[i].godLevel), playerChampionWinrate[i].wins,
                                                              playerChampionWinrate[i].losses, format(playerChampionWinrate[i].kills, ',d'), format(playerChampionWinrate[i].deaths, ',d'),
                                                              format(playerChampionWinrate[i].assists, ',d'), playerChampionWinrate[i].getKDA(), playerChampionWinrate[i].getWinratio())

if __name__ == "__main__":
    app.run(debug=DEBUG)
