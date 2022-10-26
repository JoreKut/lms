"""
create TABLE lectures
"""

from yoyo import step

__depends__ = {'20221022_02_kbMZn-create-table-courses'}

steps = [
    step(
        """
            create table if not exists lectures(
                id uuid primary key default gen_random_uuid(),
                created_at timestamp default current_timestamp,
                title text not null,
                description text,
                course_id uuid constraint fk_lectures_course
                                 references courses(id)
                                 on delete cascade,
                starts_at timestamp
            );
        """,
        """
            drop table if exists lectures;
        """
    )
]
