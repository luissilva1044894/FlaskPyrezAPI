# -*- coding: utf-8 -*-

#https://www.w3schools.com/tags/ref_language_codes.asp
INTERNAL_ERROR_404_STRINGS = {
    'en' : '🚫 INTERNAL SERVER ERROR: Page not found.',
    'es' : '🚫 INTERNAL SERVER ERROR: Página no encontrada.',
    'pl' : '🚫 BŁĄD SERWERA: Nie znaleziono strony',
    'pt' : '🚫 INTERNAL SERVER ERROR: Página não encontrada.',
}
INTERNAL_ERROR_500_STRINGS = {
    'en' : "🚫 INTERNAL SERVER ERROR: An unexpected error has occurred. If something isn't working, report on Discord Server: https://discord.gg/XkydRPS",
    'es' : '🚫 INTERNAL SERVER ERROR: Un error inesperado ha ocurrido. Si algo no funciona, por favor reporte en Discord: https://discord.gg/XkydRPS',
    'pl' : "🚫 BŁĄD SERWERA: Wystąpił nieoczekiwany błąd. If something isn't working, report on Discord Server: https://discord.gg/XkydRPS",
    'pt' : '🚫 INTERNAL SERVER ERROR: Um erro inesperado ocorreu. Se o erro persistir, report no server do Discord: https://discord.gg/XkydRPS',
}
CURRENT_MATCH_STRINGS = {
    'en' : 'Current match - {0} ({1}):{2} | VS |{3}',
    'es' : 'Partida - {0} ({1}):{2} | VS |{3}',
    'pl' : 'Tryb gry - {0} ({1}):{2} | VS |{3}',
    'pt' : 'Partida atual - {0} ({1}):{2} | VS |{3}',
}
CURRENT_MATCH_PLAYER_STRINGS = {
    'en' : ' {0} as {1} ({2})',
    'es' : ' {0}: {1} ({2})',
    'pl' : ' {0}: {1} ({2})',
    'pt' : ' {0}: {1} ({2})',
}
PLAYER_NULL_STRINGS = {
    'en' : '🚫 ERROR: Player not specified!',
    'es' : '🚫 ERROR: ¡Player no especificado!',
    'pl' : '🚫 BŁĄD: Nie podano nazwy gracza!',
    'pt' : '🚫 ERROR: Player not specified!',
}
PLAYER_NOT_FOUND_STRINGS = {
    'en' : "🚫 ERROR: “{0}” doesn't exist or it's hidden! Make sure that your account is marked as “Public Profile”'",
    'es' : '🚫 ERROR: ¡“{0}” no existe o tienes perfil oculto! Make sure that your account is marked as “Public Profile”',
    'pl' : '🚫 BŁĄD: Nie znaleziono gracza “{0}”! Make sure that your account is marked as “Public Profile”',
    'pt' : '🚫 ERRO: “{0}” não existe ou tem perfil privado!',
}
PLAYER_NOT_MATCH_STRINGS = {
    'en' : {
        0: '🚫 ERROR: “{0}” is Offline.',
        1: '🚫 ERROR: “{0}” is still in Lobby.',
        2: '🚫 ERROR: “{0}” is still selecting a champion. You need to wait until the match has started.',
        4: '🚫 ERROR: “{0}” is Online, but not in a match.',
        5: "🚫 ERROR: “{0}” doesn't exist or it's hidden.",
    },
    'es' : {
        0: '🚫 ERROR: “{0}” está Desconectado.',
        1: '🚫 ERROR: “{0}” está en el Vestíbulo.',
        2: '🚫 ERROR: “{0}” está eligiendo un campeón. Necesitas esperar la partida comenzar.',
        4: '🚫 ERROR: “{0}” está Online, pero no en partida.',
        5: '🚫 ERROR: ¡“{0}” no existe o tienes perfil oculto.',
    },
    'pl' : {
        0: '🚫 BŁĄD: “{0}” jest offline.',
        1: '🚫 BŁĄD: “{0}” jest w lobby.',
        2: '🚫 BŁĄD: “{0}” wybiera czempiona. Poczekaj aż rozpocznie się mecz.',
        4: '🚫 BŁĄD: “{0}” jest Online, ale nie rozgrywa meczu.',
        5: "🚫 BŁĄD: “{0}” doesn't exist or it's hidden.",
    },
    'pt' : {
       0: '🚫 ERRO: “{0}” está Offline.',
       1: '🚫 ERRO: “{0}” ainda está no Lobby.',
       2: '🚫 ERRO: “{0}” ainda está escolhendo um campeão. Você precisa esperar a partida começar.',
       4: '🚫 ERRO: “{0}” está Online, mas não em partida.',
       5: '🚫 ERRO: “{0}” não existe ou tem perfil privado.',
    },
}
PLAYER_LEVEL_STRINGS = {
    'en' : '{0} (Level {1})',
    'es' : '{0} (Level {1})',
    'pl' : '{0} (Poziom {1})',
    'pt' : '{0} (Nível {1})',
}
UNABLE_TO_CONNECT_STRINGS = {
    'en' : '🚫 ERROR: Unable to connect to Hi-Rez Studios API!',
    'es' : '🚫 ERROR: Unable to connect to Hi-Rez Studios API!',
    'pl' : '🚫 BŁĄD: Nie można połączyć się z API Hi-Rez Studio!',
    'pt' : '🚫 ERRO: Não foi possível conectar à API da Hi-Rez Studios!',
}
QUEUE_ID_NOT_SUPPORTED_STRINGS = {
    'en' : "🚫 ERROR: “{0}” isn't supported! “{1}” isn't playing casual or ranked, so you can't get details about their match.",
    'es' : '🚫 ERROR: ¡“{0}” no es compatible! “{1}” no está jugando casual o ranked, usted no puedes obtener detalles sobre su partida.',
    'pl' : '🚫 BŁĄD: Tryb “{0}” nie jest obsługiwany! Gracz “{1}” nie jest w trakcie szybkiej gry lub gry rankingowej, więc nie możesz sprawdzić szczegółów dotyczących tego meczu.',
    'pt' : '🚫 ERRO: “{0}” não é suportado! “{1}” não está jogando casual ou ranked, você não pode ver detalhes sobre a partida.',
}
WINS_LOSSES_STRINGS = {
    'en' : ' with {0} wins and {1} losses',
    'es' : ' con {0} victorias y {1} derrotas',
    'pl' : ' z ilością wygranych: {0} i przegranych: {1} meczy',
    'pt' : ' com {0} vitórias e {1} derrotas',
}
PLAYER_GET_RANK_STRINGS = {
    'en' : '{0} is {1}{2}{3}.{4}',
    'es' : '{0} es {1}{2}{3}.{4}',
    'pl' : '{0} posiada rangę {1}{2},{3}.{4}',
    'pt' : '{0} é {1}{2}{3}.{4}',
}
PLAYER_REGION_STRINGS = {
    'en' : {
        'LATIN_AMERICA_NORTH': 'Latin America North',
        'BRAZIL': '🇧🇷',#'Brazil',
        'EUROPE': 'Europe',
        'EU': 'Europe',
        'NORTH_AMERICA': '🇺🇸',#'North America',
        'NA': '🇺🇸',
        'SOUTHEAST_ASIA': 'Southeast Asia',
        'AUSTRALIA': '🇦🇺',#'Australia',
        'JAPAN': '🇯🇵',
        'JP': '🇯🇵',
        '': '❓',#'Unknown',
    },
    'es' : {
        'LATIN_AMERICA_NORTH': 'Norte América Latina',
        'BRAZIL': '🇧🇷',#'Brasil',
        'EUROPE': 'Europa',
        'EU': 'Europa',
        'NORTH_AMERICA': '🇺🇸',#'Estados Unidos',
        'NA': '🇺🇸',
        'SOUTHEAST_ASIA': 'Sudeste Asiático',
        'AUSTRALIA': '🇦🇺',#'Australia',
        'JAPAN': '🇯🇵',
        'JP': '🇯🇵',
        '': '❓',#'???',
    },
    'pl' : {
        'LATIN_AMERICA_NORTH': 'Latin America North',
        'BRAZIL': '🇧🇷',#'Brazil',
        'EUROPE': 'Europe',
        'EU': 'Europe',
        'NORTH_AMERICA': '🇺🇸',#'North America',
        'NA': '🇺🇸',
        'SOUTHEAST_ASIA': 'Southeast Asia',
        'AUSTRALIA': '🇦🇺',#'Australia',
        'JAPAN': '🇯🇵',
        'JP': '🇯🇵',
        '': '❓',#'???',
    },
    'pt' : {
        'LATIN_AMERICA_NORTH': 'América Latina',
        'BRAZIL': '🇧🇷',#'Brasil',
        'EUROPE': 'Europa',
        'EU': 'Europa',
        'NA': '🇺🇸',
        'NORTH_AMERICA': '🇺🇸',#'América do Norte',
        'SOUTHEAST_ASIA': 'Sudeste Asiático',
        'AUSTRALIA': '🇦🇺',#'Austrália',
        'JAPAN': '🇯🇵',
        'JP': '🇯🇵',
        '': '❓',#'???',
    },
}
MATCH_STRINGS = {
    'en' : { 'WIN': 'Win', 'LOSS': 'Loss', },
    'es' : { 'WIN': 'Victoria', 'LOSS': 'Derrota', },
    'pl' : { 'WIN': 'Win', 'LOSS': 'Loss', },
    'pt' : { 'WIN': 'Vitória', 'LOSS': 'Derrota', },
}
QUEUE_IDS_STRINGS = {#428: 'Ranked/Gamepad', 486: 'Ranked/Keyboard', 
    'en' : {
        423: 'Custom/Siege', 430: 'Custom/Siege', 431: 'Custom/Siege', 432: 'Custom/Siege', 433: 'Custom/Siege', 438: 'Custom/Siege', 439: 'Custom/Siege', 440: 'Custom/Siege', 458: 'Custom/Siege', 459: 'Custom/Siege', 473: 'Custom/Siege', 485: 'Custom/Siege', 487: 'Custom/Siege',
        454: 'Custom/Onslaught', 455: 'Custom/Onslaught', 462: 'Custom/Onslaught', 464: 'Custom/Onslaught', 483: 'Custom/Onslaught',
        468: 'Custom/TDM', 471: 'Custom/TDM', 472: 'Custom/TDM', 479: 'Custom/TDM', 480: 'Custom/TDM', 484: 'Custom/TDM',
        424: 'Casual/Siege', 428: '🎮 Ranked', 486: '🖥 Ranked', 445: 'Casual/Test Maps', 452: 'Casual/Onslaught', 469: 'Casual/TDM',
        477: 'Event/Ascension Peak', 478: 'Event/Rise of Furia', 488: 'Event/End Times', 489: 'Custom/End Times',
        425: 'Training/Siege', 453: 'Training/Onslaught', 470: 'Training/TDM', 434: 'Training/Shooting Range', 427: 'Training/Tutorial',
        465: 'Classic/Siege'
    },
    'es' : {
        423: 'Custom/Asedio', 430: 'Custom/Asedio', 431: 'Custom/Asedio', 432: 'Custom/Asedio', 433: 'Custom/Asedio', 438: 'Custom/Asedio', 439: 'Custom/Asedio', 440: 'Custom/Asedio', 458: 'Custom/Asedio', 459: 'Custom/Asedio', 473: 'Custom/Asedio', 485: 'Custom/Asedio', 487: 'Custom/Asedio',
        454: 'Custom/Matanza', 455: 'Custom/Matanza', 462: 'Custom/Matanza', 464: 'Custom/Matanza', 483: 'Custom/Matanza',
        468: 'Custom/Batalla a muerte', 471: 'Custom/Batalla a muerte', 472: 'Custom/Batalla a muerte', 479: 'Custom/Batalla a muerte', 480: 'Custom/Batalla a muerte', 484: 'Custom/Batalla a muerte',
        424: 'Casual/Asedio', 428: '🎮 Ranked', 486: '🖥 Ranked', 445: 'Casual/Test Maps', 452: 'Casual/Matanza', 469: 'Casual/Batalla a muerte',
        477: 'Evento/Asedio del Pico Ascensión', 478: 'Evento/El Ascenso de Furia', 488: 'Evento/Fin de los Tiempos', 489: 'Custom/Fin de los Tiempos',
        425: 'Entrenamiento/Asedio', 453: 'Entrenamiento/Matanza', 470: 'Entrenamiento/Batalla a muerte', 434: 'Entrenamiento/Campo de Tiro', 427: 'Entrenamiento/Tutorial',
        465: 'Classic/Asedio'
    },
    'pl' : {
        423: 'Niestandardowy/Oblężenie', 430: 'Niestandardowy/Oblężenie', 431: 'Niestandardowy/Oblężenie', 432: 'Niestandardowy/Oblężenie', 433: 'Niestandardowy/Oblężenie', 438: 'Niestandardowy/Oblężenie', 439: 'Niestandardowy/Oblężenie', 440: 'Niestandardowy/Oblężenie', 458: 'Niestandardowy/Oblężenie', 459: 'Niestandardowy/Oblężenie', 473: 'Niestandardowy/Oblężenie', 485: 'Niestandardowy/Oblężenie', 487: 'Niestandardowy/Oblężenie',
        454: 'Niestandardowy/Szturm', 455: 'Niestandardowy/Szturm', 462: 'Niestandardowy/Szturm', 464: 'Niestandardowy/Szturm', 483: 'Niestandardowy/Szturm',
        468: 'Niestandardowy/TDM', 471: 'Niestandardowy/TDM', 472: 'Niestandardowy/TDM', 479: 'Niestandardowy/TDM', 480: 'Niestandardowy/TDM', 484: 'Niestandardowy/TDM',
        424: 'Szybka gra/Oblężenie', 428: '🎮 Rankingowy', 486: '🖥 Rankingowy', 445: 'Szybka gra/Mapy Testowe', 452: 'Szybka gra/Szturm', 469: 'Szybka gra/TDM',
        477: 'Wydarzenie/Oblężenie Wzgórza Wniebowstąpienia', 478: 'Wydarzenie/Bunt Furii', 488: 'Wydarzenie/Kres Czasów', 489: 'Niestandardowy/Kres Czasów',
        425: 'Treningowy/Oblężenie', 453: 'Treningowy/Szturm', 470: 'Treningowy/TDM', 434: 'Treningowy/Strzelnica', 427: 'Treningowy/Samouczek',
        465: 'Klasyczny/Oblężenie'
    },
    'pt' : {
       423: 'Custom/Cerco', 430: 'Custom/Cerco', 431: 'Custom/Cerco', 432: 'Custom/Cerco', 433: 'Custom/Cerco', 438: 'Custom/Cerco', 439: 'Custom/Cerco', 440: 'Custom/Cerco', 458: 'Custom/Cerco', 459: 'Custom/Cerco', 473: 'Custom/Cerco', 485: 'Custom/Cerco', 487: 'Custom/Cerco',
       454: 'Custom/Chacina', 455: 'Custom/Chacina', 462: 'Custom/Chacina', 464: 'Custom/Chacina', 483: 'Custom/Chacina',
       468: 'Custom/Mata mata', 471: 'Custom/Mata mata', 472: 'Custom/Mata mata', 479: 'Custom/Mata mata', 480: 'Custom/Mata mata', 484: 'Custom/Mata mata',
       424: 'Casual/Cerco', 428: '🎮 Ranked', 486: '🖥 Ranked', 445: 'Casual/Mapa de teste', 452: 'Casual/Chacina', 469: 'Casual/Cerco',
       477: 'Evento/Cerco ao Pico da Ascensão', 478: 'Evento/O surgimento de Furia', 488: 'Evento/Fim dos Tempos', 489: 'Custom/Fim dos Tempos',
       425: 'Treinamento/Cerco', 453: 'Treinamento/Chacina', 470: 'Treinamento/Mata mata', 434: 'Treinamento/Galeria de tiro', 427: 'Treinamento/Tutorial',
       465: 'Classic/Siege'
    },
}
QUALIFYING_STRINGS = {
    'en' : 'Placements',#Qualifying
    'es' : 'Clasificatorias',
    'pl' : 'Kwalifikacje',
    'pt' : 'MD5',
}
PLAYER_RANK_STRINGS = {
    'en' : {
        0: 'Unranked',
        1: 'Bronze 5', 2: 'Bronze 4', 3: 'Bronze 3', 4: 'Bronze 2', 5: 'Bronze 1',
        6: 'Silver 5', 7: 'Silver 4', 8: 'Silver 3', 9: 'Silver 2', 10: 'Silver 1',
        11: 'Gold 5', 12: 'Gold 4', 13: 'Gold 3', 14: 'Gold 2', 15: 'Gold 1',
        16: 'Platinum 5', 17: 'Platinum 4', 18: 'Platinum 3', 19: 'Platinum 2', 20: 'Platinum 1',
        21: 'Diamond 5', 22: 'Diamond 4', 23: 'Diamond 3', 24: 'Diamond 2', 25: 'Diamond 1',
        26: 'Master', 27: 'Grandmaster'
    },
    'es' : {
        0: 'Unranked',#Qualifying
        1: 'Bronce 5', 2: 'Bronce 4', 3: 'Bronce 3', 4: 'Bronce 2', 5: 'Bronce 1',
        6: 'Plata 5', 7: 'Plata 4', 8: 'Plata 3', 9: 'Plata 2', 10: 'Plata 1',
        11: 'Oro 5', 12: 'Oro 4', 13: 'Oro 3', 14: 'Oro 2', 15: 'Oro 1',
        16: 'Platino 5', 17: 'Platino 4', 18: 'Platino 3', 19: 'Platino 2', 20: 'Platino 1',
        21: 'Diamante 5', 22: 'Diamante 4', 23: 'Diamante 3', 24: 'Diamante 2', 25: 'Diamante 1',
        26: 'Maestro', 27: 'Gran maestro'
    },
    'pl' : {
        0: 'Brak rangi',
        1: 'Brąz 5', 2: 'Brąz 4', 3: 'Brąz 3', 4: 'Brąz 2', 5: 'Brąz 1',
        6: 'Srebro 5', 7: 'Srebro 4', 8: 'Srebro 3', 9: 'Srebro 2', 10: 'Srebro 1',
        11: 'Złoto 5', 12: 'Złoto 4', 13: 'Złoto 3', 14: 'Złoto 2', 15: 'Złoto 1',
        16: 'Platyna 5', 17: 'Platyna 4', 18: 'Platyna 3', 19: 'Platyna 2', 20: 'Platyna 1',
        21: 'Diament 5', 22: 'Diament 4', 23: 'Diament 3', 24: 'Diament 2', 25: 'Diament 1',
        26: 'Mistrz', 27: 'Arcymistrz'
    },
    'pt' : {
        0: 'Unranked',
        1: 'Bronze 5', 2: 'Bronze 4', 3: 'Bronze 3', 4: 'Bronze 2', 5: 'Bronze 1',
        6: 'Prata 5', 7: 'Prata 4', 8: 'Prata 3', 9: 'Prata 2', 10: 'Prata 1',
        11: 'Ouro 5', 12: 'Ouro 4', 13: 'Ouro 3', 14: 'Ouro 2', 15: 'Ouro 1',
        16: 'Platina 5', 17: 'Platina 4', 18: 'Platina 3', 19: 'Platina 2', 20: 'Platina 1',
        21: 'Diamante 5', 22: 'Diamante 4', 23: 'Diamante 3', 24: 'Diamante 2', 25: 'Diamante 1',
        26: 'Mestre', 27: 'Grão-mestre'
    },
}
ON_LEADERBOARD_STRINGS = {
    'en' : ', {0} on the leaderboard',
    'es' : ', {0}° en el marcador',
    'pl' : ', {0} w rankingu',
    'pt' : ', {0}° no rank',
}
CHAMP_WINRATE_STRINGS = {
    'en' : '{0}: {1} Wins, {2} Losses (Kills: {3} / Deaths: {4} / Assists: {5} - {6} KDA) - Win rate: {7}%',
    'es' : '{0}: {1} victorias, {2} derrotas (Kills: {3} / Deaths: {4} / Assists: {5} - {6} KDA) - Win rate: {7}%',
    'pl' : '{0}: Wygrane: {1}, Przegrane: {2} (Zabójstwa: {3} / Śmierci: {4} / Asysty: {5} - {6} KDA) - Win rate: {7}%',
    'pt' : '{0}: {1} vitórias, {2} derrotas (Kills: {3} / Deaths: {4} / Assists: {5} - {6} KDA) - Win rate: {7}%',
}
HOUR_FORMAT_STRINGS = {
    'en' : '%m/%d/%Y %H:%M:%S %p',
    'es' : '%m/%d/%Y %H:%M:%S %p',
    'pl' : '%d/%m/%Y %H:%M:%S %p',
    'pt' : '%d/%m/%Y %H:%M:%S',
}
GAME_VERSION_STRINGS = {
    'en' : '{0} {1} is {2} - Current version: {3} ({4})',
    'es' : '{0} {1} esta {2} - actual version: {3} ({4})',
    'pl' : '{0} {1} jest {2} - Aktualna wersja: {3} ({4})',
    'pt' : '{0} {1} está {2} - Versão atual: {3} ({4})',
}
LAST_MATCH_STRINGS = {
    'en' : '{0} (Match Id: {1} | Duration: {10}m | Region: {11}): {2} ({3}/{4}/{5} - {6} KDA) Killing spree: {7} | Damage: {8} | Credits: {9} - {12} (Score: {13})',
    'es' : '{0} (Id partida: {1} | Duración: {10}m | Región: {11}): {2} ({3}/{4}/{5} - {6} KDA) Killing spree: {7} | Daño: {8} | Créditos: {9} - {12} (Resultado: {13})',
    'pl' : '{0} (Id meczu: {1} | Czas trwania: {10}m | Region: {11}): {2} ({3}/{4}/{5} - {6} KDA) Seria zabójstw: {7} | Obrażenia: {8} | Kredyty: {9} - {12} (Wynik: {13})',
    'pt' : '{0} (Id da partida: {1} | Duração: {10}m | Região: {11}): {2} ({3}/{4}/{5} - {6} KDA) Sequência: {7} | Dano: {8} | Créditos: {9} - {12} (Pontuação: {13})',
}
CURRENTLY_MATCH_STRINGS = {
    'en' : 'currently in a match (Queue: {0} | Match ID: {1})',
    'es' : 'en una partida (Queue: {0} | Match ID: {1})',
    'pl' : 'aktualnie jest w meczu (Tryb gry: {0} | ID Meczu: {1})',
    'pt' : 'em partida (Fila: {0} | ID da partida: {1})',
}
PLAYER_STALK_STRINGS = {
    'en' : '{0} is {1} - Created at: {2} | Last Seen: {3} ago | Playtime: {4}h | Platform: {5} | Region: {6}',
    'es' : '{0} está {1} - Creado en: {2} | Visto por última vez: {3} | Tiempo jugado: {4}h | Plataforma: {5} | Región: {6}',
    'pl' : '{0} jest {1} - Utworzono: {2} | Ostatnio widziany: {3} temu | Czas gry: {4}h | Platforma: {5} | Region: {6}',
    'pt' : '{0} está {1} - Criado em: {2} | Último login: {3} atrás | Horas jogadas: {4}h | Platforma: {5} | Região: {6}',
}
PALADINS_UP_STRINGS = {
    'en' : 'UP{0}',
    'es' : 'DISPONIBLE{0}',
    'pl' : 'DOSTĘPNE{0}',
    'pt' : 'OPERANTE{0}',
}
PALADINS_DOWN_STRINGS = {
    'en' : 'DOWN',
    'es' : 'INDISPONIBLE',
    'pl' : 'NIEDOSTĘPNE',
    'pt' : 'INOPERANTE',
}
PALADINS_LIMITED_ACCESS_STRINGS = {
    'en' : " but it's in maintenance (Limited Access)",
    'es' : ' pero esta en mantenimiento (acceso limitado)',
    'pl' : ' ,ale z limitowanym dostępem',
    'pt' : ' mas está em manutenção (Acesso limitado)',
}
CHAMP_NOT_PLAYED_STRINGS = {
    'en' : "🚫 ERROR: “{0}” doesn't played with “{1}”! Maybe you misspelled the champName.",
    'es' : '🚫 ERROR: ¡“{0}” no jugó con “{1}”! Tal vez usted escribió mal el nombre del campeón.',
    'pl' : '🚫 BŁAD: “{0}” nie grał jeszcze tą postacią! Może wpisałeś złą nazwę czempiona?',
    'pt' : '🚫 ERRO: “{0}” não jogou com “{1}”! Talvez você tenha digitado um campeão incorreto.',
}
PLAYER_LOW_LEVEL_STRINGS = {
    'en' : '🚫 ERROR: Player must be at least level 5.',
    'es' : '🚫 ERROR: El jugador debe tener al menos nivel 5.',
    'pl' : '🚫 BŁĄD: Gracz musi mieć minimalnie 5 poziom konta.',
    'pt' : '🚫 ERRO: O jogador precisa ter pelo menos nível 5.',
}
CHAMP_NULL_STRINGS = {
    'en' : '🚫 ERROR: ChampName not specified!',
    'es' : '🚫 ERROR: ChampName not specified!',
    'pl' : '🚫 ERROR: ChampName not specified!',
    'pt' : '🚫 ERROR: ChampName not specified!',
}
DONT_HAVE_DECKS_STRINGS = {
    'en' : "🚫 ERROR“{0}” doesn't have any “{1}” custom loadouts!.",
    'es' : "🚫 ERROR“{0}” doesn't have any “{1}” custom loadouts!",
    'pl' : "🚫 BŁĄD“{0}” doesn't have any “{1}” custom loadouts!",
    'pt' : '🚫 ERRO“{0}” não tem baralhos para “{1}”!',
}
