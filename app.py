from pyrez.api import *
from pyrez.enumerations import *

from decouple import config, Csv

from flask import Flask, jsonify, request

from langs import *

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
    platform = request.args.get("platform") if request.args.get("platform") else "pc"
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"
    
    hiRezServerStatus = paladinsXBOX.getHiRezServerStatus() if platform.lower().startswith("xb") or platform.lower() == "switch" else paladinsPS4.getHiRezServerStatus() if platform.lower().startswith("ps") else paladinsPC.getHiRezServerStatus()
    patchInfo = paladinsXBOX.getPatchInfo() if platform.lower().startswith("xb") or platform.lower() == "switch" else paladinsPS4.getPatchInfo() if platform.lower().startswith("ps") else paladinsPC.getPatchInfo()
    return GAME_VERSION_STRINGS[language].format("Paladins", "PC" if platform.lower() == "pc" else "PS4" if platform.lower().startswith("ps") else "Nintendo Switch" if platform.lower() == "switch" else "Xbox One",
                                                PALADINS_UP_STRINGS[language] if hiRezServerStatus.status else PALADINS_DOWN_STRINGS[language],
                                                patchInfo.gameVersion, hiRezServerStatus.version)

@app.route('/api/stalk', methods=['GET'])
def getStalk():
    platform = request.args.get("platform") if request.args.get("platform") else "pc"
    player = request.args.get("player")
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"

    if not player:
        return PLAYER_NULL_STRINGS[language]
    playerStalkRequest = paladinsXBOX.getPlayerStatus(player) if platform.lower().startswith("xb") or platform.lower() == "switch" else paladinsPS4.getPlayerStatus(player) if platform.lower().startswith("ps") else paladinsPC.getPlayerStatus(player)
    return "{0} is {1}.".format(player.capitalize(), (playerStalkRequest.playerStatusString.replace("God", "Champion").replace("_", " ") if playerStalkRequest.playerStatus != 3 else CURRENTLY_MATCH_STRINGS[language].format(playerStalkRequest.currentMatchID)))

@app.route('/api/lastmatch', methods=['GET'])
def getLastMatch():
    platform = request.args.get("platform") if request.args.get("platform") else "pc"
    player = request.args.get("player")
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"

    if not player:
        return PLAYER_NULL_STRINGS[language]
    lastMatchRequest = paladinsXBOX.getMatchHistory(player.lower()) if platform.lower().startswith("xb") or platform.lower() == "switch" else paladinsPS4.getMatchHistory(player.lower()) if platform.lower().startswith("ps") else paladinsPC.getMatchHistory(player.lower())
    kda = ((lastMatchRequest[0].assists / 2) + lastMatchRequest[0].kills) / lastMatchRequest[0].deaths if lastMatchRequest[0].deaths > 1 else 1
    kda = int(kda) if kda % 2 == 0 else round(kda, 2)
    return LAST_MATCH_STRINGS[language].format(lastMatchRequest[0].mapGame, lastMatchRequest[0].matchID, lastMatchRequest[0].championName.capitalize(), lastMatchRequest[0].kills, lastMatchRequest[0].deaths, lastMatchRequest[0].assists, kda, lastMatchRequest[0].killingSpree, format(lastMatchRequest[0].damage, ',d'), format(lastMatchRequest[0].credits, ',d'), lastMatchRequest[0].matchMinutes, lastMatchRequest[0].matchRegion, lastMatchRequest[0].winStatus, "{0}/{1}".format(lastMatchRequest[0].team1Score, lastMatchRequest[0].team2Score) if lastMatchRequest[0].taskForce == 1 else "{0}/{1}".format(lastMatchRequest[0].team2Score, lastMatchRequest[0].team1Score))

@app.route('/api/currentmatch', methods=['GET'])
def getCurrentMatch():
    platform = request.args.get("platform") if request.args.get("platform") else "pc"
    player = request.args.get("player")
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"
    
    if not player:
        return PLAYER_NULL_STRINGS[language]
    playerStatusRequest = paladinsXBOX.getPlayerStatus(player) if platform.lower().startswith("xb") or platform.lower() == "switch" else paladinsPS4.getPlayerStatus(player) if platform.lower().startswith("ps") else paladinsPC.getPlayerStatus(player)
    if playerStatusRequest.playerStatus != 3:
        return PLAYER_NOT_MATCH_STRINGS[language]
    else:
        tim1 = ""
        tim1Aux = 1
        tim2Aux = 1
        tim2 = ""
        players = paladinsXBOX.getMatchPlayerDetails(playerStatusRequest.currentMatchID) if platform.lower().startswith("xb") or platform.lower() == "switch" else paladinsPS4.getMatchPlayerDetails(playerStatusRequest.currentMatchID) if platform.lower().startswith("ps") else paladinsPC.getMatchPlayerDetails(playerStatusRequest.currentMatchID)
        for player in players:
            rank = paladinsXBOX.getPlayer(player.playerName) if platform.lower().startswith("xb") or platform.lower() == "switch" else paladinsPS4.getPlayer(player.playerName) if platform.lower().startswith("ps") else paladinsPC.getPlayer(player.playerName)
            if player.taskForce == 1:
                tim1 += CURRENT_MATCH_PLAYER_STRINGS[language].format(player.playerName.capitalize(), player.championName.capitalize(), PLAYER_RANK_STRINGS[language][rank.playerElo.value], "{0}".format(", " if tim1Aux <= 4 else ""))
                tim1Aux += 1
            else:
                tim2 += CURRENT_MATCH_PLAYER_STRINGS[language].format(player.playerName.capitalize(), player.championName.capitalize(), PLAYER_RANK_STRINGS[language][rank.playerElo.value], "{0}".format(", " if tim2Aux <= 4 else ""))
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
        playerRank = paladinsXBOX.getPlayer(player) if platform.lower().startswith("xb") or platform.lower() == "switch" else paladinsPS4.getPlayer(player) if platform.lower().startswith("ps") else paladinsPC.getPlayer(player)
    except:
        return PLAYER_NOT_FOUND_STRINGS[language]
    return PLAYER_GET_RANK_STRINGS[language].format(playerRank.playerName.capitalize(), playerRank.accountLevel, PLAYER_RANK_STRINGS[language][playerRank.rankedConquest.currentElo.value],
                                                "" if playerRank.rankedConquest.currentElo == Tier.Unranked else " ({0} TP{1})".format(format(playerRank.rankedConquest.currentTrumpPoints, ',d'),
                                                ON_LEADERBOARD_STRINGS[language].format(playerRank.rankedConquest.leaderboardIndex) if playerRank.rankedConquest.leaderboardIndex > 0 else ""),
                                                format(playerRank.rankedConquest.wins, ',d'), format(playerRank.rankedConquest.losses, ',d'), " (Winrate Global: {0}% & Ranked: {1}%)".format(playerRank.getWinratio(), playerRank.rankedConquest.getWinratio()))

@app.route('/api/winrate', methods=['GET'])
def getWinrate():
    platform = request.args.get("platform") if request.args.get("platform") else "pc"
    player = request.args.get("player")
    champion = str(request.args.get("champion")).lower().replace(" ", "").replace("'", "") if request.args.get("champion") else None
    language = str(request.args.get("language")).lower() if request.args.get("language") else "en"

    if not player:
        return PLAYER_NULL_STRINGS[language]
    if len(str(champion)) <= 0 or champion is None:
        try:
            playerGlobalWinrate = paladinsXBOX.getPlayer(player) if platform.lower().startswith("xb") or platform.lower() == "switch" else paladinsPS4.getPlayer(player) if platform.lower().startswith("ps") else paladinsPC.getPlayer(player)
            playerGlobalKDA = paladinsXBOX.getChampionRanks(player) if platform.lower().startswith("xb") or platform.lower() == "switch" else paladinsPS4.getChampionRanks(player) if platform.lower().startswith("ps") else paladinsPC.getChampionRanks(player)
            
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
        except:
            return PLAYER_NOT_FOUND_STRINGS[language]
    else:
        try:
            playerChampionWinrate = paladinsXBOX.getChampionRanks(player) if platform.lower().startswith("xb") or platform.lower() == "switch" else paladinsPS4.getChampionRanks(player) if platform.lower().startswith("ps") else paladinsPC.getChampionRanks(player)
            
            for i in range(0, len(playerChampionWinrate)):
                if playerChampionWinrate[i].godName.lower().replace(" ", "").replace("'", "") == champion:
                    return CHAMP_WINRATE_STRINGS[language].format(playerChampionWinrate[i].godName.replace("'", " ").capitalize(), playerChampionWinrate[i].godLevel, playerChampionWinrate[i].wins,
                                                                  playerChampionWinrate[i].losses, playerChampionWinrate[i].getWinratio(), format(playerChampionWinrate[i].kills, ',d'),
                                                                  format(playerChampionWinrate[i].deaths, ',d'), format(playerChampionWinrate[i].assists, ',d'), playerChampionWinrate[i].getKDA())
        except:
            return PLAYER_NOT_FOUND_STRINGS[language]

if __name__ == "__main__":
    app.run(debug=False)

"""
http://gotme.site-meute.com/api/v1/commands-list

!mostPlayed
!lastgame           Display the statistics of your last ranked game.                        Trahanqc: !lastgame  Nightbot: Last game won with Gragas 5/4/11 (4 KDA with 51.6% kill participation) 1 double kill
!queue              Display your current queue type. Note: The summoner must be in a game.  Trahanqc: !queue Nightbot: Ranked 5v5 Draft Pick
!rank               Display your current League of Legends ranking.                         Trahanqc: !rank Nightbot: Platinum V (86 LP) Series: ✓ X -
!streak             Display your current winning/losing streak in ranked games.             Trahanqc: !streak Nightbot: Win (1)
!version            Display the current patch version                                       Trahanqc: !version Nightbot: Current version : 8.17.1
"""