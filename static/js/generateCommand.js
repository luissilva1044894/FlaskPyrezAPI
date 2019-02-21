function checkChampName(championName) {
    var champs = [ "androxus", "ash", "barik", "bombking", "buck", "cassie", "dredge", "drogoz", "evie", "fernando", "furia", "grohk", "grover",
    "imani", "inara", "jenos", "khan", "kinessa", "koga", "lex", "lian", "maeve", "makoa", "maldamba", "moji", "pip", "ruckus",
    "seris", "shalin", "skye", "strix", "talus", "terminus", "torvald", "tyra", "viktor", "vivian", "willo", "ying", "zhin" ];
    for (i = 0; i < champs.length; i++) {
        if (String(champs[i]).toLowerCase() === String(championName).toLowerCase())
            return true;
    }
    return false;
}

//function checkFields(commandName, playerName, championName) { }
