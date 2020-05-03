var session_refresh_timer

function handle_session_event(body) {
    if (body.state == "unknown_student_card") {
           $("#student_name").text("Unknown student card. You are not registered on this course." +
            "Please contact teaching assistant or administrator! Session is terminated")

    }
//    console.log(body);
}

function refresh_session_state() {
    $.ajax(
    {url: "api/sessions/17", method: "GET"}).done(handle_session_event)
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

