var session_refresh_timer
var active_session_id

function handle_session_event(body) {
    console.log(body);

    if (body.state == "unknown_student_card") {
           $("#student_name").text("Unknown student card. You are not registered on this course." +
            "Please contact teaching assistant or administrator! Session is terminated")
    }
    if (body.state == "valid_student_card") {
            $("#student_name").text(body.student)
            $("#place_board").show()
            $("#scan_card").hide()
            $("#welcome_student").show()
            $("#loaned_lab_board_info").show()
            $("#loaned_lab_board_info").text(body.loaned_lab_board)
            $("#loaned_lab_board_operation").show()
            $("#loaned_lab_board_operation").text(body.loaned_lab_board_operation)
            $("#loaned_home_board_info").show()
            $("#loaned_home_board_info").text(body.loaned_home_board)
            $("#loaned_home_board_operation").show()
            $("#loaned_home_board_operation").text(body.loaned_lab_board_operation)
            $("#operation_info").show()
            $("#operation_info").text(body.operation)
    }

    if (body.state == "valid_rfid") {
            $("#student_name").text(body.student)
            $("#place_board").hide()
            $("#scan_card").hide()
            $("#scanned_board_text").show()
            $("#scanned_board_info").show()
            $("#scanned_board_info").text(body.scanned_board)
            $("#operation_info").text(body.operation)


    }
}

function refresh_session_state() {
    $.ajax({url: "api/sessions/"+active_session_id,
            method: "GET"})
    .done(handle_session_event)
    .fail(function() {
        clearInterval(session_refresh_timer)
        alert("Timeout/Canceled. Please start again!")
        window.location.replace("/loan")
        })

}

function session_cancel() {
    var message = {"type": "cancel_button"}
    $.ajax({url: "api/events", method: "POST", data: JSON.stringify(message), dataType: "json"})

}

function return_scanned_board() {
    var message = {"type": "return_scanned_board_button"}
    $.ajax({url: "api/events", method: "POST", data: JSON.stringify(message), dataType: "json"})

}

function loan_scanned_board() {
    var message = {"type": "loan_scanned_board_button"}
    $.ajax({url: "api/events", method: "POST", data: JSON.stringify(message), dataType: "json"})

}

function session_started(body) {
    console.log("Started session with id " + body.id)
    active_session_id = body.id
    session_refresh_timer = setInterval(refresh_session_state, 1000)
}

$(document).ready(function() {
    console.log("ready!");
    $("#cancel_button").click(session_cancel)
    $("#return_button").click(return_scanned_board)
    $("#loan_button").click(loan_scanned_board)
    $.ajax({url: "api/sessions", method: "POST"})
        .done(session_started)
        .fail(function(){
            alert("Active session found. Can not start new session, try again later or finish current session")
            window.location.replace("/loan")
        })
})

