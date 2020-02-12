class Student:
    """
    Represents a student in database. The personal date will be specified
    by the admin after student has made enrollment to the course.
    The group will be specified on the first lecture by the students/teaching assistance
    home_loan_enabled flag is to set by the admin in case the board was returned damaged
    and a student has not notified the teaching assistance about what happened
    """
    def __init__(self, studentcard=None, first_name='',
                 second_name='', matricul_no='', hrz_no='',
                 group=None, is_home_loan_enabled=True):
        """Initialises a new student with given parameters"""
        self.studentcard = studentcard
        self.first_name = first_name
        self.second_name = second_name
        self.matricul_no = matricul_no
        self.hrz_no = hrz_no
        self.group = group
        self.is_home_loan_enabled = is_home_loan_enabled




