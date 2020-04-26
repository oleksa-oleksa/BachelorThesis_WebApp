function refresh_session_state() {
    $.ajax(
    {url: "api/sessions/16", method: "GET"}).done(function(body) {
        console.log(body);
    })

}

$(document).ready(function() {
    console.log("ready!");
    setInterval(refresh_session_state, 1000)
})

