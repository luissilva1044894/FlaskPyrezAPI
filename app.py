# -*- coding: utf-8 -*-

from pyrez.api import *
from pyrez.enumerations import *
from langs import *

from decouple import config, Csv

from flask import Flask, jsonify, request

app = Flask(__name__)

try:
    DEBUG = config("DEBUG", default=False, cast=bool)
    PYREZ_AUTH_ID = config("PYREZ_AUTH_ID")
    PYREZ_DEV_ID = config("PYREZ_DEV_ID")
except:
    DEBUG = os.environ ["DEBUG"] if os.environ ["DEBUG"] else False
    PYREZ_AUTH_ID = os.environ("PYREZ_AUTH_ID")
    PYREZ_DEV_ID = os.environ("PYREZ_DEV_ID")

paladinsPC = PaladinsAPI(devId=PYREZ_DEV_ID, authKey=PYREZ_AUTH_ID)
paladinsPS4 = PaladinsAPI(devId=PYREZ_DEV_ID, authKey=PYREZ_AUTH_ID, platform=Platform.PS4)
paladinsXBOX = PaladinsAPI(devId=PYREZ_DEV_ID, authKey=PYREZ_AUTH_ID, platform=Platform.XBOX)

@app.errorhandler(404)#from flask import render_template
def not_found_error(error):
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"
    return INTERNAL_ERROR_404_STRINGS[language], 200 #return render_template("404.html"), 404 #return INTERNAL_ERROR_404_STRINGS[language], 404

@app.errorhandler(500)
def internal_error(error):
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"
    return INTERNAL_ERROR_500_STRINGS[language], 200 #return render_template("500.html"), 500 #return INTERNAL_ERROR_500_STRINGS[language], 500

@app.route("/api/version", methods=["GET"])
def getGameVersion():
    platform = str(request.args.get("platform")).lower() if request.args.get("platform") else "pc"
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"
    
    try:
        hiRezServerStatus = paladinsXBOX.getHiRezServerStatus() if platform.startswith("xb") or platform == "switch" else paladinsPS4.getHiRezServerStatus() if platform.startswith("ps") else paladinsPC.getHiRezServerStatus()
        patchInfo = paladinsXBOX.getPatchInfo() if platform.startswith("xb") or platform == "switch" else paladinsPS4.getPatchInfo() if platform.startswith("ps") else paladinsPC.getPatchInfo()
    except:
        return ""
    return GAME_VERSION_STRINGS[language].format("Paladins", "PC" if platform == "pc" else "PS4" if platform.startswith("ps") else "Nintendo Switch" if platform == "switch" else "Xbox One",
                                                PALADINS_UP_STRINGS[language] if hiRezServerStatus.status else PALADINS_DOWN_STRINGS[language],
                                                patchInfo.gameVersion, hiRezServerStatus.version)

@app.route("/api/stalk", methods=["GET"])
def getStalk():
    platform = str(request.args.get("platform")).lower() if request.args.get("platform") else "pc"
    player = fixNicknameIssues(str(request.args.get("player")).lower())
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"

    if not player:
        return PLAYER_NULL_STRINGS[language]
    try:
        playerStalkRequest = paladinsXBOX.getPlayerStatus(player) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getPlayerStatus(player) if platform.startswith("ps") else paladinsPC.getPlayerStatus(player)
    except:
        return PLAYER_NOT_FOUND_STRINGS[language]
    return "{0} is {1}.".format(player.capitalize(), (playerStalkRequest.playerStatusString.replace("God", "Champion").replace("_", " ") if playerStalkRequest.playerStatus != 3 else CURRENTLY_MATCH_STRINGS[language].format(playerStalkRequest.currentMatchID)))

@app.route("/api/lastmatch", methods=["GET"])
def getLastMatch():
    platform = str(request.args.get("platform")).lower() if request.args.get("platform") else "pc"
    player = fixNicknameIssues(str(request.args.get("player")).lower())
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

@app.route("/api/currentmatch", methods=["GET"])
def getCurrentMatch():
    platform = str(request.args.get("platform")).lower() if request.args.get("platform") else "pc"
    player = fixNicknameIssues(str(request.args.get("player")).lower())
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"
    
    if not player:
        return PLAYER_NULL_STRINGS[language]
    try:
        playerStatusRequest = paladinsXBOX.getPlayerStatus(player) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getPlayerStatus(player) if platform.startswith("ps") else paladinsPC.getPlayerStatus(player)
    except:
        return PLAYER_NOT_FOUND_STRINGS[language]
    if playerStatusRequest.playerStatus != 3:
        return PLAYER_NOT_MATCH_STRINGS[language].format(player.capitalize())
    else:
        tim1 = ""
        tim1Aux = 1
        tim2Aux = 1
        tim2 = ""
        players = paladinsXBOX.getMatchPlayerDetails(playerStatusRequest.currentMatchID) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getMatchPlayerDetails(playerStatusRequest.currentMatchID) if platform.startswith("ps") else paladinsPC.getMatchPlayerDetails(playerStatusRequest.currentMatchID)
        if players:
            for player in players:
                rank = paladinsXBOX.getPlayer(player.playerId) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getPlayer(player.playerId) if platform.startswith("ps") else paladinsPC.getPlayer(player.playerId)
                if player.taskForce == 1:
                    tim1 += CURRENT_MATCH_PLAYER_STRINGS[language].format(player.playerName, player.championName.capitalize(), PLAYER_RANK_STRINGS[language][rank.playerElo.value], "{0}".format(", " if tim1Aux <= 4 else ""))
                    tim1Aux += 1
                else:
                    tim2 += CURRENT_MATCH_PLAYER_STRINGS[language].format(player.playerName, player.championName.capitalize(), PLAYER_RANK_STRINGS[language][rank.playerElo.value], "{0}".format(", " if tim2Aux <= 4 else ""))
                    tim2Aux += 1
            return CURRENT_MATCH_STRINGS[language].format(tim1, tim2)
        else:
            return PLAYER_NOT_MATCH_STRINGS[language]
    
@app.route("/api/rank", methods=["GET"])
def getRank():
    platform = str(request.args.get("platform")).lower() if request.args.get("platform") else "pc"
    player = fixNicknameIssues(str(request.args.get("player")).lower())
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"

    if not player:
        return PLAYER_NULL_STRINGS[language]
    try:
        playerRank = paladinsXBOX.getPlayer(player) if platform.startswith("xb") or platform == "switch" else paladinsPS4.getPlayer(player) if platform.startswith("ps") else paladinsPC.getPlayer(player)
    except:
        return PLAYER_NOT_FOUND_STRINGS[language]
    return PLAYER_GET_RANK_STRINGS[language].format(playerRank.playerName, playerRank.accountLevel, PLAYER_RANK_STRINGS[language][playerRank.rankedConquest.currentElo.value],
                                                "" if playerRank.rankedConquest.currentElo == Tier.Unranked else " ({0} TP{1})".format(format(playerRank.rankedConquest.currentTrumpPoints, ',d'),
                                                ON_LEADERBOARD_STRINGS[language].format(playerRank.rankedConquest.leaderboardIndex) if playerRank.rankedConquest.leaderboardIndex > 0 else ""),
                                                format(playerRank.rankedConquest.wins, ',d'), format(playerRank.rankedConquest.losses, ',d'), " (Winrate Global: {0}% & Ranked: {1}%)".format(playerRank.getWinratio(), playerRank.rankedConquest.getWinratio()))

@app.route("/api/winrate", methods=["GET"])
def getWinrate():
    platform = str(request.args.get("platform")).lower() if request.args.get("platform") else "pc"
    player = fixNicknameIssues(str(request.args.get("player")).lower())
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
        return CHAMP_WINRATE_STRINGS[language].format(playerGlobalWinrate.playerName, playerGlobalWinrate.accountLevel, playerGlobalWinrate.wins,
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
    app.run(debug=DEBUG)

def fixNicknameIssues(nickname):
    return str(nickname).replace("%20", ' ').replace("%21", '!').replace("%22", '"').replace("%23", '#').replace("%24", '$').replace("%25", '%').replace("%26", '&').replace("%27", "'").replace("%28", '(').replace("%29", ')').replace("%2A", '*').replace("%2B", '+').replace("%2C", ',').replace("%2D", '-').replace("%2E", '.')
                        .replace("%2F", '/').replace("%30", '0').replace("%31", '1').replace("%32", '2').replace("%33", '3').replace("%34", '4').replace("%35", '5').replace("%36", '6').replace("%37", '7').replace("%38", '8').replace("%39", '9').replace("%3A", ':').replace("%3B", ';').replace("%3C", '<').replace("%3D", '=')
                        .replace("%3E", '>').replace("%3F", '?').replace("%40", '@').replace("%41", 'A').replace("%42", 'B').replace("%43", 'C').replace("%44", 'D').replace("%45", 'E').replace("%46", 'F').replace("%47", 'G').replace("%48", 'H').replace("%49", 'I').replace("%4A", 'J').replace("%4B", 'K').replace("%4C", 'L')
                        .replace("%4D", 'M').replace("%4E", 'N').replace("%4F", 'O').replace("%50", 'P').replace("%51", 'Q').replace("%52", 'R').replace("%53", 'S').replace("%54", 'T').replace("%55", 'U').replace("%56", 'V').replace("%57", 'W').replace("%58", 'X').replace("%59", 'Y').replace("%5A", 'Z').replace("%5B", '[')#.replace("%5C", '\')
                        .replace("%5D", ']').replace("%5E", '^').replace("%5F", '_').replace("%60", '`').replace("%61", 'a').replace("%62", 'b').replace("%63", 'c').replace("%64", 'd').replace("%65", 'e').replace("%66", 'f').replace("%67", 'g').replace("%68", 'h').replace("%69", 'i').replace("%6A", 'j').replace("%6B", 'k')
                        .replace("%6C", 'l').replace("%6D", 'm').replace("%6E", 'n').replace("%6F", 'o').replace("%70", 'p').replace("%71", 'q').replace("%72", 'r').replace("%73", 's').replace("%74", 't').replace("%75", 'u').replace("%76", 'v').replace("%77", 'w').replace("%78", 'x').replace("%79", 'y').replace("%7A", 'z')
                        .replace("%7B", '{').replace("%7C", '|').replace("%7D", '}').replace("%7E", '~').replace("%E2%82%AC", '`').replace("%C6%92", 'ƒ').replace("%E2%80%9E", '„').replace("%E2%80%A6", '…').replace("%E2%80%A0", '†').replace("‡", '%E2%80%A1').replace("%CB%86", 'ˆ').replace("%E2%80%B0", '‰').replace("%C5%A0", 'Š')
                        .replace("%E2%80%B9", '‹').replace("%C5%92", 'Œ').replace("%C5%BD", 'Ž').replace("%E2%80%98", '‘').replace("%E2%80%99", '’').replace("%E2%80%9C", '“').replace("%E2%80%9D", '”').replace("%E2%80%A2", '•').replace("%E2%80%93", '–').replace("%E2%80%94", '—').replace("%CB%9C", '˜').replace("%E2%84", '™')
                        .replace("%C5%A1", 'š').replace("%E2%80", '›').replace("%C5%93", 'œ').replace("%C5%BE", 'ž').replace("%C5%B8", 'Ÿ').replace("%C2%A1", '¡').replace("%C2%A2", '¢').replace("%C2%A3", '£').replace("%C2%A4", '¤').replace("%C2%A5", '¥').replace("%C2%A6", '¦').replace("%C2%A7", '§').replace("%C2%A9", '©')
                        .replace("%C2%AA", 'ª').replace("%C2%AB", '«').replace("%C2%AC", '¬').replace("%C2%AE", '®').replace("%C2%AF", '¯').replace("%C2%B0", '°').replace("%C2%B1", '±').replace("%C2%B2", '²').replace("%C2%B3", '³').replace("%C2%B4", '´').replace("%C2%B5", 'µ').replace("%C2%B6", '¶').replace("%C2%B7", '·')
                        .replace("%C2%B8", '¸').replace("%C2%B9", '¹').replace("%C2%BA", 'º').replace("%C2%BB", '»').replace("%C2%BC", '¼').replace("%C2%BD", '½').replace("%C2%BE", '¾').replace("%C2%BF", '¿').replace("%C3%80", 'À').replace("%C3%81", 'Á').replace("%C3%82", 'Â').replace("%C3%83", 'Ã').replace("%C3%84", 'Ä')
                        .replace("%C3%85", 'Å').replace("%C3%86", 'Æ').replace("%C3%87", 'Ç').replace("%C3%88", 'È').replace("%C3%89", 'É').replace("%C3%8A", 'Ê').replace("%C3%8B", 'Ë').replace("%C3%8C", 'Ì').replace("%C3%8D", 'Í').replace("%C3%8E", 'Î').replace("%C3%8F", 'Ï').replace("%C3%90", 'Ð').replace("%C3%91", 'Ñ')
                        .replace("%C3%92", 'Ò').replace("%C3%93", 'Ó').replace("%C3%94", 'Ô').replace("%C3%95", 'Õ').replace("%C3%96", 'Ö').replace("%C3%97", '×').replace("%C3%98", 'Ø').replace("%C3%99", 'Ù').replace("%C3%9A", 'Ú').replace("%C3%9B", 'Û').replace("%C3%9C", 'Ü').replace("%C3%9D", 'Ý').replace("%C3%9E", 'Þ')
                        .replace("%C3%9F", 'ß').replace("%C3%A0", 'à').replace("%C3%A1", 'á').replace("%C3%A2", 'â').replace("%C3%A3", 'ã').replace("%C3%A4", 'ä').replace("%C3%A5", 'å').replace("%C3%A6", 'æ').replace("%C3%A7", 'ç').replace("%C3%A8", 'è').replace("%C3%A9", 'é').replace("%C3%AA", 'ê').replace("%C3%AB", 'ë')
                        .replace("%C3%AC", 'ì').replace("%C3%AD", 'í').replace("%C3%AE", 'î').replace("%C3%AF", 'ï').replace("%C3%B0", 'ð').replace("%C3%B1", 'ñ').replace("%C3%B2", 'ò').replace("%C3%B3", 'ó').replace("%C3%B4", 'ô').replace("%C3%B5", 'õ').replace("%C3%B6", 'ö').replace("%C3%B7", '÷').replace("%C3%B8", 'ø')
                        .replace("%C3%B9", 'ù').replace("%C3%BA", 'ú').replace("%C3%BB", 'û').replace("%C3%BC", 'ü').replace("%C3%BD", 'ý').replace("%C3%BE", 'þ').replace("%C3%BF", 'ÿ')
