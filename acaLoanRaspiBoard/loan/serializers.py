def render_session(session):
    session_state = session.state

    student = session.get_active_student()
    if student is not None:
        student_first_name = student.first_name
        student_second_name = student.second_name
        session_student = student_first_name + " " + student_second_name

        boards = student.get_student_boards()

        if boards["lab"] == "":
            loaned_lab_board = "No lab boards assigned. You can take a board (1-11) to work during exercise time in lab."
        else:
            loaned_lab_board = str(boards["lab"].board_no) + " " + str(boards["lab"].board_status)

        if boards["home"] == "":
            loaned_home_board = str(boards["home"].board_no) + " " + str(boards["home"].board_status)
        else:
            loaned_home_board = "No home loan board assigned. You can loan a board (12-16) to work at home."
    else:
        session_student = ""
        loaned_lab_board = ""
        loaned_home_board = ""

    scanned_board = session.get_active_board()
    if scanned_board is not None:
        session_board = scanned_board.board_no
        operation = "Got board number!"

    else:
        session_board = ""
        operation = "Please scan board"

    session_dict = {"state": session_state, "student": session_student, "scanned_board": session_board,
                    "loaned_lab_board": loaned_lab_board, "loaned_home_board": loaned_home_board, "operation": operation}
    return session_dict
