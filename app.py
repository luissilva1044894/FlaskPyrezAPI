# -*- coding: utf-8 -*-

from pyrez.api import *
from pyrez.enumerations import *
from langs import *

from datetime import datetime

from decouple import config, Csv

from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

from enum import Enum
class LanguagesSupported(Enum):
    English = "en"
    Portuguese = "pt"
    Spanish = "es"
class PlatformsSupported(Enum):
    PC = "pc"
    Xbox = "10"
    PS4 = "9"
    Switch = "22"

try:
    DEBUG = config("DEBUG", default=False, cast=bool)
    PYREZ_AUTH_ID = config("PYREZ_AUTH_ID")
    PYREZ_DEV_ID = config("PYREZ_DEV_ID")
except:
    DEBUG = os.environ["DEBUG"] if os.environ["DEBUG"] else False
    PYREZ_AUTH_ID = os.environ("PYREZ_AUTH_ID")
    PYREZ_DEV_ID = os.environ("PYREZ_DEV_ID")

paladinsAPI = PaladinsAPI(devId=PYREZ_DEV_ID, authKey=PYREZ_AUTH_ID)

@app.errorhandler(404)
def not_found_error(error=None):
    language = getLanguage(request.args)
    return INTERNAL_ERROR_404_STRINGS[language], 200 #return render_template("404.html"), 404 #return INTERNAL_ERROR_404_STRINGS[language], 404

@app.errorhandler(500)
def internal_error(error=None):
    language = getLanguage(request.args)
    return INTERNAL_ERROR_500_STRINGS[language], 200 #return render_template("500.html"), 500 #return INTERNAL_ERROR_500_STRINGS[language], 500

@app.route('/', methods=["GET"])
@app.route("/api", methods=["GET"])
@app.route("/index", methods=["GET"])
@app.route("/index.html", methods=["GET"])
def index():#ip = request.remote_addr
    return render_template("index.html") #redirect(url_for("index"))

def formatDecimal(data, form = ",d"):
    return format(data, form) if data else 0

def getLanguage(requestArgs):
    aux = str(requestArgs.get("language")).lower() if requestArgs.get("language") else LanguagesSupported.English.value
    try:
        return LanguagesSupported(aux).value
    except ValueError:
        return LanguagesSupported.English.value

def getPlatform(requestArgs):
    aux = str(requestArgs.get("platform")).lower() if requestArgs.get("platform") else PlatformsSupported.PC
    return PlatformsSupported.Xbox if aux.startswith("xb") else PlatformsSupported.Switch if aux.startswith("sw") else PlatformsSupported.PS4 if aux.startswith("ps") else PlatformsSupported.PC

def getPlayerId(playerName, platform = PlatformsSupported.PC):
    if not playerName or playerName == "none" or playerName == "null":
        return 0
    elif str(playerName).isnumeric():
        return playerName if len(str(playerName)) > 5 or len(str(playerName)) < 12 else 0
    elif str(platform.value).isnumeric():
        temp = paladinsAPI.getPlayerIdsByGamerTag(platform, playerName)
    else:
        temp = paladinsAPI.getPlayerIdByName(playerName)
    return temp[0].get("player_id") if temp else -1

def getLastSeen(lastSeen, language = LanguagesSupported.English):
    now = datetime.utcnow()
    delta = now - lastSeen
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    fmt = "{d}d" if days else "{h}h, {m}m" if hours else "{m}m, {s}s"
    return fmt.format(d=days, h=hours, m=minutes, s=seconds)

@app.route("/api/version", methods=["GET"])
def getGameVersion():
    platform = getPlatform(request.args)
    language = getLanguage(request.args)

    try:
        hiRezServerStatus = paladinsAPI.getHiRezServerStatus()#paladinsAPI.getHiRezServerStatus(platform)
        hiRezServerStatus = hiRezServerStatus[1] if platform == PlatformsSupported.Xbox or platform == PlatformsSupported.Switch else hiRezServerStatus[2] if platform == PlatformsSupported.PS4 else hiRezServerStatus[0]
        patchInfo = paladinsAPI.getPatchInfo()
    except:
        return UNABLE_TO_CONNECT_STRINGS[language]
    return GAME_VERSION_STRINGS[language].format("Paladins", "Xbox One" if platform == PlatformsSupported.Xbox else "PS4" if platform == PlatformsSupported.PS4 else "Nintendo Switch" if platform == PlatformsSupported.Switch else "PC",
                        PALADINS_UP_STRINGS[language] if hiRezServerStatus.status else PALADINS_DOWN_STRINGS[language],
                        patchInfo.gameVersion, hiRezServerStatus.version)

@app.route("/api/stalk", methods=["GET"])
def getStalk():
    platform = getPlatform(request.args)
    player = str(request.args.get("player")).lower()
    language = getLanguage(request.args)

    try:
        playerId = getPlayerId(player, platform)
        if playerId == 0:
            return PLAYER_NULL_STRINGS[language]
        elif playerId == -1:
            return PLAYER_NOT_FOUND_STRINGS[language].format(player)#Se der Player not found, retornar só "Nonsocial is not found"?!
        getPlayerRequest = paladinsAPI.getPlayer(playerId)
        playerStalkRequest = paladinsAPI.getPlayerStatus(playerId)
    except:
        return INTERNAL_ERROR_500_STRINGS[language]
    return PLAYER_STALK_STRINGS[language].format(PLAYER_LEVEL_STRINGS[language].format(getPlayerRequest.playerName, getPlayerRequest.accountLevel),
                        playerStalkRequest.playerStatusString.replace("God", "Champion").replace("_", " ") if playerStalkRequest.playerStatus != 3 else CURRENTLY_MATCH_STRINGS[language].format(QUEUE_IDS_STRINGS[playerStalkRequest.currentMatchQueueId], playerStalkRequest.currentMatchId),
                        getPlayerRequest.createdDatetime.strftime(HOUR_FORMAT_STRINGS[language]), getLastSeen(getPlayerRequest.lastLoginDatetime, language), formatDecimal(getPlayerRequest.hoursPlayed), getPlayerRequest.platform, getPlayerRequest.playerRegion)

@app.route("/api/lastmatch", methods=["GET"])
def getLastMatch():
    platform = getPlatform(request.args)
    player = str(request.args.get("player")).lower()
    language = getLanguage(request.args)

    try:
        playerId = getPlayerId(player, platform)
        if playerId == 0:
            return PLAYER_NULL_STRINGS[language]
        elif playerId == -1:
            return PLAYER_NOT_FOUND_STRINGS[language].format(player)
        getPlayerRequest = paladinsAPI.getPlayer(playerId)
        lastMatchRequest = paladinsAPI.getMatchHistory(playerId)
    except:
        return INTERNAL_ERROR_500_STRINGS[language]
    kda = ((lastMatchRequest[0].assists / 2) + lastMatchRequest[0].kills) / lastMatchRequest[0].deaths if lastMatchRequest[0].deaths > 1 else 1
    kda = int(kda) if kda % 2 == 0 else round(kda, 2)
    return LAST_MATCH_STRINGS[language].format(lastMatchRequest[0].mapGame, lastMatchRequest[0].matchId, lastMatchRequest[0].championName,
                        lastMatchRequest[0].kills, lastMatchRequest[0].deaths, lastMatchRequest[0].assists, kda, lastMatchRequest[0].killingSpree,
                        formatDecimal(lastMatchRequest[0].damage), formatDecimal(lastMatchRequest[0].credits), lastMatchRequest[0].matchMinutes,
                        lastMatchRequest[0].matchRegion, lastMatchRequest[0].winStatus, "{0}/{1}".format(lastMatchRequest[0].team1Score,
                        lastMatchRequest[0].team2Score) if lastMatchRequest[0].taskForce == 1 else "{0}/{1}".format(lastMatchRequest[0].team2Score, lastMatchRequest[0].team1Score))

@app.route("/api/currentmatch", methods=["GET"])
def getCurrentMatch():
    platform = getPlatform(request.args)
    player = str(request.args.get("player")).lower()
    language = getLanguage(request.args)

    try:
        playerId = getPlayerId(player, platform)
        if playerId == 0:
            return PLAYER_NULL_STRINGS[language]
        elif playerId == -1:
            return PLAYER_NOT_FOUND_STRINGS[language].format(player)
        getPlayerRequest = paladinsAPI.getPlayer(playerId)#Não preciso disso?!
        playerStatusRequest = paladinsAPI.getPlayerStatus(playerId)
    except:
        return INTERNAL_ERROR_500_STRINGS[language]
    if playerStatusRequest.playerStatus != 3:
        return PLAYER_NOT_MATCH_STRINGS[language].format(getPlayerRequest.playerName)
        # Posso mostrar se o cara tá off, jogando outra coisa ou algo assim
    else:
        #if playerStatusRequest.currentMatchQueueId != 424 or playerStatusRequest.currentMatchQueueId != 428 or playerStatusRequest.currentMatchQueueId != 445 or playerStatusRequest.currentMatchQueueId != 452:#Olhar o id da fila 424, 428, 445, 452
            #return ""
        tim1Aux = tim2Aux = 1
        tim1 = tim2 = ""
        players = paladinsAPI.getMatchPlayerDetails(playerStatusRequest.currentMatchId)
        if players:
            for play in players:
                if playerStatusRequest.currentMatchQueueId == 428 or playerStatusRequest.currentMatchQueueId == 486:
                    #rank = PLAYER_RANK_STRINGS[language][play.tier]# if play.tier != 0 else PLAYER_RANK_STRINGS[language][0] if play.wins + play.losses == 0 else QUALIFYING_STRINGS[language]
                    if play.playerName.lower() == player.lower():
                        rank = PLAYER_RANK_STRINGS[language][getPlayerRequest.playerRankController.value if playerStatusRequest.currentMatchQueueId == 428 else getPlayerRequest.playerRankKeyboard.value]
                    else:
                        if play.accountLevel >= 15:
                                getPlayer = paladinsAPI.getPlayer(play.playerId)
                                rank = PLAYER_RANK_STRINGS[language][getPlayer.playerRankController.value if playerStatusRequest.currentMatchQueueId == 428 else getPlayer.playerRankKeyboard.value]
                        else:
                            rank = PLAYER_RANK_STRINGS[language][0]
                else:
                    if play.playerName.lower() == player.lower():
                        rank = PLAYER_RANK_STRINGS[language][getPlayerRequest.rankedKeyboard.currentRank.value if getPlayerRequest.rankedController.wins + getPlayerRequest.rankedController.losses == 0 else getPlayerRequest.rankedController.currentRank.value]
                    else:
                        if play.accountLevel >= 15:
                            getPlayer = paladinsAPI.getPlayer(play.playerId)
                            rank = PLAYER_RANK_STRINGS[language][getPlayer.rankedKeyboard.currentRank.value if getPlayer.rankedController.wins + getPlayerRequest.rankedController.losses == 0 else getPlayer.rankedController.currentRank.value]
                        else:
                            rank = PLAYER_RANK_STRINGS[language][0]
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
    if request.args.get("query"):
        query = request.args.get("query").split(' ')
        player = query[0]
    else:
        player = str(request.args.get("player")).lower()
    platform = getPlatform(request.args)
    language = getLanguage(request.args)

    playerId = getPlayerId(player, platform)
    if playerId == 0:
        return PLAYER_NULL_STRINGS[language]
    elif playerId == -1:
        return PLAYER_NOT_FOUND_STRINGS[language].format(player)
    getPlayerRequest = paladinsAPI.getPlayer(playerId)
    if getPlayerRequest.rankedController.wins + getPlayerRequest.rankedController.losses == 0 and getPlayerRequest.rankedKeyboard.wins + getPlayerRequest.rankedKeyboard.losses >= 1:
        return PLAYER_GET_RANK_STRINGS[language].format(PLAYER_LEVEL_STRINGS[language].format(getPlayerRequest.playerName, getPlayerRequest.accountLevel),
                                PLAYER_RANK_STRINGS[language][getPlayerRequest.rankedKeyboard.currentRank.value] if getPlayerRequest.rankedKeyboard.currentRank != Tier.Unranked else PLAYER_RANK_STRINGS[language][0] if getPlayerRequest.rankedKeyboard.wins + getPlayerRequest.rankedKeyboard.losses == 0 else QUALIFYING_STRINGS[language],
                                "" if getPlayerRequest.rankedKeyboard.currentRank == Tier.Unranked else " ({0} TP{1})".format(formatDecimal(getPlayerRequest.rankedKeyboard.currentTrumpPoints), ON_LEADERBOARD_STRINGS[language].format(getPlayerRequest.rankedKeyboard.leaderboardIndex) if getPlayerRequest.rankedKeyboard.leaderboardIndex > 0 else ""),
                                "" if getPlayerRequest.rankedKeyboard.currentRank == Tier.Unranked and getPlayerRequest.rankedKeyboard.wins + getPlayerRequest.rankedKeyboard.losses == 0 else WINS_LOSSES_STRINGS[language].format(formatDecimal(getPlayerRequest.rankedKeyboard.wins), formatDecimal(getPlayerRequest.rankedKeyboard.losses)),
                                " (Winrate Global: {0}%{1})".format (getPlayerRequest.getWinratio(), "" if getPlayerRequest.rankedKeyboard.wins + getPlayerRequest.rankedKeyboard.losses == 0 else " & Ranked: {0}%".format(getPlayerRequest.rankedKeyboard.getWinratio())))
    else:
        #"PLAYER_RANK_STRINGS[language][getPlayerRequest.rankedController.currentRank.value] & PLAYER_RANK_STRINGS[language][getPlayerRequest.rankedKeyboard.currentRank.value]" if vitorias e derrotas console > 1 e vitorias e derrotas keyboard > 1 else "2" if vitorias e derrotas console > 1 else "3"
        return PLAYER_GET_RANK_STRINGS[language].format(PLAYER_LEVEL_STRINGS[language].format(getPlayerRequest.playerName, getPlayerRequest.accountLevel),
                                PLAYER_RANK_STRINGS[language][getPlayerRequest.rankedController.currentRank.value] if getPlayerRequest.rankedController.currentRank != Tier.Unranked else PLAYER_RANK_STRINGS[language][0] if getPlayerRequest.rankedController.wins + getPlayerRequest.rankedController.losses == 0 else QUALIFYING_STRINGS[language],
                                "" if getPlayerRequest.rankedController.currentRank == Tier.Unranked else " ({0} TP{1})".format(formatDecimal(getPlayerRequest.rankedController.currentTrumpPoints), ON_LEADERBOARD_STRINGS[language].format(getPlayerRequest.rankedController.leaderboardIndex) if getPlayerRequest.rankedController.leaderboardIndex > 0 else ""),
                                "" if getPlayerRequest.rankedController.currentRank == Tier.Unranked and getPlayerRequest.rankedController.wins + getPlayerRequest.rankedController.losses == 0 else WINS_LOSSES_STRINGS[language].format(formatDecimal(getPlayerRequest.rankedController.wins), formatDecimal(getPlayerRequest.rankedController.losses)),
                                " (Winrate Global: {0}%{1})".format(getPlayerRequest.getWinratio(), "" if getPlayerRequest.rankedController.wins + getPlayerRequest.rankedController.losses == 0 else " & Ranked: {0}%".format(getPlayerRequest.rankedController.getWinratio())))

@app.route("/api/kda", methods=["GET"])
@app.route("/api/winrate", methods=["GET"])
def getWinrate():
    platform = getPlatform(request.args)
    player = str(request.args.get("player")).lower()
    champion = str(request.args.get("champion")).lower().replace(" ", "").replace("'", "") if request.args.get("champion") and str(request.args.get("champion")).lower() != "null" else None
    language = getLanguage(request.args)

    try:
        playerId = getPlayerId(player, platform)
        if playerId == 0:
            return PLAYER_NULL_STRINGS[language]
        elif playerId == -1:
            return PLAYER_NOT_FOUND_STRINGS[language].format(player)
        getPlayerRequest = paladinsAPI.getPlayer(playerId)
        playerGlobalKDA = paladinsAPI.getChampionRanks(playerId)
    except:
        return INTERNAL_ERROR_500_STRINGS[language]
    if champion:
        for i in range(0, len(playerGlobalKDA)):
            if playerGlobalKDA[i].godName.lower().replace(" ", "").replace("'", "") == champion:
                return CHAMP_WINRATE_STRINGS[language].format(PLAYER_LEVEL_STRINGS[language].format(playerGlobalKDA[i].godName.replace("'", " "), playerGlobalKDA[i].godLevel), playerGlobalKDA[i].wins,
                        playerGlobalKDA[i].losses, formatDecimal(playerGlobalKDA[i].kills), formatDecimal(playerGlobalKDA[i].deaths),
                        formatDecimal(playerGlobalKDA[i].assists), playerGlobalKDA[i].getKDA(), playerGlobalKDA[i].getWinratio())
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
                        getPlayerRequest.losses, formatDecimal(kills), formatDecimal(deaths),
                        formatDecimal(assists), int(kda) if kda % 2 == 0 else round(kda, 2), getPlayerRequest.getWinratio())

if __name__ == "__main__":
    app.run(debug=DEBUG)