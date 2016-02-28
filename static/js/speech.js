/**
 * Created by vihan on 2/27/16.
 */
var client_access_token = '5d89bf4493e7452d87caa4a29fae5d2d'
console.log("BLAH");

function getJSessionId(){
    var jsId = document.cookie.match(/JSESSIONID=[^;]+/);
    if(jsId != null) {
        if (jsId instanceof Array)
            jsId = jsId[0].substring(11);
        else
            jsId = jsId.substring(11);
    }
    return jsId;
}

var config = {
    server: 'wss://api.api.ai:4435/api/ws/query',
    token: client_access_token,// Use Client access token there (see agent keys).
    sessionId: sessionId,
    onInit: function () {
        console.log("> ON INIT use config");
    }
};
var apiAi = new ApiAi(config);
apiAi.sessionId = '1234';
if (apiAi != undefined) {
    console.log("Exists");
} else {
    console.log("DNE");
}

// Permission to use microphone
apiAi.init();

console.log(apiAi.isInitialise());

apiAi.onInit = function () {
    console.log("> ON INIT use direct assignment property");
    apiAi.open();
};

apiAi.onOpen = function () {
    apiAi.startListening();
    console.log("Started");
};

apiAi.onResults = function (data) {
    var status = data.status;
    var code;
    if (!(status && (code = status.code) && isFinite(parseFloat(code)) && code < 300 && code > 199)) {
        text.innerHTML = JSON.stringify(status);
        return;
    }
    processResult(data.result);
};

function processResult(result) {
    console.log("What should I do?");
}

//function stopListening() {
//        apiAi.stopListening();
//        console.log("Stopped listening");
//}
//
//apiAi.onInit = function() {
//    document.getElementById('stopListening').onclick = stopListening();
//};
//
//var el = document.getElementById("stopListening");
//if (el.addEventListener)
//    el.addEventListener("click", stopListening, false);
//else if (el.attachEvent)
//    el.attachEvent('onclick', stopListening);
