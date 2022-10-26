"""
Add Table courses_lecturers
"""

from yoyo import step

__depends__ = {'20221025_01_X4qvf-add-table-lecturers', '20221022_02_kbMZn-create-table-courses'}

steps = [
    step(
        """
            create table if not exists courses_lecturers(
                course_id uuid references courses(id)
                    on delete cascade,
                lecturer_id uuid 
                    references lecturers(id)
                    on delete cascade
            )
        """
    )
]
