function getTranslatedString(language, msg) {
    var engString = [];
    engString["chatMsg"] = "Copy paste the following command in your chat"
    engString["dontChange"] = "YOU DON'T NEED TO CHANGE ANYTHING"
    engString["backendMsg"] = "Or put the following command in <span id=\"backend-title-bot\">{BOTNAME}</span> backend"
    engString["close"] = "Close"
    engString["cmdCreated"] = "Command !{NAME} <strong>created</strong> successfully!"
    engString["invalidCmdName"] = "<strong>Invalid command name</strong>!"
    engString["invalidPlayerName"] = "<strong>Invalid Player Name</strong>!"

    var esString = [];
    esString["chatMsg"] = "Copy paste the following command in your chat"
    esString["dontChange"] = "YOU DON'T NEED TO CHANGE ANYTHING"
    esString["backendMsg"] = "Or put the following command in <span id=\"backend-title-bot\">{BOTNAME}</span> backend"
    esString["close"] = "Close"
    esString["cmdCreated"] = "Command !{NAME} <strong>created</strong> successfully!"
    esString["invalidCmdName"] = "<strong>Invalid command name</strong>!"
    esString["invalidPlayerName"] = "<strong>Invalid Player Name</strong>!"

    var ptString = [];
    ptString["chatMsg"] = "Copie e cole o código em seu chat"
    ptString["dontChange"] = "VOCÊ NÃO PRECISA MUDAR NADA"
    ptString["backendMsg"] = "Or put the following command in <span id=\"backend-title-bot\">{BOTNAME}</span> backend"
    ptString["close"] = "Fechar"
    ptString["cmdCreated"] = "Comando !{NAME} <strong>criado</strong> com sucesso!"
    ptString["invalidCmdName"] = "<strong>Nome do comando inválido</strong>!"
    ptString["invalidPlayerName"] = "<strong>Nome do comando inválido</strong>!"

    var languages = [];
    
    languages["en"] = engString;
    languages["es"] = esString;
    languages["pt"] = ptString;

    return languages[language][msg]
}

function getElementById(elementName) { return document.getElementById(elementName) }

function commandTypeChanged() {
    var commandType = String(getElementById("command_type").value).toLowerCase();
    getElementById("champion_name").disabled = !(commandType === commandType["1"].text.toLowerCase() || commandType === commandType["2"].text.toLowerCase());
}

function checkButtonPos() {
    getElementById("generate_command").disabled = !(getElementById("command_name").value && getElementById("player_name").value)
}
function onPageLoaded() {
    getElementById("champion_name").disabled = true;
    $("#result").html('');

    $("#player_name").on('keypress', function(e) {
        if(e.keyCode == 13) { $("#generate_command").trigger('click'); }
    });
}
function clearField(divName) {
    div = defaultFor(divName, "#alerts"), alert_div = $(div);
    alert_div.html('');
}

function defaultFor(arg, val) { return typeof arg !== 'undefined' ? arg : val; }

function addCommandOutput(codeMsgChat, codeMsgBackend, botName, lang="en") {
    div = defaultFor(div, "#result-warning"), alert_div = $(div), divMsg = "";

    divMsg = "<div class=\"alert alert-dismissible alert-success\" role=\"alert\"><button type=\"button\" class=\"close\" data-dismiss=\"alert\"><span aria-hidden=\"true\">&times;</span><span class=\"sr-only\">{CLOSE}</span></button>".replace("{CLOSE}", getTranslatedString[lang]["close"]);
    divMsg += "<div id=\"chat-title\" class=\"command-title\"><h4>{CHAT_MSG} <small>{DONT_CHANGE}</small>: ".replace("{CHAT_MSG}", getTranslatedString[lang]["chatMsg"]).replace("{DONT_CHANGE}", getTranslatedString[lang]["dontChange"]);
    divMsg += "<code id=\"code-chat-bot\">{CODE_CHAT}</code></h4></div>".replace("{CODE_CHAT}", codeMsgChat);
    divMsg += "<div id=\"backend-title\" class=\"command-title\"><h4>{BACKEND_MSG} ".replace("{BACKEND_MSG}", getTranslatedString[lang]["backendMsg"].replace("{BOT_NAME}", botName));
    divMsg += "<small>{DONT_CHANGE}</small>: <code id=\"code-backend-bot\">{CODE_BACKEND}</code></h4></div>".replace("{DONT_CHANGE}", getTranslatedString[lang]["dontChange"]).replace("{CODE_BACKEND}", codeMsgBackend);
    alert_div.append(divMsg);
}

function addAlert(message, classes, clear, dismiss, div, lang="en"/*, timer = 1 * 60*/) {
    var dismiss = defaultFor(dismiss, true), div = defaultFor(div, "#result-warning"), alert = "", alert_div = $(div);

    if(clear) clearField(div);

    classe = (classes == 'alert-locked' || classes == 'alert-unlocked') ? 'alert-info' : classes;
    alert = '<div class="alert alert-dismissible ' + classe + '" role="alert">';
    if(dismiss)
        alert += "<button type=\"button\" class=\"close\" data-dismiss=\"alert\"><span aria-hidden=\"true\">&times;</span><span class=\"sr-only\">{CLOSE}</span></button>".replace("{CLOSE}", getTranslatedString[lang]["close"]);

    switch(classes) {
        case 'alert-danger' : alert += '<span class="fa fa-exclamation-circle" aria-hidden="true"></span> '; break;
        case 'alert-success' : alert += '<span class="fa fa-check" aria-hidden="true"></span> '; break;
        case 'alert-warning' : alert += '<span class="fa fa-flag" aria-hidden="true"></span> '; break;
        case 'alert-info' : alert += '<span class="fa fa-cog" aria-hidden="true"></span> '; break;
        case 'alert-locked' : alert += '<span class="fa fa-lock" aria-hidden="true"></span> '; break;
        case 'alert-unlocked' : alert += '<span class="fa fa-unlock" aria-hidden="true"></span> '; break;
    }
    alert += message + '</div>';
    //if(timer != 0) var timeout = setInterval(function() { if(timer == 0) { clearInterval(timeout); alert_div.hide(); } else { console.log(--timer); } }, 1000);

    alert_div.append(alert);
}