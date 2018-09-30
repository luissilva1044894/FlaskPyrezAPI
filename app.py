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
    "en" : "Current match: {0} | VS | {1}",
    "es" : "Current match: {0} | VS | {1}",
    "pt" : "Partida atual: {0} | VS | {1}",
}
CURRENT_MATCH_PLAYER_STRINGS = {
    "en" : "{0} as {1} ({2}){3}",
    "es" : "{0}: {1} ({2}){3}",
    "pt" : "{0}: {1} ({2}){3}",
}
PLAYER_NULL_STRINGS = {
    "en" : "Player not specified!",
    "es" : "Player not specified!",
    "pt" : "Player not specified!",
}
PLAYER_NOT_FOUND_STRINGS = {
    "en" : "Player not found!",
    "es" : "Player not found!",
    "pt" : "Jogador inválido!",
}
PLAYER_NOT_MATCH_STRINGS = {
    "en" : "Player isn't in a match!",
    "es" : "Player isn't in a match!",
    "pt" : "Jogador não está em partida!",
}
PLAYER_GET_RANK_STRINGS = {
    "en" : "{0} (Level {1}) is {2}{3} with {4} wins and {5} losses.{6}",
    "es" : "{0} (Level {1}) is {2}{3} with {4} wins and {5} losses.{6}",
    "pt" : "{0} (Nível {1}) é {2}{3} com {4} vitórias e {5} derrotas.{6}",
}
PLAYER_RANK_STRINGS = {
    "en" : {
        0: "Unranked",
        1: "Bronze V", 2: "Bronze IV", 3: "Bronze III", 4: "Bronze II", 5: "Bronze I",
        6: "Silver V", 7: "Silver IV", 8: "Silver III", 9: "Silver II", 10: "Silver I",
        11: "Gold V", 12: "Gold IV", 13: "Gold III", 14: "Gold II", 15: "Gold I",
        16: "Platinum V", 17: "Platinum IV", 18: "Platinum III", 19: "Platinum II", 20: "Platinum I",
        21: "Diamond V", 22: "Diamond IV", 23: "Diamond III", 24: "Diamond II", 25: "Diamond I",
        26: "Master", 27: "Grandmaster"
    },
    "es" : {
        0: "Unranked",
        1: "Bronce V", 2: "Bronce IV", 3: "Bronce III", 4: "Bronce II", 5: "Bronce I",
        6: "Plata V", 7: "Plata IV", 8: "Plata III", 9: "Plata II", 10: "Plata I",
        11: "Oro V", 12: "Oro IV", 13: "Oro III", 14: "Oro II", 15: "Oro I",
        16: "Platino V", 17: "Platino IV", 18: "Platino III", 19: "Platino II", 20: "Platino I",
        21: "Diamante V", 22: "Diamante IV", 23: "Diamante III", 24: "Diamante II", 25: "Diamante I",
        26: "Maestro", 27: "Gran maestro"
    },
    "pt" : {
        0: "Unranked",
        1: "Bronze V", 2: "Bronze IV", 3: "Bronze III", 4: "Bronze II", 5: "Bronze I",
        6: "Prata V", 7: "Prata IV", 8: "Prata III", 9: "Prata II", 10: "Prata I",
        11: "Ouro V", 12: "Ouro IV", 13: "Ouro III", 14: "Ouro II", 15: "Ouro I",
        16: "Platina V", 17: "Platina IV", 18: "Platina III", 19: "Platina II", 20: "Platina I",
        21: "Diamante V", 22: "Diamante IV", 23: "Diamante III", 24: "Diamante II", 25: "Diamante I",
        26: "Mestre", 27: "Grão-mestre"
    }
}
ON_LEADERBOARD_STRINGS = {
    "en" : ", {0} on the leaderboard",
    "es" : ", {0} on the leaderboard",
    "pt" : ", {0}° no rank",
}
CHAMP_WINRATE_STRINGS = {
    "en" : "{0} (Level {1}): {2} Wins, {3} Losses (Kills: {4} / Deaths: {5} / Assists: {6} - {7} KDA) - Winrate: {8}%",
    "es" : "{0} (Level {1}): {2} Wins, {3} Losses (Kills: {4} / Deaths: {5} / Assists: {6} - {7} KDA) - Winrate: {8}%",
    "pt" : "{0} (Nível {1}): vitórias: {2}, Derrotas: {3} (Kills: {4} / Deaths: {5} / Assists: {6} - {7} KDA) - Winrate: {8}%",
}
GAME_VERSION_STRINGS = {
    "en" : "{0} {1} is {2} - Current version: {3} ({4})",
    "es" : "{0} {1} is {2} - Current version: {3} ({4})",
    "pt" : "{0} {1} está {2} - Versão atual: {3} ({4})",
}
LAST_MATCH_STRINGS = {
    "en" : "{0} - Match ID: {1}, Duration: {10}m, Region: {11}: {2} ({3}/{4}/{5} - {6} KDA) Killing spree: {7}, Damage: {8}, Credits: {9} - {12} (Score: {13})",
    "es" : "{0} - Match ID: {1}, Duration: {10}m, Region: {11}: {2} ({3}/{4}/{5} - {6} KDA) Killing spree: {7}, Damage: {8}, Credits: {9} - {12} (Score: {13})",
    "pt" : "{0} - Id da partida: {1}, Duração: {10}m, Região: {11}: {2} ({3}/{4}/{5} - {6} KDA) Sequência: {7}, Dano: {8}, Creditos: {9} - {12} (Score: {13})",
}
CURRENTLY_MATCH_STRINGS = {
    "en" : "currently in a match (Match ID: {0})",
    "es" : "currently in a match (Match ID: {0})",
    "pt" : "está em partida (ID da partida: {0})",
}
PALADINS_UP_STRINGS = {
    "en" : "UP",
    "es" : "DISPONIBLE",
    "pt" : "OPERANTE",
}
PALADINS_DOWN_STRINGS = {
    "en" : "DOWN",
    "es" : "INDISPONIBLE",
    "pt" : "INOPERANTE",
}

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
            rank = paladinsXBOX.getPlayer(player.playerName) if platform.lower().startswith("xb") or platform.lower () == "switch" else paladinsPS4.getPlayer(player.playerName) if platform.lower().startswith("ps") else paladinsPC.getPlayer(player.playerName)
            if player.taskForce == 1:
                tim1 += CURRENT_MATCH_PLAYER_STRINGS[language].format(player.playerName.capitalize(), player.championName.capitalize(), rank.playerElo, "{0}".format(", " if tim1Aux <= 4 else ""))
                tim1Aux += 1
            else:
                tim2 += CURRENT_MATCH_PLAYER_STRINGS[language].format(player.playerName.capitalize(), player.championName.capitalize(), rank.playerElo, "{0}".format(", " if tim2Aux <= 4 else ""))
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
    champion = str(request.args.get("champion")).lower ().replace (" ", "").replace("'", "") if request.args.get("champion") else None
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
                if (playerChampionWinrate[i].godName.lower().replace(" ", "").replace("'", "") == champion):
                    return CHAMP_WINRATE_STRINGS[language].format(playerChampionWinrate[i].godName.replace("'", " ").capitalize(), playerChampionWinrate[i].godLevel, playerChampionWinrate[i].wins,
                                                                  playerChampionWinrate[i].losses, playerChampionWinrate[i].getWinratio(), format(playerChampionWinrate[i].kills, ',d'),
                                                                  format(playerChampionWinrate[i].deaths, ',d'), format(playerChampionWinrate[i].assists, ',d'), playerChampionWinrate[i].getKDA())
        except:
            return PLAYER_NOT_FOUND_STRINGS[language]

if __name__ == "__main__":
    app.run(debug=False)


"""
elo = str(playerRequest.rankedConquest.currentElo)
elo = elo.replace ("Silver", "Prata").replace ("Gold", "Ouro").replace ("Platinum", "Platina").replace ("Diamond", "Diamante").replace ("Master", "Mestre").replace ("Grandmaster", "Grão-mestre")


http://gotme.site-meute.com/api/v1/commands-list

!mostPlayed
!lastgame           Display the statistics of your last ranked game.                        Trahanqc: !lastgame  Nightbot: Last game won with Gragas 5/4/11 (4 KDA with 51.6% kill participation) 1 double kill
!queue              Display your current queue type. Note: The summoner must be in a game.  Trahanqc: !queue Nightbot: Ranked 5v5 Draft Pick
!rank               Display your current League of Legends ranking.                         Trahanqc: !rank Nightbot: Platinum V (86 LP) Series: ✓ X -
!streak             Display your current winning/losing streak in ranked games.             Trahanqc: !streak Nightbot: Win (1)
!version            Display the current patch version                                       Trahanqc: !version Nightbot: Current version : 8.17.1



Victorias
"""