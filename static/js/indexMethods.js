function getElementById(elementName) { return document.getElementById(elementName) }

function commandTypeChanged() {
    var commandType = String(getElementById("command_type").value).toLowerCase();
    getElementById("champion_name").disabled = !(commandType === "getdecks" || commandType === "getwinrate");
}

function checkButtonPos() {
    // getElementById("generate_command").disabled = !(getElementById("command_name").value && getElementById("player_name").value)
}

function onPageLoaded() {
    // getElementById("demo").innerHTML = "Iframe is loaded.";
    getElementById("champion_name").disabled = true;
    // getElementById("generate_command").disabled = true;
}