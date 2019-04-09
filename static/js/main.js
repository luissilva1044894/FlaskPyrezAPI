function getTranslatedString(language, msg) {
    var engString = [];
    engString["chatMsg"] = "Copy paste the following command in your chat"
    engString["dontChange"] = "(YOU DON'T NEED TO CHANGE ANYTHING)"
    engString["backendMsg"] = "Or copy-paste the following text in the “message” field at <span id=\"backend-title-bot\">{BOT_NAME}</span>'s backend"
    engString["close"] = "Close"
    engString["cmdCreated"] = "Command !{CMD_NAME} <strong>created</strong> successfully!"
    engString["invalidCmdName"] = "<strong>Invalid command name</strong>!"
    engString["invalidPlayerName"] = "<strong>Invalid Player Name</strong>!"
    engString["copyToClipboardSuccess"] = "Copied!"
    engString["copyToClipboardMsg"] = "Copy to Clipboard"

    var esString = [];
    esString["chatMsg"] = "Copy paste the following command in your chat"
    esString["dontChange"] = "(YOU DON'T NEED TO CHANGE ANYTHING)"
    esString["backendMsg"] = "Or copy-paste the following text in the “message” field at <span id=\"backend-title-bot\">{BOT_NAME}</span>'s backend"
    esString["close"] = "Close"
    esString["cmdCreated"] = "Command !{CMD_NAME} <strong>created</strong> successfully!"
    esString["invalidCmdName"] = "<strong>Invalid command name</strong>!"
    esString["invalidPlayerName"] = "<strong>Invalid Player Name</strong>!"
    esString["copyToClipboardSuccess"] = "Copied!"
    esString["copyToClipboardMsg"] = "Copy to Clipboard"

    var ptString = [];
    ptString["chatMsg"] = "Copie e cole o código em seu chat"
    ptString["dontChange"] = "(VOCÊ NÃO PRECISA MUDAR NADA)"
    ptString["backendMsg"] = "Ou adicione diretamente como comando nas configurações do <span id=\"backend-title-bot\">{BOT_NAME}</span>"
    ptString["close"] = "Fechar"
    ptString["cmdCreated"] = "Comando !{CMD_NAME} <strong>criado</strong> com sucesso!"
    ptString["invalidCmdName"] = "<strong>Nome do comando inválido</strong>!"
    ptString["invalidPlayerName"] = "<strong>Nome do comando inválido</strong>!"
    ptString["copyToClipboardSuccess"] = "Código copiado!"
    ptString["copyToClipboardMsg"] = "Copiar comando"

    var plString = [];
    plString["chatMsg"] = "Copy paste the following command in your chat"
    plString["dontChange"] = "(YOU DON'T NEED TO CHANGE ANYTHING)"
    plString["backendMsg"] = "Or copy-paste the following text in the “message” field at <span id=\"backend-title-bot\">{BOT_NAME}</span>'s backend"
    plString["close"] = "Close"
    plString["cmdCreated"] = "Command !{CMD_NAME} <strong>created</strong> successfully!"
    plString["invalidCmdName"] = "<strong>Invalid command name</strong>!"
    plString["invalidPlayerName"] = "<strong>Invalid Player Name</strong>!"
    plString["copyToClipboardSuccess"] = "Copied!"
    plString["copyToClipboardMsg"] = "Copy to Clipboard"

    var languages = [];
    
    languages["en"] = engString;
    languages["es"] = esString;
    languages["pl"] = plString;
    languages["pt"] = ptString;

    return languages[language][msg]
}

function getElementById(elementName) { return document.getElementById(elementName) }

function commandTypeChanged() {
    var commandType = getElementById("command_type"), commandCooldown = getElementById("command_cooldown");
    commandCooldown.min = commandType.value.toLowerCase() === commandType["0"].value.toLowerCase() ? 25 : 5;
    commandCooldown.value = commandCooldown.min;
}

function checkButtonPos() {
    getElementById("generate_command").disabled = !(getElementById("command_name").value && getElementById("player_name").value)
}
function keyCodeTrigger(keyCode, elementId) {
    if(keyCode == 13) { $(elementId).trigger("click"); }
}
function onPageLoaded() {
    $("#result").html('');
    //$("#any-number-of-elements").input(function(event) {
    //    alert(this.value);
        //event.preventDefault();
    //});
    $("#command_cooldown").on("keypress", function(e) {
    //https://mathiasbynens.be/notes/oninput
    //https://stackoverflow.com/questions/9361193/why-is-input-type-number-maxlength-3-not-working-in-safari
    //https://stackoverflow.com/questions/8354975/how-can-i-limit-possible-inputs-in-a-html5-number-element : https://jsfiddle.net/DRSDavidSoft/zb4ft1qq/2/
        //keyCodeTrigger(e.keyCode);
        var commandCooldown = getElementById("command_cooldown");
        commandCooldown.value = commandCooldown.value % commandCooldown.max;
    });
    $("#player_name").on("keypress", function(e) {
        //checkButtonPos();
        keyCodeTrigger(e.keyCode, "#generate_command");
    });
    $("#command_name").on("keypress", function(e) {
        //checkButtonPos();
        keyCodeTrigger(e.keyCode, "#generate_command");
    });
}
function clearField(divName) {
    div = defaultFor(divName, "#alerts"), alert_div = $(div);
    alert_div.html('');
}

function defaultFor(arg, val) { return typeof arg !== "undefined" ? arg : val; }

function addCommandOutput(codeMsgChat, codeMsgBackend, botName, lang="en") {
    div = defaultFor(div, "#result-warning"), alert_div = $(div), divMsg = "", botElement = getElementById("bot_name");
    switch(botName.toLowerCase()) {
        case botElement["0"].text.toLowerCase(): botName = "<a href=\"https://botisimo.com/account/commands\" target=\"blank\" title=\"Botisimo Dashboard\">Botisimo</a>"; break;
        case botElement["1"].text.toLowerCase(): botName = "<a href=\"https://beta.nightbot.tv/commands/custom\" target=\"blank\" title=\"Nightbot Dashboard\">Nightbot</a>"; break;
        case botElement["2"].text.toLowerCase(): botName = "<a href=\"https://streamelements.com/dashboard/bot/commands/custom\" target=\"blank\" title=\"Stream Elements Dashboard\">Stream Elements</a>"; break;
    }
    //console.log(botName.toLowerCase()); console.log(botElement.value.toLowerCase()); console.log(botElement["0"].text.toLowerCase()); console.log(botElement[botElement.value - 1].text.toLowerCase());

    divMsg = "<div class=\"alert alert-dismissible alert-success\" role=\"alert\"><button type=\"button\" class=\"close\" data-dismiss=\"alert\"><span aria-hidden=\"true\">&times;</span><span class=\"sr-only\">{CLOSE}</span></button>".replace("{CLOSE}", getTranslatedString(lang, "close"));
    divMsg += "<div id=\"chat-title\" class=\"command-title\"><h4>{CHAT_MSG} <small>{DONT_CHANGE}</small>: ".replace("{CHAT_MSG}", getTranslatedString(lang, "chatMsg")).replace("{DONT_CHANGE}", getTranslatedString(lang, "dontChange"));
    divMsg += "<code id=\"code-chat-bot\">{CODE_CHAT}</code>".replace("{CODE_CHAT}", codeMsgChat);
    divMsg += "<div class=\"btn-group\"><span> </span><button id=\"code-chat-copy-to-clip-button\" class=\"copy-to-clip-button\" title=\"{COPY_TO_CLIPBOARD}\" data-clipboard-text=\"{CODE_CHAT}\" style=\"font-size: 20px;\"><i class=\"fa fa-copy\" style=\"font-size:20px;line-height: 0;\" aria-hidden=\"true\"></i></button></div></h4></div>".replace("{CODE_CHAT}", codeMsgChat).replace("{COPY_TO_CLIPBOARD}", getTranslatedString(lang, "copyToClipboardMsg"));
    divMsg += "<div id=\"backend-title\" class=\"command-title\"><h4>{BACKEND_MSG} ".replace("{BACKEND_MSG}", getTranslatedString(lang, "backendMsg").replace("{BOT_NAME}", botName));
    divMsg += "<small>{DONT_CHANGE}</small>: <code id=\"code-backend-bot\">{CODE_BACKEND}</code>".replace("{DONT_CHANGE}", getTranslatedString(lang, "dontChange")).replace("{CODE_BACKEND}", codeMsgBackend);
    divMsg += "<div class=\"btn-group\"><span> </span><button id=\"backend-copy-to-clip-button\" class=\"copy-to-clip-button\" title=\"{COPY_TO_CLIPBOARD}\" data-clipboard-text=\"{CODE_BACKEND}\" style=\"font-size: 20px;\"><i class=\"fa fa-copy\" style=\"font-size:20px;line-height: 0;\" aria-hidden=\"true\"></i></button></div></h4></div>".replace("{CODE_BACKEND}", codeMsgBackend).replace("{COPY_TO_CLIPBOARD}", getTranslatedString(lang, "copyToClipboardMsg"));
    alert_div.append(divMsg);
}

function addAlert(message, classes, clear, dismiss, div, lang="en"/*, timer = 1 * 60*/) {
    var dismiss = defaultFor(dismiss, true), div = defaultFor(div, "#result-warning"), alert = "", alert_div = $(div);

    if(clear) clearField(div);

    classe = (classes == "alert-locked" || classes == "alert-unlocked") ? "alert-info" : classes;
    alert = "<div class=\"alert alert-dismissible " + classe + "\" role=\"alert\">";
    if(dismiss)
        alert += "<button type=\"button\" class=\"close\" data-dismiss=\"alert\"><span aria-hidden=\"true\">&times;</span><span class=\"sr-only\">{CLOSE}</span></button>".replace("{CLOSE}", getTranslatedString(lang, "close"));

    switch(classes) {
        case "alert-danger" : alert += "<span class=\"fa fa-exclamation-circle\" aria-hidden=\"true\"></span> "; break;
        case "alert-success" : alert += "<span class=\"fa fa-check\" aria-hidden=\"true\"></span> "; break;
        case "alert-warning" : alert += "<span class=\"fa fa-flag\" aria-hidden=\"true\"></span> "; break;
        case "alert-info" : alert += "<span class=\"fa fa-cog\" aria-hidden=\"true\"></span> "; break;
        case "alert-locked" : alert += "<span class=\"fa fa-lock\" aria-hidden=\"true\"></span> "; break;
        case "alert-unlocked" : alert += "<span class=\"fa fa-unlock\" aria-hidden=\"true\"></span> "; break;
    }
    alert += message + '</div>';
    //if(timer != 0) var timeout = setInterval(function() { if(timer == 0) { clearInterval(timeout); alert_div.hide(); } else { console.log(--timer); } }, 1000);

    alert_div.append(alert);
}