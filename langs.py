INTERNAL_ERROR_404_STRINGS = {
    "en" : "INTERNAL SERVER ERROR: Page not found.",
    "es" : "INTERNAL SERVER ERROR: Page not found.",
    "pt" : "INTERNAL SERVER ERROR: Página não encontrada.",
}
INTERNAL_ERROR_500_STRINGS = {
    "en" : "INTERNAL SERVER ERROR: An unexpected error has occurred.",
    "es" : "INTERNAL SERVER ERROR: An unexpected error has occurred.",
    "pt" : "INTERNAL SERVER ERROR: Um erro inesperado ocorreu.",
}
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
    "en" : "ERROR: Player not specified!",
    "es" : "ERROR: Player not specified!",
    "pt" : "ERROR: Player not specified!",
}
PLAYER_NOT_FOUND_STRINGS = {
    "en" : "ERROR: Player not found!",
    "es" : "ERROR: Player not found!",
    "pt" : "ERRO: Jogador inválido!",
}
PLAYER_NOT_MATCH_STRINGS = {
    "en" : "ERROR: {0} isn't in a match!",
    "es" : "ERROR: {0} isn't in a match!",
    "pt" : "ERRO: {0} não está em partida!",
}
PLAYER_GET_RANK_STRINGS = {
    "en" : "{0} (Level {1}) is {2}{3} with {4} wins and {5} losses.{6}",
    "es" : "{0} (Level {1}) eres {2}{3} con {4} victorias y {5} derrotas.{6}",
    "pt" : "{0} (Nível {1}) é {2}{3} com {4} vitórias e {5} derrotas.{6}",
}
PLAYER_RANK_STRINGS = {
    "en" : {
        0: "Unranked",
        1: "Bronze 5", 2: "Bronze 4", 3: "Bronze 3", 4: "Bronze 2", 5: "Bronze 1",
        6: "Silver 5", 7: "Silver 4", 8: "Silver 3", 9: "Silver 2", 10: "Silver 1",
        11: "Gold 5", 12: "Gold 4", 13: "Gold 3", 14: "Gold 2", 15: "Gold 1",
        16: "Platinum 5", 17: "Platinum 4", 18: "Platinum 3", 19: "Platinum 2", 20: "Platinum 1",
        21: "Diamond 5", 22: "Diamond 4", 23: "Diamond 3", 24: "Diamond 2", 25: "Diamond 1",
        26: "Master", 27: "Grandmaster"
    },
    "es" : {
        0: "Unranked",
        1: "Bronce 5", 2: "Bronce 4", 3: "Bronce 3", 4: "Bronce 2", 5: "Bronce 1",
        6: "Plata 5", 7: "Plata 4", 8: "Plata 3", 9: "Plata 2", 10: "Plata 1",
        11: "Oro 5", 12: "Oro 4", 13: "Oro 3", 14: "Oro 2", 15: "Oro 1",
        16: "Platino 5", 17: "Platino 4", 18: "Platino 3", 19: "Platino 2", 20: "Platino 1",
        21: "Diamante 5", 22: "Diamante 4", 23: "Diamante 3", 24: "Diamante 2", 25: "Diamante 1",
        26: "Maestro", 27: "Gran maestro"
    },
    "pt" : {
        0: "Unranked",
        1: "Bronze 5", 2: "Bronze 4", 3: "Bronze 3", 4: "Bronze 2", 5: "Bronze 1",
        6: "Prata 5", 7: "Prata 4", 8: "Prata 3", 9: "Prata 2", 10: "Prata 1",
        11: "Ouro 5", 12: "Ouro 4", 13: "Ouro 3", 14: "Ouro 2", 15: "Ouro 1",
        16: "Platina 5", 17: "Platina 4", 18: "Platina 3", 19: "Platina 2", 20: "Platina 1",
        21: "Diamante 5", 22: "Diamante 4", 23: "Diamante 3", 24: "Diamante 2", 25: "Diamante 1",
        26: "Mestre", 27: "Grão-mestre"
    },
}
ON_LEADERBOARD_STRINGS = {
    "en" : ", {0} on the leaderboard",
    "es" : ", {0} on the leaderboard",
    "pt" : ", {0}° no rank",
}
CHAMP_WINRATE_STRINGS = {
    "en" : "{0} (Level {1}): {2} Wins, {3} Losses (Kills: {4} / Deaths: {5} / Assists: {6} - {7} KDA) - Winrate: {8}%",
    "es" : "{0} (Level {1}): {2} victorias, {3} derrotas (Kills: {4} / Deaths: {5} / Assists: {6} - {7} KDA) - Winrate: {8}%",
    "pt" : "{0} (Nível {1}): {2} vitórias, {3} derrotas (Kills: {4} / Deaths: {5} / Assists: {6} - {7} KDA) - Winrate: {8}%",
}
GAME_VERSION_STRINGS = {
    "en" : "{0} {1} is {2} - Current version: {3} ({4})",
    "es" : "{0} {1} esta {2} - actual version: {3} ({4})",
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