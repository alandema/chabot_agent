function getBotResponse() {
    var rawText = $("#textInput").val().trim();
    if (rawText === '') {
        $("#textInput").addClass('error');
        setTimeout(() => $("#textInput").removeClass('error'), 500);
        return;
    }
    
    $("#textInput").prop("disabled", true);
    
    var formattedText = rawText.replace(/\n/g, '<br>');
    var userHtml = '<p class="userText"><span>' + formattedText + "</span></p>";
    $("#textInput").val("");
    $("#chatbox").append(userHtml);
    document
        .getElementById("userInput")
        .scrollIntoView({ block: "start", behavior: "smooth" });
    
    if ($("#chatbox").children().length > 0) {
        $(".background-text").hide();
    }

    $.get("/get", { msg: rawText }).done(function (data) {
        var formattedResponse = data.replace(/\n/g, '<br>');
        var botHtml = '<p class="botText"><span>' + formattedResponse + "</span></p>";
        $("#chatbox").append(botHtml);
        document
            .getElementById("userInput")
            .scrollIntoView({ block: "start", behavior: "smooth" });
    }).always(function() {
        $("#textInput").prop("disabled", false);
    });
}

$(document).ready(function () {
    $("#textInput").keypress(function (e) {
        if (e.which == 13) {  // Enter key
            if (e.shiftKey) {
                // Allow new line with Shift+Enter
                return true;  // Let the default behavior happen (new line insertion)
            } else {
                e.preventDefault();
                getBotResponse();
            }
        }
    });
});