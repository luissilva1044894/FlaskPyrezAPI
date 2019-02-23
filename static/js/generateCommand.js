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

function generateCommand(language="en") { // !command add duo Estou duo com X e o elo dele é: (_ELO2_)
    var commandName = String(getElementById("command_name").value).trim().replace(' ', '').replace('!', ''),
            commandType = getElementById("command_type"),
            cooldown = String(getElementById("command_cooldown").value).length > 0 && getElementById("command_cooldown").value >= 5 && getElementById("command_cooldown").value <= 300 ? defaultFor(getElementById("command_cooldown").value) : String(commandType.value).toLowerCase() === "currentmatch" ? 25 : 5;
            playerName = getElementById("player_name"), // Usar o PaladinsGuru para ver se o player existe: https://github.com/Protovision/paladins_scouter/blob/master/paladins_scouter.c
            championName = checkChampName(defaultFor(getElementById("champion_name").value, "")) ? getElementById("champion_name").value : "",
            platform = getElementById("platform_form"),
            language = getElementById("language_form"), // int
            botName = getElementById("bot_name"), // int
            userLevel = getElementById("user_access"),
            userCanUse = getElementById("user_can_use");
    var endpointLink = getEndpoint().replace("index.html", "") + "api/" + String(commandType.value);
    $("#result-warning").show();
    if (commandName.length > 0 && String(playerName.value).trim().replace(' ', '').length > 3) {
        var permLvl = "", cmd = "", cmdChat = "";

        switch(botName.value) {
            case "2" :
                switch(userLevel.value) {
                    case "2" : default: permLvl = "%1"; break;
                    case "3" : permLvl = "%2"; break;
                    case "4" :  case "5" : "%8"; break;
                }
                cmdChat += "!addcom !{CMD_NAME} {PERM_LVL} ".replace("{CMD_NAME}", commandName).replace("{PERM_LVL}", permLvl);
                cmd += userCanUse.checked ? "@customapi@[{ENDPOINT_LINK}?player=@target@[1]&platform=@target@[3]&champion=@target@[2]&language={LANGUAGE}&channel=@channel@&bot={BOT_NAME}&user=@user@)" : "@customapi@[{ENDPOINT_LINK}?player={PLAYER_NAME}&platform={PLATFORM}&language={LANGUAGE}&channel=@channel@&bot={BOT_NAME}&user=@user@)";
            break;
            case "3" : case "5" :
                switch(userLevel.value) {
                    case "2" : permLvl = "+r"; break;
                    case "3" : permLvl = "+s"; break;
                    case "4" : permLvl = "+m"; break;
                    case "5" : permLvl = botName.value === "7" ? "+e" : "+c"; break;
                    default: permLvl = "+a";
                }
                cmdChat += "!command add !{CMD_NAME} {PERM_LVL} ".replace("{CMD_NAME}", commandName).replace("{PERM_LVL}", permLvl);
                cmd += userCanUse.checked ? "$readapi({ENDPOINT_LINK}?query=$dummyormsg&platform={platform}&language={LANGUAGE}&channel=$mychannel&user=$realuser&bot={BOT_NAME})" : "$readapi({ENDPOINT_LINK}?player={PLAYER_NAME}&platform={PLATFORM}&language={LANGUAGE}&channel=$mychannel&user=$realuser&bot={BOT_NAME})";
            break;
            case "4" :
                switch(userLevel.value) {
                    case "2" : permLvl = 300; break;
                    case "3" : permLvl = 250; break;
                    case "4" : permLvl = 500; break;
                    case "5" : permLvl = 2000; break;
                    case "6" : permLvl = 1000; break;
                    default: permLvl = 100;
                }
                cmdChat += "!command add !{CMD_NAME} ".replace("{CMD_NAME}", commandName).replace("{PERM_LVL}", permLvl);
                if(String(commandType.value).toLowerCase() === commandType["1"].text.toLowerCase() || String(commandType.value).toLowerCase() === commandType["2"].text.toLowerCase()) {
                    cmd += userCanUse.checked ? "${customapi.{ENDPOINT_LINK}?query=${1:}&champion=${2:}&platform=${3:}&language={LANGUAGE}&channel=${channel}&bot={BOT_NAME}&user=${sender}}" : "${customapi.{ENDPOINT_LINK}?player={PLAYER_NAME}&platform={PLATFORM}&language={LANGUAGE}&channel=${channel}&bot={BOT_NAME}&user=${sender}}";
                } else {
                    if(String(commandType.value).toLowerCase() === commandType["5"].text.toLowerCase()) {
                        cmd += userCanUse.checked ? "${customapi.{ENDPOINT_LINK}?platform=${1}&language={LANGUAGE}&channel=${channel}&bot={BOT_NAME}&user=${sender}}" : "${customapi.{ENDPOINT_LINK}?platform={PLATFORM}&language={LANGUAGE}&channel=${channel}&bot={BOT_NAME}&user=${sender}}"
                    } else {
                        cmd += userCanUse.checked ? "${customapi.{ENDPOINT_LINK}?query=${1:}&platform=${2:}&language={LANGUAGE}&channel=${channel}&bot={BOT_NAME}&user=${sender}}" : "${customapi.{ENDPOINT_LINK}?player={PLAYER_NAME}&platform={PLATFORM}&language={LANGUAGE}&channel=${channel}&bot={BOT_NAME}&user=${sender}}";
                    }
                }
            break;
            default:
                switch(userLevel.value) {
                    case "2" : permLvl = "reg"; break;
                    case "3" : permLvl = "susbcriber"; break;
                    case "4" : permLvl = "mod"; break;
                    case "5" : permLvl = "owner"; break;
                    default: permLvl = "everyone";
                }
                cmdChat += "!addcom -cd={CD} -ul={PERM_LVL} !{CMD_NAME} ".replace("{CD}", cooldown).replace("{PERM_LVL}", permLvl).replace("{CMD_NAME}", commandName)
                
                customAPICode = "$(customapi {ENDPOINT_LINK}?{PARAMS})";
                cmdUsers = "$(eval `$(querystring)`.trim()==''?\"{IF}\":\"{ELSE}\" ; )"
                if(String(commandType.value).toLowerCase() === commandType["1"].text.toLowerCase() || String(commandType.value).toLowerCase() === commandType["2"].text.toLowerCase()) {
                    if(userCanUse.checked) {
                        cmdUsers = cmdUsers.replace("{IF}", customAPICode.replace("{PARAMS}", "player={PLAYER_NAME}&platform={PLATFORM}&champion={championName}&language={LANGUAGE}&channel=$(channel)&bot={BOT_NAME}&user=$(user)"))
                        cmdUsers = cmdUsers.replace("{ELSE}", customAPICode.replace("{PARAMS}", "query=$(querystring)&champion=$(2)&platform=$(3)&language={LANGUAGE}&channel=$(channel)&bot={BOT_NAME}&user=$(user)"))
                    } else customAPICode = customAPICode.replace("{PARAMS}", "player={PLAYER_NAME}&platform={PLATFORM}&champion=$(1)&language={LANGUAGE}&channel=$(channel)&bot={BOT_NAME}&user=$(user)");
                } else {
                    if(String(commandType.value).toLowerCase() === commandType["5"].text.toLowerCase()) {
                        if(userCanUse.checked) customAPICode = customAPICode.replace("{PARAMS}", "platform=$(1)&language={LANGUAGE}&channel=$(channel)&bot={BOT_NAME}&user=$(user)");
                        else customAPICode = customAPICode.replace("{PARAMS}", "platform={PLATFORM}&language={language}&channel=$(channel)&bot={BOT_NAME}&user=$(user)");
                    } else {
                        if(userCanUse.checked) {
                            cmdUsers = cmdUsers.replace("{IF}", customAPICode.replace("{PARAMS}", "player={PLAYER_NAME}&platform={PLATFORM}&language={LANGUAGE}&channel=$(channel)&bot={BOT_NAME}&user=$(user)"))
                            cmdUsers = cmdUsers.replace("{ELSE}", customAPICode.replace("{PARAMS}", "query=$(querystring)&platform=$(2)&language={LANGUAGE}&channel=$(channel)&bot={BOT_NAME}&user=$(user)"))
                        } else customAPICode = customAPICode.replace("{PARAMS}", "player={PLAYER_NAME}&platform={PLATFORM}&language={LANGUAGE}&channel=$(channel)&bot={BOT_NAME}&user=$(user)");
                    }
                }
                cmd += userCanUse.checked ? cmdUsers : customAPICode;
            break;
        }
        addAlert("{CMD_CREATED}".replace("{CMD_CREATED}", getTranslatedString[lang]["cmdCreated"].replace("{NAME}", commandName)), "alert-success", true, true, "#result-warning", lang);//, 1 * 60);
        cmd = cmd.replace("{ENDPOINT_LINK}", endpointLink).replace("{PLAYER_NAME}", encodeURI(playerName.value)).replace("{PLATFORM}", platform.value).replace("{LANGUAGE}", language.value).replace("{BOT_NAME}", botName[botName.value - 1].text.replace(" ", "")).replace("{championName}", championName)
        cmd = cmd.replace("{ENDPOINT_LINK}", endpointLink).replace("{LANGUAGE}", language.value).replace("{BOT_NAME}", botName[botName.value - 1].text.replace(" ", ""))
        addCommandOutput(cmdChat + cmd, cmd, botName[botName.value - 1].text, lang)
    } else {
        if(commandName.length <= 0) {
            addAlert("{INVALID_CMD_NAME}".replace("{INVALID_CMD_NAME}", getTranslatedString[lang]["invalidCmdName"]), "alert-danger", true, true, "#result-warning", lang);
            $("#command_name").focus();
        } else {
            addAlert("{INVALID_PLAYER_NAME}".replace("{INVALID_PLAYER_NAME}", getTranslatedString[lang]["invalidPlayerName"]), "alert-danger", true, true, "#result-warning", lang);
            //$("#result").html('');
            $("#player_name").focus();
        }
    }
}