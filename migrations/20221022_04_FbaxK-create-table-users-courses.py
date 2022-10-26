"""
create TABLE users_courses
"""

from yoyo import step

__depends__ = {'20221022_03_hNZYu-create-table-lectures'}

steps = [
    step(
        """
            create table if not exists users_courses(
                id uuid primary key default gen_random_uuid(),
                created_at timestamp default current_timestamp,
                user_id uuid constraint fk_user
                        references users(id)
                        on delete cascade,
                course_id uuid constraint fk_users_course
                        references courses(id)
                        on delete cascade 
            );
        """,
        """
            drop table if exists users_courses;
        """
    )
]
