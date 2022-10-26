"""
Add Table lecturers
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
            create table lecturers(
                id uuid primary key default gen_random_uuid(),
                firstname text not null,
                lastname text not null,
                patronymic text
            )
        """
    )
]
