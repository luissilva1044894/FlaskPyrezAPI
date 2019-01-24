# -*- coding: utf-8 -*-

from pyrez.api import *
from pyrez.enumerations import *
from langs import *

from datetime import datetime

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

paladinsAPI = PaladinsAPI(devId=PYREZ_DEV_ID, authKey=PYREZ_AUTH_ID)
paladinsPC = PaladinsAPI(devId=PYREZ_DEV_ID, authKey=PYREZ_AUTH_ID)
paladinsPS4 = PaladinsAPI(devId=PYREZ_DEV_ID, authKey=PYREZ_AUTH_ID, platform=Platform.PS4)
paladinsXBOX = PaladinsAPI(devId=PYREZ_DEV_ID, authKey=PYREZ_AUTH_ID, platform=Platform.XBOX)

@app.errorhandler(404)
def not_found_error(error=None):
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"
    return INTERNAL_ERROR_404_STRINGS[language], 200 #return render_template("404.html"), 404 #return INTERNAL_ERROR_404_STRINGS[language], 404

@app.errorhandler(500)
def internal_error(error=None):
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"
    return INTERNAL_ERROR_500_STRINGS[language], 200 #return render_template("500.html"), 500 #return INTERNAL_ERROR_500_STRINGS[language], 500

@app.route('/', methods=["GET"])
@app.route("/api", methods=["GET"])
@app.route("/index", methods=["GET"])
@app.route("/index.html", methods=["GET"])
def index():#ip = request.remote_addr
    return render_template("index.html") #redirect(url_for("index"))

def getPlayerId(playerName, platform = "pc"):
    if platform.lower() == "pc":
        return paladinsAPI.getPlayerIdByName(playerName)[0].get("player_id")
    else:
        portalId = 10 if platform.startswith("xb") else 22 if platform.startswith("sw") else 22
        return paladinsAPI.getPlayerIdsByGamerTag(portalId, playerName)[0].get("player_id")

def getLastSeen(lastSeen, language = "en"):
    now = datetime.utcnow()
    delta = now - lastSeen
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    fmt = "{d}d" if days else "{h}h, {m}m" if hours else "{m}m, {s}s"
    return fmt.format(d=days, h=hours, m=minutes, s=seconds)

@app.route("/api/version", methods=["GET"])
def getGameVersion():
    platform = str(request.args.get("platform")).lower() if request.args.get("platform") and request.args.get("platform").lower() != "null" else "pc"
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"
    
    try:
        hiRezServerStatus = paladinsXBOX.getHiRezServerStatus() if platform.startswith("xb") or platform == "switch" else paladinsPS4.getHiRezServerStatus() if platform.startswith("ps") else paladinsPC.getHiRezServerStatus()
        patchInfo = paladinsXBOX.getPatchInfo() if platform.startswith("xb") or platform == "switch" else paladinsPS4.getPatchInfo() if platform.startswith("ps") else paladinsPC.getPatchInfo()
    except:
        return UNABLE_TO_CONNECT_STRINGS[language]
    return GAME_VERSION_STRINGS[language].format("Paladins", "PC" if platform == "pc" else "PS4" if platform.startswith("ps") else "Nintendo Switch" if platform == "switch" else "Xbox One",
                        PALADINS_UP_STRINGS[language] if hiRezServerStatus.status else PALADINS_DOWN_STRINGS[language],
                        patchInfo.gameVersion, hiRezServerStatus.version)

#Need to fix
@app.route("/api/stalk", methods=["GET"])
def getStalk():
    platform = str(request.args.get("platform")).lower() if request.args.get("platform") and request.args.get("platform").lower() != "null" else "pc"
    player = str(request.args.get("player")).lower()
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"

    if not player or str(player).lower() == "none" or str(player).lower() == "null":
        return PLAYER_NULL_STRINGS[language]
    try:
        #Se der Player not found, retornar só "Nonsocial is not found"?!
        #getPlayerRequest = paladinsXBOX.getPlayer(player) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getPlayer(player) if platform.startswith("ps") else paladinsPC.getPlayer(player)
        getPlayerRequest = paladinsAPI.getPlayer(getPlayerId(player, platform))
        if not getPlayerRequest:
            return PLAYER_NOT_FOUND_STRINGS[language]
        playerStalkRequest = paladinsXBOX.getPlayerStatus(getPlayerRequest.playerId) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getPlayerStatus(getPlayerRequest.playerId) if platform.startswith("ps") else paladinsPC.getPlayerStatus(getPlayerRequest.playerId)
    except:
        return INTERNAL_ERROR_500_STRINGS[language]
    return PLAYER_STALK_STRINGS[language].format(PLAYER_LEVEL_STRINGS[language].format(getPlayerRequest.playerName, getPlayerRequest.accountLevel),
                        playerStalkRequest.playerStatusString.replace("God", "Champion").replace("_", " ") if playerStalkRequest.playerStatus != 3 else CURRENTLY_MATCH_STRINGS[language].format(QUEUE_IDS_STRINGS[playerStalkRequest.currentMatchQueueId], playerStalkRequest.currentMatchId),
                        getPlayerRequest.createdDatetime.strftime(HOUR_FORMAT_STRINGS[language]), getLastSeen(getPlayerRequest.lastLoginDatetime, language), format(getPlayerRequest.hoursPlayed, ',d'), getPlayerRequest.platform, getPlayerRequest.playerRegion)

@app.route("/api/lastmatch", methods=["GET"])
def getLastMatch():
    platform = str(request.args.get("platform")).lower() if request.args.get("platform") and request.args.get("platform").lower() != "null" else "pc"
    player = str(request.args.get("player")).lower()
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"

    if not player or str(player).lower() == "none" or str(player).lower() == "null":
        return PLAYER_NULL_STRINGS[language]
    try:
        #getPlayerRequest = paladinsXBOX.getPlayer(player) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getPlayer(player) if platform.startswith("ps") else paladinsPC.getPlayer(player)
        getPlayerRequest = paladinsAPI.getPlayer(getPlayerId(player, platform))
        if not getPlayerRequest:
            return PLAYER_NOT_FOUND_STRINGS[language]
        lastMatchRequest = paladinsXBOX.getMatchHistory(getPlayerRequest.playerId) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getMatchHistory(getPlayerRequest.playerId) if platform.startswith("ps") else paladinsPC.getMatchHistory(getPlayerRequest.playerId)
    except:
        return INTERNAL_ERROR_500_STRINGS[language]
    kda = ((lastMatchRequest[0].assists / 2) + lastMatchRequest[0].kills) / lastMatchRequest[0].deaths if lastMatchRequest[0].deaths > 1 else 1
    kda = int(kda) if kda % 2 == 0 else round(kda, 2)
    return LAST_MATCH_STRINGS[language].format(lastMatchRequest[0].mapGame, lastMatchRequest[0].matchId, lastMatchRequest[0].championName,
                        lastMatchRequest[0].kills, lastMatchRequest[0].deaths, lastMatchRequest[0].assists, kda, lastMatchRequest[0].killingSpree,
                        format(lastMatchRequest[0].damage, ',d'), format(lastMatchRequest[0].credits, ',d'), lastMatchRequest[0].matchMinutes,
                        lastMatchRequest[0].matchRegion, lastMatchRequest[0].winStatus, "{0}/{1}".format(lastMatchRequest[0].team1Score,
                        lastMatchRequest[0].team2Score) if lastMatchRequest[0].taskForce == 1 else "{0}/{1}".format(lastMatchRequest[0].team2Score, lastMatchRequest[0].team1Score))

@app.route("/api/currentmatch", methods=["GET"])
def getCurrentMatch():
    platform = str(request.args.get("platform")).lower() if request.args.get("platform") and request.args.get("platform").lower() != "null" else "pc"
    player = str(request.args.get("player")).lower()
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"

    if not player or str(player).lower() == "none" or str(player).lower() == "null":
        return PLAYER_NULL_STRINGS[language]
    try:
        #getPlayerRequest = paladinsXBOX.getPlayer(player) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getPlayer(player) if platform.startswith("ps") else paladinsPC.getPlayer(player)
        getPlayerRequest = paladinsAPI.getPlayer(getPlayerId(player, platform))
        if not getPlayerRequest:
            return PLAYER_NOT_FOUND_STRINGS[language]
        playerStatusRequest = paladinsXBOX.getPlayerStatus(getPlayerRequest.playerId) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getPlayerStatus(getPlayerRequest.playerId) if platform.startswith("ps") else paladinsPC.getPlayerStatus(getPlayerRequest.playerId)
    except:
        return INTERNAL_ERROR_500_STRINGS[language]
    if playerStatusRequest.playerStatus != 3:
        return PLAYER_NOT_MATCH_STRINGS[language].format(getPlayerRequest.playerName)
        # Posso mostrar se o cara tá off, jogando outra coisa ou algo assim
    else:
        #if playerStatusRequest.currentMatchQueueId != 424 or playerStatusRequest.currentMatchQueueId != 428 or playerStatusRequest.currentMatchQueueId != 445 or playerStatusRequest.currentMatchQueueId != 452:#Olhar o id da fila 424, 428, 445, 452
            #return ""
        tim1 = ""
        tim1Aux = 1
        tim2Aux = 1
        tim2 = ""
        players = paladinsXBOX.getMatchPlayerDetails(playerStatusRequest.currentMatchId) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getMatchPlayerDetails(playerStatusRequest.currentMatchId) if platform.startswith("ps") else paladinsPC.getMatchPlayerDetails(playerStatusRequest.currentMatchId)
        if players:
            for play in players:
                if playerStatusRequest.currentMatchQueueId == 428 or playerStatusRequest.currentMatchQueueId == 486:
                    rank = PLAYER_RANK_STRINGS[language][play.tier]# if play.tier != 0 else UNRANKED_STRINGS[language] if play.wins + play.losses == 0 else QUALIFYING_STRINGS[language]
                else:
                    if play.playerName.lower() == player.lower():
                        rank = PLAYER_RANK_STRINGS[language][getPlayerRequest.rankedKeyboard.value if getPlayerRequest.rankedController.wins + getPlayerRequest.rankedController.losses == 0 else getPlayerRequest.rankedController.value]
                    else:
                        getPlayer = paladinsXBOX.getPlayer(play.playerId) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getPlayer(play.playerId) if platform.startswith("ps") else paladinsPC.getPlayer(play.playerId)
                        #rank = PLAYER_RANK_STRINGS[language][getPlayer.rankedKeyboard.value if getPlayer.rankedController.wins + getPlayer.rankedController.losses == 0 else getPlayer.rankedController.value]
                        rank = PLAYER_RANK_STRINGS[language][getPlayerRequest.rankedKeyboard.value if getPlayerRequest.rankedController.wins + getPlayerRequest.rankedController.losses == 0 else getPlayerRequest.rankedController.value]
                if play.taskForce == 1:
                    tim1 += CURRENT_MATCH_PLAYER_STRINGS[language].format(play.playerName, play.championName, rank, "{0}".format(", " if tim1Aux <= 4 else ""))
                    tim1Aux += 1
                else:
                    tim2 += CURRENT_MATCH_PLAYER_STRINGS[language].format(play.playerName, play.championName, rank, "{0}".format(", " if tim2Aux <= 4 else ""))
                    tim2Aux += 1
            return CURRENT_MATCH_STRINGS[language].format(QUEUE_IDS_STRINGS[playerStatusRequest.currentMatchQueueId], tim1, tim2)
        else:
            return PLAYER_NOT_MATCH_STRINGS[language]

@app.route("/api/rank", methods=["GET"])
def getRank():
    platform = str(request.args.get("platform")).lower() if request.args.get("platform") and request.args.get("platform").lower() != "null" else "pc"
    player = str(request.args.get("player")).lower()
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"

    if not player or str(player).lower() == "none" or str(player).lower() == "null":
        return PLAYER_NULL_STRINGS[language]
    try:
        #getPlayerRequest = paladinsXBOX.getPlayer(player) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getPlayer(player) if platform.startswith("ps") else paladinsPC.getPlayer(player)
        getPlayerRequest = paladinsAPI.getPlayer(getPlayerId(player, platform))
        if not getPlayerRequest:
            return PLAYER_NOT_FOUND_STRINGS[language]
    except:
        return INTERNAL_ERROR_500_STRINGS[language]
    # Olhar isso dos 2 ranks '-'
    if getPlayerRequest.rankedController.wins + getPlayerRequest.rankedController.losses == 0 and getPlayerRequest.rankedKeyboard.wins + getPlayerRequest.rankedKeyboard.losses >= 1:
        return PLAYER_GET_RANK_STRINGS[language].format(PLAYER_LEVEL_STRINGS[language].format(getPlayerRequest.playerName, getPlayerRequest.accountLevel),
                                PLAYER_RANK_STRINGS[language][getPlayerRequest.rankedKeyboard.currentRank.value] if getPlayerRequest.rankedKeyboard.currentRank != Tier.Unranked else UNRANKED_STRINGS[language] if getPlayerRequest.rankedKeyboard.wins + getPlayerRequest.rankedKeyboard.losses == 0 else QUALIFYING_STRINGS[language],
                                "" if getPlayerRequest.rankedKeyboard.currentRank == Tier.Unranked else " ({0} TP{1})".format(format(getPlayerRequest.rankedKeyboard.currentTrumpPoints, ',d'), ON_LEADERBOARD_STRINGS[language].format(getPlayerRequest.rankedKeyboard.leaderboardIndex) if getPlayerRequest.rankedKeyboard.leaderboardIndex > 0 else ""),
                                "" if getPlayerRequest.rankedKeyboard.currentRank == Tier.Unranked and getPlayerRequest.rankedKeyboard.wins + getPlayerRequest.rankedKeyboard.losses == 0 else WINS_LOSSES_STRINGS[language].format(format(getPlayerRequest.rankedKeyboard.wins, ',d'), format(getPlayerRequest.rankedKeyboard.losses, ',d')),
                                " (Winrate Global: {0}%{1})".format (getPlayerRequest.getWinratio(), "" if getPlayerRequest.rankedKeyboard.wins + getPlayerRequest.rankedKeyboard.losses == 0 else " & Ranked: {0}%".format(getPlayerRequest.rankedKeyboard.getWinratio())))
    else:
        return PLAYER_GET_RANK_STRINGS[language].format(PLAYER_LEVEL_STRINGS[language].format(getPlayerRequest.playerName, getPlayerRequest.accountLevel),
                                PLAYER_RANK_STRINGS[language][getPlayerRequest.rankedController.currentRank.value] if getPlayerRequest.rankedController.currentRank != Tier.Unranked else UNRANKED_STRINGS[language] if getPlayerRequest.rankedController.wins + getPlayerRequest.rankedController.losses == 0 else QUALIFYING_STRINGS[language],
                                "" if getPlayerRequest.rankedController.currentRank == Tier.Unranked else " ({0} TP{1})".format(format(getPlayerRequest.rankedController.currentTrumpPoints, ',d'), ON_LEADERBOARD_STRINGS[language].format(getPlayerRequest.rankedController.leaderboardIndex) if getPlayerRequest.rankedController.leaderboardIndex > 0 else ""),
                                "" if getPlayerRequest.rankedController.currentRank == Tier.Unranked and getPlayerRequest.rankedController.wins + getPlayerRequest.rankedController.losses == 0 else WINS_LOSSES_STRINGS[language].format(format(getPlayerRequest.rankedController.wins, ',d'), format(getPlayerRequest.rankedController.losses, ',d')),
                                " (Winrate Global: {0}%{1})".format (getPlayerRequest.getWinratio(), "" if getPlayerRequest.rankedController.wins + getPlayerRequest.rankedController.losses == 0 else " & Ranked: {0}%".format(getPlayerRequest.rankedController.getWinratio())))

@app.route("/api/kda", methods=["GET"])
@app.route("/api/winrate", methods=["GET"])
def getWinrate():
    platform = str(request.args.get("platform")).lower() if request.args.get("platform") and request.args.get("platform").lower() != "null" else "pc"
    player = str(request.args.get("player")).lower()
    champion = str(request.args.get("champion")).lower().replace(" ", "").replace("'", "") if request.args.get("champion") and str(request.args.get("champion")).lower() != "null" else None
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"

    if not player or str(player).lower() == "none" or str(player).lower() == "null":
        return PLAYER_NULL_STRINGS[language]
    try:
        #getPlayerRequest = paladinsXBOX.getPlayer(player) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getPlayer(player) if platform.startswith("ps") else paladinsPC.getPlayer(player)
        getPlayerRequest = paladinsAPI.getPlayer(getPlayerId(player, platform))
        if not getPlayerRequest:
            return PLAYER_NOT_FOUND_STRINGS[language]
        #playerGlobalKDA = paladinsXBOX.getChampionRanks(getPlayerRequest.playerId) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getChampionRanks(getPlayerRequest.playerId) if platform.startswith("ps") else paladinsPC.getChampionRanks(getPlayerRequest.playerId)
        playerGlobalKDA = paladinsAPI.getChampionRanks(getPlayerRequest.playerId)
    except:
        return INTERNAL_ERROR_500_STRINGS[language]
    if champion:
        for i in range(0, len(playerGlobalKDA)):
            if playerGlobalKDA[i].godName.lower().replace(" ", "").replace("'", "") == champion:
                return CHAMP_WINRATE_STRINGS[language].format(PLAYER_LEVEL_STRINGS[language].format(playerGlobalKDA[i].godName.replace("'", " "), playerGlobalKDA[i].godLevel), playerGlobalKDA[i].wins,
                        playerGlobalKDA[i].losses, format(playerGlobalKDA[i].kills, ',d'), format(playerGlobalKDA[i].deaths, ',d'),
                        format(playerGlobalKDA[i].assists, ',d'), playerGlobalKDA[i].getKDA(), playerGlobalKDA[i].getWinratio())
    else:
        deaths = 0
        kills = 0
        assists = 0
        for i in range(0, len(playerGlobalKDA)):
            kills += playerGlobalKDA[i].kills
            deaths += playerGlobalKDA[i].deaths
            assists += playerGlobalKDA[i].assists
        kda = ((assists / 2) + kills) / deaths if deaths > 1 else 1
        return CHAMP_WINRATE_STRINGS[language].format(PLAYER_LEVEL_STRINGS[language].format(getPlayerRequest.playerName, getPlayerRequest.accountLevel), getPlayerRequest.wins,
                        getPlayerRequest.losses, format(kills, ',d'), format(deaths, ',d'),
                        format(assists, ',d'), int(kda) if kda % 2 == 0 else round(kda, 2), getPlayerRequest.getWinratio())

if __name__ == "__main__":
    app.run(debug=DEBUG)