def render_session(session):
    session_state = session.state

    student = session.get_active_student()
    if student is not None:
        student_first_name = student.first_name
        student_second_name = student.second_name
        session_student = student_first_name + " " + student_second_name

        loaned_board = student.first_name
    else:
        session_student = ""
        loaned_board = ""

    scanned_board = session.get_active_board()
    if scanned_board is not None:
        session_board = scanned_board.board_no
    else:
        session_board = "Please scan board"

    session_dict = {"state": session_state, "student": session_student, "scanned_board": session_board,
                    "loaned_board": loaned_board}
    return session_dict
