"""
create TABLE courses
"""

from yoyo import step

__depends__ = {'20221022_01_7iV19-create-users'}

steps = [
    step(
        """
            create table if not exists courses(
                id uuid primary key default gen_random_uuid(),
                created_at timestamp default current_timestamp,
                title text,
                description text
            );
        """,
        """
            drop table if exists courses;
        """
    )
]
