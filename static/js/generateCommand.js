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
function generateCommand() {
    // http://nonsocial.herokuapp.com/api/currentmatch?{IGN}&platform={PLATFORM}&language={LANGUAGE}
    // http://nonsocial.herokuapp.com/api/decks?{IGN}&champion={CHAMPION}&platform={PLATFORM}&language={LANGUAGE}
    // http://nonsocial.herokuapp.com/api/winrate?{IGN}&champion={CHAMPION}&platform={PLATFORM}&language={LANGUAGE}
    // http://nonsocial.herokuapp.com/api/lastmatch?{IGN}&platform={PLATFORM}&language={LANGUAGE}
    // http://nonsocial.herokuapp.com/api/rank?{IGN}&platform={PLATFORM}&language={LANGUAGE}
    // http://nonsocial.herokuapp.com/api/version?platform={PLATFORM}&language={LANGUAGE}
    // http://nonsocial.herokuapp.com/api/stalk?{IGN}&platform={PLATFORM}&language={LANGUAGE}


    var commandName = getElementById("command_name"),
            commandType = getElementById("command_type"),
            cooldown = getElementById("command_cooldown"),
            playerName = getElementById("player_name"),
            championName = getElementById("champion_name"),
            platform = getElementById("platform_form"),
            language = getElementById("language_form"), // int
            botName = getElementById("bot_name"), // int
            userAccess = getElementById("user_access"),
            resultsElement = getElementById("results");
    cmd = ""

    var endpointLink = "{{ url_for(commandType.value, _external=True) }}";
    // alert(checkChampName(String(championName.value).trim().replace(' ', '').replace("'", "").toLowerCase()))
    if (String(commandName.value).trim().replace(' ', '').length > 0 && String(playerName.value).trim().replace(' ', '').length > 3) {
        if(String(botName.value) === "1") {
            perm = ""
            switch(userAccess.value) {
                case "2" : perm = "reg"; break;
                case "3" : perm = "susbcriber"; break;
                case "4" : perm = "mod"; break;
                case "5" : perm = "owner"; break;
                default: perm = "everyone";
            }
            if(String(commandType.value).toLowerCase() === "getdecks" || String(commandType.value).toLowerCase() === "getwinrate") {
                cmd = "!addcom -cd={cd} -ul={perm} !{commandName} $(eval `$(querystring)`.trim()==''?'$(customapi {endpointLink}?player={playerName}&platform={platform}&champion={championName}&language={language})':'$(customapi {endpointLink}?query=$(querystring)&champion=$(2)&platform=$(3)&language={language})' ; )";
                cmd = cmd.replace("{endpointLink}", endpointLink).replace("{cd}", cooldown.value).replace("{perm}", perm).replace("{commandName}", commandName.value).replace("{commandType}", commandType.value).replace("{playerName}", encodeURI(playerName.value)).replace("{platform}", platform.value).replace("{language}", language.value).replace("{championName}", championName.value)
                cmd = cmd.replace("{endpointLink}", endpointLink).replace("{commandType}", commandType.value).replace("{language}", language.value)
                getElementById("demo").innerHTML = cmd
                alert(cmd);
            } else {
                cmd = "!addcom -cd={cd} -ul={perm} !{commandName} $(eval `$(querystring)`.trim()==''?'$(customapi {endpointLink}?player={playerName}&platform={platform}&language={language})':'$(customapi {endpointLink}?query=$(querystring)&platform=$(2)&language={language})' ; )";
                cmd = cmd.replace("{endpointLink}", endpointLink).replace("{cd}", cooldown.value).replace("{perm}", perm).replace("{commandName}", commandName.value).replace("{commandType}", commandType.value).replace("{playerName}", encodeURI(playerName.value)).replace("{platform}", platform.value).replace("{language}", language.value)
                cmd = cmd.replace("{endpointLink}", endpointLink).replace("{commandType}", commandType.value).replace("{language}", language.value)
                getElementById("demo").innerHTML = cmd
                alert(cmd);
            }
        }
    }
    // Enable: resultsElement.attributes.removeNamedItem("hidden");
    
    // Disable:
    //var typ = document.createAttribute("hidden");
    //resultsElement.attributes.setNamedItem(typ)

    // alert(encodeURI(botName.value))

    // alert("?!")
    // alert("" + commandName.value)
}