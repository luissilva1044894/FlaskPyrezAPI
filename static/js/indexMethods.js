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

function addCommandOutput(codeMsgChat, codeMsgBackend, botName) {
    div = defaultFor(div, "#result-warning"), alert_div = $(div), divMsg = "";

    divMsg = "<div class=\"alert alert-dismissible alert-success\" role=\"alert\"><button type=\"button\" class=\"close\" data-dismiss=\"alert\"><span aria-hidden=\"true\">&times;</span><span class=\"sr-only\">Close</span></button>";
    divMsg += "<div id=\"chat-title\" class=\"command-title\"><h4>Copy paste the following command in your chat <small>(YOU DON'T NEED TO CHANGE ANYTHING)</small>: <code id=\"code-chat-bot\">"
    divMsg += codeMsgChat;
    divMsg += "</code></h4></div>";
    divMsg += "<div id=\"backend-title\" class=\"command-title\"><h4>Or put the following command in <span id=\"backend-title-bot\">";
    divMsg += botName;
    divMsg += "</span> backend <small>(YOU DON'T NEED TO CHANGE ANYTHING)</small>: <code id=\"code-backend-bot\">";
    divMsg += codeMsgBackend;
    divMsg += "</code></h4></div>";
    alert_div.append(divMsg);
}

function addAlert(message, classes, clear, dismiss, div, timer = 1 * 60) {
    var dismiss = defaultFor(dismiss, true), div = defaultFor(div, "#result-warning"), alert = "", alert_div = $(div);

    if(clear) clearField(div);

    classe = (classes == 'alert-locked' || classes == 'alert-unlocked') ? 'alert-info' : classes;
    alert = '<div class="alert alert-dismissible ' + classe + '" role="alert">';
    if(dismiss)
        alert += '<button type="button" class="close" data-dismiss="alert"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>';

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