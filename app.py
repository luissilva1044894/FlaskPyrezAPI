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
    language = getLanguage(request)
    return INTERNAL_ERROR_404_STRINGS[language], 200 #return render_template("404.html"), 404 #return INTERNAL_ERROR_404_STRINGS[language], 404

@app.errorhandler(500)
def internal_error(error=None):
    language = getLanguage(request)
    return INTERNAL_ERROR_500_STRINGS[language], 200 #return render_template("500.html"), 500 #return INTERNAL_ERROR_500_STRINGS[language], 500

@app.route('/', methods=["GET"])
@app.route("/api", methods=["GET"])
@app.route("/index", methods=["GET"])
@app.route("/index.html", methods=["GET"])
def index():#ip = request.remote_addr
    return render_template("index-{0}.html".format(getLanguage(request))) #redirect(url_for("index"))

def formatDecimal(data, form = ",d"):
    return format(data, form) if data else 0

def getAcceptedLanguages(requestArgs):
    return str(request.accept_languages).split('-')[0] if len(str(request.accept_languages)) > 0 else LanguagesSupported.English.value

def getLanguage(requestArgs):
    aux = str(requestArgs.args.get("language", default=getAcceptedLanguages(requestArgs))).lower()
    try:
        return LanguagesSupported(aux).value
    except ValueError:
        return LanguagesSupported.English.value

def getPlatform(requestArgs):
    aux = str(requestArgs.get("platform", default=str(PlatformsSupported.PC.value))).lower()
    return PlatformsSupported.Xbox if aux.startswith("xb") else PlatformsSupported.Switch if aux.startswith("sw") else PlatformsSupported.PS4 if aux.startswith("ps") else PlatformsSupported.PC

def getPlayerName(requestArgs):
    return str(requestArgs.get("query", default=str(requestArgs.get("player", default=None)).lower()).split(' ')[0]).lower()

def getPlayerId(playerName, platform = PlatformsSupported.PC):
    if PlatformsSupported.PC:
        playerName = playerName.strip()#.strip(',.-')
    if not playerName or playerName == "none" or playerName == "null" or playerName == "$(1)" or playerName == "query=$(querystring)":
        return 0
    elif str(playerName).isnumeric():
        return playerName if len(str(playerName)) > 5 or len(str(playerName)) < 12 else 0
    elif str(platform.value).isnumeric():
        temp = paladinsAPI.getPlayerIdsByGamerTag(playerName, platform)
    else:
        temp = paladinsAPI.getPlayerIdByName(playerName)
    return temp[0].playerId if temp else -1

def getLastSeen(lastSeen, language = LanguagesSupported.English):
    now = datetime.utcnow()
    delta = now - lastSeen
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    fmt = "{d}d" if days else "{h}h, {m}m" if hours else "{m}m, {s}s"
    return fmt.format(d=days, h=hours, m=minutes, s=seconds)

@app.route("/api/decks", methods=["GET"])
def getDecks():
    platform = getPlatform(request.args)
    playerName = getPlayerName(request.args)
    championName = str(request.args.get("champion")).lower().replace(" ", "").replace("'", "") if request.args.get("champion") and str(request.args.get("champion")).lower() != "null" else None
    language = getLanguage(request)
    return INTERNAL_ERROR_404_STRINGS[language]

@app.route("/api/version", methods=["GET"])
def getGameVersion():
    platform = getPlatform(request.args)
    language = getLanguage(request)

    try:
        hiRezServerStatus = paladinsAPI.getHiRezServerStatus()
        hiRezServerStatus = hiRezServerStatus[1] if platform == PlatformsSupported.Xbox or platform == PlatformsSupported.Switch else hiRezServerStatus[2] if platform == PlatformsSupported.PS4 else hiRezServerStatus[0]
        patchInfo = paladinsAPI.getPatchInfo()
    except:
        return UNABLE_TO_CONNECT_STRINGS[language]
    return GAME_VERSION_STRINGS[language].format("Paladins", "Xbox One" if platform == PlatformsSupported.Xbox else "PS4" if platform == PlatformsSupported.PS4 else "Nintendo Switch" if platform == PlatformsSupported.Switch else "PC",
                        PALADINS_UP_STRINGS[language].format(PALADINS_LIMITED_ACCESS_STRINGS[language] if hiRezServerStatus.limitedAccess else "") if hiRezServerStatus.status else PALADINS_DOWN_STRINGS[language],
                        patchInfo.gameVersion, hiRezServerStatus.version)

@app.route("/api/stalk", methods=["GET"])
def getStalk():
    platform = getPlatform(request.args)
    playerName = getPlayerName(request.args)
    language = getLanguage(request)

    try:
        playerId = getPlayerId(playerName, platform)
        if playerId == 0:
            return PLAYER_NULL_STRINGS[language]
        elif playerId == -1:
            return PLAYER_NOT_FOUND_STRINGS[language].format(playerName)
        getPlayerRequest = paladinsAPI.getPlayer(playerId)
        playerStalkRequest = paladinsAPI.getPlayerStatus(playerId)
    except:
        return INTERNAL_ERROR_500_STRINGS[language]
    return PLAYER_STALK_STRINGS[language].format(PLAYER_LEVEL_STRINGS[language].format(getPlayerRequest.playerName, getPlayerRequest.accountLevel),
                        playerStalkRequest.statusString.replace("God", "Champion").replace("_", " ") if playerStalkRequest.status != 3 else CURRENTLY_MATCH_STRINGS[language].format(QUEUE_IDS_STRINGS[language][playerStalkRequest.matchQueueId], playerStalkRequest.matchId),
                        getPlayerRequest.createdDatetime.strftime(HOUR_FORMAT_STRINGS[language]), getLastSeen(getPlayerRequest.lastLoginDatetime, language), formatDecimal(getPlayerRequest.hoursPlayed), getPlayerRequest.platform, getPlayerRequest.playerRegion)

@app.route("/api/lastmatch", methods=["GET"])
def getLastMatch():
    platform = getPlatform(request.args)
    playerName = getPlayerName(request.args)
    language = getLanguage(request)

    #try:
    playerId = getPlayerId(playerName, platform)
    if playerId == 0:
        return PLAYER_NULL_STRINGS[language]
    if playerId == -1:
        return PLAYER_NOT_FOUND_STRINGS[language].format(playerName)
    lastMatchRequest = paladinsAPI.getMatchHistory(playerId)[0]
    #except:
    #    return INTERNAL_ERROR_500_STRINGS[language]
    kda = ((lastMatchRequest.assists / 2) + lastMatchRequest.kills) / lastMatchRequest.deaths if lastMatchRequest.deaths > 1 else 1
    kda = int(kda) if kda % 2 == 0 else round(kda, 2)
    return LAST_MATCH_STRINGS[language].format(lastMatchRequest.mapName, lastMatchRequest.matchId, lastMatchRequest.godId.getName() if isinstance(lastMatchRequest.godId, Champions) else lastMatchRequest.godName,
                        lastMatchRequest.kills, lastMatchRequest.deaths, lastMatchRequest.assists, kda, lastMatchRequest.killingSpree,
                        formatDecimal(lastMatchRequest.damage), formatDecimal(lastMatchRequest.credits), lastMatchRequest.matchMinutes,
                        lastMatchRequest.matchRegion, lastMatchRequest.winStatus, "{0}/{1}".format(lastMatchRequest.team1Score,
                        lastMatchRequest.team2Score) if lastMatchRequest.taskForce == 1 else "{0}/{1}".format(lastMatchRequest.team2Score, lastMatchRequest.team1Score))

def isQueueIdValid(queueId):
    return queueId == 424 or queueId == 425 or queueId == 427 or queueId == 428 or queueId == 452 or queueId == 453 or queueId == 469 or queueId == 470 or queueId == 486 if str(queueId).isnumeric() else False
@app.route("/api/currentmatch", methods=["GET"])
def getCurrentMatch():
    platform = getPlatform(request.args)
    playerName = getPlayerName(request.args)
    language = getLanguage(request)

    try:
        playerId = getPlayerId(playerName, platform)
        if playerId == 0 or playerId == -1:
            return PLAYER_NULL_STRINGS[language] if playerId == 0 else PLAYER_NOT_FOUND_STRINGS[language].format(playerName)
        playerStatusRequest = paladinsAPI.getPlayerStatus(playerId)
    except:
        return INTERNAL_ERROR_500_STRINGS[language]
    if not playerStatusRequest.status.isInGame():
        return PLAYER_NOT_MATCH_STRINGS[language][playerStatusRequest.status].format(playerName)
    if not isQueueIdValid(playerStatusRequest.matchQueueId):
        return QUEUE_ID_NOT_SUPPORTED_STRINGS[language].format(QUEUE_IDS_STRINGS[language][playerStatusRequest.matchQueueId], playerName)
    team1 = []
    team2 = []
    players = paladinsAPI.getLiveMatchDetails(playerStatusRequest.matchId)
    if players:
        for player in players:
            if playerStatusRequest.matchQueueId.isRanked():#playerStatusRequest.matchQueueId == 428 or playerStatusRequest.matchQueueId == 486:
                rank = PLAYER_RANK_STRINGS[language][player.tier] if player.tier != 0 else PLAYER_RANK_STRINGS[language][0] if player.tierWins + player.tierLosses == 0 else QUALIFYING_STRINGS[language]
            else:
                if player.accountLevel >= 15:
                    getPlayer = paladinsAPI.getPlayer(player.playerId)
                    rank = PLAYER_RANK_STRINGS[language][getPlayer.rankedKeyboard.currentRank if getPlayer.rankedController.hasPlayedRanked() else getPlayer.rankedController.currentRank]
                else:
                    rank = PLAYER_RANK_STRINGS[language][0]
            if player.taskForce == 1:
                team1.append(CURRENT_MATCH_PLAYER_STRINGS[language].format(player.playerName, player.godId.getName() if isinstance(player.godId, Champions) else player.godName, rank))
            else:
                team2.append(CURRENT_MATCH_PLAYER_STRINGS[language].format(player.playerName, player.godId.getName() if isinstance(player.godId, Champions) else player.godName, rank))
        return CURRENT_MATCH_STRINGS[language].format(players[0].mapName.replace("LIVE ").replace("Practice ").replace(" (Onslaught)").replace(" (Onslaught) ").replace(" (TDM)").replace(" (TDM) ").replace("Ranked ").replace("'", ''),
                        QUEUE_IDS_STRINGS[language][playerStatusRequest.matchQueueId], ",".join(team1), ",".join(team2))
    else:
        return "An unexpected error has occurred!"

@app.route("/api/rank", methods=["GET"])
def getRank():
    playerName = getPlayerName(request.args)
    platform = getPlatform(request.args)
    language = getLanguage(request)

    try:
        playerId = getPlayerId(playerName, platform)
        if playerId == 0:
            return PLAYER_NULL_STRINGS[language]
        elif playerId == -1:
            return PLAYER_NOT_FOUND_STRINGS[language].format(playerName)
        getPlayerRequest = paladinsAPI.getPlayer(playerId)
    except:
        return INTERNAL_ERROR_500_STRINGS[language]
    r1 = getPlayerRequest.rankedController
    r2 = getPlayerRequest.rankedKeyboard
    if r1.wins + r1.losses == 0 and r2.wins + r2.losses >= 1:
        return PLAYER_GET_RANK_STRINGS[language].format(PLAYER_LEVEL_STRINGS[language].format(getPlayerRequest.playerName, getPlayerRequest.accountLevel),
                                PLAYER_RANK_STRINGS[language][r2.currentRank.value] if r2.currentRank != Tier.Unranked else PLAYER_RANK_STRINGS[language][0] if r2.wins + r2.losses == 0 else QUALIFYING_STRINGS[language],
                                "" if r2.currentRank == Tier.Unranked else " ({0} TP{1})".format(formatDecimal(r2.currentTrumpPoints), ON_LEADERBOARD_STRINGS[language].format(r2.leaderboardIndex) if r2.leaderboardIndex > 0 else ""),
                                "" if r2.currentRank == Tier.Unranked and r2.wins + r2.losses == 0 else WINS_LOSSES_STRINGS[language].format(formatDecimal(r2.wins), formatDecimal(r2.losses)),
                                " (Winrate Global: {0}%{1})".format (getPlayerRequest.getWinratio(), "" if r2.wins + r2.losses == 0 else " & Ranked: {0}%".format(r2.getWinratio())))
    else:
        return PLAYER_GET_RANK_STRINGS[language].format(PLAYER_LEVEL_STRINGS[language].format(getPlayerRequest.playerName, getPlayerRequest.accountLevel),
                                PLAYER_RANK_STRINGS[language][r1.currentRank.value] if r1.currentRank != Tier.Unranked else PLAYER_RANK_STRINGS[language][0] if r1.wins + r1.losses == 0 else QUALIFYING_STRINGS[language],
                                "" if r1.currentRank == Tier.Unranked else " ({0} TP{1})".format(formatDecimal(r1.currentTrumpPoints), ON_LEADERBOARD_STRINGS[language].format(r1.leaderboardIndex) if r1.leaderboardIndex > 0 else ""),
                                "" if r1.currentRank == Tier.Unranked and r1.wins + r1.losses == 0 else WINS_LOSSES_STRINGS[language].format(formatDecimal(r1.wins), formatDecimal(r1.losses)),
                                " (Winrate Global: {0}%{1})".format(getPlayerRequest.getWinratio(), "" if r1.wins + r1.losses == 0 else " & Ranked: {0}%".format(r1.getWinratio())))

@app.route("/api/kda", methods=["GET"])
@app.route("/api/winrate", methods=["GET"])
def getWinrate():
    platform = getPlatform(request.args)
    playerName = getPlayerName(request.args)
    championName = str(request.args.get("champion")).lower().replace(" ", "").replace("'", "") if request.args.get("champion") and str(request.args.get("champion")).lower() != "null" else None
    language = getLanguage(request)

    try:
        playerId = getPlayerId(playerName, platform)
        if playerId == 0:
            return PLAYER_NULL_STRINGS[language]
        elif playerId == -1:
            return PLAYER_NOT_FOUND_STRINGS[language].format(playerName)
        getPlayerRequest = paladinsAPI.getPlayer(playerId)
        if getPlayerRequest.accountLevel > 5:
            playerGlobalKDA = paladinsAPI.getChampionRanks(playerId)
        else:
            return PLAYER_LOW_LEVEL_STRINGS[language]
    except:
        return INTERNAL_ERROR_500_STRINGS[language]
    if championName:
        for champ in playerGlobalKDA:
            if champ.godName.lower().replace(" ", "").replace("'", "") == championName:
                return CHAMP_WINRATE_STRINGS[language].format(PLAYER_LEVEL_STRINGS[language].format(champ.godName.replace("'", " "), champ.godLevel), champ.wins, champ.losses,
                        formatDecimal(champ.kills), formatDecimal(champ.deaths), formatDecimal(champ.assists), champ.getKDA(), champ.getWinratio())
        return CHAMP_NOT_PLAYED_STRINGS[language].format(playerName, championName)
    else:
        deaths = 0
        kills = 0
        assists = 0
        for champ in playerGlobalKDA:
            kills += champ.kills
            deaths += champ.deaths
            assists += champ.assists
        kda = ((assists / 2) + kills) / deaths if deaths > 1 else 1
        return CHAMP_WINRATE_STRINGS[language].format(PLAYER_LEVEL_STRINGS[language].format(getPlayerRequest.playerName, getPlayerRequest.accountLevel), getPlayerRequest.wins, getPlayerRequest.losses,
                        formatDecimal(kills), formatDecimal(deaths), formatDecimal(assists), int(kda) if kda % 2 == 0 else round(kda, 2), getPlayerRequest.getWinratio())

if __name__ == "__main__":
    app.run(debug=DEBUG)