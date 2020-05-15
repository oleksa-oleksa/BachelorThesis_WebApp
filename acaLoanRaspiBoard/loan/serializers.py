def render_session(session):
    session_state = session.state

    student = session.get_active_student()
    if student is not None:
        student_first_name = student.first_name
        student_second_name = student.second_name
        session_student = student_first_name + " " + student_second_name
    else:
        session_student = ""

    # board = session.get_active_board()

    session_dict = {"state": session_state, "student": session_student}
    return session_dict
