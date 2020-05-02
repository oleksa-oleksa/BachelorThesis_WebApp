var session_refresh_timer

function refresh_session_state() {
    $.ajax(
    {url: "api/sessions/17", method: "GET"}).done(function(body) {
        console.log(body);
    })
    .fail(function() {
        clearInterval(session_refresh_timer)
        alert("Something is wrong. Timeout. Please start again!")
        window.location.replace("/loan")
        })

}

$(document).ready(function() {
    console.log("ready!");
    session_refresh_timer = setInterval(refresh_session_state, 1000)
})

